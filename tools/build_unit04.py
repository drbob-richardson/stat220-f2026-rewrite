#!/usr/bin/env python3
"""Unit 4: Prediction and Choosing Predictors. Code companion and homework."""
from nblib import CodeNB, HW

URL = "https://drbob-richardson.github.io/stat220/F2026/data/moving_jobs.csv"
DELIVERY_URL = "https://drbob-richardson.github.io/stat220/F2026/data/delivery_routes.csv"

# =====================================================================
# CODE COMPANION
# =====================================================================
nb = CodeNB(4, "Prediction and Choosing Predictors",
            "Predict a new case, put the right interval on it, measure error honestly, and "
            "compare a few sets of predictors. Short cells, meant to be run one at a time.")

nb.section("Setup")
nb.code(f"""import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score, train_test_split

jobs = pd.read_csv("{URL}")
jobs.head()""")

nb.section("1. Fit the model")
nb.code("""fit = smf.ols("hours ~ volume_cuft + crew_size + stairs_flights + miles + packing_service",
              data=jobs).fit()
fit.params.round(4)""")

nb.section("2. Predict one new job")
nb.md("A new customer: 800 cubic feet, a crew of 3, two flights of stairs, 12 miles, and packing.")
nb.code("""new = pd.DataFrame({"volume_cuft": [800], "crew_size": [3], "stairs_flights": [2],
                    "miles": [12], "packing_service": [1]})
fit.predict(new)""")

nb.section("3. The two intervals")
nb.code("""fit.get_prediction(new).summary_frame(alpha=0.05).round(2)""")
nb.md("`mean_ci_lower` and `mean_ci_upper` are the **confidence interval** for the average job "
      "like this one. `obs_ci_lower` and `obs_ci_upper` are the **prediction interval** for this "
      "one job. The prediction interval is the wide one, and it is the one a dispatcher needs.")

nb.section("4. Is the new job inside the data?",
           "Each value on its own, and then the combination.")
nb.code("""print(jobs[["volume_cuft", "crew_size", "miles"]].describe().loc[["min", "max"]])

near = jobs[(jobs.volume_cuft.between(700, 900)) & (jobs.crew_size == 3)]
print(f"\\ncompleted jobs with a similar volume AND the same crew size: {len(near)}")""")
nb.md("Both checks matter. A value can be ordinary on its own while the combination never "
      "happened, and the model gives no warning when that is the case.")

nb.section("5. Error on your own rows is too small")
nb.code("""X = jobs[["volume_cuft", "crew_size", "stairs_flights", "miles", "packing_service"]]
y = jobs["hours"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

m = LinearRegression().fit(X_train, y_train)
print("error on the rows it was fitted on:", round(np.sqrt(((y_train - m.predict(X_train))**2).mean()), 2))
print("error on the rows held back      :", round(np.sqrt(((y_test - m.predict(X_test))**2).mean()), 2))""")

nb.section("6. Cross-validation, so every row gets held out once")
nb.code("""folds = KFold(5, shuffle=True, random_state=0)
mse = -cross_val_score(LinearRegression(), X, y, cv=folds, scoring="neg_mean_squared_error")
print("error in each of the five rounds:", np.sqrt(mse).round(3))
print("average:", np.sqrt(mse.mean()).round(3), "hours")""")

nb.section("7. Compare a few sets of predictors",
           "One branch office, 60 jobs, where an extra column actually costs something.")
nb.code("""branch = jobs.sample(60, random_state=5)

sets = {
    "volume only": ["volume_cuft"],
    "the five that make sense": ["volume_cuft", "crew_size", "stairs_flights",
                                 "miles", "packing_service"],
    "those five plus three junk": ["volume_cuft", "crew_size", "stairs_flights",
                                   "miles", "packing_service",
                                   "est_boxes", "dispatcher_rating", "weekend"],
}
for name, cols in sets.items():
    mse = -cross_val_score(LinearRegression(), branch[cols], branch.hours, cv=folds,
                           scoring="neg_mean_squared_error").mean()
    print(f"{name:<28} cross-validated error {np.sqrt(mse):.3f}")""")
