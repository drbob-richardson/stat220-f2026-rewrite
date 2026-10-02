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
nb.code(f"""import pandas as pd
import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score, train_test_split

jobs = pd.read_csv("{URL}")
jobs.head()""")

nb.section("1. Fit the model")
nb.code("""fit = smf.ols("hours ~ volume_cuft + crew_size + stairs_flights + miles + packing_service",
              data=jobs).fit()
fit.params.round(3)""")

nb.section("2. Predict one new job")
nb.md("A new customer: 800 cubic feet, a crew of 3, two flights of stairs, 12 miles, and packing.")
nb.code("""new = pd.DataFrame({"volume_cuft": [800], "crew_size": [3], "stairs_flights": [2],
                    "miles": [12], "packing_service": [1]})
fit.predict(new)""")

nb.section("3. Both intervals at once")
nb.code("""fit.get_prediction(new).summary_frame(alpha=0.05).round(2)""")
nb.md("`mean_ci` is the **confidence interval** for the average job like this one. `obs_ci` is "
      "the **prediction interval** for this one job. The prediction interval is the wide one, "
      "and it is the one a dispatcher needs.")

nb.section("4. Error on the rows you fitted on is too small")
nb.code("""X = jobs[["volume_cuft", "crew_size", "stairs_flights", "miles", "packing_service"]]
y = jobs["hours"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
model = LinearRegression().fit(X_train, y_train)

print("error on the rows it was fitted on:", round(((y_train - model.predict(X_train))**2).mean()**0.5, 2))
print("error on the rows held back      :", round(((y_test - model.predict(X_test))**2).mean()**0.5, 2))""")

nb.section("5. Cross-validation holds out every row once")
nb.code("""folds = KFold(5, shuffle=True, random_state=0)
scores = -cross_val_score(LinearRegression(), X, y, cv=folds, scoring="neg_mean_squared_error")

print("error in each round:", (scores**0.5).round(2))
print("average            :", round(scores.mean()**0.5, 2), "hours")""")

nb.section("6. A smaller office, where an extra column costs something",
           "The same company, but only the 60 jobs one branch has done.")
nb.code("""branch = jobs.sample(60, random_state=5)

sensible = ["volume_cuft", "crew_size", "stairs_flights", "miles", "packing_service"]
junk = ["est_boxes", "dispatcher_rating", "weekend"]""")

nb.section("7. Score the five that make sense")
nb.code("""scores = -cross_val_score(LinearRegression(), branch[sensible], branch.hours, cv=folds,
                          scoring="neg_mean_squared_error")
print("cross-validated error:", round(scores.mean()**0.5, 3), "hours")""")

nb.section("8. Now add three columns that mean nothing")
nb.code("""scores = -cross_val_score(LinearRegression(), branch[sensible + junk], branch.hours, cv=folds,
                          scoring="neg_mean_squared_error")
print("cross-validated error:", round(scores.mean()**0.5, 3), "hours")""")
nb.md("Worse, on 60 jobs. With all 600 the same three columns would cost almost nothing, which "
      "is why the amount of data you have decides how much model you can afford.")

nb.section("9. The same two models, by R-squared and AIC")
nb.code("""small = smf.ols("hours ~ volume_cuft + crew_size + stairs_flights + miles + packing_service",
                data=branch).fit()
big = smf.ols("hours ~ volume_cuft + crew_size + stairs_flights + miles + packing_service"
              " + est_boxes + dispatcher_rating + weekend", data=branch).fit()

print("five predictors :  R2", round(small.rsquared, 4), "  AIC", round(small.aic, 1))
print("plus three junk :  R2", round(big.rsquared, 4), "  AIC", round(big.aic, 1))""")
nb.md("$R^2$ is higher for the model with the junk in it, and AIC is worse. $R^2$ goes up "
      "whenever you add a column, so it cannot choose a model for you.")

nb.section("10. A squared term is just another column",
           "Powers of a predictor are polynomial regression, and still ordinary least squares.")
