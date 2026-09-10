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
           "Fit, tune, predict, put a range on it, and compare. Step 2 is set aside "
           "here: choosing a hyperparameter honestly is Unit 4.")
nb.code("""# 1. fit
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=1)

# 2. tune: depth is a choice, not something fitting discovers.
#    Choosing it well is Unit 4. Here we simply take 4.
DEPTH = 4
tree = DecisionTreeRegressor(max_depth=DEPTH, random_state=0).fit(Xtr, ytr)
print(f"  depth chosen: {DEPTH}  (how to choose it honestly is Unit 4)")

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
        """One dataset throughout: `campus_cafe.csv`, 700 days at a campus coffee shop. It is not
one of the datasets from the code companion.

| column | what it is |
|---|---|
| `temp_f` | outside temperature that day |
| `exam_week` | 1 during finals and midterms, 0 otherwise |
| `promo` | 1 if a discount ran that day |
| `foot_traffic` | people who walked past the shop |
| `drinks_sold` | drinks sold that day |
| `revenue` | dollars taken that day |
| `sold_out` | 1 if they ran out of a main item |

**Most of the code is written for you.** Run each cell, read what comes back, and answer the
question. The reasoning is the graded part, not the typing. Start by running this:

```python
import pandas as pd, numpy as np
import statsmodels.api as sm, statsmodels.formula.api as smf
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.linear_model import LinearRegression

cafe = pd.read_csv("https://drbob-richardson.github.io/stat220/F2026/data/campus_cafe.csv")
P = ["drinks_sold", "exam_week", "promo", "temp_f"]
cafe.head()
```""")

hw.problem(1, """*Reading a situation.* No computer. Two or three sentences each.""")
hw.part("a", "The owner wants to know how many drinks to prepare tomorrow, given the forecast "
             "temperature. Name the type of `y`, name the model family, and say why.",
        kind="markdown")
hw.part("b", "The owner wants to know whether running a promotion actually raises revenue, "
             "because she is deciding whether to keep doing it. Name the type of `y` and the "
             "family, and say what makes this a different job from part a.", kind="markdown")
hw.part("c", "A classmate suggests a random forest for part b. It would run on that data without "
             "complaining. Would you use it, and what would it cost you?", kind="markdown")

hw.problem(2, """*The type of `y` picks the model.* Three outcomes in one table.""")
hw.given("a", "Run this. Report the coefficient on `drinks_sold` in a full sentence, with units.",
'''# a number -> linear regression
m_rev = smf.ols("revenue ~ drinks_sold + exam_week", data=cafe).fit()
print(m_rev.params.round(3))''')
hw.given("b", "Run this. Why can this model never predict a negative number of drinks?",
'''# a count -> Poisson regression
m_cnt = smf.glm("drinks_sold ~ temp_f + exam_week + promo",
                data=cafe, family=sm.families.Poisson()).fit()
print(m_cnt.params.round(4))
print("smallest prediction:", round(m_cnt.predict().min(), 1))''')
hw.given("c", "The first model below is the right one for a yes/no outcome. The second forces a "
              "linear model onto it. Say what has gone wrong in the second, and what it tells you.",
'''# a yes/no -> logistic regression
m_out = smf.logit("sold_out ~ drinks_sold", data=cafe).fit(disp=0)
p_ok = m_out.predict()
print(f"logistic fitted probabilities: {p_ok.min():.3f} to {p_ok.max():.3f}")

# the same outcome, forced into a linear model
p_bad = smf.ols("sold_out ~ drinks_sold", data=cafe).fit().predict()
print(f"linear   fitted probabilities: {p_bad.min():.2f} to {p_bad.max():.2f}")
print("how many fall outside 0 to 1:", int(((p_bad < 0) | (p_bad > 1)).sum()))''')

hw.problem(3, """*What each kind of model hands back.* Both predict `revenue` from the same four
columns.""")
hw.given("a", "Run this. Report the 95% confidence interval for `exam_week` and say what it means "
              "in dollars.",
'''reg = smf.ols("revenue ~ " + " + ".join(P), data=cafe).fit()
print(reg.summary().tables[1])
print("95% CI for exam_week:", reg.conf_int().loc["exam_week"].round(2).tolist())''')
hw.given("b", "Run this. Which predictor does the forest lean on most, and which barely registers?",
'''forest = RandomForestRegressor(n_estimators=300, random_state=0).fit(cafe[P], cafe["revenue"])
print(pd.Series(forest.feature_importances_, index=P).round(3).to_string())''')
hw.given("c", "This checks which quantities each model can produce. For each one the forest "
              "cannot, say why not. Use the word distribution.",
'''for name, model in [("regression", reg), ("forest", forest)]:
    have = [a for a in ["pvalues", "conf_int", "aic"] if hasattr(model, a)]
    print(f"{name:<12} can give you: {have}")''')

hw.problem(4, """*Is model A better than model B?* Same rows, same measure, both times.""")
hw.given("a", "Run this. One of the two additions makes AIC go up rather than down. Which, and "
              "what does that mean?",
'''for f in ["revenue ~ drinks_sold",
          "revenue ~ drinks_sold + exam_week",
          "revenue ~ drinks_sold + exam_week + promo"]:
    print(f"{f:<48} AIC = {smf.ols(f, data=cafe).fit().aic:8.1f}")''')
hw.given("b", "Run this. Which model would you ship, and does the answer surprise you?",
'''folds = KFold(5, shuffle=True, random_state=0)   # one fold object, used for both
for name, mod in [("regression", LinearRegression()),
                  ("forest", RandomForestRegressor(n_estimators=300, random_state=0))]:
    mse = -cross_val_score(mod, cafe[P], cafe["revenue"], cv=folds,
                           scoring="neg_mean_squared_error").mean()
    print(f"  {name:<12} cross-validated MSE {mse:7.1f}   RMSE {np.sqrt(mse):5.1f} dollars")''')
hw.part("c", "You have AIC values from part a and cross-validated errors from part b. Explain in "
             "two sentences why you cannot settle the regression-versus-forest question using "
             "AIC.", kind="markdown")

hw.problem(5, """*One prediction, with a range on it.*""")
hw.given("a", "Run this. Report the prediction and the interval, and say whether the interval "
              "caught the true value.",
'''Xtr, Xte, ytr, yte = train_test_split(cafe[P], cafe["revenue"],
                                      test_size=0.25, random_state=1)
fit = LinearRegression().fit(Xtr, ytr)

pred = fit.predict(Xte.iloc[[0]])[0]           # one held-out day
resid = yte - fit.predict(Xte)                 # errors on days it never saw
lo, hi = np.percentile(resid, [5, 95])

print(f"prediction          : {pred:6.1f}")
print(f"90% interval        : {pred + lo:6.1f} to {pred + hi:.1f}")
print(f"what it actually was: {yte.iloc[0]:6.1f}")''')
hw.part("b", "The owner asks for one number and no range. Write the single sentence you would say "
             "to her instead, using your numbers from part a.", kind="markdown")
hw.part("c", "Look back at your two answers about `exam_week`. The forest gave it an importance "
             "near the bottom of the four. The regression gave it a coefficient several dollars "
             "away from zero. Explain how both can be true, and say which number you would take "
             "to the owner.", kind="markdown")

hw.write("Stat_220_HW_Unit02_Map_of_Models.ipynb")
