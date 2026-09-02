#!/usr/bin/env python3
"""Unit 5 --- Regression as Reasoning: code companion + homework."""
from nblib import CodeNB, HW

# =====================================================================
# CODE COMPANION
# =====================================================================
nb = CodeNB(5, "Regression as Reasoning",
            "What least squares actually minimizes, why a slope has a standard error, how a "
            "dummy variable turns a t-test into a regression, and how a lurking variable "
            "rewrites a coefficient in front of you.")

nb.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats

rng = np.random.default_rng(220)
plt.rcParams["figure.figsize"] = (7, 3.5)

cars = pd.read_csv("https://richardson.byu.edu/220/cars.csv").dropna()
print(cars.shape); cars.head()""")

nb.section("1. A first fit, read out loud")
nb.code("""X = sm.add_constant(cars[["weight"]])
fit = sm.OLS(cars["mpg"], X).fit()
b0, b1 = fit.params["const"], fit.params["weight"]
print(fit.summary().tables[1])
print(f"\\nSlope = {b1:.5f} mpg per pound.")
print(f"Per 1000 lbs: {1000*b1:.2f} mpg.  <-- always rescale to units a human can feel")
print(f"Weight range in the data: {cars.weight.min():.0f} to {cars.weight.max():.0f} lbs")""")
nb.md("The raw slope, $-0.0076$, looks like nothing. Per 1,000 pounds it is $-7.6$ mpg, which is "
      "enormous. Same number, same model: the units decide whether anyone understands you.")

nb.section("2. What least squares actually minimizes",
           "Try a grid of candidate slopes and watch the sum of squared residuals bottom out at "
           "exactly the fitted value.")
nb.code("""slopes = np.linspace(b1 - 0.004, b1 + 0.004, 200)
sse = [((cars.mpg - (b0 + s*cars.weight))**2).sum() for s in slopes]
plt.plot(slopes*1000, sse, color="#4878a8", lw=2)
plt.axvline(b1*1000, color="#c0392b", lw=2, label=f"least-squares slope = {b1*1000:.2f}/1000lb")
plt.xlabel("candidate slope (mpg per 1000 lbs)"); plt.ylabel("sum of squared residuals")
plt.legend(); plt.title("The fit is the bottom of this bowl"); plt.show()""")

nb.section("3. A slope is an estimate, so it wobbles",
           "Resample the data and refit. The spread of the slopes IS the standard error.")
nb.code("""boot_slopes = []
for _ in range(2000):
    samp = cars.sample(len(cars), replace=True)
    boot_slopes.append(np.polyfit(samp.weight, samp.mpg, 1)[0])
boot_slopes = np.array(boot_slopes)

print(f"bootstrap SE of the slope : {boot_slopes.std()*1000:.3f} (per 1000 lbs)")
print(f"statsmodels SE            : {fit.bse['weight']*1000:.3f} (per 1000 lbs)")
print(f"t = slope/SE              : {fit.tvalues['weight']:.1f}   <-- the Unit 1 template again")""")

nb.section("4. A dummy variable IS a two-group comparison",
           "Regression on a 0/1 predictor reproduces the two-sample t-test exactly.")
nb.code("""cars["is_american"] = (cars["origin"] == "American").astype(int)
d = sm.OLS(cars["mpg"], sm.add_constant(cars[["is_american"]])).fit()

amer = cars.loc[cars.is_american == 1, "mpg"]
other = cars.loc[cars.is_american == 0, "mpg"]

print(f"regression intercept (non-American mean) : {d.params['const']:.3f}")
print(f"actual non-American mean                 : {other.mean():.3f}")
print(f"regression dummy coefficient (difference): {d.params['is_american']:.3f}")
print(f"actual difference in means               : {amer.mean() - other.mean():.3f}")
print(f"\\nregression t = {d.tvalues['is_american']:.3f}")
print(f"pooled two-sample t = {stats.ttest_ind(amer, other, equal_var=True).statistic:.3f}")""")
nb.md("They are the same procedure. Everything you learned about two-group tests in Unit 1 "
      "transfers directly to regression coefficients. Only the packaging changed.")

nb.section("5. Omitted-variable bias, where you know the truth",
           "Simulate a world in which x has NO effect on y, but both are driven by z.")
nb.code("""n = 3000
z = rng.normal(0, 1, n)                    # the lurking variable
x = 0.8*z + rng.normal(0, 0.6, n)          # x is driven by z
y = 2.0*z + rng.normal(0, 1.0, n)          # y is driven by z, NOT by x

naive = sm.OLS(y, sm.add_constant(x)).fit()
adjusted = sm.OLS(y, sm.add_constant(np.column_stack([x, z]))).fit()

