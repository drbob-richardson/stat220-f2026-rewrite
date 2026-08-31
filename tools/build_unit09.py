#!/usr/bin/env python3
"""Unit 9 --- Causal Thinking: code companion + homework."""
from nblib import CodeNB, HW

nb = CodeNB(9, "Causal Thinking",
            "Build each of the three third-variable roles in a world where you set the truth, "
            "then watch the same patterns appear in real data. If you can produce a bias on "
            "purpose, you can recognize it in the wild.")

nb.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

rng = np.random.default_rng(220)
plt.rcParams["figure.figsize"] = (7, 3.5)""")

nb.section("1. A collider: making a correlation out of nothing",
           "Two independent variables. Select on their sum, and they become related.")
nb.code("""d1 = rng.integers(1, 7, 4000)
d2 = rng.integers(1, 7, 4000)
keep = (d1 + d2) >= 9

print(f"correlation among ALL rolls           : {np.corrcoef(d1, d2)[0,1]:+.3f}")
print(f"correlation among rolls summing to 9+ : {np.corrcoef(d1[keep], d2[keep])[0,1]:+.3f}")
print(f"\\n{keep.sum()} of {len(d1)} rolls survived the filter")""")
nb.code("""# The same structure with continuous variables: hiring on test + interview.
test = rng.normal(size=6000)
interview = rng.normal(size=6000)
hired = (test + interview) > 1.6

fig, axes = plt.subplots(1, 2, figsize=(11, 3.4))
axes[0].plot(test, interview, ".", ms=2, color="#7f8c8d", alpha=.4)
axes[0].set_title(f"all applicants: r = {np.corrcoef(test, interview)[0,1]:+.2f}")
axes[1].plot(test[hired], interview[hired], ".", ms=3, color="#c0392b")
axes[1].set_title(f"hired only: r = {np.corrcoef(test[hired], interview[hired])[0,1]:+.2f}")
for ax in axes: ax.set_xlabel("test score"); ax.set_ylabel("interview score")
plt.tight_layout(); plt.show()""")
nb.md("An HR analyst studying current employees would conclude that test performance and interview "
      "performance trade off against each other. They do not. The hiring rule created the pattern, "
      "and it exists only inside the hired group.")

nb.section("2. A confounder: an effect that is not there")
nb.code("""n = 4000
z = rng.normal(0, 1, n)                       # lurking variable
x = 0.8*z + rng.normal(0, 0.6, n)             # treatment, driven by z
y = 2.0*z + rng.normal(0, 1.0, n)             # outcome, driven by z, NOT by x

naive = sm.OLS(y, sm.add_constant(x)).fit()
adj = sm.OLS(y, sm.add_constant(np.column_stack([x, z]))).fit()
print(f"TRUE effect of x on y      : 0.000")
print(f"naive estimate             : {naive.params[1]:+.3f}  (t = {naive.tvalues[1]:6.1f})")
print(f"controlling for z          : {adj.params[1]:+.3f}  (t = {adj.tvalues[1]:6.1f})")""")

nb.section("3. A mediator: controlling away a real effect")
nb.code("""n = 4000
train = rng.integers(0, 2, n)                 # randomized training
skill = 1.5*train + rng.normal(0, 1, n)       # training raises skill
sales = 2.0*skill + rng.normal(0, 1, n)       # skill raises sales; no other path

total = sm.OLS(sales, sm.add_constant(train)).fit()
direct = sm.OLS(sales, sm.add_constant(np.column_stack([train, skill]))).fit()
print(f"TRUE total effect of training : {1.5*2.0:.2f}")
print(f"estimated total effect        : {total.params[1]:.3f}   <-- correct")
print(f"'controlling for skill'       : {direct.params[1]:.3f}   <-- the effect vanishes")""")
nb.md("Training was randomized, so the total effect is unbiased. Controlling for skill blocks the "
      "only channel through which training works and reports approximately zero. Adding a variable "
      "is not a safe default: it is a claim about the causal structure.")

nb.section("4. The same story in real data")
nb.code("""cars = pd.read_csv("https://richardson.byu.edu/220/cars.csv").dropna()
raw = sm.OLS(cars.mpg, sm.add_constant(cars[["acceleration"]])).fit()
adj = sm.OLS(cars.mpg, sm.add_constant(cars[["acceleration", "weight"]])).fit()
print(f"raw slope on acceleration       : {raw.params['acceleration']:+.3f} mpg per second")
print(f"adjusting for weight            : {adj.params['acceleration']:+.3f} mpg per second")
print(f"share of the raw association that survived: "
      f"{adj.params['acceleration']/raw.params['acceleration']:.0%}")""")

nb.section("5. Difference in differences, and what breaks it")
nb.code("""def did(treat_effect, common_trend, pre_gap=12.0, n=400, treated_drift=0.0):
    \"\"\"treated_drift lets us violate parallel trends on purpose.\"\"\"
    ctrl_pre  = rng.normal(30, 5, n)
    ctrl_post = ctrl_pre + common_trend + rng.normal(0, 3, n)
    trt_pre   = rng.normal(30 + pre_gap, 5, n)
    trt_post  = trt_pre + common_trend + treated_drift + treat_effect + rng.normal(0, 3, n)
    return ((trt_post.mean() - trt_pre.mean()) - (ctrl_post.mean() - ctrl_pre.mean()))

