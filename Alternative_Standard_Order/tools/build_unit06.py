#!/usr/bin/env python3
"""Unit 6 --- Building and Trusting a Model: code companion + homework."""
from nblib import CodeNB, HW

# =====================================================================
# CODE COMPANION
# =====================================================================
nb = CodeNB(6, "Building and Trusting a Model",
            "Watch a model memorize noise, watch cross-validation catch it, and watch leakage "
            "produce a 'great' model out of pure random numbers. Then see what correlated "
            "predictors do to coefficients you were about to interpret.")

nb.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression, LassoCV, lasso_path
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import make_pipeline

rng = np.random.default_rng(220)
plt.rcParams["figure.figsize"] = (7, 3.5)""")

nb.section("1. Overfitting, watched happening",
           "The truth is a gentle curve. We fit polynomials of growing degree to 25 noisy points "
           "and score them on fresh data from the same truth.")
nb.code("""def truth(x):
    return 1.5*np.sin(1.2*x) + 0.4*x

n_train = 25
x_tr = np.sort(rng.uniform(-3, 3, n_train)); y_tr = truth(x_tr) + rng.normal(0, 0.5, n_train)
x_te = np.sort(rng.uniform(-3, 3, 500));     y_te = truth(x_te) + rng.normal(0, 0.5, 500)

print(f"{'degree':>7} {'train RMSE':>12} {'test RMSE':>12}")
train_e, test_e, degrees = [], [], range(1, 16)
for d in degrees:
    m = make_pipeline(PolynomialFeatures(d), LinearRegression()).fit(x_tr[:, None], y_tr)
    tr = np.sqrt(np.mean((y_tr - m.predict(x_tr[:, None]))**2))
    te = np.sqrt(np.mean((y_te - m.predict(x_te[:, None]))**2))
    train_e.append(tr); test_e.append(te)
    if d in (1, 3, 5, 9, 15):
        print(f"{d:>7} {tr:>12.3f} {te:>12.3f}")

plt.plot(list(degrees), train_e, "o-", label="training error", color="#4878a8")
plt.plot(list(degrees), test_e, "o-", label="error on new data", color="#c0392b")
plt.axvline(list(degrees)[int(np.argmin(test_e))], ls="--", color="#2e8b57",
            label=f"best degree = {list(degrees)[int(np.argmin(test_e))]}")
plt.xlabel("polynomial degree (flexibility)"); plt.ylabel("RMSE"); plt.legend()
plt.title("Training error only ever goes down"); plt.show()""")
nb.md("The training curve slides toward zero and keeps going. Nothing in it warns you that the "
      "model got worse at its actual job around degree 6. That gap is the entire reason "
      "cross-validation exists.")

nb.section("2. Cross-validation picks the complexity for you")
nb.code("""cv = KFold(5, shuffle=True, random_state=1)
print(f"{'degree':>7} {'CV RMSE':>10} {'std err':>10}")
means, ses = [], []
for d in range(1, 12):
    scores = -cross_val_score(make_pipeline(PolynomialFeatures(d), LinearRegression()),
                              x_tr[:, None], y_tr, cv=cv,
                              scoring="neg_root_mean_squared_error")
    means.append(scores.mean()); ses.append(scores.std()/np.sqrt(len(scores)))
    print(f"{d:>7} {scores.mean():>10.3f} {scores.std()/np.sqrt(len(scores)):>10.3f}")

best = int(np.argmin(means))
threshold = means[best] + ses[best]
simplest = next(i for i, m in enumerate(means) if m <= threshold)
print(f"\\nlowest CV error at degree {best+1}")
print(f"one-standard-error rule picks degree {simplest+1} "
      f"(simplest model within {threshold:.3f})")""")

nb.section("3. Leakage: how to get a great model from pure noise",
           "This is the most important cell in the unit. The outcome is random. Nothing predicts "
           "it. We will still produce an impressive cross-validated score.")
nb.code("""n, p = 80, 3000
X = rng.normal(size=(n, p))
y = rng.normal(size=n)                    # pure noise: NO signal exists

