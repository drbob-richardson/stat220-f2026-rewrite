#!/usr/bin/env python3
"""Unit 3: Linear Regression. Code companion and homework."""
from nblib import CodeNB, HW

# =====================================================================
# CODE COMPANION
# =====================================================================
nb = CodeNB(3, "Linear Regression",
            "Fit a line, read the coefficient table, add and remove variables, and put a "
            "category in the model. Short cells, meant to be run one at a time.")

nb.section("Setup")
nb.code("""import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

cars = pd.read_csv("https://richardson.byu.edu/220/cars.csv").dropna()
cars.head()""")

nb.section("1. Look at the data first")
nb.code("""plt.scatter(cars.weight, cars.mpg, s=10)
plt.xlabel("weight (lb)"); plt.ylabel("mpg"); plt.show()""")

nb.section("2. Fit the line")
nb.md("`\"mpg ~ weight\"` reads as *mpg explained by weight*. The outcome goes on the left.")
nb.code("""fit = smf.ols("mpg ~ weight", data=cars).fit()
print(fit.summary())""")

nb.section("3. The coefficient table is the part you read")
nb.code("""print(fit.summary().tables[1])""")
nb.md("`coef` is the slope, `std err` its standard error, `t` the slope divided by that standard "
      "error, `P>|t|` the p-value for a true slope of zero, and the last two columns the 95% "
      "interval. The p-value here is 0.000, so a slope this far from zero would be very "
      "surprising if weight had no relationship with mpg.")

nb.section("4. Pull out one number at a time")
nb.code("""print("slope   :", fit.params["weight"])
print("SE      :", fit.bse["weight"])
print("t       :", fit.tvalues["weight"])
print("p-value :", fit.pvalues["weight"])
print("interval:", fit.conf_int().loc["weight"].tolist())""")
nb.md("The slope is $-0.0076$ mpg per pound, which is $-7.6$ mpg per 1,000 pounds. Always rescale "
      "to units someone can picture.")

nb.section("5. How well does it fit?")
nb.code("""print("R-squared  :", fit.rsquared)
print("residual SD:", fit.resid.std())""")
nb.md("$R^2$ is the share of the variation in mpg the line accounts for. The residual SD says a "
      "typical car sits about that many mpg off the line.")

nb.section("6. Look at what the line missed")
nb.code("""plt.scatter(fit.fittedvalues, fit.resid, s=10)
plt.axhline(0, color="red")
plt.xlabel("fitted mpg"); plt.ylabel("residual"); plt.show()""")
nb.md("These residuals curve, which says a straight line is not quite the right shape here.")

nb.section("7. Add a variable")
nb.code("""fit2 = smf.ols("mpg ~ weight + horsepower", data=cars).fit()
print(fit2.summary().tables[1])""")
nb.code("""print("weight alone      :", fit.params["weight"])
print("weight + horsepower:", fit2.params["weight"])""")
nb.md("The weight coefficient changed when horsepower joined the model. Now it means *holding "
      "horsepower fixed*, which is a different question from the one the first model answered.")

nb.section("8. Remove a variable")
nb.code("""fit3 = smf.ols("mpg ~ weight + horsepower + acceleration", data=cars).fit()
print(fit3.pvalues.round(4))""")
nb.md("Acceleration has a large p-value, so we cannot tell its coefficient from zero with the "
      "other two already in the model. Drop it and the model is `fit2` again.")

nb.section("9. A yes/no predictor")
nb.code("""cars["is_american"] = (cars.origin == "American").astype(int)
smf.ols("mpg ~ weight + is_american", data=cars).fit().params""")
nb.md("A 0/1 predictor shifts the line up or down. Its coefficient is the gap between American "
      "and other cars of the same weight.")

nb.section("10. A category with several levels")
nb.code("""smf.ols("mpg ~ weight + C(origin)", data=cars).fit().params""")
nb.md("`C(origin)` makes one level the baseline, here American, and each coefficient compares its "
      "level to that baseline.")

nb.section("11. Predict a new case")
nb.code("""new = pd.DataFrame({"weight": [3000], "horsepower": [110]})
fit2.predict(new)""")
nb.md("Weight runs from 1,613 to 5,140 pounds in this data, so 3,000 is a fair question. A "
      "6,000-pound truck would not be.")

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
