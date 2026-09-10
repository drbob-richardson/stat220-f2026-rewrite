#!/usr/bin/env python3
"""Unit 2: A Map of Models. Code companion and homework.

Mirrors the deck: a section per model family, then the comparison machinery,
then the five steps walked on one model.
"""
from nblib import CodeNB, HW

nb = CodeNB(2, "A Map of Models",
            "Fit every family on the menu to the same problem, see what each one hands back, "
            "and then compare two of them honestly.")

nb.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression, LassoCV
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(220)
plt.rcParams["figure.figsize"] = (7, 3.5)

cars = pd.read_csv("https://richardson.byu.edu/220/cars.csv").dropna()
bikes = pd.read_csv("https://richardson.byu.edu/220/bikes.csv").dropna()
PREDS = ["weight", "displacement", "horsepower", "acceleration", "model_year", "cylinder"]
X, y = cars[PREDS], cars["mpg"]
print(cars.shape, bikes.shape)""")

nb.section("1. Two kinds of model on the same data",
           "One names a distribution for mpg. The other just predicts it.")
nb.code("""lin = smf.ols("mpg ~ weight + horsepower + model_year", data=cars).fit()
forest = RandomForestRegressor(n_estimators=400, random_state=0).fit(X, y)
print("linear, in-sample R^2:", round(lin.rsquared, 3))
print("forest, in-sample R^2:", round(forest.score(X, y), 3))""")

nb.section("2. What each one hands back")
nb.code("""print(lin.summary().tables[1])
print("\\nAIC:", round(lin.aic, 1))
print("95% CI for weight:", lin.conf_int().loc["weight"].round(5).to_dict())

print("\\n--- the forest ---")
imp = pd.Series(forest.feature_importances_, index=PREDS).sort_values(ascending=False)
print(imp.round(3).to_string())
for attr in ["pvalues", "conf_int", "aic", "bse"]:
    print(f"forest.{attr}:", "yes" if hasattr(forest, attr) else "does not exist")""")
nb.md("Importances, and nothing else. No likelihood means no standard error, no $p$-value and no "
      "AIC. Those are undefined here, not hidden.")

nb.section("3. The type of y picks the probability model",
           "Linear for a number, logistic for a yes/no, Poisson for a count. These are not "
           "interchangeable.")
nb.code("""# a number
m_num = smf.ols("mpg ~ weight", data=cars).fit()

# a yes/no
cars["efficient"] = (cars["mpg"] > 30).astype(int)
m_bin = smf.logit("efficient ~ weight", data=cars).fit(disp=0)

# a count
m_cnt = smf.glm("Count ~ Temperature", data=bikes,
                family=sm.families.Poisson()).fit()

print(f"linear   slope on weight : {m_num.params['weight']:.5f} mpg per pound")
print(f"logistic slope on weight : {m_bin.params['weight']:.5f} log-odds per pound")
print(f"Poisson  slope on temp   : {m_cnt.params['Temperature']:.5f} log-rate per degree")
print(f"\\nlogistic predictions stay in [0,1]: "
      f"{m_bin.predict().min():.3f} to {m_bin.predict().max():.3f}")
print(f"Poisson predictions stay positive : {m_cnt.predict().min():.1f} to {m_cnt.predict().max():.1f}")""")

nb.section("4. What goes wrong if you force the type",
           "An ordinary regression on a yes/no outcome will run. Look at what it returns.")
nb.code("""bad = smf.ols("efficient ~ weight", data=cars).fit()
p = bad.predict()
print(f"predicted 'probabilities' range from {p.min():.2f} to {p.max():.2f}")
print("number of predictions outside [0, 1]:", int(((p < 0) | (p > 1)).sum()))""")

nb.section("5. The non-probability families work on any y",
           "The same tree, forest and boosting, in regression mode and in classification mode.")
nb.code("""from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

reg = DecisionTreeRegressor(max_depth=3, random_state=0).fit(X, y)
clf = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X, cars["efficient"])
print("same algorithm, numeric outcome  ->", type(reg).__name__)
print("same algorithm, yes/no outcome   ->", type(clf).__name__)
print("\\nregression tree predicts:", reg.predict(X[:3]).round(1))
print("classifier predicts       :", clf.predict_proba(X[:3])[:, 1].round(2), "(probabilities)")""")
nb.md("The outcome type never rules these out. What rules them out is needing a coefficient.")

nb.section("6. Four non-probability models, same data",
           "Tree, forest, boosting and k-nearest neighbours on one predictor, so you can see "
           "the shape each one produces.")
nb.code("""x1 = cars[["weight"]].values
grid = np.linspace(x1.min(), x1.max(), 300).reshape(-1, 1)
models = {
    "tree (depth 3)":  DecisionTreeRegressor(max_depth=3, random_state=0),
    "random forest":   RandomForestRegressor(n_estimators=200, random_state=0),
    "boosting":        GradientBoostingRegressor(n_estimators=200, max_depth=2, random_state=0),
    "kNN (k=20)":      KNeighborsRegressor(n_neighbors=20),
}
fig, axes = plt.subplots(1, 4, figsize=(12, 2.8), sharey=True)
for ax, (name, m) in zip(axes, models.items()):
    m.fit(x1, y)
    ax.scatter(x1, y, s=6, color="grey", alpha=0.3)
    ax.plot(grid, m.predict(grid), color="purple", lw=2)
    ax.set_title(name, fontsize=9); ax.set_xlabel("weight")
