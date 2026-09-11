#!/usr/bin/env python3
"""Unit 2: A Map of Models. Code companion and homework.

The companion stays inside what the unit teaches and what the homework needs.
No tuning, no prediction intervals, no model families the assignment never asks
about. Those get code in the units that teach them.
"""
from nblib import CodeNB, HW

nb = CodeNB(2, "A Map of Models",
            "Fit the same data two ways and see exactly which questions each kind of model can "
            "answer, then compare two candidates honestly.")

nb.code("""import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score

cars = pd.read_csv("https://richardson.byu.edu/220/cars.csv").dropna()
bikes = pd.read_csv("https://richardson.byu.edu/220/bikes.csv").dropna()
PREDS = ["weight", "horsepower", "model_year"]
X, y = cars[PREDS], cars["mpg"]
print(cars.shape, bikes.shape)""")

nb.section("1. Two kinds of model on the same data",
           "One names a distribution for mpg. The other just predicts it.")
nb.code("""lin = smf.ols("mpg ~ weight + horsepower + model_year", data=cars).fit()
forest = RandomForestRegressor(n_estimators=300, random_state=0).fit(X, y)

print("linear, in-sample R^2:", round(lin.rsquared, 3))
print("forest, in-sample R^2:", round(forest.score(X, y), 3))""")
nb.md("The forest fits better. That is not the interesting part. What each one will *tell you* is.")

nb.section("2. What each one hands back")
nb.code("""print(lin.summary().tables[1])
print("\\nAIC:", round(lin.aic, 1))

print("\\n--- the forest ---")
imp = pd.Series(forest.feature_importances_, index=PREDS).sort_values(ascending=False)
print(imp.round(3).to_string())

for attr in ["pvalues", "conf_int", "aic"]:
    print(f"forest.{attr}:", "yes" if hasattr(forest, attr) else "does not exist")""")
nb.md("Importances, and nothing else. No distribution means no likelihood, and no likelihood "
      "means there is no standard error, no $p$-value and no AIC to report. Those quantities are "
      "undefined here rather than hidden.")

nb.section("3. The type of y picks the probability model",
           "Linear for a number, logistic for a yes/no, Poisson for a count.")
nb.code("""# a number
m_num = smf.ols("mpg ~ weight", data=cars).fit()

# a yes/no
cars["efficient"] = (cars["mpg"] > 30).astype(int)
m_bin = smf.logit("efficient ~ weight", data=cars).fit(disp=0)

# a count
m_cnt = smf.glm("Count ~ Temperature", data=bikes, family=sm.families.Poisson()).fit()

print(f"linear   slope on weight: {m_num.params['weight']:.5f}")
print(f"logistic slope on weight: {m_bin.params['weight']:.5f}   (log-odds)")
print(f"Poisson  slope on temp  : {m_cnt.params['Temperature']:.5f}   (log-rate)")

print(f"\\nlogistic predictions stay in [0,1]: {m_bin.predict().min():.3f} to {m_bin.predict().max():.3f}")
print(f"Poisson predictions stay positive : {m_cnt.predict().min():.1f} to {m_cnt.predict().max():.1f}")""")

nb.section("4. What happens if you force the wrong one",
           "An ordinary regression on a yes/no outcome runs. Look at what it returns.")
nb.code("""bad = smf.ols("efficient ~ weight", data=cars).fit().predict()
print(f"predicted 'probabilities' range from {bad.min():.2f} to {bad.max():.2f}")
print("how many are not possible probabilities:", int(((bad < 0) | (bad > 1)).sum()))""")

nb.section("5. The type of y does not rule out a forest",
           "The same algorithm has a regression mode and a classification mode.")
nb.code("""from sklearn.ensemble import RandomForestClassifier

rf_num = RandomForestRegressor(n_estimators=100, random_state=0).fit(X, y)
rf_bin = RandomForestClassifier(n_estimators=100, random_state=0).fit(X, cars["efficient"])

print("numeric outcome ->", type(rf_num).__name__, "  predicts:", rf_num.predict(X[:3]).round(1))
print("yes/no outcome  ->", type(rf_bin).__name__, "predicts:",
      rf_bin.predict_proba(X[:3])[:, 1].round(2), "(probabilities)")""")
nb.md("The outcome never rules a forest out. What rules it out is needing a coefficient.")

nb.section("6. Is model A better than model B?",
           "Same rows, same measure, scored where neither model was fitted.")
nb.code("""folds = KFold(5, shuffle=True, random_state=0)   # one fold object, used for every candidate

for name, mod in [("linear regression", LinearRegression()),
                  ("random forest", RandomForestRegressor(n_estimators=300, random_state=0))]:
    fit = mod.fit(X, y)
    train_mse = np.mean((fit.predict(X) - y) ** 2)
    cv = -cross_val_score(mod, X, y, cv=folds, scoring="neg_mean_squared_error")
    print(f"  {name:<20} training MSE {train_mse:6.2f}   CV MSE {cv.mean():6.2f}"
          f"   RMSE {np.sqrt(cv.mean()):5.2f} mpg")""")
nb.md("Read the two columns against each other. Training error says how well a model reproduces "
      "rows it already saw. The cross-validated column is the one that counts, and RMSE is the "
      "version you quote to a person, because it is back in the units of $y$.")

nb.section("7. The other way to compare: AIC",
           "Needs a likelihood, so probability models only, and only on identical rows.")
