#!/usr/bin/env python3
"""Unit 3: Linear Regression. Code companion and homework."""
from nblib import CodeNB, HW

# =====================================================================
# CODE COMPANION
# =====================================================================
nb = CodeNB(3, "Linear Regression",
            "Fitting a line, reading a slope with its units and its uncertainty, checking the "
            "residuals, putting a category into a model, and watching a coefficient change when "
            "another variable joins it.")

nb.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from scipy import stats

rng = np.random.default_rng(220)
plt.rcParams["figure.figsize"] = (7, 3.5)

cars = pd.read_csv("https://richardson.byu.edu/220/cars.csv").dropna()
print(cars.shape); cars.head()""")

nb.section("1. A first fit, read out loud")
nb.code("""fit = smf.ols("mpg ~ weight", data=cars).fit()
print(fit.summary().tables[1])

b1 = fit.params["weight"]
lo, hi = fit.conf_int().loc["weight"]
print(f"\\nSlope      : {b1:.5f} mpg per pound")
print(f"Per 1000 lb: {1000*b1:.2f} mpg, 95% interval {1000*lo:.2f} to {1000*hi:.2f}")
print(f"Weight runs from {cars.weight.min():.0f} to {cars.weight.max():.0f} lb in this data")""")
nb.md("The raw slope, $-0.0076$, looks like nothing. Per 1,000 pounds it is $-7.6$ mpg, which is "
      "large. Same number, same model. The units decide whether anyone understands you.")

nb.section("2. What least squares actually minimizes",
           "Try a grid of candidate slopes and watch the sum of squared residuals bottom out at "
           "exactly the fitted value.")
nb.code("""b0 = fit.params["Intercept"]
slopes = np.linspace(b1 - 0.004, b1 + 0.004, 200)
sse = [((cars.mpg - (b0 + s*cars.weight))**2).sum() for s in slopes]

plt.plot(slopes*1000, sse, color="#4878a8", lw=2)
plt.axvline(b1*1000, color="#c0392b", lw=2, label=f"least-squares slope = {b1*1000:.2f} per 1000 lb")
plt.xlabel("candidate slope (mpg per 1000 lb)"); plt.ylabel("sum of squared residuals")
plt.legend(); plt.show()""")

nb.section("3. A slope is an estimate, so it wobbles",
           "Here we know the truth because we made it up. Simulate the same study many times and "
           "the spread of the slopes is what the standard error is estimating.")
nb.code("""def one_study(n=200, true_slope=1.5):
    x = rng.normal(0, 1, n)
    y = 3 + true_slope*x + rng.normal(0, 2, n)
    return smf.ols("y ~ x", data=pd.DataFrame({"x": x, "y": y})).fit()

one = one_study()
many = np.array([one_study().params["x"] for _ in range(1000)])

print(f"true slope                      : 1.500")
print(f"one study's estimate            : {one.params['x']:.3f}")
print(f"that study's reported SE         : {one.bse['x']:.3f}")
print(f"SD of 1000 estimates (the truth) : {many.std():.3f}")
plt.hist(many, bins=30, color="#4878a8", edgecolor="white")
plt.axvline(1.5, color="#c0392b", lw=2, label="true slope")
plt.xlabel("estimated slope"); plt.legend(); plt.show()""")
nb.md("The standard error printed by a single fit is an estimate of that spread, computed without "
      "ever rerunning the study. The $t$-statistic is the same ratio as in Unit 1: the estimate "
      "divided by its standard error.")

nb.section("4. Look at what the model missed",
           "Residuals against fitted values. A shapeless cloud is what you want.")
nb.code("""plt.scatter(fit.fittedvalues, fit.resid, s=12, alpha=0.6, color="#4878a8")
plt.axhline(0, color="#c0392b", lw=1.5)
plt.xlabel("fitted mpg"); plt.ylabel("residual (actual minus fitted)"); plt.show()

print(f"R-squared   : {fit.rsquared:.3f}")
print(f"residual SD : {np.sqrt(fit.scale):.2f} mpg")""")
nb.md("The residuals bend: they sit above zero at both ends and below it in the middle, so the "
      "line under-predicts the lightest and heaviest cars. That is a straight line fitted to a "
      "relationship that curves. The residual SD says a typical car sits about that many mpg off "
      "the line, which is the number to quote when someone asks how good the model is.")

nb.section("5. A 0/1 predictor is a two-group comparison",
           "Regression on a dummy variable reproduces the two-sample t-test exactly.")
nb.code("""cars["is_american"] = (cars["origin"] == "American").astype(int)
d = smf.ols("mpg ~ is_american", data=cars).fit()

amer = cars.loc[cars.is_american == 1, "mpg"]
other = cars.loc[cars.is_american == 0, "mpg"]