print(f"TRUE effect of x on y            : 0.000")
print(f"naive slope on x                 : {naive.params[1]:.3f}  (t = {naive.tvalues[1]:.1f})")
print(f"slope on x, controlling for z    : {adjusted.params[1]:.3f}  (t = {adjusted.tvalues[1]:.1f})")""")
nb.md("The naive regression reports a large, overwhelmingly significant effect of something that "
      "does nothing. No amount of data fixes it: with more rows the t-statistic just grows. Only "
      "including z fixes it, and in real work you have to *know* to look for z.")

nb.section("6. The same thing, in real data",
           "Do slower-accelerating cars really get better mileage?")
nb.code("""raw = sm.OLS(cars["mpg"], sm.add_constant(cars[["acceleration"]])).fit()
adj = sm.OLS(cars["mpg"], sm.add_constant(cars[["acceleration", "weight"]])).fit()

print(f"raw slope on acceleration            : {raw.params['acceleration']:+.3f} mpg per second")
print(f"controlling for weight               : {adj.params['acceleration']:+.3f} mpg per second")
print(f"the raw association shrank by        : "
      f"{100*(1 - adj.params['acceleration']/raw.params['acceleration']):.0f}%")
print(f"\\ncorr(acceleration, weight) = {cars.acceleration.corr(cars.weight):+.2f}")""")
nb.md("Heavy cars are both slow to accelerate and thirsty. Most of the raw relationship was weight "
      "under another name. We did **not** prove that acceleration has no effect. We showed "
      "that the raw number was mostly something else.")

nb.section("7. Significant does not mean useful")
nb.code("""m = sm.OLS(cars["mpg"], sm.add_constant(cars[["acceleration"]])).fit()
print(f"p-value on acceleration : {m.pvalues['acceleration']:.2e}")
print(f"R-squared               : {m.rsquared:.3f}")
print(f"residual SD             : {np.sqrt(m.scale):.2f} mpg")
print("\\nOverwhelmingly significant, and it explains under a fifth of the variation.")
print("Those two facts answer different questions and neither one is 'is the model good'.")""")

nb.write("Code_Unit05_Regression.ipynb")


# =====================================================================
# HOMEWORK
# =====================================================================
hw = HW(5, "Regression as Reasoning",
        """Answer each problem in the cell(s) provided. Replace *Your answer* with your response
for written parts, and put code in the empty code cells.

The first problem is a **simulation lab** where you set the true slope yourself, so you can see
exactly what a regression can and cannot recover. The next three are **real modeling problems with
a decision attached**. The last asks what your coefficients license you to claim.

**Data** (all real):

- `https://richardson.byu.edu/220/cars.csv`: fuel economy and engine specs for 392 cars.
- `https://richardson.byu.edu/220/housing_data.csv`: house prices with size, bedrooms, garage,
  and neighborhood.
- `https://richardson.byu.edu/220/rent.csv`: rental listings across six cities.""")

hw.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

rng = np.random.default_rng(220)
cars = pd.read_csv("https://richardson.byu.edu/220/cars.csv").dropna()
homes = pd.read_csv("https://richardson.byu.edu/220/housing_data.csv")
rent = pd.read_csv("https://richardson.byu.edu/220/rent.csv")
print(cars.shape, homes.shape, rent.shape)
homes.head()""")

# ---------------- P1: simulation lab ----------------
hw.problem(1, """*Simulation lab: what a slope can and cannot recover.* You set the truth, then
see what regression reports.""")
hw.part("a", """Simulate $n = 3000$ observations where $y = 1.5x + \\varepsilon$ with
$x \\sim N(0,1)$ and $\\varepsilon \\sim N(0,2)$. Fit the regression and confirm the slope estimate
is close to 1.5. Report the estimate, its standard error, and a 95% interval.""")
hw.part("b", """Repeat the whole simulation 1,000 times and plot the distribution of the estimated
slope. Report its mean and standard deviation, and compare the standard deviation to the standard
error your single fit reported in Part a.""")
hw.part("c", """**Omitted-variable bias.** Now build a world where $x$ has *no* effect at all:
let $z \\sim N(0,1)$, $x = 0.8z + \\text{noise}$, and $y = 2z + \\text{noise}$. Fit $y$ on $x$ alone
and report the slope and its $t$-statistic. Then fit $y$ on $x$ and $z$ together and report the
slope on $x$.""")
hw.part("d", """In Part c the naive regression should report a large, highly significant effect of
a variable that does nothing. Increase $n$ to 30,000 and refit the naive model. Does the bias get
smaller? Explain what that tells you about the relationship between sample size and this kind of
error.""")
hw.part("e", """**Overcontrol.** Build a world where $x$ genuinely causes $m$, and $m$ causes $y$,
with no other paths. Fit $y$ on $x$, and then $y$ on $x$ and $m$. Report both slopes on $x$ and
explain why controlling for $m$ makes the effect disappear even though $x$ really does matter.""")
hw.part("f", """From Parts c and e: adding a variable helped in one case and hurt in the other. In
3 to 4 sentences, state what you must know about the world (not the data) to tell those two
situations apart.""", "written")

