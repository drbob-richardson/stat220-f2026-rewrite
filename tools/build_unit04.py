#!/usr/bin/env python3
"""Unit 4: Prediction and Choosing Predictors. Code companion and homework."""
from nblib import CodeNB, HW

URL = "https://drbob-richardson.github.io/stat220/F2026/data/moving_jobs.csv"

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
hw = HW(4, "Prediction and Choosing Predictors",
        f"""`moving_jobs.csv` is 600 completed jobs at a moving company. `hours` is the crew's
time on site. The predictors that make sense are `volume_cuft`, `crew_size`, `stairs_flights`,
`miles`, and `packing_service`. The company also records `est_boxes`, `dispatcher_rating`,
and `weekend`.

```python
import numpy as np, pandas as pd
import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score, train_test_split

jobs = pd.read_csv("{URL}")
folds = KFold(5, shuffle=True, random_state=0)
jobs.head()
```""")

# ---------------- P1: a quote, with the right interval ----------------
hw.problem(1, """*Quoting a customer.* A customer is moving 650 cubic feet, with a crew of 2,
one flight of stairs, 20 miles, and no packing service.""")
hw.given("a", "Report the predicted hours, the confidence interval, and the prediction interval. "
              "Say in one sentence what each of the two intervals is about.",
'''fit = smf.ols("hours ~ volume_cuft + crew_size + stairs_flights + miles + packing_service",
              data=jobs).fit()

new = pd.DataFrame({"volume_cuft": [650], "crew_size": [2], "stairs_flights": [1],
                    "miles": [20], "packing_service": [0]})
print(fit.get_prediction(new).summary_frame(alpha=0.05).round(2))''')
hw.part("b", "The dispatcher has to block time on Tuesday's schedule for this one job. Which of "
             "the two intervals should they use, and why?", kind="markdown")
hw.part("c", "The owner asks a different question: across the next hundred jobs like this, what "
             "will our average time be? Which interval answers that one?", kind="markdown")

# ---------------- P2: is the case inside the data ----------------
hw.problem(2, """*A job that looks ordinary.* A customer reports 500 cubic feet and 90 boxes.""")
hw.given("a", "Each value is common on its own. Report how many completed jobs are near each "
              "value, and how many are near both.",
'''near_volume = jobs.volume_cuft.between(400, 600)
near_boxes = jobs.est_boxes.between(82, 98)

print("jobs near this volume    :", near_volume.sum())
print("jobs near this box count :", near_boxes.sum())
print("jobs near both           :", (near_volume & near_boxes).sum())''')
hw.part("b", "In three or four sentences, explain what your part a numbers mean for a prediction "
             "for this customer, and what you would tell the person who asked for it.",
        kind="markdown")

# ---------------- P3: honest error ----------------
hw.problem(3, """*How wrong will it be?* The owner wants one number for how far off a quote
typically is.""")
hw.given("a", "Report both numbers, and say which one you would give the owner.",
'''X = jobs[["volume_cuft", "crew_size", "stairs_flights", "miles", "packing_service"]]
y = jobs["hours"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
m = LinearRegression().fit(X_train, y_train)

print("on the rows it was fitted on:", round(np.sqrt(((y_train - m.predict(X_train))**2).mean()), 3))
print("on the rows held back       :", round(np.sqrt(((y_test - m.predict(X_test))**2).mean()), 3))''')
hw.part("b", "Explain in two or three sentences why those two numbers differ, and why the gap "
             "would be larger for a model with many more predictors.", kind="markdown")

# ---------------- P4: choosing predictors ----------------
hw.problem(4, """*Which predictors belong?* The branch office has 60 completed jobs so far.""")
hw.given("a", "Report the cross-validated error and the AIC for each set. Say which set you "
              "would ship.",
'''branch = jobs.sample(60, random_state=5)
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
    aic = smf.ols("hours ~ " + " + ".join(cols), data=branch).fit()
    print(f"{name:<28} CV error {np.sqrt(mse):.3f}   R2 {aic.rsquared:.4f}   AIC {aic.aic:.1f}")''')
hw.part("b", "One set has the highest $R^2$ and is still not the set you would ship. Explain "
             "what $R^2$ is doing here in two or three sentences.", kind="markdown")
hw.part("c", "A colleague says to run the same comparison on all 600 jobs instead of 60, and "
             "expects the junk columns to look better there. Would you expect the same "
             "conclusion? Say why.", kind="markdown")

# ---------------- P5: what can we say ----------------
hw.problem(5, """*What can and cannot be said.* No computer.""")
hw.part("a", "A colleague tried 65 columns, kept the 11 with p-values under 0.05, and reports "
             "$R^2 = 0.96$ with every predictor significant. Write the two or three sentences "
             "you would say in response.", kind="markdown")
hw.part("b", "A lasso fit sends `weekend` to exactly zero. Does that show weekends have no "
             "effect on how long a move takes? Explain.", kind="markdown")
hw.part("c", "Your model predicts well and `est_boxes` has a large coefficient. The owner asks "
             "whether telling customers to use fewer, larger boxes would shorten jobs. Answer "
             "in two or three sentences.", kind="markdown")

hw.write("Stat_220_HW_Unit04_Prediction.ipynb")