print(f"intercept (mean of the 0 group)  : {d.params['Intercept']:.3f}")
print(f"actual mean of the 0 group       : {other.mean():.3f}")
print(f"dummy coefficient (difference)   : {d.params['is_american']:.3f}")
print(f"actual difference in means       : {amer.mean() - other.mean():.3f}")
print(f"\\nregression t        : {d.tvalues['is_american']:.3f}")
print(f"pooled two-sample t : {stats.ttest_ind(amer, other, equal_var=True).statistic:.3f}")""")
nb.md("Same estimate, same standard error, same $p$-value. The two-group comparison from Unit 1 "
      "is a regression with one 0/1 predictor.")

nb.section("6. A category with more than two levels",
           "One level becomes the baseline and every other coefficient is read against it.")
nb.code("""m = smf.ols("mpg ~ C(origin)", data=cars).fit()
print(m.params.round(2), "\\n")
print("baseline is the level that is missing from that list:",
      sorted(cars.origin.unique())[0])
print(cars.groupby("origin").mpg.mean().round(2))""")
nb.md("Each coefficient is that origin versus the baseline, not versus zero and not versus the "
      "other levels. Add the baseline mean to a coefficient and you get that group's mean.")

nb.section("7. When the slope itself differs by group: an interaction")
nb.code("""inter = smf.ols("mpg ~ weight * is_american", data=cars).fit()
print(inter.params.round(6), "\\n")

b_w = inter.params["weight"]
b_wa = inter.params["weight:is_american"]
print(f"slope for non-American cars : {1000*b_w:.2f} mpg per 1000 lb")
print(f"slope for American cars     : {1000*(b_w + b_wa):.2f} mpg per 1000 lb")
print(f"p-value on the interaction  : {inter.pvalues['weight:is_american']:.3f}")""")
nb.md("With the interaction in the model, the coefficient on `weight` is the slope for the group "
      "coded 0, not an overall slope. The interaction term is the gap between the two slopes.")

nb.section("8. A coefficient changes when another variable joins it",
           "First in a made-up world where we know the answer, then in the real data.")
nb.code("""n = 3000
z = rng.normal(0, 1, n)                    # the lurking variable
x = 0.8*z + rng.normal(0, 0.6, n)          # x is driven by z
y = 2.0*z + rng.normal(0, 1.0, n)          # y is driven by z, NOT by x
sim = pd.DataFrame({"x": x, "y": y, "z": z})

naive = smf.ols("y ~ x", data=sim).fit()
adjusted = smf.ols("y ~ x + z", data=sim).fit()
print(f"true effect of x on y         : 0.000")
print(f"slope on x, z left out        : {naive.params['x']:.3f}  (t = {naive.tvalues['x']:.1f})")
print(f"slope on x, z included        : {adjusted.params['x']:.3f}  (t = {adjusted.tvalues['x']:.1f})")""")
nb.md("The naive regression reports a large, overwhelmingly significant effect of something that "
      "does nothing. More rows would only make the $t$-statistic bigger. Including $z$ is what "
      "fixes it, and in real work you have to know to look for $z$.")

nb.code("""raw = smf.ols("mpg ~ acceleration", data=cars).fit()
adj = smf.ols("mpg ~ acceleration + weight", data=cars).fit()

print(f"slope on acceleration, alone          : {raw.params['acceleration']:+.3f} mpg per second")
print(f"slope on acceleration, with weight    : {adj.params['acceleration']:+.3f} mpg per second")
print(f"share of the raw association left     : "
      f"{100*adj.params['acceleration']/raw.params['acceleration']:.0f}%")
print(f"\\ncorr(acceleration, weight) = {cars.acceleration.corr(cars.weight):+.2f}")""")
nb.md("Heavy cars are both slow to accelerate and thirsty, so most of the raw relationship was "
      "weight under another name. This does not show that acceleration has no effect. It shows "
      "that the raw number was mostly something else.")

nb.section("9. Significant is not the same as useful")
nb.code("""print(f"p-value on acceleration : {raw.pvalues['acceleration']:.2e}")
print(f"R-squared               : {raw.rsquared:.3f}")
print(f"residual SD             : {np.sqrt(raw.scale):.2f} mpg")""")
nb.md("Overwhelmingly significant, and it explains under a fifth of the variation. The $p$-value, "
      "the slope, and $R^2$ answer three different questions.")

nb.write("Code_Unit03_Regression.ipynb")


# =====================================================================
# HOMEWORK
# =====================================================================
hw = HW(3, "Linear Regression",
        """`housing_data.csv` is 1,000 home sales with `house_price`, `square_footage`,
`num_bedrooms`, `has_garage` (1 or 0), and `neighborhood`.

