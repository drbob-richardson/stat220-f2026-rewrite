#!/usr/bin/env python3
"""Unit 7 --- Prediction and Its Uncertainty: code companion + homework."""
from nblib import CodeNB, HW

# =====================================================================
# CODE COMPANION
# =====================================================================
nb = CodeNB(7, "Prediction and Its Uncertainty",
            "Separate the four layers of prediction error, build an interval out of the model's "
            "own mistakes, check whether it covers what it claims, and watch regression to the "
            "mean manufacture an effect that is not there.")

nb.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(220)
plt.rcParams["figure.figsize"] = (7, 3.5)""")

nb.section("1. Two of the four layers, separated",
           "Estimation uncertainty shrinks with data. Irreducible noise does not. Here is the "
           "difference, measured.")
nb.code("""def experiment(n):
    x = rng.uniform(0, 10, n)
    y = 3 + 2*x + rng.normal(0, 4, n)              # noise SD is 4, always
    fit = np.polyfit(x, y, 1)
    x0 = 5.0
    return np.polyval(fit, x0)                     # our estimate of the LINE at x0

truth_at_5 = 3 + 2*5
for n in [20, 100, 1000, 10_000]:
    ests = np.array([experiment(n) for _ in range(400)])
    print(f"n = {n:>6}: SD of the fitted line at x=5 is {ests.std():.3f}   "
          f"(irreducible noise is still 4.000)")""")
nb.md("The first column collapses toward zero. The second never moves. More data tells you where "
      "the line is, and tells you nothing about where the next individual point will fall. That "
      "is why the two intervals below have such different widths.")

nb.section("2. Confidence band vs prediction band")
nb.code("""n = 200
x = rng.uniform(0, 10, n)
y = 3 + 2*x + rng.normal(0, 4, n)
X = sm.add_constant(x)
fit = sm.OLS(y, X).fit()

grid = np.linspace(0, 10, 100)
pred = fit.get_prediction(sm.add_constant(grid))
ci = pred.conf_int()                       # for the MEAN
pi = pred.conf_int(obs=True)               # for a NEW OBSERVATION

plt.plot(x, y, "o", color="#7f8c8d", ms=3, alpha=.5)
plt.plot(grid, pred.predicted_mean, color="#4878a8", lw=2)
plt.fill_between(grid, pi[:, 0], pi[:, 1], color="#c0392b", alpha=.15, label="prediction band")
plt.fill_between(grid, ci[:, 0], ci[:, 1], color="#4878a8", alpha=.45, label="confidence band")
plt.legend(); plt.title("Same model, two very different questions"); plt.show()

mid = len(grid)//2
print(f"width of the confidence band at x=5 : {ci[mid,1]-ci[mid,0]:.2f}")
print(f"width of the prediction band at x=5 : {pi[mid,1]-pi[mid,0]:.2f}")
print(f"ratio: {(pi[mid,1]-pi[mid,0])/(ci[mid,1]-ci[mid,0]):.1f}x wider")""")

nb.section("3. An interval made of the model's own mistakes",
           "Real data, no distributional theory: predict bike demand, then size the interval from "
           "held-out residuals.")
nb.code("""bikes = pd.read_csv("https://richardson.byu.edu/220/bikes.csv")
feats = ["Temperature", "Humidity", "Wind_speed", "Visibility", "Rainfall"]
Xb, yb = bikes[feats].values, bikes["Count"].values
Xtr, Xte, ytr, yte = train_test_split(Xb, yb, test_size=0.4, random_state=7)

model = RandomForestRegressor(n_estimators=300, random_state=0).fit(Xtr, ytr)
resid = yte - model.predict(Xte)                    # errors on data it never saw
lo, hi = np.percentile(resid, [5, 95])

new_day = np.array([[20, 50, 2, 1500, 0]])
point = model.predict(new_day)[0]
print(f"point prediction for the new day : {point:,.0f} rentals")
print(f"held-out residual percentiles    : {lo:,.0f} to {hi:,.0f}")
print(f"90% prediction interval          : {point+lo:,.0f} to {point+hi:,.0f}")
print(f"\\ntraining RMSE {np.sqrt(np.mean((ytr - model.predict(Xtr))**2)):,.0f} vs "
      f"held-out RMSE {np.sqrt(np.mean(resid**2)):,.0f}")""")
nb.md("Note the last line. If you had sized the interval from the *training* residuals it would "
      "have been far too narrow, because the model has partly memorized those days.")

nb.section("4. Is the interval honest? Count the coverage.")
nb.code("""half = len(Xte)//2
calib_resid = yte[:half] - model.predict(Xte[:half])
lo_c, hi_c = np.percentile(calib_resid, [5, 95])

check_pred = model.predict(Xte[half:])
inside = ((yte[half:] >= check_pred + lo_c) & (yte[half:] <= check_pred + hi_c)).mean()
print(f"nominal coverage : 90%")
print(f"actual coverage  : {inside:.1%}   (on days used for neither fitting nor calibration)")