# --- THE WRONG WAY: pick the best features using all the data, then cross-validate ---
corrs = np.array([abs(np.corrcoef(X[:, j], y)[0, 1]) for j in range(p)])
top = np.argsort(-corrs)[:10]
wrong = cross_val_score(LinearRegression(), X[:, top], y, cv=cv,
                        scoring="r2").mean()

# --- THE RIGHT WAY: select inside each fold, using only that fold's training data ---
right_scores = []
for tr_idx, te_idx in cv.split(X):
    c = np.array([abs(np.corrcoef(X[tr_idx, j], y[tr_idx])[0, 1]) for j in range(p)])
    sel = np.argsort(-c)[:10]
    m = LinearRegression().fit(X[tr_idx][:, sel], y[tr_idx])
    ss_res = ((y[te_idx] - m.predict(X[te_idx][:, sel]))**2).sum()
    ss_tot = ((y[te_idx] - y[tr_idx].mean())**2).sum()
    right_scores.append(1 - ss_res/ss_tot)

print(f"select first, then cross-validate  : R^2 = {wrong:+.3f}   <-- looks like a real model")
print(f"select inside each fold (correct)  : R^2 = {np.mean(right_scores):+.3f}   <-- the truth")
print("\\nThere is no signal in this data at all. The first number is manufactured entirely")
print("by letting the feature selection peek at the outcomes it would later be graded on.")""")

nb.section("4. Multicollinearity: coefficients that cannot be trusted individually")
nb.code("""cars = pd.read_csv("https://richardson.byu.edu/220/cars.csv").dropna()
print(f"corr(weight, displacement) = {cars.weight.corr(cars.displacement):.3f}\\n")

coefs = []
for _ in range(500):
    samp = cars.sample(len(cars), replace=True)
    fit = sm.OLS(samp.mpg, sm.add_constant(samp[["weight", "displacement"]])).fit()
    coefs.append([fit.params["weight"], fit.params["displacement"]])
coefs = np.array(coefs)

full = sm.OLS(cars.mpg, sm.add_constant(cars[["weight", "displacement"]])).fit()
print(f"weight coefficient      : {full.params['weight']:+.5f}  "
      f"(bootstrap range {np.percentile(coefs[:,0],2.5):+.5f} to {np.percentile(coefs[:,0],97.5):+.5f})")
print(f"displacement coefficient: {full.params['displacement']:+.5f}  "
      f"(bootstrap range {np.percentile(coefs[:,1],2.5):+.5f} to {np.percentile(coefs[:,1],97.5):+.5f})")
print(f"\\ncorrelation between the two ESTIMATES across resamples: "
      f"{np.corrcoef(coefs[:,0], coefs[:,1])[0,1]:+.2f}")""")
nb.md("The two coefficients are strongly *negatively* correlated across resamples: when the data "
      "gives more credit to weight, it takes it away from displacement. The pair is pinned down "
      "but the individuals are not. Predictions are fine. Interpreting either coefficient alone is not.")

nb.section("5. Trees, and the shape they can capture")
nb.code("""x = cars[["weight"]].values; y = cars["mpg"].values
grid = np.linspace(x.min(), x.max(), 400).reshape(-1, 1)

fig, axes = plt.subplots(1, 3, figsize=(12, 3))
for ax, (name, m) in zip(axes, [
        ("straight line", LinearRegression()),
        ("tree, depth 2", DecisionTreeRegressor(max_depth=2, random_state=0)),
        ("tree, depth 12", DecisionTreeRegressor(max_depth=12, random_state=0))]):
    m.fit(x, y)
    ax.plot(x, y, "o", color="#7f8c8d", ms=3, alpha=.5)
    ax.plot(grid, m.predict(grid), color="#4878a8", lw=2.5)
    ax.set_title(name); ax.set_xlabel("weight")
axes[0].set_ylabel("mpg"); plt.tight_layout(); plt.show()""")

nb.section("6. Does the flexible model actually win?",
           "Compare honestly, on the same folds, and look at the fold-to-fold noise before "
           "declaring a winner.")
nb.code("""feats = ["weight", "horsepower", "displacement", "acceleration", "model_year", "cylinder"]
Xc, yc = cars[feats].values, cars["mpg"].values