print(f"true effect 7, parallel trends hold      : DiD = {did(7, 6):.2f}")
print(f"true effect 0, parallel trends hold      : DiD = {did(0, 6):.2f}")
print(f"true effect 0, treated region drifting +5: DiD = {did(0, 6, treated_drift=5):.2f}  <-- fake effect")
print("\\nA before/after comparison in the treated region alone would have reported:")
print(f"  {did(7, 6) + 6:.2f} instead of 7, crediting the common trend to the treatment.")""")

nb.section("6. What randomization actually buys",
           "Compare a randomized rollout to letting customers opt in, when the truth is identical.")
nb.code("""n = 6000
engagement = rng.normal(0, 1, n)              # unmeasured customer motivation
TRUE_EFFECT = 2.0

# (a) customers CHOOSE the feature: engaged customers opt in
chose = (engagement + rng.normal(0, 0.5, n)) > 0.4
y_choice = 10 + TRUE_EFFECT*chose + 4*engagement + rng.normal(0, 2, n)
obs = y_choice[chose].mean() - y_choice[~chose].mean()

# (b) we RANDOMIZE who gets it
assigned = rng.integers(0, 2, n).astype(bool)
y_rand = 10 + TRUE_EFFECT*assigned + 4*engagement + rng.normal(0, 2, n)
exp = y_rand[assigned].mean() - y_rand[~assigned].mean()

print(f"TRUE effect                        : {TRUE_EFFECT:.2f}")
print(f"observational (customers opt in)   : {obs:.2f}   <-- {obs/TRUE_EFFECT:.1f}x too big")
print(f"randomized assignment              : {exp:.2f}")
print("\\nSame customers, same true effect. Only the assignment mechanism changed.")""")

nb.write("Code_Unit09_Causal.ipynb")


hw = HW(9, "Causal Thinking",
        """Answer each problem in the cell(s) provided. Replace *Your answer* with your response
for written parts, and put code in the empty code cells.

The first problem is a **simulation lab** where you build each bias deliberately. The next three
are **real questions where somebody wants to act on the answer**. The last asks what would have to
be true for your estimate to be causal.

**Data** (all real):

- `https://richardson.byu.edu/220/cars.csv`: fuel economy and engine specs.
- `https://richardson.byu.edu/220/insurance_all.csv`: charges with smoking status, age, BMI.
- `https://richardson.byu.edu/220/credit_risk.csv`: loans with interest rate and default.""")

hw.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

rng = np.random.default_rng(220)
cars = pd.read_csv("https://richardson.byu.edu/220/cars.csv").dropna()
ins = pd.read_csv("https://richardson.byu.edu/220/insurance_all.csv")
credit = pd.read_csv("https://richardson.byu.edu/220/credit_risk.csv")
print(cars.shape, ins.shape, credit.shape)""")

hw.problem(1, """*Simulation lab: build all three biases on purpose.* In each part you know the
true effect, so you can measure exactly how wrong each analysis is.""")
hw.part("a", """**Confounder.** Simulate $z \\sim N(0,1)$, $x = 0.8z + \\text{noise}$, and
$y = 2z + \\text{noise}$, so $x$ has *no* effect on $y$. Report the naive slope on $x$ with its
$t$-statistic, and the slope after controlling for $z$.""")
hw.part("b", """**Collider.** Simulate independent `test` and `interview` scores, then keep only
applicants with `test + interview > 1.6`. Report the correlation in the full pool and among those
"hired," and plot both.""")
hw.part("c", """**Mediator.** Simulate randomized `training` that raises `skill`, where `skill`
raises `sales` and there is no other path. Report the total effect of training, and the estimate
you get when you control for `skill`. State which of the two answers the question *should we run
the training*.""")
hw.part("d", """Make a table summarizing Parts a--c: for each of the three structures, the true
effect, the estimate without the third variable, and the estimate with it. Which structures does
controlling help, and which does it hurt?""")
hw.part("e", """**Randomization versus choice.** Simulate 6,000 customers with unmeasured
engagement, where a feature has a true effect of 2.0. Compare the estimated effect when customers
opt in (engaged ones choose it) against when you randomize assignment. Report both.""")
hw.part("f", """In Part e the observational estimate is badly inflated even though nothing about
the feature changed. Explain the mechanism, and say why collecting ten times more observational
data would not help.""", "written")

