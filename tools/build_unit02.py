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
        """Everything here uses one dataset, `campus_cafe.csv`: 700 days at a campus coffee shop.
It is not one of the datasets from the code companion, so you are reading a new table for the
first time, which is the normal situation.

```python
import pandas as pd, numpy as np
import statsmodels.api as sm, statsmodels.formula.api as smf
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_score, train_test_split

cafe = pd.read_csv("https://drbob-richardson.github.io/stat220/F2026/data/campus_cafe.csv")
cafe.head()
```

| column | what it is |
|---|---|
| `day_of_week` | Mon through Fri |
| `temp_f` | outside temperature that day |
| `exam_week` | 1 during finals and midterms, 0 otherwise |
| `promo` | 1 if a discount ran that day |
| `foot_traffic` | people who walked past the shop |
| `drinks_sold` | drinks sold that day |
| `revenue` | dollars taken that day |
| `sold_out` | 1 if they ran out of a main item |

The first problem needs no computer at all.""")

hw.problem(1, """*Reading a situation.* No code. Two or three sentences each.""")
hw.part("a", "The owner wants to know how many drinks to prepare for tomorrow, given the "
             "forecast temperature. Name the type of `y`, name the model family you would fit, "
             "and say why in one sentence.", kind="markdown")
hw.part("b", "The owner wants to know whether running a promotion actually raises revenue, "
             "because she is deciding whether to keep doing it. Name the type of `y` and the "
             "family, and say what makes this a different job from part a.", kind="markdown")
hw.part("c", "A student suggests fitting a random forest for part b. A forest would run on that "
             "data without complaining. Say whether you would use it, and what it would cost "
             "you.", kind="markdown")
hw.part("d", "The owner asks for the chance they run out of an item on a given day. Name the "
             "type of `y` and the family. What is the output of that model, and what still has "
             "to be decided before anyone can act on it?", kind="markdown")

hw.problem(2, """*The type of `y` picks the model.* Three outcomes in this one table.""")
hw.part("a", "Fit a linear regression of `revenue` on `drinks_sold` and `exam_week`. Report the "
             "coefficient on `drinks_sold` with its units, in a full sentence.")
hw.part("b", "Fit a Poisson regression of `drinks_sold` on `temp_f`, `exam_week` and `promo`. "
             "Report the coefficient on `temp_f`, and say in one sentence why this model can "
             "never predict a negative number of drinks.")
hw.part("c", "Fit a logistic regression of `sold_out` on `drinks_sold`. Report the smallest and "
             "largest fitted probability.")
hw.part("d", "Now fit an ordinary linear regression to `sold_out ~ drinks_sold`. Count how many "
             "of its predicted values fall outside 0 to 1, and say in one sentence what that "
             "tells you about forcing the wrong model onto an outcome.")

hw.problem(3, """*What each kind of model hands back.* Predicting `revenue`.""")
hw.part("a", "Fit a linear regression of `revenue` on `drinks_sold`, `exam_week`, `promo` and "
             "`temp_f`. Print the coefficient table and report the 95% confidence interval for "
             "`exam_week`.")
hw.part("b", "Fit a random forest on the same four predictors. Report its feature importances.")
hw.part("c", "For each of these four, say whether you can get it from the regression, from the "
             "forest, from both, or from neither: a $p$-value, a confidence interval for a "
             "coefficient, an AIC, an error on data the model never saw.", kind="markdown")
hw.part("d", "In two to three sentences, explain why the missing ones are missing. Use the word "
             "distribution.", kind="markdown")

hw.problem(4, """*Is model A better than model B?* Same rows, same measure, both times.""")
hw.part("a", "Fit three nested linear models for `revenue`: `drinks_sold`, then "
             "`+ exam_week`, then `+ promo`. Report the AIC of each.")
hw.part("b", "One of those additions makes AIC go up rather than down. Say which, and explain "
             "in one sentence what that means.", kind="markdown")
hw.part("c", "Now score the four-predictor regression from Problem 3 against the random forest "
             "using 5-fold cross-validation. Build one `KFold` object and pass the same one to "
             "both. Report each model's mean squared error.")
hw.part("d", "You now have AIC values and cross-validated errors. Explain in two sentences why "
             "you cannot settle the regression-versus-forest question with AIC.", kind="markdown")

hw.problem(5, """*One prediction, with a range on it.*""")
hw.part("a", "Split the data with `train_test_split(..., test_size=0.25, random_state=1)`. Fit "
             "the four-predictor linear regression on the training rows only.")
hw.part("b", "Predict `revenue` for the first held-out day and report the number.")
hw.part("c", "Collect the model's errors on all the held-out days, take the 5th and 95th "
             "percentiles, and attach them to your prediction from part b. Did your interval "
             "contain that day's actual revenue?")
hw.part("d", "The owner asks for one number and no range. Write the one sentence you would say "
             "to her instead, using your numbers from parts b and c.", kind="markdown")
hw.part("e", "Look back at your two answers about `exam_week`. The forest gave it an "
             "importance near the bottom of the four predictors. The regression gave it a "
             "coefficient whose 95% interval was several dollars a day, comfortably away from "
             "zero. Explain how both of those can be true at once, and say which number you "
             "would take to the owner.", kind="markdown")

hw.write("Stat_220_HW_Unit02_Map_of_Models.ipynb")
