#!/usr/bin/env python3
"""Unit 6: Inference Without a Formula. Code companion and homework.

The companion runs on the rental listings the Unit 5 homework used, so the
lecture, the companion and the slides are all the same data. The homework runs
on the delivery routes from the Unit 4 homework, which already carry three
columns that do nothing, so the importance exercise needs no invented data.
"""
from nblib import CodeNB, HW

RENT = "https://drbob-richardson.github.io/stat220/F2026/data/rent.csv"
ROUTES = "https://drbob-richardson.github.io/stat220/F2026/data/delivery_routes.csv"

# =====================================================================
# CODE COMPANION
# =====================================================================
nb = CodeNB(6, "Inference Without a Formula",
            "Get a ranking out of a forest, find out the default ranking is wrong, and build "
            "intervals for things no formula covers. Short cells, meant to be run one at a time.")

nb.section("Setup", "The last column is added here and means nothing. That is the point of it.")
nb.code(f"""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(6)
rents = pd.read_csv("{RENT}")
rents = rents[(rents.Rent > 0) & (rents.Size > 0)].copy()
rents["id_number"] = rng.integers(100000, 999999, len(rents))
rents.head()""")

nb.section("1. Fit a forest")
nb.code("""cols = ["Size", "BHK", "Bathroom", "City", "FurnishingStatus", "id_number"]
X = pd.get_dummies(rents[cols], drop_first=True)
y = np.log(rents.Rent)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

forest = RandomForestRegressor(n_estimators=300, random_state=0, oob_score=True,
                               n_jobs=-1).fit(X_train, y_train)
print("held-out R2:", round(forest.score(X_test, y_test), 3))
print("out-of-bag R2:", round(forest.oob_score_, 3))""")
nb.md("The out-of-bag number comes free: every tree is fitted on its own resample, so each row "
      "can be scored by the trees that never saw it.")

nb.section("2. The importance the software gives you by default")
nb.code("""impurity = pd.Series(forest.feature_importances_, index=X.columns)
impurity.sort_values(ascending=False).head(6).round(3)""")
nb.md("`id_number` is a column of random digits. Look at where it placed.")

nb.section("3. Permutation importance instead")
nb.code("""perm = permutation_importance(forest, X_test, y_test, n_repeats=10,
                              random_state=0, n_jobs=-1)
permutation = pd.Series(perm.importances_mean, index=X.columns)
permutation.sort_values(ascending=False).head(6).round(3)""")

nb.section("4. The two rankings side by side")
nb.code("""pd.DataFrame({"impurity": impurity.round(3),
              "permutation": permutation.round(3)}).sort_values("impurity", ascending=False)""")
nb.md("The two disagree about the real columns and they disagree about the fake one. Only one of "
      "them puts a random number where it belongs.")

nb.section("5. One resample, to see what it is")
nb.code("""one = rents.sample(len(rents), replace=True)
print("rows:", len(one), " distinct rows drawn:", one.index.nunique())
print("share of the original rows that appear at least once:",
      round(one.index.nunique() / len(rents), 3))""")
nb.md("About 63% of the rows appear, some of them more than once. That reshuffling is the whole "
      "mechanism.")

nb.section("6. An interval where a formula already exists",
           "Fit the elasticity 400 times, on 400 resamples.")
nb.code("""RHS = "BHK + Bathroom + C(City) + C(FurnishingStatus)"

boot = []
for i in range(400):
    sample = rents.sample(len(rents), replace=True)
    fit = smf.ols(f"np.log(Rent) ~ np.log(Size) + {RHS}", data=sample).fit()
    boot.append(fit.params["np.log(Size)"])

print("bootstrap 95%:", np.percentile(boot, [2.5, 97.5]).round(4))""")

nb.section("7. What the formula says")
nb.code("""full = smf.ols(f"np.log(Rent) ~ np.log(Size) + {RHS}", data=rents).fit()
print("estimate:", round(full.params["np.log(Size)"], 4))
print("formula 95%:", full.conf_int().loc["np.log(Size)"].values.round(4))""")
nb.md("The two agree. That is the argument for trusting the method on quantities where no formula "
      "is available.")

nb.section("8. A gap between two medians, which has no formula")
nb.code("""mumbai = rents.Rent[rents.City == "Mumbai"]
delhi = rents.Rent[rents.City == "Delhi"]

gap = [mumbai.sample(len(mumbai), replace=True).median()
       - delhi.sample(len(delhi), replace=True).median() for _ in range(2000)]

print("gap in medians:", f"Rs {mumbai.median() - delhi.median():,.0f}")
print("95% interval  :", [f"Rs {v:,.0f}" for v in np.percentile(gap, [2.5, 97.5])])""")
nb.md("Each city is resampled on its own, so each keeps its own sample size.")