hw.problem(2, """*Real data: a coefficient that changes its mind.* Use `cars` and the naive
question: does slower acceleration cause better fuel economy?""")
hw.part("a", """Fit `mpg` on `acceleration` alone and report the slope with its interval and
$R^2$.""")
hw.part("b", """Add `weight`. Report the new acceleration coefficient and the fraction of the raw
association that survived. Report the correlation between `acceleration` and `weight`.""")
hw.part("c", """Draw the causal diagram you believe connects weight, acceleration, and mpg (in a
comment or markdown), and classify `weight` as confounder, collider, or mediator. Justify your
choice from mechanism, not from the data.""", "written")
hw.part("d", """Estimate the slope separately within four weight bands (`pd.qcut`). Report the four
slopes and explain how they relate to your Part a and Part b answers.""")
hw.part("e", """An executive proposes detuning engines to hit a fuel-economy target. Write the
3 to 4 sentence response, saying what your analysis supports and what experiment would settle it.""", "written")

hw.problem(3, """*Real data: the effect of smoking on medical costs.* Use `ins`. An insurer wants
to justify a smoker surcharge and would like to say smoking *causes* the extra cost.""")
hw.part("a", """Report the raw difference in mean `charges` between smokers and non-smokers, with a
bootstrap interval.""")
hw.part("b", """Fit a regression of `charges` on `smoker`, `age`, `bmi`, `children`, and `region`.
Report the smoker coefficient and compare it to the raw difference.""")
hw.part("c", """Add a `smoker` by `bmi` interaction. Report the coefficients and describe in words
how the estimated smoking penalty depends on BMI.""")
hw.part("d", """Name two confounders that are **not** in this dataset. For each, say whether
omitting it likely makes the smoker coefficient too large or too small, and why.""", "written")
hw.part("e", """A randomized experiment on smoking is impossible. Describe the kinds of evidence
epidemiologists used instead, and explain what made that evidence persuasive despite the absence
of randomization.""", "written")

hw.problem(4, """*Designing the study you would actually run.* Use `credit` as background:
loans carry an interest rate and either default or not.""")
hw.part("a", """Report the average `loan_int_rate` for defaulted and non-defaulted loans, and the
difference.""")
hw.part("b", """A junior analyst concludes "high rates cause default, so we should lower rates."
Explain the reverse-causation problem specifically: how is the rate set in the first place?""", "written")
hw.part("c", """Design a study that could estimate the causal effect of the interest rate on
default. Specify the assignment mechanism, the comparison group, the outcome, the time window, and
the main threat to validity.""", "written")
hw.part("d", """Your company instead changed rate policy in one region in July and left another
region unchanged. Simulate this difference-in-differences setup with a true effect of $-3$
percentage points and a common time trend of $+2$, and verify that DiD recovers $-3$ while a
before-and-after comparison in the treated region does not.""")
hw.part("e", """Now break the design: rerun your simulation with the treated region drifting by an
extra $+5$ points for reasons unrelated to the policy. Report what DiD estimates, and describe the
check you would run on real data to detect this before trusting the result.""")

hw.problem(5, """*What can and cannot be said.* Written answers.""")
hw.part("a", """For each analysis in this assignment, state whether the estimate is causal,
associational, or somewhere between, and name the specific assumption that would have to hold to
promote it.""", "written")
hw.part("b", """A colleague's rule is "control for everything available, to be safe." Using your
Problem 1 results, explain concretely why this is wrong, with one example where it helps and one
where it hurts.""", "written")
hw.part("c", """Explain why "we have millions of rows" does not address confounding, and contrast
it with what a randomized experiment on 500 people would buy you.""", "written")
hw.part("d", """Your company is about to launch a feature to everyone next quarter. Describe how to
get a causal estimate at essentially zero cost, and what you would need to negotiate with the
engineering team to make it happen.""", "written")
hw.part("e", """Pick one claim you have personally believed from a news article or company blog
post. State the causal claim, name the most plausible confounder or selection effect, and describe
the study that would actually settle it.""", "written")

hw.write("Stat_220_HW_Unit09_Causal.ipynb")