for name, model in [("linear regression", LinearRegression()),
                    ("tree (depth 4)", DecisionTreeRegressor(max_depth=4, random_state=0)),
                    ("random forest", RandomForestRegressor(n_estimators=300, random_state=0))]:
    sc = -cross_val_score(model, Xc, yc, cv=cv, scoring="neg_root_mean_squared_error")
    print(f"{name:>20}: RMSE {sc.mean():.3f}  (fold-to-fold SD {sc.std():.3f})")""")
nb.md("Read the second column before celebrating the first. If two models differ by less than the "
      "fold-to-fold spread, you have not shown that one is better. You have shown they are hard "
      "to tell apart on this much data.")

nb.write("Code_Unit06_Model_Building.ipynb")


# =====================================================================
# HOMEWORK
# =====================================================================
hw = HW(6, "Building and Trusting a Model",
        """Answer each problem in the cell(s) provided. Replace *Your answer* with your response
for written parts, and put code in the empty code cells.

The first problem is a **simulation lab** where you know the true model, so overfitting and
leakage become visible rather than theoretical. The next three are **real modeling problems**. The
last asks what your model is entitled to claim.

**Data** (all real):

- `https://richardson.byu.edu/220/cars.csv`: fuel economy and engine specs for 392 cars.
- `https://richardson.byu.edu/220/airfoil.csv`: 1,503 wind-tunnel sound-pressure measurements.
- `https://richardson.byu.edu/220/housing_data.csv`: house prices with size, bedrooms, garage,
  neighborhood.""")

hw.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression, LassoCV, RidgeCV, lasso_path
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import make_pipeline

rng = np.random.default_rng(220)
cars = pd.read_csv("https://richardson.byu.edu/220/cars.csv").dropna()
airfoil = pd.read_csv("https://richardson.byu.edu/220/airfoil.csv")
homes = pd.read_csv("https://richardson.byu.edu/220/housing_data.csv")
print(cars.shape, airfoil.shape, homes.shape)""")

# ---------------- P1: simulation lab ----------------
hw.problem(1, """*Simulation lab: overfitting and leakage, where you know the truth.*""")
hw.part("a", """Define a true curve, for example $f(x) = 1.5\\sin(1.2x) + 0.4x$. Generate 25
training points with noise $N(0, 0.5)$ and 500 test points from the same truth. Fit polynomials of
degree 1 through 15 and plot training RMSE and test RMSE against degree on one figure.""")
hw.part("b", """Report the degree that minimizes test error and the degree that minimizes training
error. Explain in 2 to 3 sentences why the training curve is useless as a model-selection tool.""")
hw.part("c", """Now use only the training data: run 5-fold cross-validation for each degree,
report the CV RMSE and its standard error, and identify both the CV-minimizing degree and the
**one-standard-error** choice. Compare them to your Part b answer.""")
hw.part("d", """**The leakage experiment.** Generate $n = 80$ observations with $p = 3000$ random
predictors and an outcome that is pure noise, unrelated to everything. First, select the 10
predictors most correlated with the outcome using *all* the data, then cross-validate a linear
model on those 10 and report the $R^2$.""")
hw.part("e", """Now do it correctly: perform the selection **inside each fold**, using only that
fold's training rows, and report the cross-validated $R^2$. Report both numbers together.""")
hw.part("f", """You just produced an impressive score from data containing no signal whatsoever.
Explain the mechanism in 3 to 4 sentences, and state the one-sentence rule that prevents it.""", "written")

# ---------------- P2: real multiple regression ----------------
hw.problem(2, """*Real data: building a fuel-economy model.* Use `cars`.""")
hw.part("a", """Fit `mpg` on `weight`, `horsepower`, `model_year`, and `origin`. Report the
coefficients and write a one-sentence interpretation of the `model_year` coefficient, being
careful about what is held fixed.""")
hw.part("b", """Report the correlation matrix of `weight`, `horsepower`, and `displacement`. Then
fit a model with all three and describe what happens to the individual coefficients compared to
fitting each alone.""")
hw.part("c", """Quantify the instability: bootstrap the model with `weight` and `displacement`
500 times and report the range of each coefficient, plus the correlation between the two estimates
across resamples. What does that correlation tell you?""")
hw.part("d", """Does multicollinearity hurt the model's *predictions*? Compare cross-validated
RMSE with and without `displacement`, and reconcile your answer with Part c.""")
hw.part("e", """Add an interaction between `weight` and `model_year`. Report the coefficient and
explain, in plain language, what it would mean for the fuel-economy penalty of weight to change
over time.""")
hw.part("f", """A journalist asks you to state "how much fuel economy improved per model year."
Write the 3 to 4 sentence answer, including the number, the uncertainty, and the reason the raw
year-over-year comparison would have given a different figure.""", "written")