# The same check, done wrongly, using training residuals to size the interval.
tr_resid = ytr - model.predict(Xtr)
lo_t, hi_t = np.percentile(tr_resid, [5, 95])
inside_bad = ((yte[half:] >= check_pred + lo_t) & (yte[half:] <= check_pred + hi_t)).mean()
print(f"\\nif sized from TRAINING residuals instead: {inside_bad:.1%} coverage "
      f"(interval width {hi_t-lo_t:,.0f} vs {hi_c-lo_c:,.0f})")""")

nb.section("5. Regression to the mean, and the intervention it fakes",
           "Nobody improves. Nothing is done. We will still measure a large 'effect'.")
nb.code("""n_people = 2000
skill = rng.normal(50, 8, n_people)          # true ability, FIXED all year
q1 = skill + rng.normal(0, 10, n_people)     # quarter 1 = skill + luck
q2 = skill + rng.normal(0, 10, n_people)     # quarter 2 = skill + fresh luck

bottom = q1 < np.percentile(q1, 10)          # "our worst performers"
top = q1 > np.percentile(q1, 90)             # "our stars"

print(f"bottom 10% in Q1: averaged {q1[bottom].mean():.1f}, then {q2[bottom].mean():.1f} "
      f"({q2[bottom].mean()-q1[bottom].mean():+.1f})   <-- 'the training worked!'")
print(f"top 10%    in Q1: averaged {q1[top].mean():.1f}, then {q2[top].mean():.1f} "
      f"({q2[top].mean()-q1[top].mean():+.1f})   <-- 'success went to their heads'")
print(f"\\ntrue skill of the bottom group: {skill[bottom].mean():.1f} "
      f"(vs {skill.mean():.1f} overall) --- they really are below average, just not that far")""")
nb.md("Both stories write themselves, and both are wrong. Selecting on an extreme measurement "
      "selects partly on luck, and luck does not repeat. Any evaluation that picks a group *because* "
      "they scored badly and then measures improvement will find one.")

nb.section("6. Extrapolation: two models that agree, until they do not")
nb.code("""xs = np.linspace(1, 6, 40)
ys = 2 + 1.2*xs + rng.normal(0, 0.4, 40)

lin = np.polyfit(xs, ys, 1)
quad = np.polyfit(xs, ys, 2)
future = np.linspace(1, 14, 200)

plt.plot(xs, ys, "o", color="#7f8c8d", ms=4, label="observed range")
plt.plot(future, np.polyval(lin, future), color="#4878a8", lw=2, label="linear fit")
plt.plot(future, np.polyval(quad, future), color="#c0392b", lw=2, label="quadratic fit")
plt.axvspan(1, 6, color="#dfe6ec", alpha=.6)
plt.legend(); plt.title("Both fit the data. They disagree by a factor of two at x=14."); plt.show()

for x0 in [6, 10, 14]:
    print(f"x = {x0:>2}: linear says {np.polyval(lin, x0):6.1f}, "
          f"quadratic says {np.polyval(quad, x0):6.1f}")""")

nb.write("Code_Unit07_Prediction.ipynb")


# =====================================================================
# HOMEWORK
# =====================================================================
hw = HW(7, "Prediction and Its Uncertainty",
        """Answer each problem in the cell(s) provided. Replace *Your answer* with your response
for written parts, and put code in the empty code cells.

The first problem is a **simulation lab** where you control the truth and can therefore separate
the layers of error. The next three are **real forecasting problems with a decision attached**.
The last asks how much your forecast should be trusted.

**Data** (all real):

- `https://richardson.byu.edu/220/bikes.csv`: 365 days of rentals with weather.
- `https://richardson.byu.edu/220/housing_data.csv`: house prices with size and neighborhood.
- `https://richardson.byu.edu/220/insurance_all.csv`: annual medical charges per person.""")

hw.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(220)
bikes = pd.read_csv("https://richardson.byu.edu/220/bikes.csv")
homes = pd.read_csv("https://richardson.byu.edu/220/housing_data.csv")
ins = pd.read_csv("https://richardson.byu.edu/220/insurance_all.csv")
print(bikes.shape, homes.shape, ins.shape)""")

# ---------------- P1: simulation lab ----------------
hw.problem(1, """*Simulation lab: separating the layers of error.* You choose the truth, so you can
watch each source of error behave differently.""")
hw.part("a", """Simulate from $y = 3 + 2x + \\varepsilon$ with $x \\sim U(0,10)$ and
$\\varepsilon \\sim N(0, 4)$. For $n = 20, 100, 1000, 10000$, repeat 400 times and record the
standard deviation of the fitted line's value at $x = 5$. Report the four numbers alongside the
irreducible noise SD.""")
hw.part("b", """Which layer shrank and which did not? Explain in 2 to 3 sentences what this implies
for a manager who wants a more accurate forecast for one specific customer.""", "written")
hw.part("c", """With $n = 200$, plot the fitted line with both a confidence band (for the mean) and
a prediction band (for a new observation). Report the width of each at $x = 5$ and their ratio.""")
hw.part("d", """**Model error, the quiet layer.** Now generate data from a genuinely curved truth,
$y = 3 + 2x + 0.35x^2 + \\varepsilon$, and fit a straight line. Plot the residuals against $x$.
Report the coverage of the model's nominal 95% prediction intervals, and explain why the software
gave no warning.""")
hw.part("e", """**Regression to the mean.** Simulate 2,000 employees whose true skill never
changes, observed with noise in two quarters. Select the bottom 10% by Q1 and report their Q1 and
Q2 averages, then do the same for the top 10%. Report both changes.""")
hw.part("f", """Using Part e, write the two false headlines a manager could produce from those
numbers, and the one sentence that corrects both.""", "written")

