#!/usr/bin/env python3
"""Unit 5: When a Line Is Not Enough. Code companion and homework.

The companion runs on the diamonds, the same stones the slides use, so a
student can follow the lecture line by line. The homework runs on rental
listings, so it is not the worked example with the numbers changed.
"""
from nblib import CodeNB, HW

GEMS = "https://drbob-richardson.github.io/stat220/F2026/data/diamonds.csv"
RENT = "https://drbob-richardson.github.io/stat220/F2026/data/rent.csv"

# =====================================================================
# CODE COMPANION
# =====================================================================
nb = CodeNB(5, "When a Line Is Not Enough",
            "Read a residual plot, fix a fan with a log, grow a decision tree, and use what the "
            "tree found to improve the regression. Short cells, meant to be run one at a time.")

nb.section("Setup")
nb.code(f"""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from sklearn.tree import DecisionTreeRegressor, export_text
from sklearn.model_selection import train_test_split

gems = pd.read_csv("{GEMS}")
gems.head()""")

nb.section("1. The obvious model")
nb.code("""fit = smf.ols("price ~ carat + C(cut) + C(color) + C(clarity)", data=gems).fit()
print("R-squared:", round(fit.rsquared, 3))""")

nb.section("2. Look at the residuals before you believe it")
nb.code("""plt.scatter(fit.fittedvalues, fit.resid, s=6, alpha=0.4)
plt.axhline(0, color="red")
plt.xlabel("fitted price"); plt.ylabel("residual");""")
nb.md("A fan, and an arc. Both of the things the line cannot do.")

nb.section("3. Measure the fan instead of squinting at it")
nb.code("""resid = pd.DataFrame({"fitted": fit.fittedvalues, "resid": fit.resid})
low = resid[resid.fitted < resid.fitted.median()].resid.std()
high = resid[resid.fitted >= resid.fitted.median()].resid.std()
print("fan ratio:", round(high / low, 2))""")
nb.md("Near 1 means even spread. This is 2, so the errors on expensive stones are twice the "
      "size of the errors on cheap ones.")

nb.section("4. Take logs of both")
nb.code("""logfit = smf.ols("np.log(price) ~ np.log(carat) + C(cut) + C(color) + C(clarity)",
                 data=gems).fit()
print("R-squared:", round(logfit.rsquared, 3))""")

nb.section("5. The same picture, after the fix")
nb.code("""plt.scatter(logfit.fittedvalues, logfit.resid, s=6, alpha=0.4)
plt.axhline(0, color="red")
plt.xlabel("fitted log price"); plt.ylabel("residual");""")

nb.section("6. Read the coefficient")
nb.code("""b = logfit.params["np.log(carat)"]
print("elasticity:", round(b, 2))
print("a stone 10% heavier costs about", round(100 * (1.10**b - 1), 1), "% more")""")
nb.md("Both sides logged, so the coefficient is a percentage for a percentage.")

nb.section("7. One split, chosen by hand",
           "A tree picks the cut that makes the two groups as alike inside as possible. "
           "That is all it does, so you can do it yourself.")
nb.code("""def sse(cut):
    left = gems.price[gems.carat <= cut]
    right = gems.price[gems.carat > cut]
    return ((left - left.mean())**2).sum() + ((right - right.mean())**2).sum()

for cut in [0.5, 0.8, 1.0, 1.2, 1.5]:
    print(cut, format(sse(cut), ".3g"))""")

nb.section("8. The same split, from sklearn")
nb.code("""X = pd.get_dummies(gems[["carat", "cut", "color", "clarity"]], drop_first=True)
stump = DecisionTreeRegressor(max_depth=1, random_state=0).fit(X, gems.price)
print(export_text(stump, feature_names=list(X.columns), decimals=2))""")

nb.section("9. Keep splitting")
nb.code("""tree = DecisionTreeRegressor(max_depth=3, random_state=0).fit(X, gems.price)
print(export_text(tree, feature_names=list(X.columns), decimals=2))""")
nb.md("Read it out loud: the first cut is at **1.00 carat**. A round number, not a number the "
      "data had any reason to prefer.")