nb.md("The junk columns make it worse. On all 600 jobs they would cost almost nothing, which is "
      "why the size of your data decides how much you can afford.")

nb.section("8. The same three sets, by R-squared and AIC")
nb.code("""for name, cols in sets.items():
    f = smf.ols("hours ~ " + " + ".join(cols), data=branch).fit()
    print(f"{name:<28} R2 {f.rsquared:.4f}   adj R2 {f.rsquared_adj:.4f}   AIC {f.aic:.1f}")""")
nb.md("$R^2$ is highest for the model with the junk in it. Adjusted $R^2$ and AIC both prefer "
      "the five that make sense. $R^2$ alone cannot choose a model.")

nb.section("9. A squared term is just another column",
           "Adding powers of a predictor is polynomial regression, and it is still ordinary "
           "least squares underneath.")
nb.code("""straight = ["volume_cuft", "crew_size", "stairs_flights", "miles", "packing_service"]
branch2 = branch.assign(volume_sq=branch.volume_cuft**2)

for name, cols in [("five predictors", straight),
                   ("plus volume squared", straight + ["volume_sq"])]:
    mse = -cross_val_score(LinearRegression(), branch2[cols], branch2.hours, cv=folds,
                           scoring="neg_mean_squared_error").mean()
    print(f"{name:<22} cross-validated error {np.sqrt(mse):.3f}")""")
nb.md("The relationship really does bend, but with 60 jobs there is not enough data to pay for "
      "the bend. With all 600 the squared term earns its place.")

nb.section("10. Lasso, which shrinks and drops")
nb.code("""from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler

cols = ["volume_cuft", "crew_size", "stairs_flights", "miles", "packing_service",
        "est_boxes", "dispatcher_rating", "weekend"]
Z = StandardScaler().fit_transform(branch[cols])

alphas = np.logspace(-3, 0.7, 80)          # the penalties to try
las = LassoCV(alphas=alphas, cv=5, random_state=0, max_iter=50000).fit(Z, branch.hours)
print("penalty chosen by cross-validation:", round(las.alpha_, 4))
print(pd.Series(las.coef_.round(3), index=cols).to_string())""")
nb.md("At the penalty with the best error the junk columns survive with coefficients near zero. "
      "Push the penalty higher and they go to exactly zero before any real predictor does.")

nb.write("Code_Unit04_Prediction.ipynb")


# =====================================================================
# HOMEWORK
# =====================================================================
# Deliberately a different dataset from the slides and the companion, so the
# homework is not the worked example with the numbers changed.
hw = HW(4, "Prediction and Choosing Predictors",
        f"""`delivery_routes.csv` is 500 completed delivery routes. `minutes` is how long the
route took. The predictors that make sense are `stops`, `packages`, `miles`, `downtown`, and
`rain`. The company also records `van_age_years`, `dispatcher_rating`, and `month`.

```python
import numpy as np, pandas as pd
import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score, train_test_split

routes = pd.read_csv("{DELIVERY_URL}")
folds = KFold(5, shuffle=True, random_state=0)
routes.head()
```""")

# ---------------- P1: a route, with the right interval ----------------
hw.problem(1, """*Planning tomorrow's schedule.* Tomorrow's route has 45 stops, 110 packages,
38 miles, goes downtown, and no rain is forecast.""")
hw.given("a", "Report the predicted minutes, the confidence interval, and the prediction "
              "interval. Say in one sentence what each of the two intervals is about.",
'''fit = smf.ols("minutes ~ stops + packages + miles + downtown + rain", data=routes).fit()

new = pd.DataFrame({"stops": [45], "packages": [110], "miles": [38],
                    "downtown": [1], "rain": [0]})
print(fit.get_prediction(new).summary_frame(alpha=0.05).round(1))''')
hw.part("b", "The dispatcher has to tell one driver when to expect to finish tomorrow. Which of "
             "the two intervals should they use, and why?", kind="markdown")
