#!/usr/bin/env python3
"""Unit 12 --- Putting It Together: code companion + capstone homework."""
from nblib import CodeNB, HW

nb = CodeNB(12, "Putting It Together",
            "One dataset, one question, worked end to end the way the whole course says it should "
            "be done. Use this as the template for the capstone: notice how much of it happens "
            "before any model is fitted.")

nb.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(220)
plt.rcParams["figure.figsize"] = (7, 3.5)""")

nb.md("## The question\n\n"
      "*A bike-share operator asks: how many bikes should we deploy tomorrow, and what will it "
      "cost us to be wrong?* That is a prediction question with a decision attached, which means "
      "the deliverable is not a model. It is a number, an interval, and a recommendation.")

nb.section("Step 1. Interrogate the data before modeling it",
           "Where did it come from, what is one observation, and who is missing?")
nb.code("""bikes = pd.read_csv("https://richardson.byu.edu/220/bikes.csv")
print(bikes.shape)
print(bikes.dtypes.to_dict())
print(f"\\nmissing values per column: {bikes.isna().sum().sum()} total")
print(f"rows: {len(bikes)} consecutive days")
print(f"lag-1 autocorrelation of Count: {bikes['Count'].autocorr(1):.3f}   "
      f"<-- days are NOT independent")
print(f"\\nRainfall is nonzero on {(bikes.Rainfall > 0).mean():.1%} of days")
print(f"Seasons present: {sorted(bikes.Seasons.unique())}")""")
nb.md("Two things already matter. Days are autocorrelated, so a random train/test split leaks "
      "information across the boundary. The data also covers only one year, so anything we say about "
      "next year assumes the world does not move.")

nb.section("Step 2. Look at the outcome before choosing a method")
nb.code("""c = bikes["Count"]
print(f"mean {c.mean():.0f}, median {c.median():.0f}, SD {c.std():.0f}, "
      f"skew {stats.skew(c):.2f}, min {c.min()}, max {c.max()}")
fig, axes = plt.subplots(1, 2, figsize=(11, 3.2))
axes[0].hist(c, bins=40, color="#4878a8", edgecolor="white"); axes[0].set_title("daily rentals")
axes[1].plot(c.values, color="#4878a8", lw=1); axes[1].set_title("across the year (seasonality)")
plt.tight_layout(); plt.show()""")

nb.section("Step 3. Split honestly, given what one observation is",
           "Because days are correlated, we hold out a contiguous block rather than random days.")
nb.code("""split = int(len(bikes)*0.7)
train, test = bikes.iloc[:split], bikes.iloc[split:]
feats = ["Temperature", "Humidity", "Wind_speed", "Visibility", "Rainfall"]

model = RandomForestRegressor(n_estimators=400, random_state=0).fit(train[feats], train["Count"])
pred_test = model.predict(test[feats])
resid = test["Count"].values - pred_test

print(f"training RMSE : {np.sqrt(np.mean((train['Count'] - model.predict(train[feats]))**2)):.0f}")
print(f"held-out RMSE : {np.sqrt(np.mean(resid**2)):.0f}")
print(f"\\nfor comparison, always predicting the training mean: "
      f"{np.sqrt(np.mean((test['Count'] - train['Count'].mean())**2)):.0f}")""")
nb.md("Always print the trivial baseline. A model is only worth deploying if it beats *predict "
      "the average*, and it is surprising how often that check is skipped.")

nb.section("Step 4. An interval from the model's own mistakes")
nb.code("""lo, hi = np.percentile(resid, [5, 95])
tomorrow = pd.DataFrame([{"Temperature": 20, "Humidity": 50, "Wind_speed": 2,
                          "Visibility": 1500, "Rainfall": 0}])
point = model.predict(tomorrow[feats])[0]
print(f"point prediction     : {point:,.0f} rentals")
print(f"90% interval         : {point+lo:,.0f} to {point+hi:,.0f}")
print(f"interval width       : {hi-lo:,.0f} rentals")

half = len(resid)//2
lo_c, hi_c = np.percentile(resid[:half], [5, 95])
covered = ((test['Count'].values[half:] >= pred_test[half:] + lo_c) &
           (test['Count'].values[half:] <= pred_test[half:] + hi_c)).mean()
print(f"\\ncalibration check: nominal 90%, actual coverage {covered:.0%}")""")

nb.section("Step 5. Turn the distribution into a decision",
           "Each bike costs $3 for the day and each rental earns $9. The point forecast is not the "
           "answer to 'how many bikes'.")
nb.code("""# Tomorrow's demand is the point forecast plus an error drawn from the errors
# the model actually made on days it had never seen.
demand_scenarios = np.clip(point + resid[rng.integers(0, len(resid), 20_000)], 0, None)