nb.section("10. How deep to go")
nb.code("""Xtr, Xte, ytr, yte = train_test_split(X, gems.price, test_size=0.3, random_state=0)

for depth in [1, 3, 5, 8, 12, 20]:
    t = DecisionTreeRegressor(max_depth=depth, random_state=0).fit(Xtr, ytr)
    fitted = np.sqrt(((ytr - t.predict(Xtr))**2).mean())
    heldout = np.sqrt(((yte - t.predict(Xte))**2).mean())
    print(f"depth {depth:>2}   on its own rows {fitted:7.0f}   on held-back rows {heldout:7.0f}")""")
nb.md("The first column falls forever. The second one bottoms out and then drifts back up. "
      "That second column is the only one that can choose a depth for you.")

nb.section("11. Why the tree cut at 1.00")
nb.code("""plt.hist(gems.carat[(gems.carat > 0.7) & (gems.carat < 1.4)], bins=70)
plt.axvline(1.0, color="red")
plt.xlabel("carat"); plt.ylabel("stones");""")
nb.md("A pile at 1.00 and a hole just below it. Cutters grind away weight to reach the round "
      "number, because buyers shop for *a one carat diamond*.")

nb.section("12. Put the tree's hint into the regression")
nb.code("""gems["over1"] = (gems.carat >= 1.0).astype(int)
jump = smf.ols("np.log(price) ~ np.log(carat) + over1 + C(cut) + C(color) + C(clarity)",
               data=gems).fit()

print("crossing one carat adds", round(100 * (np.exp(jump.params["over1"]) - 1), 1), "% to price")
print("p-value:", format(jump.pvalues["over1"], ".2g"))
print("AIC:", round(logfit.aic), "->", round(jump.aic))""")

nb.section("13. Say it in a sentence someone can use")
nb.code("""weight = 100 * ((1.01 / 0.98)**jump.params["np.log(carat)"] - 1)
jump_pct = 100 * (np.exp(jump.params["over1"]) - 1)

total = 100 * ((1 + weight/100) * (1 + jump_pct/100) - 1)
print(f"0.98 to 1.01 carat: {weight:.0f}% for the weight, {jump_pct:.0f}% for the round number")
print(f"total: about {total:.0f}% more for nearly the same rock")""")
nb.md("The tree found where to look. The regression said how much, and how sure.")

nb.write("Code_Unit05_When_a_Line_Is_Not_Enough.ipynb")


# =====================================================================
# HOMEWORK
# =====================================================================
hw = HW(5, "When a Line Is Not Enough",
        f"""`rent.csv` is 4,743 rental listings from six Indian cities. `Rent` is the monthly
rent in rupees. The predictors are `Size` (square feet), `BHK` (bedrooms), `Bathroom`, `City`,
and `FurnishingStatus`.

Rent in this market runs from about Rs 1,200 to Rs 3,500,000 a month, which is exactly the kind
of spread that breaks a straight line.

Run the next two cells first. The first installs what you need, and the second loads the data
everything else uses.""")

hw.code("""%pip install -q numpy pandas statsmodels scikit-learn matplotlib""")

hw.code(f"""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from sklearn.tree import DecisionTreeRegressor, export_text
from sklearn.model_selection import train_test_split

rent = pd.read_csv("{RENT}")
RHS = "BHK + Bathroom + C(City) + C(FurnishingStatus)"
rent.head()""")

# ---------------- P1: diagnose ----------------
hw.problem(1, """*Is the line in trouble?* Fit rent on the predictors as they come, and look
before you report anything.""")
hw.given("a", "Report the $R^2$ and the fan ratio, and paste the residual plot. The fan ratio is "
              "the spread of the residuals on the high half of the fitted values over the spread "
              "on the low half; 1 means even.",
'''plain = smf.ols(f"Rent ~ Size + {RHS}", data=rent).fit()

r = pd.DataFrame({"fitted": plain.fittedvalues, "resid": plain.resid})
fan = r[r.fitted >= r.fitted.median()].resid.std() / r[r.fitted < r.fitted.median()].resid.std()
print("R2:", round(plain.rsquared, 3), "  fan ratio:", round(fan, 2))

plt.scatter(plain.fittedvalues, plain.resid, s=6, alpha=0.4)
plt.axhline(0, color="red")
plt.xlabel("fitted rent"); plt.ylabel("residual");''')
hw.part("b", "Name the two things wrong with this residual plot, and say for each one what it "
             "means about the predictions the model would make.", kind="markdown")