axes[0].set_ylabel("mpg")
plt.tight_layout(); plt.show()""")

nb.section("7. Lasso: a shortlist out of many columns")
nb.code("""Xs = StandardScaler().fit_transform(cars[PREDS])
las = LassoCV(cv=5, random_state=0).fit(Xs, y)
kept = pd.Series(las.coef_, index=PREDS)
print(f"penalty chosen by cross-validation: {las.alpha_:.4f}\\n")
print(kept.round(3).to_string())
print("\\nsurvivors:", [p for p, c in kept.items() if abs(c) > 1e-8])""")
nb.md("Those coefficients were shrunk on purpose, so read the survivors as a shortlist and not "
      "as effects.")

nb.section("8. Comparing two models: the measure",
           "Same rows, same measure, scored on data neither model was fitted to.")
nb.code("""folds = KFold(5, shuffle=True, random_state=0)
cands = {
    "linear regression": LinearRegression(),
    "tree, depth 4":     DecisionTreeRegressor(max_depth=4, random_state=0),
    "tree, depth 10":    DecisionTreeRegressor(max_depth=10, random_state=0),
    "random forest":     RandomForestRegressor(n_estimators=300, random_state=0),
}
for name, m in cands.items():
    fit = m.fit(X, y)
    train_mse = np.mean((fit.predict(X) - y) ** 2)
    s = -cross_val_score(m, X, y, cv=folds, scoring="neg_mean_squared_error")
    print(f"  {name:<20} training MSE {train_mse:6.2f}   CV MSE {s.mean():6.2f} "
          f"(sd {s.std(ddof=1):4.2f})   RMSE {np.sqrt(s.mean()):5.2f} mpg")""")
nb.md("Read the two columns against each other. The depth-10 tree wins on training error and "
      "loses on the honest one.")

nb.section("9. The other way to compare: AIC",
           "Only for probability models, and only on identical rows.")
nb.code("""for f in ["mpg ~ weight", "mpg ~ weight + horsepower",
          "mpg ~ weight + horsepower + model_year"]:
    m = smf.ols(f, data=cars).fit()
    k = int(m.df_model) + 1
    print(f"  {f:<42} k={k}  logL={m.llf:8.1f}  AIC={m.aic:8.1f}  BIC={m.bic:8.1f}")
print("\\ncheck the arithmetic:  2k - 2*logL =",
      round(2 * 4 - 2 * smf.ols('mpg ~ weight + horsepower + model_year', data=cars).fit().llf, 1))""")

nb.section("10. The five steps, on one regression tree",
           "Fit, tune, predict, put a range on it, and compare. All five in one place.")
nb.code("""# 1. fit
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=1)

# 2. tune, on folds fixed before looking
for d in [2, 3, 4, 6, 10]:
    s = -cross_val_score(DecisionTreeRegressor(max_depth=d, random_state=0),
                         Xtr, ytr, cv=folds, scoring="neg_mean_squared_error")
    print(f"  depth {d:<3} CV MSE {s.mean():6.2f}")

tree = DecisionTreeRegressor(max_depth=4, random_state=0).fit(Xtr, ytr)

# 3. predict one held-out car
one = Xte.iloc[[0]]
pred = tree.predict(one)[0]

# 4. a range, from errors on cars it never saw
resid = yte - tree.predict(Xte)
lo, hi = np.percentile(resid, [5, 95])
print(f"\\n  prediction: {pred:.1f} mpg")
print(f"  90% interval from held-out errors: {pred + lo:.1f} to {pred + hi:.1f}")
print(f"  actual: {yte.iloc[0]:.1f}")