fleets = np.arange(0, int(demand_scenarios.max()), 10)
profits = [(9*np.minimum(demand_scenarios, f) - 3*f).mean() for f in fleets]
best = fleets[int(np.argmax(profits))]

plt.plot(fleets, profits, color="#4878a8", lw=2)
plt.axvline(point, ls="--", color="#7f8c8d", label=f"point forecast ({point:,.0f})")
plt.axvline(best, color="#2e8b57", lw=2, label=f"profit-maximizing fleet ({best:,})")
plt.xlabel("bikes deployed"); plt.ylabel("expected profit ($)"); plt.legend(); plt.show()

print(f"deploying the point forecast : ${(9*np.minimum(demand_scenarios, point) - 3*point).mean():,.0f}/day")
print(f"deploying the optimum        : ${max(profits):,.0f}/day")""")

nb.md("## Step 6. The deliverable\n\n"
      "The recommendation below is what actually gets handed over. Notice what makes it "
      "defensible: a comparison against the trivial baseline, an interval built from real "
      "out-of-sample errors, a coverage check on that interval, a fleet size chosen from costs "
      "rather than from the point forecast, and an explicit statement of when it stops being "
      "valid.")

nb.code("""print(f\"\"\"RECOMMENDATION
  deploy               : {best:,} bikes
  expected demand      : {point:,.0f} rentals
  90% range            : {point+lo:,.0f} to {point+hi:,.0f}
  expected profit      : ${max(profits):,.0f}/day
  vs point-forecast fleet: ${max(profits) - (9*np.minimum(demand_scenarios, point) - 3*point).mean():,.0f}/day better

  caveats: one year, one city, so next season is assumed to resemble last;
           weather beyond the observed range is extrapolation.
\"\"\")""")

nb.write("Code_Unit12_End_to_End.ipynb")


hw = HW(12, "Capstone: Putting It Together",
        """This is the capstone. It is a full analysis plus the reasoning that goes with it, and
the reasoning is worth more than the code.

The first problem is **the five-beat drill** on scenarios that could come from any unit. The next
three are a **complete analysis, a decision, and a forecast**. The last is a critique, which is the
skill you will use most often and practice least.

You will be graded on whether you *interrogated* the data as much as on whether you modeled it.

**Data** (all real):

- `https://richardson.byu.edu/220/insurance_all.csv`: annual medical charges per person.
- `https://richardson.byu.edu/220/credit_risk.csv`: approved loans with a default indicator.
- `https://richardson.byu.edu/220/bikes.csv`: daily bike-rental counts with weather.""")

hw.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
from sklearn.model_selection import train_test_split, cross_val_score, KFold

rng = np.random.default_rng(220)
ins = pd.read_csv("https://richardson.byu.edu/220/insurance_all.csv")
credit = pd.read_csv("https://richardson.byu.edu/220/credit_risk.csv")
bikes = pd.read_csv("https://richardson.byu.edu/220/bikes.csv")
print(ins.shape, credit.shape, bikes.shape)""")

hw.problem(1, """*The five-beat drill.* For each scenario, write a complete answer using the five
beats: clarify the question, state your assumptions, name your approach, name the traps, and say
what would change your mind. Three to six sentences each. No code.""")
hw.part("a", """*"Signups are up 22% this week since we launched the new homepage. Roll it out
everywhere."*""", "written")
hw.part("b", """*"Our churn model is 96% accurate with an AUC of 0.99. Can we act on it
Monday?"*""", "written")
hw.part("c", """*"The campaign didn't work overall, but it was hugely effective for women aged
35 to 44 in the Midwest. Let's target them."*""", "written")
hw.part("d", """*"Customers who use our mobile app spend three times more. We should push everyone
to install it."*""", "written")
hw.part("e", """*"Our hiring model is 88% accurate at predicting top performers. Let's screen
applications with it."*""", "written")
hw.part("f", """*"Customer lifetime value is \\$1,840. I've put it in the pricing model."*""", "written")