# ---------------- P2: fix it ----------------
hw.problem(2, """*The fix.* Log both sides and look again.""")
hw.given("a", "Report the $R^2$ and the fan ratio for the logged model, next to the ones from "
              "problem 1.",
'''logged = smf.ols(f"np.log(Rent) ~ np.log(Size) + {RHS}", data=rent).fit()

r = pd.DataFrame({"fitted": logged.fittedvalues, "resid": logged.resid})
fan = r[r.fitted >= r.fitted.median()].resid.std() / r[r.fitted < r.fitted.median()].resid.std()
print("R2:", round(logged.rsquared, 3), "  fan ratio:", round(fan, 2))
print("coefficient on log(Size):", round(logged.params["np.log(Size)"], 3))

plt.scatter(logged.fittedvalues, logged.resid, s=6, alpha=0.4)
plt.axhline(0, color="red")
plt.xlabel("fitted log rent"); plt.ylabel("residual");''')
hw.part("b", "The coefficient on `np.log(Size)` is about 0.26. Write the sentence you would "
             "give a renter: what happens to the rent when the apartment is 10% bigger, with "
             "everything else the same?", kind="markdown")
hw.part("c", "The $R^2$ went from problem 1's value to this one. Explain in two sentences why "
             "those two numbers cannot be compared directly.", kind="markdown")

# ---------------- P3: grow a tree ----------------
hw.problem(3, """*A different idea.* Grow a shallow tree on the same columns and read it.""")
hw.given("a", "Print the tree and report its first three splits.",
'''X = pd.get_dummies(rent[["Size", "BHK", "Bathroom", "City", "FurnishingStatus"]],
                   drop_first=True)
y = np.log(rent.Rent)

tree = DecisionTreeRegressor(max_depth=3, random_state=0).fit(X, y)
print(export_text(tree, feature_names=list(X.columns), decimals=2))''')
hw.part("b", "Read the tree out loud: describe in plain words the kind of listing that lands in "
             "the most expensive leaf, and the kind that lands in the cheapest.", kind="markdown")
hw.part("c", "The tree never splits on `FurnishingStatus`. Say what that does and does not tell "
             "you about whether furnishing matters.", kind="markdown")

# ---------------- P4: how deep ----------------
hw.problem(4, """*How deep should it go?*""")
hw.given("a", "Report the table, and say which depth you would use.",
'''Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)

for depth in [1, 2, 4, 6, 8, 10, 12]:
    t = DecisionTreeRegressor(max_depth=depth, random_state=0).fit(Xtr, ytr)
    own = np.sqrt(((ytr - t.predict(Xtr))**2).mean())
    held = np.sqrt(((yte - t.predict(Xte))**2).mean())
    print(f"depth {depth:>2}   own rows {own:.3f}   held back {held:.3f}")''')
hw.part("b", "One column falls all the way down and the other turns around. Explain what each "
             "column is measuring and why only one of them can choose the depth.",
        kind="markdown")

# ---------------- P5: tree as scout ----------------
hw.problem(5, """*Let the tree inform the regression.* The tree splits on Mumbai, and then uses
a different `Size` cut inside the Mumbai branch than outside it. That is the tree's way of
saying that size is worth something different in Mumbai.""")
hw.given("a", "Report the interaction coefficient, its p-value, and the AIC of both models.",
'''rent["mumbai"] = (rent.City == "Mumbai").astype(int)
inter = smf.ols(f"np.log(Rent) ~ np.log(Size) + np.log(Size):mumbai + {RHS}", data=rent).fit()

b = inter.params["np.log(Size)"]
extra = inter.params["np.log(Size):mumbai"]
print("elasticity outside Mumbai:", round(b, 3))
print("elasticity in Mumbai     :", round(b + extra, 3))
print("p-value on the interaction:", format(inter.pvalues["np.log(Size):mumbai"], ".2g"))
print("AIC:", round(logged.aic), "->", round(inter.aic))''')
hw.part("b", "Write three or four sentences a property manager could use. Give the number, the "
             "units, what is being held fixed, and what they should do about it.",
        kind="markdown")
hw.part("c", "A colleague says this proves that building bigger apartments in Mumbai causes "
             "higher rent per square foot. Say what is wrong with that, and what the data does "
             "support.", kind="markdown")

hw.write("Stat_220_HW_Unit05_When_a_Line_Is_Not_Enough.ipynb")
