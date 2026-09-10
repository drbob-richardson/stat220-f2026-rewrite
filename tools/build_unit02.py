#!/usr/bin/env python3
"""Unit 2: A Map of Models. Code companion and homework."""
from nblib import CodeNB, HW

# =====================================================================
# CODE COMPANION
# =====================================================================
nb = CodeNB(2, "A Map of Models",
            "Fit the same data twice, once with a model that names a distribution and once "
            "with one that does not, and see exactly which questions each one can answer.")

nb.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_score

rng = np.random.default_rng(220)
plt.rcParams["figure.figsize"] = (7, 3.5)

cars = pd.read_csv("https://richardson.byu.edu/220/cars.csv").dropna()
print(cars.shape)
cars.head(3)""")

nb.section("1. The same data, two kinds of model",
           "One names a distribution for mpg. The other just predicts it.")
nb.code("""X = cars[["weight", "horsepower", "model_year"]]
y = cars["mpg"]

lin = smf.ols("mpg ~ weight + horsepower + model_year", data=cars).fit()
forest = RandomForestRegressor(n_estimators=400, random_state=0).fit(X, y)

print("linear regression, in-sample R^2:", round(lin.rsquared, 3))
print("random forest,     in-sample R^2:", round(forest.score(X, y), 3))""")
nb.md("The forest fits better. That is not the interesting part. What each one will "
      "*tell you* is the interesting part.")

nb.section("2. What the probability model hands you")
nb.code("""print(lin.summary().tables[1])
print()
print("AIC:", round(lin.aic, 1))
print("95% CI for the weight coefficient:")
print(lin.conf_int().loc["weight"].round(5).to_dict())""")
nb.md("A slope, a standard error, a $p$-value, a confidence interval, and an AIC. Every one of "
      "those comes out of the sentence `mpg ~ Normal(b0 + b1*weight + ..., sigma^2)`.")

nb.section("3. What the algorithmic model hands you")
nb.code("""imp = pd.Series(forest.feature_importances_, index=X.columns).sort_values(ascending=False)
print(imp.round(3).to_string())

for attr in ["pvalues", "conf_int", "aic", "bse"]:
    print(f"forest.{attr}:", "yes" if hasattr(forest, attr) else "does not exist")""")
nb.md("Importances, and nothing else. There is no likelihood, so there is no standard error, no "
      "$p$-value, and no AIC. Those quantities are not hidden, they are undefined.")

nb.section("4. Importances are not effects",
           "The regression says weight is negative. Ask the forest for a direction and it has none.")
nb.code("""print("regression coefficient on weight:", round(lin.params['weight'], 5))
print("forest importance for weight:      ", round(imp['weight'], 3), " (no sign, no units)")

# and the ranking is unstable when the rows change
from collections import Counter
tops = []
for b in range(30):
    idx = rng.integers(0, len(y), len(y))
    f = RandomForestRegressor(n_estimators=150, random_state=b).fit(X.iloc[idx], y.iloc[idx])
    tops.append(pd.Series(f.feature_importances_, index=X.columns).idxmax())
print("\\nmost important variable across 30 resamples:", dict(Counter(tops)))""")

nb.section("5. Comparing models: two different numbers",
           "AIC needs a likelihood. Cross-validation does not.")
nb.code("""m1 = smf.ols("mpg ~ weight", data=cars).fit()
m2 = smf.ols("mpg ~ weight + horsepower", data=cars).fit()
m3 = smf.ols("mpg ~ weight + horsepower + model_year", data=cars).fit()
for name, m in [("weight", m1), ("+ horsepower", m2), ("+ model_year", m3)]:
    print(f"  {name:<14} AIC = {m.aic:8.1f}")