hw.problem(2, """*A full analysis.* A regional insurer wants to know **how much more it costs to
cover a smoker**, in order to price a surcharge. Use `ins` and work the whole workflow, not just
the model.""")
hw.part("a", """**Provenance first.** Describe what population this dataset plausibly represents,
name two groups likely missing, and state what one observation is. Then examine `charges`: mean,
median, skew, and a plot. Say which summary the insurer's question calls for and why.""")
hw.part("b", """Compute the raw difference in mean charges between smokers and non-smokers with a
bootstrap 95% interval. State the number the way you would in a memo.""")
hw.part("c", """Fit a regression of `charges` on `smoker`, `age`, `bmi`, `children`, and `region`.
Report the smoker coefficient with its interval and explain what changed relative to Part b.""")
hw.part("d", """Check the model: plot residuals against fitted values, identify the problem, refit
with $\\log(\\text{charges})$, and explain how the smoker coefficient's interpretation changes on
the log scale.""")
hw.part("e", """The insurer wants to say smoking *causes* these costs. State what would have to be
true, name two confounders absent from the data, and say whether you would defend causal language
in a regulatory filing.""", "written")
hw.part("f", """Write the final recommendation in 4 to 6 sentences: the surcharge number, its
uncertainty, the assumption it rests on, and the one thing that would change your advice.""", "written")

hw.problem(3, """*A decision under uncertainty.* Use `credit`. A lender will use a model to decide
whom to approve. A default costs \\$4,000 on average. Rejecting an applicant who would have repaid costs
\\$900 in forgone profit.""")
hw.part("a", """Split the data, fit a logistic regression of `loan_status` on `person_income`,
`loan_amnt`, `loan_int_rate`, and `person_age`, and report held-out AUC and the trivial
baseline's accuracy.""")
hw.part("b", """Sweep the approval threshold, compute total cost at each, and report the
cost-minimizing threshold alongside the cost at 0.5. Report the savings per 1,000 applicants.""")
hw.part("c", """State the operating point in business language: what fraction are approved, what
fraction of those default, and what fraction of good applicants are turned away.""", "written")
hw.part("d", """Check calibration by binning predicted probabilities against observed default
rates. Explain why calibration specifically matters for the expected-cost calculation you just
did.""")
hw.part("e", """This dataset contains only approved loans and has a default rate far above any real
portfolio. Explain both problems and state, with direction, how each one distorts the threshold you
chose.""", "written")

hw.problem(4, """*A forecast with honest uncertainty.* Use `bikes`. An operations team must decide
how many bikes to deploy each morning. Each bike costs \\$3 for the day and each rental earns \\$9.""")
hw.part("a", """Report the lag-1 autocorrelation of `Count` and explain what it implies about
splitting the data. Then split the year into a training period and a later held-out period rather
than at random, and justify that choice.""")
hw.part("b", """Fit a model predicting `Count` from the weather variables. Report training RMSE,
held-out RMSE, and the RMSE of the trivial "predict the average" baseline.""")
hw.part("c", """Build a 90% prediction interval from held-out residuals for a day with temperature
20, humidity 50, wind 2, visibility 1500, rainfall 0. Then check the interval's actual coverage on
data used for neither fitting nor calibration.""")
hw.part("d", """Using the predictive distribution rather than the point forecast, choose the fleet
size that maximizes expected profit. Report it, and explain why it is not equal to the point
forecast.""")
hw.part("e", """Predict for a day at 40 degrees, hotter than anything observed. Report the number,
then explain what is dangerous about it and what you would tell the team instead.""")
hw.part("f", """Write the 4 to 6 sentence recommendation for the operations team, including the
fleet size, the expected profit, the interval, and the two conditions under which you would revisit
it.""", "written")

hw.problem(5, """*The critique.* Below is a summary a colleague wrote. Take it apart, then rebuild
it.""")
hw.md("""> *"We analyzed 1,500 loans and found that borrowers who rent default at 57%, versus 29%
> for homeowners, a 97% higher default rate (chi-square p < 0.001). We also tested 14 other
> variables and found that loan purpose matters (p = 0.03). Our random forest achieved 89%
> accuracy, and feature importance shows income is the most important driver of default.
> Recommendation: stop lending to renters and to applicants with low income."*""")
hw.part("a", """Identify at least **six** distinct statistical problems with that paragraph. For
each, name the error and say why it matters here specifically.""", "written")
hw.part("b", """Verify two of its numerical claims against the data: the default rates by home
ownership, and the accuracy of a random forest compared to predicting the majority class. Report
what you find.""")
hw.part("c", """Rewrite the paragraph as you would present it, keeping every claim the data
supports and qualifying or removing the rest. Aim for 5 to 8 sentences.""", "written")
hw.part("d", """Beyond the statistics, state one fairness or legal concern with the proposed policy,
and explain how a model trained on historical approvals could encode it even with no protected
attribute in the data.""", "written")
hw.part("e", """Write the single most important question you would have asked before any of this
analysis began, and explain in two sentences why it outranks everything else on your list.""", "written")

hw.write("Stat_220_HW_Unit12_Capstone.ipynb")