# ---------------- P2: real forecasting ----------------
hw.problem(2, """*Real data: forecasting bike demand with honest error bars.* Use `bikes`,
predicting `Count` from the weather variables. The operations team must decide how many bikes to
deploy tomorrow morning.""")
hw.part("a", """Split the data into training and held-out sets. Fit a model of your choice and
report both the training RMSE and the held-out RMSE. Explain the gap.""")
hw.part("b", """Build a 90% prediction interval from **held-out residuals**: take the 5th and 95th
percentiles of the held-out errors and attach them to a point prediction for a day with
temperature 20, humidity 50, wind 2, visibility 1500, rainfall 0. Report the point and the
interval.""")
hw.part("c", """Now check the interval honestly. Split your held-out set in two: use the first half
to size the interval and the second half to measure how often the true count falls inside. Report
the actual coverage against the nominal 90%.""")
hw.part("d", """Repeat Part c but size the interval from **training** residuals instead. Report the
coverage and the interval width, and explain the direction of the error.""")
hw.part("e", """The team asks for a forecast for a day at 40 degrees, hotter than anything in the
data. Produce the prediction, then explain what is dangerous about it and what you would tell the
team instead.""")

# ---------------- P3: prediction vs explanation ----------------
hw.problem(3, """*Real data: predicting one house versus locating an average.* Use `homes`.""")
hw.part("a", """Fit `house_price` on `square_footage` and `neighborhood`. For a 2,000-square-foot
house in a neighborhood of your choice, report both a 95% **confidence** interval for the mean
price of such houses and a 95% **prediction** interval for one such house.""")
hw.part("b", """Report the ratio of the two widths. Explain to a homeowner, in two sentences, why
the number that matters to *them* is the wider one.""", "written")
hw.part("c", """A bank wants to know the average value of a portfolio of 300 such houses. Which
interval applies, and roughly how does its width change with the 300? Compute it.""")
hw.part("d", """Compute the coverage of your prediction intervals on held-out houses. Are they
honest? If not, say in which direction and propose a fix.""")
hw.part("e", """Report the range of `square_footage` in the data, then predict the price of a
6,000-square-foot house. Explain what the model is really doing when you ask that, and what you
would say to whoever requested the number.""")

# ---------------- P4: the layers in a real disaster ----------------
hw.problem(4, """*Real data: which layer is about to hurt you?* Use `ins` to predict `charges`.""")
hw.part("a", """Fit a model predicting `charges` from `age`, `bmi`, `children`, `smoker`, and
`region`. Report held-out RMSE and plot held-out residuals against predicted values.""")
hw.part("b", """The residual plot should not look like an even band. Describe the pattern and say
which of the four layers of error it points to.""", "written")
hw.part("c", """Compute the coverage of nominal 90% prediction intervals separately for smokers and
non-smokers. Report both. What does the difference tell you about a single interval width applied
to everyone?""")
hw.part("d", """Simulate distribution shift: refit the model using only non-smokers, then evaluate
it on smokers. Report how much worse the RMSE gets, and connect it to a real scenario in which a
deployed model would experience exactly this.""")
hw.part("e", """Rank the four layers of error (noise, estimation, model structure, shift) by how
much each threatens a deployed version of this model, and justify the ranking in 3 to 4
sentences.""", "written")

# ---------------- P5: what can we say ----------------
hw.problem(5, """*What can and cannot be said.* Written answers.""")
hw.part("a", """Write the sentence you would put in a report to accompany your Problem 2 bike
forecast: the point, the interval, what the interval means, and the condition under which it stops
being valid.""", "written")
hw.part("b", """A colleague reports "our model predicts \\$4.2M next quarter, 95% CI \\$4.15M to
\\$4.25M." Given everything in this unit, list three questions you would ask before that number
goes in a board deck.""", "written")
hw.part("c", """Explain the difference between a model being *accurate* and a model being
*calibrated*, using one of your results from this assignment as the example.""", "written")
hw.part("d", """Your Problem 1e simulation produced a large apparent improvement with no
intervention. Describe a real evaluation you have seen (in business, sports, education, or
medicine) that is vulnerable to exactly this, and say what design would fix it.""", "written")
hw.part("e", """Suppose your bike model is deployed and performs noticeably worse next spring than
it did in testing. Write the diagnostic checklist you would work through, in order, and say what
evidence would distinguish the possible causes.""", "written")

hw.write("Stat_220_HW_Unit07_Prediction.ipynb")