# 5. compare against the obvious alternative
for name, m in [("tree, depth 4", DecisionTreeRegressor(max_depth=4, random_state=0)),
                ("linear", LinearRegression())]:
    s = -cross_val_score(m, X, y, cv=folds, scoring="neg_mean_squared_error")
    print(f"  {name:<16} CV MSE {s.mean():6.2f}")""")

nb.section("What to take away")
nb.md("""
1. The type of `y` picks the probability model and cannot rule out a tree.
2. A model that names no distribution has no p-value, no confidence interval and no AIC.
3. Compare candidates on the same rows with the same measure, scored where neither was fitted.
4. AIC needs a likelihood. Cross-validated error works on anything.
5. Every model goes through the same five steps. Only the tools change.
""")

nb.write("Code_Unit02_Map_of_Models.ipynb")

# =====================================================================
# HOMEWORK
# =====================================================================
hw = HW(2, "A Map of Models",
        """The first problem is a simulation where you set the truth, so you can check whether each
model recovers it. The rest use real data, where nobody knows the truth and the last question is
what you are entitled to say.

Load these once at the top:

```python
cars  = pd.read_csv("https://richardson.byu.edu/220/cars.csv").dropna()
bikes = pd.read_csv("https://richardson.byu.edu/220/bikes.csv").dropna()
rent  = pd.read_csv("https://richardson.byu.edu/220/rent.csv").dropna()
```""")

hw.problem(1, """*Simulation lab: what each kind of model can recover.* You control the truth here.""")
hw.part("a", "Simulate 400 rows where `y = 3 + 2*x1 - 1*x2 + noise`, with `x1` and `x2` "
             "independent standard normals and noise standard deviation 2. Fit a linear "
             "regression and report the three coefficients with their confidence intervals. "
             "Do the intervals cover the true values?")
hw.part("b", "Fit a random forest to the same data and report its importances. Can you recover "
             "the true coefficient on `x1` from them? Explain in two sentences why or why not.")
hw.part("c", "Now make the truth genuinely nonlinear: `y = 3*sin(2*x1) + x2 + noise`. Refit both "
             "and compare error on 200 held-out rows. Which wins, and what did the winner give up?")

hw.problem(2, """*The type of y picks the model.* Three outcomes, three families.""")
hw.part("a", "Using `cars`, fit `mpg ~ weight` with an ordinary regression and report the slope "
             "with its units.")
hw.part("b", "Create `efficient = (mpg > 30)` and fit a logistic regression on `weight`. Report "
             "the range of its fitted probabilities.")
hw.part("c", "Now fit an ordinary linear regression to `efficient ~ weight`. Report how many of "
             "its predicted values fall outside 0 to 1, and say in one sentence what that tells "
             "you.")
hw.part("d", "Using `bikes`, fit a Poisson regression of `Count` on `Temperature`. Report the "
             "coefficient and explain in one sentence why its predictions can never go negative.")
hw.part("e", "Fit a random forest to each of the three outcomes above. Did the outcome type stop "
             "you in any case? Answer in two sentences.", kind="markdown")

hw.problem(3, """*Comparing two models honestly.* Use `cars`, predicting `mpg` from all six
numeric predictors.""")
hw.part("a", "Fit three nested linear models: `weight`, then `+ horsepower`, then "
             "`+ model_year`. Report the AIC of each and say which you would keep.")
hw.part("b", "Score a linear regression and a depth-10 tree with 5-fold cross-validation, "
             "reusing one `KFold` object. Report training MSE and cross-validated MSE for both.")
hw.part("c", "The depth-10 tree has by far the lower training error. Explain in two to three "
             "sentences why that is not evidence it is the better model.", kind="markdown")
hw.part("d", "Can you compute an AIC for the tree? Say why or why not in one sentence.",
        kind="markdown")

hw.problem(4, """*The five steps on one model.* Use `cars`. Hold out 25% before you start.""")
hw.part("a", "**Tune.** Cross-validate a regression tree over depths 2, 3, 4, 6 and 10 on the "
             "training rows only. Report the CV error for each and pick a depth.")
hw.part("b", "**Fit and predict.** Fit at your chosen depth and predict for one held-out car. "
             "Report the prediction.")
hw.part("c", "**Put a range on it.** Take the model's errors on the held-out cars, compute the "
             "5th and 95th percentiles, and attach them to your prediction. Did the interval "
             "contain the true value?")
hw.part("d", "**Compare.** Score your tree and a linear regression on the same folds. Which "
             "would you ship, and why?", kind="markdown")

hw.problem(5, """*What can and cannot be said.* Written answers, no new computation.""")
hw.part("a", "A colleague reports that the forest had the lowest cross-validated error and "
             "concludes that weight is the biggest driver of fuel economy. Give two separate "
             "reasons that conclusion is not supported.", kind="markdown")
hw.part("b", "You need to tell a regulator how much an extra 500 pounds costs in fuel economy. "
             "Which of the models you fitted can answer that, and which cannot?", kind="markdown")
hw.part("c", "Across this assignment you used coefficients, importances, AIC, and cross-"
             "validated error. For each, write one sentence on the question it answers.",
        kind="markdown")

hw.write("Stat_220_HW_Unit02_Map_of_Models.ipynb")