nb.code("""branch = branch.assign(volume_sq=branch.volume_cuft**2)

scores = -cross_val_score(LinearRegression(), branch[sensible + ["volume_sq"]], branch.hours,
                          cv=folds, scoring="neg_mean_squared_error")
print("cross-validated error:", round(scores.mean()**0.5, 3), "hours")""")
nb.md("The relationship really does bend, but 60 jobs cannot pay for the bend. With all 600 the "
      "squared term earns its place.")

nb.section("11. Forward selection, step one",
           "Nothing is in the model yet. Try each column on its own and look at every p-value.")
nb.code("""for c in sensible + junk:
    fit = smf.ols("hours ~ " + c, data=branch).fit()
    print(c, " p =", format(fit.pvalues[c], ".2g"))""")
nb.md("Volume has the smallest p-value by a wide margin, so forward selection adds it first.")

nb.section("12. Forward selection, step two",
           "Volume is in. Try each of the others beside it, and again look at all of them.")
nb.code("""for c in sensible + junk:
    if c == "volume_cuft":
        continue
    fit = smf.ols("hours ~ volume_cuft + " + c, data=branch).fit()
    print(c, " p =", format(fit.pvalues[c], ".2g"))""")
nb.md("The p-values all moved once volume was in the model. Packing service is the smallest now, "
      "so it goes in next. Notice that `est_boxes` looked useful on its own and stopped looking "
      "useful beside volume, because the two carry nearly the same information.")

nb.section("13. The rest of the search, in a loop",
           "The same two steps, repeated until nothing left clears 0.05.")
nb.code("""chosen = []
remaining = sensible + junk

while remaining:
    pvals = {}
    for c in remaining:
        fit = smf.ols("hours ~ " + " + ".join(chosen + [c]), data=branch).fit()
        pvals[c] = fit.pvalues[c]

    best = min(pvals, key=pvals.get)
    if pvals[best] >= 0.05:
        break
    print("add", best, " p =", format(pvals[best], ".2g"))
    chosen.append(best)
    remaining.remove(best)

print()
print("forward selection keeps:", chosen)""")

nb.section("14. Backward elimination, the other direction",
           "Start with everything. Drop whichever column has the largest p-value, and stop when "
           "they are all under 0.05.")
nb.code("""keep = sensible + junk

while True:
    fit = smf.ols("hours ~ " + " + ".join(keep), data=branch).fit()
    pvals = fit.pvalues.drop("Intercept")
    if pvals.max() < 0.05:
        break
    print("drop", pvals.idxmax(), " p =", round(pvals.max(), 3))
    keep.remove(pvals.idxmax())

print()
print("backward elimination keeps:", keep)""")
nb.md("The three junk columns are the first to go on the way out, which is the ranking you want. "
      "But notice what the two searches cost you: the p-values printed at the end belong to a "
      "model that won a search, not to a test you planned, so they look stronger than they are. "
      "This is why the unit prefers a few candidate sets compared on held-out error.")

nb.section("15. Lasso shrinks the weak columns toward zero")
nb.code("""from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

# the scaler goes inside the pipeline, so each fold is scaled using only its own rows
model = make_pipeline(StandardScaler(), LassoCV(cv=5, random_state=0, max_iter=50000))
model.fit(branch[sensible + junk], branch.hours)

pd.Series(model[-1].coef_.round(3), index=sensible + junk)""")
nb.md("The three junk columns come back near zero. Raise the penalty and they hit exactly zero "
      "before any of the five real predictors does.")

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

Run the next two cells first. The first one installs what you need, and the second loads the
data that everything else here uses.""")

# Colab already has all of these, so this finishes in a second and prints nothing.
# On your own machine it installs anything you are missing.
hw.code("""%pip install -q numpy pandas statsmodels scikit-learn matplotlib""")

hw.code(f"""import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score, train_test_split

routes = pd.read_csv("{DELIVERY_URL}")
folds = KFold(5, shuffle=True, random_state=0)
routes.head()""")

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