# ---------------- P3: honest comparison ----------------
hw.problem(3, """*Real data: does the flexible model actually win?* Use `airfoil`, predicting
`Pressure` from the other five columns.""")
hw.part("a", """Using the **same** 5-fold splits for every model, report cross-validated RMSE for
a linear regression, a depth-4 tree, a depth-12 tree, and a random forest. Include the
fold-to-fold standard deviation for each.""")
hw.part("b", """Which model would you ship? Justify using the fold-to-fold spread, not just the
means.""", "written")
hw.part("c", """Build the complexity curve: for tree depths 1 through 15, plot training RMSE,
cross-validated RMSE, and test RMSE on a held-out split. Report the depth chosen by CV.""")
hw.part("d", """Apply the one-standard-error rule to your CV results and report the depth it
selects. How much accuracy did you give up, and what did you buy with it?""")
hw.part("e", """Repeat Part a with the data **standardized inside a pipeline** versus standardized
on the full dataset before splitting. Report both CV scores. Explain whether the difference is
large here, and describe a dataset where this same mistake would matter enormously.""")

# ---------------- P4: selection and regularization ----------------
hw.problem(4, """*Real data: choosing among predictors without fooling yourself.* Use `cars` with
the six numeric predictors, standardized.""")
hw.part("a", """Compute and plot the lasso path. Describe the order in which predictors enter as
the penalty weakens, and what that ordering does and does not tell you.""")
hw.part("b", """Fit `LassoCV` and `RidgeCV`. Report the selected penalty and coefficients for each,
and note which coefficients the lasso set exactly to zero.""")
hw.part("c", """Compare cross-validated RMSE for ordinary least squares, ridge, and lasso. Is the
difference meaningful relative to the fold-to-fold spread?""")
hw.part("d", """Add 20 columns of pure random noise to the predictors and refit `LassoCV`. How many
noise columns receive a nonzero coefficient? What does that tell you about using the lasso as a
variable-selection procedure?""")
hw.part("e", """Run a stepwise-style search by hand: from the full predictor set plus your 20 noise
columns, repeatedly keep the variable with the smallest $p$-value until five remain. Report the
final model's $p$-values. Explain why those $p$-values cannot be interpreted the usual way.""")
hw.part("f", """Fit a random forest on `cars` 30 times on different random 60% subsets and plot
the distribution of each feature's importance. Comment on the stability, especially for `weight`
and `displacement`.""")

# ---------------- P5: what can we say ----------------
hw.problem(5, """*What can and cannot be said.* Written answers.""")
hw.part("a", """Your Problem 2 model gives a coefficient on `weight`. Write the interpretation that
is supported, and then the causal interpretation that is not, and explain exactly what would have
to be true to upgrade one to the other.""", "written")
hw.part("b", """In Problem 3, one model had the lowest cross-validated error. Explain why that does
not establish that it is the best model, and name two considerations beyond accuracy that would
decide what you deploy.""", "written")
hw.part("c", """In Problem 4, the lasso dropped a predictor. Explain why "the lasso dropped it"
is not evidence that the predictor is unrelated to fuel economy.""", "written")
hw.part("d", """A colleague reports: "our random forest says horsepower is the most important
driver of fuel economy, so reducing horsepower is the fastest route to efficiency." Identify every
unsupported step in that sentence.""", "written")
hw.part("e", """Write the model-card paragraph you would attach to your Problem 3 model: what it
predicts, on what population, how it was validated, its honest error, and the two situations in
which it should not be used.""", "written")

hw.write("Stat_220_HW_Unit06_Model_Building.ipynb")