nb.section("9. An interval on an importance score",
           "Resample the training rows only. The test set stays as it is.")
nb.code("""def importance_of(X_fit, y_fit, seed):
    f = RandomForestRegressor(n_estimators=40, random_state=0, n_jobs=-1).fit(X_fit, y_fit)
    r = permutation_importance(f, X_test, y_test, n_repeats=4, random_state=seed, n_jobs=-1)
    return pd.Series(r.importances_mean, index=X.columns)

rows = []
for i in range(25):
    take = rng.integers(0, len(X_train), len(X_train))
    rows.append(importance_of(X_train.iloc[take], y_train.iloc[take], i))
reps = pd.DataFrame(rows)

for c in ["City_Mumbai", "Size", "Bathroom", "BHK", "id_number"]:
    lo, hi = np.percentile(reps[c], [2.5, 97.5])
    print(f"{c:<14} [{lo:+.3f}, {hi:+.3f}]", "  straddles zero" if lo <= 0 <= hi else "")""")

nb.section("10. The mistake that makes everything look important",
           "The same thing, resampling before the split instead of after.")
nb.code("""rows = []
for i in range(25):
    sample = rents.sample(len(rents), replace=True)
    Xs = pd.get_dummies(sample[cols], drop_first=True)
    ys = np.log(sample.Rent)
    a, b, c, d = train_test_split(Xs, ys, test_size=0.3, random_state=i)
    f = RandomForestRegressor(n_estimators=40, random_state=0, n_jobs=-1).fit(a, c)
    r = permutation_importance(f, b, d, n_repeats=4, random_state=i, n_jobs=-1)
    rows.append(pd.Series(r.importances_mean, index=Xs.columns))

bad = pd.DataFrame(rows)
lo, hi = np.percentile(bad["id_number"], [2.5, 97.5])
print(f"id_number, resampling before the split: [{lo:+.3f}, {hi:+.3f}]")""")
nb.md("The same column of random digits now has an interval sitting well above zero. Resampling "
      "first puts the same listing in the training set and the test set, the forest remembers it, "
      "and shuffling any column appears to hurt. Nothing errors.")

nb.section("11. The whole method, as something you can reuse",
           "Everything above is this function with a different third argument.")
nb.code("""def bootstrap_interval(data, statistic, n=2000, level=95, seed=0):
    \"\"\"Resample `data` with replacement, apply `statistic`, return the interval.\"\"\"
    r = np.random.default_rng(seed)
    kept = [statistic(data.iloc[r.integers(0, len(data), len(data))]) for _ in range(n)]
    edge = (100 - level) / 2
    return np.percentile(kept, [edge, 100 - edge])


print("median rent      :", bootstrap_interval(rents, lambda s: s.Rent.median()).round(0))
print("mean rent        :", bootstrap_interval(rents, lambda s: s.Rent.mean()).round(0))
print("90th percentile  :", bootstrap_interval(rents, lambda s: s.Rent.quantile(0.9)).round(0))
print("share over 50k   :", bootstrap_interval(rents, lambda s: (s.Rent > 50000).mean()).round(4))""")
nb.md("Four quantities, four intervals, one function. Three of the four have no standard error "
      "formula you could have looked up.")

nb.write("Code_Unit06_Inference_Without_a_Formula.ipynb")


# =====================================================================
# HOMEWORK
# =====================================================================
hw = HW(6, "Inference Without a Formula",
        f"""`delivery_routes.csv` is the 500 routes from the Unit 4 homework. `minutes` is how
long a route took. Five columns describe the route: `stops`, `packages`, `miles`, `downtown` and
`rain`. Three more get recorded and have nothing to do with how long anything takes:
`van_age_years`, `dispatcher_rating` and `month`. You will need that last fact.

Run the next two cells first.""")

hw.code("""%pip install -q numpy pandas statsmodels scikit-learn matplotlib""")

hw.code(f"""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

routes = pd.read_csv("{ROUTES}")
PREDICTORS = ["stops", "packages", "miles", "downtown", "rain",
              "van_age_years", "dispatcher_rating", "month"]
routes.head()""")