# ---------------- P2: real simple regression ----------------
hw.problem(2, """*Real data: what does weight cost you in fuel economy?* Use `cars`. An engineering
team wants a number they can use in design tradeoffs.""")
hw.part("a", """Fit `mpg` on `weight`. Report the slope, its standard error, and a 95% confidence
interval, **expressed per 1,000 pounds** rather than per pound.""")
hw.part("b", """Write the one-sentence interpretation you would give the engineering team,
including the units and the range of weights the data actually covers.""", "written")
hw.part("c", """Plot the data with the fitted line, and plot residuals against fitted values.
Describe any pattern you see in the residuals and what it suggests about the straight-line
assumption.""")
hw.part("d", """Report $R^2$ and the residual standard deviation. Explain what each one tells the
team, and which is more useful for deciding whether the model is good enough to design with.""")
hw.part("e", """The team asks for the predicted mpg of a proposed 6,000-pound vehicle. Produce the
prediction, then explain in 2 to 3 sentences why you would refuse to hand over the number without a
warning.""")

# ---------------- P3: categorical + interaction ----------------
hw.problem(3, """*Real data: pricing houses with categories.* Use `homes`, which has
`house_price`, `square_footage`, `num_bedrooms`, `has_garage`, and `neighborhood`.""")
hw.part("a", """Fit `house_price` on `square_footage` alone. Report the slope with units and a
95% interval.""")
hw.part("b", """Add `has_garage` (a 0/1 variable). Report its coefficient and write the sentence
that interprets it. What exactly is being held fixed in that sentence?""")
hw.part("c", """Add `neighborhood`, a categorical variable. Report the coefficients and explain
what the omitted level (the baseline) is and how to read the others relative to it.""")
hw.part("d", """Fit a model with an **interaction** between `square_footage` and `neighborhood`
(for example with `smf.ols("house_price ~ square_footage * neighborhood", data=homes)`). Report
the interaction terms and state, in plain language, what it would mean for the price-per-square-
foot to differ by neighborhood.""")
hw.part("e", """Compare the models from Parts c and d. Does the interaction earn its complexity?
Justify your answer with something more than $R^2$ going up.""")
hw.part("f", """A realtor asks: "so how much is a garage worth?" Write the 3 to 4 sentence answer
you would give, including the number, its uncertainty, and the population it applies to.""", "written")

# ---------------- P4: confounding in real data ----------------
hw.problem(4, """*Real data: a coefficient that changes its mind.* Use `cars` again, and the
deliberately naive question: does slower acceleration improve fuel economy?""")
hw.part("a", """Fit `mpg` on `acceleration` alone. Report the slope, its $t$-statistic, and $R^2$.
Interpret the slope in its units.""")
hw.part("b", """Now fit `mpg` on `acceleration` and `weight`. Report the new acceleration
coefficient and compute what fraction of the raw association survived.""")
hw.part("c", """Report the correlation between `acceleration` and `weight`, and explain the
mechanism: why does weight produce a spurious relationship between acceleration and mpg?""", "written")
hw.part("d", """Split the cars into four weight bands with `pd.qcut` and fit the acceleration slope
separately within each band. Report the four slopes and relate them to your Parts a and b.""")
hw.part("e", """An executive proposes detuning engines so cars accelerate more slowly, in order to
hit a fuel-economy target. Write the 3 to 4 sentence response you would give, using your results,
and say what evidence would actually settle the question.""", "written")

# ---------------- P5: what can we say ----------------
hw.problem(5, """*What can and cannot be said.* Written answers.""")
hw.part("a", """For your Problem 2 weight coefficient, write (i) a statement that is fully
supported by the analysis, and (ii) a statement that sounds similar but is not supported. Explain
what separates them.""", "written")
hw.part("b", """Your Problem 3 model includes `neighborhood`. Does its coefficient tell you what
would happen to a house's price if you moved the house to a different neighborhood? Explain.""", "written")
hw.part("c", """In Problem 4, the acceleration coefficient shrank by about 80% after adjusting for
weight. Does that mean acceleration has no effect on fuel economy? State precisely what the
analysis does and does not establish.""", "written")
hw.part("d", """All three datasets are observational. For each one, name a variable that is not in
the data but probably matters, and say which coefficient it would most distort.""", "written")
hw.part("e", """A colleague summarizes your work as "we found that weight causes lower mpg, garages
add value, and acceleration doesn't matter." Rewrite that sentence so that every claim in it is one
your analyses actually support.""", "written")

hw.write("Stat_220_HW_Unit05_Regression.ipynb")