hw.part("c", "The operations manager asks a different question: across all the downtown routes "
             "like this one, what is our average time? Which interval answers that one?",
        kind="markdown")

# ---------------- P2: is the case inside the data ----------------
hw.problem(2, """*A route that looks ordinary.* A planner asks for a prediction for a route with
25 stops and 120 packages.""")
hw.given("a", "Each value is common on its own. Report how many completed routes are near each "
              "value, and how many are near both.",
'''near_stops = routes.stops.between(20, 30)
near_packages = routes.packages.between(110, 130)

print("routes near this stop count   :", near_stops.sum())
print("routes near this package count:", near_packages.sum())
print("routes near both              :", (near_stops & near_packages).sum())
print("correlation between stops and packages:", round(routes.stops.corr(routes.packages), 2))''')
hw.part("b", "In three or four sentences, explain what your part a numbers mean for a prediction "
             "for this route, and what you would tell the planner who asked for it.",
        kind="markdown")

# ---------------- P3: honest error ----------------
hw.problem(3, """*How wrong will it be?* A new depot has 50 completed routes so far, and the
manager wants one number for how far off a time estimate typically is.""")
hw.given("a", "Report both numbers, and say which one you would give the manager.",
'''depot = routes.sample(50, random_state=3)
X = depot[["stops", "packages", "miles", "downtown", "rain"]]
y = depot["minutes"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
m = LinearRegression().fit(X_train, y_train)

print("on the rows it was fitted on:", round(np.sqrt(((y_train - m.predict(X_train))**2).mean()), 1))
print("on the rows held back       :", round(np.sqrt(((y_test - m.predict(X_test))**2).mean()), 1))''')
hw.part("b", "Explain in two or three sentences why those two numbers differ, and which way the "
             "difference would go if the depot had 500 routes instead of 50.", kind="markdown")

# ---------------- P4: choosing predictors ----------------
hw.problem(4, """*Which predictors belong?* Still the 50-route depot.""")
hw.given("a", "Report the cross-validated error, the $R^2$, and the AIC for each set. Say which "
              "set you would ship.",
'''sets = {
    "stops only": ["stops"],
    "the five that make sense": ["stops", "packages", "miles", "downtown", "rain"],
    "those five plus three junk": ["stops", "packages", "miles", "downtown", "rain",
                                   "van_age_years", "dispatcher_rating", "month"],
}
for name, cols in sets.items():
    mse = -cross_val_score(LinearRegression(), depot[cols], depot.minutes, cv=folds,
                           scoring="neg_mean_squared_error").mean()
    f = smf.ols("minutes ~ " + " + ".join(cols), data=depot).fit()
    print(f"{name:<28} CV error {np.sqrt(mse):5.1f}   R2 {f.rsquared:.4f}   AIC {f.aic:.1f}")''')
hw.part("b", "One set has the highest $R^2$ and is still not the set you would ship. Explain "
             "what $R^2$ is doing here in two or three sentences.", kind="markdown")
hw.part("c", "A colleague wants to add a squared term in `stops` on top of the five. Say what "
             "you would check before agreeing, and what you would expect with only 50 routes.",
        kind="markdown")

# ---------------- P5: what can we say ----------------
hw.problem(5, """*What can and cannot be said.* No computer.""")
hw.part("a", "A colleague ran stepwise selection over 65 columns, kept the 11 with p-values "
             "under 0.05, and reports an $R^2$ of 0.96 with every predictor significant. Write "
             "the two or three sentences you would say in response.", kind="markdown")
hw.part("b", "A lasso fit sends `rain` to exactly zero. Does that show rain has no effect on "
             "how long a route takes? Explain.", kind="markdown")
hw.part("c", "The model predicts well and `packages` has a large coefficient. The manager asks "
             "whether splitting the same deliveries into more packages would make routes take "
             "longer. Answer in two or three sentences.", kind="markdown")

hw.write("Stat_220_HW_Unit04_Prediction.ipynb")