# ---------------- P1 ----------------
hw.problem(1, """Fit a forest to the routes and find out how well it does.""")
hw.given("a", "Report the held-out $R^2$ and the out-of-bag $R^2$. Say in one sentence what the "
              "out-of-bag number is and why it costs nothing to compute.",
'''X = routes[PREDICTORS]
y = routes["minutes"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

forest = RandomForestRegressor(n_estimators=300, random_state=0, oob_score=True,
                               n_jobs=-1).fit(X_train, y_train)
print("held-out R2:", round(forest.score(X_test, y_test), 3))
print("out-of-bag R2:", round(forest.oob_score_, 3))''')
hw.part("b", "The two numbers are close. Say what it would mean if the out-of-bag number were "
             "much higher than the held-out one.", kind="markdown")

# ---------------- P2 ----------------
hw.problem(2, """Now ask which columns it is using. Run both importance methods and compare them.""")
hw.given("a", "Report both rankings in one table.",
'''impurity = pd.Series(forest.feature_importances_, index=PREDICTORS)
perm = permutation_importance(forest, X_test, y_test, n_repeats=10, random_state=0, n_jobs=-1)
permutation = pd.Series(perm.importances_mean, index=PREDICTORS)

print(pd.DataFrame({"impurity": impurity.round(4),
                    "permutation": permutation.round(4)}).sort_values("impurity",
                                                                      ascending=False))''')
hw.part("b", "Both methods put `month` above `downtown` and `rain`. Two of those three columns "
             "are real and one is not. Say which, and explain in two or three sentences how a "
             "real predictor can finish below a column that means nothing.", kind="markdown")

# ---------------- P3 ----------------
hw.problem(3, """A ranking is not the same as an effect. Fit a regression on the same eight columns and see what it says instead.""")
hw.given("a", "Report the coefficient and p-value for `downtown`, `rain` and `month`.",
'''fit = smf.ols("minutes ~ " + " + ".join(PREDICTORS), data=routes).fit()
for c in ["downtown", "rain", "month"]:
    print(f"{c:<10} coef {fit.params[c]:+7.3f}   p {fit.pvalues[c]:.2g}")''')
hw.part("b", "The forest ranked `month` above `rain`. The regression says something different. "
             "Explain in three or four sentences what each of the two is measuring, and which "
             "one answers the question 'does rain add time to a route'.", kind="markdown")

# ---------------- P4 ----------------
hw.problem(4, """A ranking does not tell you whether a column is doing anything at all, or
whether it just happened to land above one that is doing nothing. Resampling does. Resample the
training rows only, and score against the test set you already have.""")
hw.given("a", "Report the point estimate and a 95% bootstrap interval for each column, and say "
              "which ones you cannot separate from zero.",
'''rng = np.random.default_rng(6)

def importance_of(X_fit, y_fit, seed):
    f = RandomForestRegressor(n_estimators=60, random_state=0, n_jobs=-1).fit(X_fit, y_fit)
    r = permutation_importance(f, X_test, y_test, n_repeats=4, random_state=seed, n_jobs=-1)
    return pd.Series(r.importances_mean, index=PREDICTORS)

base = importance_of(X_train, y_train, 0)
reps = pd.DataFrame([importance_of(X_train.iloc[take], y_train.iloc[take], k)
                     for k, take in enumerate(rng.integers(0, len(X_train),
                                                           (30, len(X_train))))])

for c in PREDICTORS:
    lo, hi = np.percentile(reps[c], [2.5, 97.5])
    flag = "  cannot separate from zero" if lo <= 0 <= hi else ""
    print(f"{c:<18} {base[c]:+.4f}  [{lo:+.4f}, {hi:+.4f}]{flag}")''')
hw.part("b", "In problem 3 the regression found `rain` real, with about seven extra minutes and a "
             "small p-value. Here the importance of `rain` cannot be separated from zero. Both "
             "results are correct. Explain in three or four sentences how that happens, and say "
             "which of the two you would report to someone asking whether rain slows deliveries.",
        kind="markdown")

# ---------------- P5 ----------------
hw.problem(5, """No computer for this one. Three colleagues, three claims.""")
hw.part("a", "A colleague fits a forest to customer data and reports that `account_number` is the "
             "second most important variable, using the default importance. Write the two or "
             "three sentences you would say in response.", kind="markdown")
hw.part("b", "Another colleague bootstraps a sample of 40 patients, gets a 95% interval, and says "
             "it shows the treatment works in the wider population. The 40 patients were all "
             "recruited from one clinic. Explain what the interval does and does not cover.",
        kind="markdown")
hw.part("c", "A third colleague resamples the whole dataset, then splits each resample into "
             "training and test rows, and reports bootstrap intervals for permutation importance. "
             "Every column comes out important. Say what went wrong.", kind="markdown")

hw.write("Stat_220_HW_Unit06_Inference_Without_a_Formula.ipynb")