```python
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

rng = np.random.default_rng(220)
homes = pd.read_csv("https://richardson.byu.edu/220/housing_data.csv")
homes.head()
```""")

# ---------------- P1: simulation lab ----------------
hw.problem(1, """*A slope you already know the answer to.* You set the truth, then see what the
regression reports back.""")
hw.given("a", "Run this. The true slope is 1.5. Report the estimate and its 95% interval, and say "
              "whether the interval covers the truth.",
'''n = 200
x = rng.normal(0, 1, n)
y = 3 + 1.5*x + rng.normal(0, 2, n)

fit = smf.ols("y ~ x", data=pd.DataFrame({"x": x, "y": y})).fit()
print(f"estimated slope : {fit.params['x']:.3f}")
print(f"standard error  : {fit.bse['x']:.3f}")
print("95% interval    :", fit.conf_int().loc["x"].round(3).tolist())''')
hw.given("b", "This repeats that study 500 times. Compare the spread of the 500 estimates to the "
              "standard error one study reported in part a, and say what a standard error is "
              "measuring.",
'''slopes = []
for _ in range(500):
    xs = rng.normal(0, 1, n)
    ys = 3 + 1.5*xs + rng.normal(0, 2, n)
    slopes.append(smf.ols("y ~ x", data=pd.DataFrame({"x": xs, "y": ys})).fit().params["x"])

print(f"mean of the 500 estimates : {np.mean(slopes):.3f}")
print(f"SD of the 500 estimates   : {np.std(slopes):.3f}")''')
hw.part("c", "In part b the estimates are centered on 1.5 but individually off by a fair amount. "
             "A classmate says the regression is therefore unreliable. Answer them in two or "
             "three sentences.", kind="markdown")

# ---------------- P2: a slope with a decision attached ----------------
hw.problem(2, """*What is a square foot worth?* A homeowner is deciding whether to add 400 square
feet and wants a number.""")
hw.part("a", "Fit `house_price` on `square_footage` and report the slope with its units and its "
             "95% confidence interval. (`smf.ols(\"house_price ~ square_footage\", data=homes)"
             ".fit()`, then `.conf_int()`.)")
hw.part("b", "Write the one sentence you would tell the homeowner, including the units and the "
             "range of sizes the data actually covers.", kind="markdown")
hw.given("c", "Here is what the model missed. Say whether you see a pattern, and what that means "
              "for trusting the line.",
'''fit2 = smf.ols("house_price ~ square_footage", data=homes).fit()
plt.scatter(fit2.fittedvalues, fit2.resid, s=10, alpha=0.5)
plt.axhline(0, color="red"); plt.xlabel("fitted price"); plt.ylabel("residual"); plt.show()

print(f"R-squared   : {fit2.rsquared:.3f}")
print(f"residual SD : {np.sqrt(fit2.scale):,.0f} dollars")''')
hw.part("d", "The homeowner asks for the predicted price of a 6,000 square foot house. Look at "
             "the range in your part a answer and say, in two or three sentences, what you would "
             "tell them.", kind="markdown")

# ---------------- P3: categories ----------------
hw.problem(3, """*Adding a category.* The same homes, now with a garage and a neighborhood.""")
hw.given("a", "Report the coefficient on `has_garage` and write the sentence that interprets it. "
              "Say exactly what is being held fixed.",
'''g = smf.ols("house_price ~ square_footage + has_garage", data=homes).fit()
print(g.params.round(1))
print("\\n95% interval on has_garage:", g.conf_int().loc["has_garage"].round(0).tolist())''')
hw.given("b", "`neighborhood` has several levels. Name the baseline level, and explain how to "
              "read one of the other coefficients.",
'''nb_fit = smf.ols("house_price ~ square_footage + C(neighborhood)", data=homes).fit()
print(nb_fit.params.round(1))
print("\\nlevels in the data:", sorted(homes.neighborhood.unique()))''')
hw.part("c", "A realtor asks what a garage is worth. Answer in two or three sentences, using the "
             "number, its uncertainty, and the homes it applies to.", kind="markdown")

# ---------------- P4: a coefficient that changes ----------------
hw.problem(4, """*A coefficient that changes its mind.* Does an extra bedroom raise the price?""")
hw.given("a", "Report the bedroom coefficient from each model and say how much of the first one "
              "survived.",
'''alone = smf.ols("house_price ~ num_bedrooms", data=homes).fit()
with_size = smf.ols("house_price ~ num_bedrooms + square_footage", data=homes).fit()

print(f"bedrooms alone          : {alone.params['num_bedrooms']:+,.0f} dollars per bedroom")
print(f"bedrooms, with size in  : {with_size.params['num_bedrooms']:+,.0f} dollars per bedroom")
print(f"\\ncorr(bedrooms, square footage) = "
      f"{homes.num_bedrooms.corr(homes.square_footage):+.2f}")''')
hw.part("b", "Explain the mechanism in two or three sentences: why does leaving square footage "
             "out change the bedroom coefficient?", kind="markdown")
hw.part("c", "A builder asks whether splitting the same floor space into more bedrooms would "
             "raise the price. Which of the two numbers is closer to an answer for them, and what "
             "would still worry you?", kind="markdown")

# ---------------- P5: what can we say ----------------
hw.problem(5, """*What can and cannot be said.* No computer.""")
hw.part("a", "For your Problem 2 square footage slope, write one claim the analysis supports and "
             "one that sounds similar but it does not. Say what separates them.", kind="markdown")
hw.part("b", "Does the neighborhood coefficient in Problem 3 tell you what would happen to a "
             "house's price if you picked it up and moved it to that neighborhood? Explain.",
        kind="markdown")
hw.part("c", "A colleague summarizes the assignment as \"we found that square footage causes "
             "price to rise, garages add value, and bedrooms do not matter.\" Rewrite it so every "
             "claim is one your analyses support.", kind="markdown")

hw.write("Stat_220_HW_Unit03_Regression.ipynb")