nb.code("""for f in ["mpg ~ weight",
          "mpg ~ weight + horsepower",
          "mpg ~ weight + horsepower + model_year"]:
    m = smf.ols(f, data=cars).fit()
    k = int(m.df_model) + 1
    print(f"  {f:<44} k={k}  logL={m.llf:8.1f}  AIC={m.aic:8.1f}")

full = smf.ols("mpg ~ weight + horsepower + model_year", data=cars).fit()
print(f"\\ncheck the arithmetic: 2k - 2*logL = {2 * 4 - 2 * full.llf:.1f}")""")
nb.md("Lower is better, and only differences mean anything. You could not put the forest on this "
      "table at all, which is why the cross-validated comparison above exists.")

nb.section("What to take away")
nb.md("""
1. The type of `y` picks the probability model, and rules out nothing on the other side.
2. A model that names no distribution has no p-value, no confidence interval and no AIC.
3. Compare candidates on the same rows, with the same measure, where neither was fitted.
4. AIC needs a likelihood. Cross-validated error works on anything.
""")

nb.write("Code_Unit02_Map_of_Models.ipynb")

# =====================================================================
# HOMEWORK
# =====================================================================
hw = HW(2, "A Map of Models",
        """`campus_cafe.csv` is 700 days at a campus coffee shop: `temp_f`, `exam_week`,
`promo`, `foot_traffic`, `drinks_sold`, `revenue`, and `sold_out`.

```python
import pandas as pd, numpy as np
import statsmodels.api as sm, statsmodels.formula.api as smf
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import LinearRegression

cafe = pd.read_csv("https://drbob-richardson.github.io/stat220/F2026/data/campus_cafe.csv")
cafe.head()
```""")

hw.problem(1, """*Reading a situation.* No computer.""")
hw.part("a", "The owner wants to know how many drinks to prepare tomorrow, given the forecast "
             "temperature. What type is `y` here, and which model family would you name?",
        kind="markdown")
hw.part("b", "The owner wants to know whether running a promotion actually raises revenue, since "
             "she is deciding whether to keep doing it. What type is `y`, which family, and what "
             "makes this a different job from part a?", kind="markdown")
hw.part("c", "The owner wants the chance they run out of an item on a given day. What type is "
             "`y`, and which family?", kind="markdown")
hw.part("d", "A classmate says to just use a random forest for all three. A forest would run on "
             "all three without complaining. Say which of the three you would refuse to use it "
             "for, and why.", kind="markdown")

hw.problem(2, """*What happens if you ignore the type of `y`.*""")
hw.given("a", "`sold_out` is a yes/no column. Describe what the linear model produced "
              "that the logistic model did not, and say why that is a problem.",
'''# the right model for a yes/no outcome
p_ok = smf.logit("sold_out ~ drinks_sold", data=cafe).fit(disp=0).predict()

# the same outcome, forced into a linear model
p_bad = smf.ols("sold_out ~ drinks_sold", data=cafe).fit().predict()

print(f"logistic gives values from {p_ok.min():.3f} to {p_ok.max():.3f}")
print(f"linear   gives values from {p_bad.min():.2f} to {p_bad.max():.2f}")
print("linear values that are not possible probabilities:",
      int(((p_bad < 0) | (p_bad > 1)).sum()), "out of", len(p_bad))''')
hw.part("b", "`drinks_sold` is a count. Name the probability model you would use for it, and say "
             "in one sentence what would go wrong with an ordinary linear model there.",
        kind="markdown")

hw.problem(3, """*What a model can and cannot hand back.*""")
hw.given("a", "List the quantities the forest could not produce, and explain why not. "
              "Your answer should use the word distribution.",
'''X = cafe[["drinks_sold", "exam_week", "promo", "temp_f"]]
reg = LinearRegression().fit(X, cafe["revenue"])
forest = RandomForestRegressor(n_estimators=300, random_state=0).fit(X, cafe["revenue"])
sm_reg = smf.ols("revenue ~ drinks_sold + exam_week + promo + temp_f", data=cafe).fit()

for name, model in [("regression", sm_reg), ("forest", forest)]:
    have = [a for a in ["pvalues", "conf_int", "aic"] if hasattr(model, a)]
    print(f"{name:<12} can give you: {have if have else 'none of them'}")''')
hw.part("b", "Go back to the three jobs in Problem 1. Which one of them could a forest not do at "
             "all, given what you just saw?", kind="markdown")

hw.problem(4, """*Is model A better than model B?*""")
hw.given("a", "These three models are compared by AIC. Say which one you would keep, and "
              "what it means that one of the additions made AIC go up.",
'''for f in ["revenue ~ drinks_sold",
          "revenue ~ drinks_sold + exam_week",
          "revenue ~ drinks_sold + exam_week + promo"]:
    print(f"{f:<48} AIC = {smf.ols(f, data=cafe).fit().aic:8.1f}")''')
hw.given("b", "Say which model you would ship, and whether the result surprises you.",
'''folds = KFold(5, shuffle=True, random_state=0)   # one fold object, used for both
for name, mod in [("regression", LinearRegression()),
                  ("forest", RandomForestRegressor(n_estimators=300, random_state=0))]:
    mse = -cross_val_score(mod, X, cafe["revenue"], cv=folds,
                           scoring="neg_mean_squared_error").mean()
    print(f"  {name:<12} cross-validated MSE {mse:7.1f}   RMSE {np.sqrt(mse):5.1f} dollars")''')
hw.part("c", "You could compare the three models in part a with AIC, but you could not use AIC "
             "for the comparison in part b. Explain why in two sentences.", kind="markdown")

hw.problem(5, """*Putting it together.* No computer.""")
hw.part("a", "The owner reads that a forest predicted revenue almost as well as the regression, "
             "and asks whether she should use the forest to decide about promotions. Answer her "
             "in three or four sentences.", kind="markdown")

hw.write("Stat_220_HW_Unit02_Map_of_Models.ipynb")