folds = KFold(5, shuffle=True, random_state=0)
for name, mod in [("linear", None), ("forest", forest)]:
    if mod is None:
        from sklearn.linear_model import LinearRegression
        mod = LinearRegression()
    s = -cross_val_score(mod, X, y, cv=folds, scoring="neg_mean_squared_error")
    print(f"  {name:<14} CV MSE = {s.mean():6.2f}")""")
nb.md("The AICs are comparable to each other. The cross-validated errors are comparable to each "
      "other. An AIC and a CV error are not comparable at all, so pick one method and use it for "
      "every candidate.")

nb.section("6. Parameters versus hyperparameters",
           "One comes out of fitting. The other you choose, and cross-validation is how.")
nb.code("""for depth in [2, 4, 6, 10, None]:
    f = RandomForestRegressor(n_estimators=200, max_depth=depth, random_state=0)
    s = -cross_val_score(f, X, y, cv=folds, scoring="neg_mean_squared_error")
    label = "unlimited" if depth is None else depth
    print(f"  max_depth = {str(label):<10} CV MSE = {s.mean():6.2f}")""")
nb.md("`max_depth` is a hyperparameter: no amount of fitting discovers it. The honest way to set "
      "it is on folds you fixed before looking at the answer.")

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
cars = pd.read_csv("https://richardson.byu.edu/220/cars.csv").dropna()
rent = pd.read_csv("https://richardson.byu.edu/220/rent.csv").dropna()
```""")

hw.problem(1, """*Simulation lab: what each kind of model can recover.* You control the truth here.""")
hw.part("a", "Simulate 400 rows where `y = 3 + 2*x1 - 1*x2 + noise`, with `x1` and `x2` "
             "independent standard normals and noise standard deviation 2. Fit a linear "
             "regression and report the three coefficients with their confidence intervals. "
             "Do the intervals cover the true values?")
hw.part("b", "Fit a random forest to the same data. Report its importances. Can you recover "
             "the true coefficient on `x1` from them? Explain in two sentences why or why not.")
hw.part("c", "Raise the noise standard deviation to 8 and refit both. Which model's output "
             "degrades in a way you can measure, and which one degrades silently?")
hw.part("d", "Now make the truth genuinely nonlinear: `y = 3*sin(2*x1) + x2 + noise`. Refit "
             "both and compare out-of-sample error on 200 held-out rows. Which wins now, and "
             "what did the winner give up?", kind="code")

hw.problem(2, """*Real data: reading what each model reports.* Use `cars`, predicting `mpg`.""")
hw.part("a", "Fit `mpg ~ weight + horsepower + model_year`. Write one sentence interpreting "
             "the coefficient on `model_year`, with its units.")
hw.part("b", "Fit a random forest on the same three predictors. Report the importances, and "
             "state which of the following you can get from the forest and which you cannot: "
             "a p-value, a confidence interval, an AIC, an out-of-sample error.")
hw.part("c", "Explain in two to three sentences why the missing ones are missing. Your answer "
             "should use the word likelihood.", kind="markdown")

hw.problem(3, """*Real data: comparing models honestly.* Use `rent`, predicting `Rent`.""")
hw.part("a", "Fit three nested linear models: `Size`, then `Size + BHK`, then "
             "`Size + BHK + Bathroom`. Report the AIC of each and say which you would keep.")
hw.part("b", "Now score all three with 5-fold cross-validation, reusing one `KFold` object. "
             "Does cross-validation pick the same model AIC did?")
hw.part("c", "Add a random forest to the comparison. Which of your two comparison methods "
             "can include it, and why can the other one not?")
hw.part("d", "In two to three sentences, say which method you would report and why.",
        kind="markdown")

hw.problem(4, """*The job decides the model.* No new fitting is required for parts a to c.""")
hw.part("a", "A city council asks whether apartment size drives rent, and will use your number "
             "to write policy. Name the model family you would fit and say why in one sentence.",
        kind="markdown")
hw.part("b", "A listings website wants to show an estimated rent on every page. Name the "
             "family and the reason.", kind="markdown")
hw.part("c", "For part b, would you report a confidence interval or a prediction interval "
             "around the number shown to a user? Explain the difference in one sentence.",
        kind="markdown")
hw.part("d", "Fit whichever model you named in part a and report the coefficient with its "
             "interval, in rupees per square foot.")

hw.problem(5, """*What can and cannot be said.* Written answers, no new computation.""")
hw.part("a", "Your forest achieved a lower cross-validated error than your regression on the "
             "rent data. Write the two-sentence summary you would send a manager who has asked "
             "whether size causes higher rent.", kind="markdown")
hw.part("b", "A colleague reports that `Bathroom` had the highest importance in the forest and "
             "concludes that adding a bathroom is the best way to raise rent. Give two separate "
             "reasons that conclusion is not supported.", kind="markdown")
hw.part("c", "Across this assignment you used coefficients, importances, AIC, and cross-"
             "validated error. For each, write one sentence on the question it answers.",
        kind="markdown")

hw.write("Stat_220_HW_Unit02_Map_of_Models.ipynb")
