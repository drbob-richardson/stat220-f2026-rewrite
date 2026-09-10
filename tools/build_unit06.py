#!/usr/bin/env python3
"""Unit 6: Causal Claims and Where the Data Came From. Code companion and homework.

Merged from the old Causal Thinking and Where the Data Comes From units. A
collider and survivorship bias are the same mechanism, so they sit next to
each other here on purpose.
"""
from nblib import CodeNB, HW

# =====================================================================
# CODE COMPANION
# =====================================================================
nb = CodeNB(6, "Causal Claims and Where the Data Came From",
            "Build a confounder, a collider, and a mediator in worlds where you set the truth, "
            "then watch the same patterns show up in real data and in how the rows were "
            "collected in the first place.")

nb.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

rng = np.random.default_rng(220)
plt.rcParams["figure.figsize"] = (7, 3.5)

rent = pd.read_csv("https://richardson.byu.edu/220/rent.csv")
TRUTH = rent["Rent"].mean()
print(f"treating the rent listings as a population: true mean rent = {TRUTH:,.0f}")""")

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

nb.section("3. Survivorship: studying only what came back")
nb.code("""n = 20_000
quality = rng.normal(0, 1, n)             # a startup's underlying quality
luck = rng.normal(0, 1, n)
survives = (quality + luck) > 1.2         # you only get to interview survivors

print(f"correlation(quality, luck) in ALL startups     : "
      f"{np.corrcoef(quality, luck)[0,1]:+.3f}")
print(f"correlation among SURVIVORS                    : "
      f"{np.corrcoef(quality[survives], luck[survives])[0,1]:+.3f}")
print(f"\\nmean quality, all startups : {quality.mean():+.3f}")
print(f"mean quality, survivors      : {quality[survives].mean():+.3f}")
print("\\nStudy only survivors and you will conclude that quality and luck are substitutes,")
print("and you will badly overestimate how much quality the average founder had.")""")

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

nb.section("1. Four sampling designs, scored against the truth",
           "Only one kind of error shrinks with effort. The other is baked in.")
nb.code("""def simple(n):
    return rent.sample(n).Rent.mean()

def convenience(n):
    # a scraper that only indexed smaller units
    small = rent[rent.Size <= rent.Size.median()]
    return small.sample(n).Rent.mean()

def cluster(n_cities=2, per=50):
    cities = rng.choice(rent.City.unique(), n_cities, replace=False)
    sub = rent[rent.City.isin(cities)]
    return sub.sample(min(n_cities*per, len(sub))).Rent.mean()

def stratified(n=100):
    parts = []
    for city, g in rent.groupby("City"):
        k = max(1, int(round(n * len(g)/len(rent))))
        parts.append(g.sample(min(k, len(g))).Rent)
    return pd.concat(parts).mean()

print(f"{'design':>14} {'mean estimate':>15} {'bias':>10} {'SD':>10} {'RMSE':>10}")
for name, fn in [("simple random", lambda: simple(100)),
                 ("convenience", lambda: convenience(100)),
                 ("cluster", cluster),
                 ("stratified", stratified)]:
    est = np.array([fn() for _ in range(600)])
    bias, sd = est.mean() - TRUTH, est.std()
    print(f"{name:>14} {est.mean():>15,.0f} {bias:>10,.0f} {sd:>10,.0f} "
          f"{np.sqrt(bias**2 + sd**2):>10,.0f}")""")
nb.md("Simple and stratified are both unbiased, and stratified is tighter for the same cost. Cluster is "
      "unbiased but far noisier, because two cities is closer to n=2 than n=100. Convenience is "
      "in a different category: it is *wrong*, and no sample size fixes it.")

nb.section("2. Bias does not shrink. Ever.")
nb.code("""truth, bias = 0.50, 0.04
ns = np.logspace(1, 6, 60)
rmse_biased = np.sqrt(bias**2 + truth*(1-truth)/ns)
rmse_clean = np.sqrt(truth*(1-truth)/ns)

plt.loglog(ns, rmse_biased*100, color="#c0392b", lw=2.5, label="biased sample (4-point tilt)")
plt.loglog(ns, rmse_clean*100, color="#4878a8", lw=2.5, label="true random sample")
plt.xlabel("sample size"); plt.ylabel("typical error (percentage points)"); plt.legend(); plt.show()

n_equiv = truth*(1-truth)/bias**2
print(f"a RANDOM sample of {n_equiv:.0f} matches a biased sample of ANY size")
big_n = 1_000_000
se = np.sqrt(truth*(1-truth)/big_n)
print(f"\\nwith n = {big_n:,} from the biased process:")
print(f"  reported 95% CI half-width : {1.96*se*100:.3f} points")
print(f"  actual distance from truth : {bias*100:.1f} points")
print("  the interval is 25x too narrow to contain the truth. This is the dangerous case.")""")

nb.section("5. Missing values hiding as zeros, in real clinical data")
nb.code("""dia = pd.read_csv("https://richardson.byu.edu/220/diabetes.csv")
for col in ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]:
    z = (dia[col] == 0).sum()
    print(f"{col:>15}: {z:>4} zeros ({z/len(dia):5.1%}) "
          f"{'  <-- physiologically impossible' if z > 0 else ''}")""")
nb.code("""ins_all = dia["Insulin"]
real = ins_all[ins_all > 0]
imputed = pd.concat([real, pd.Series([real.mean()]*int((ins_all == 0).sum()))])

print(f"{'approach':>28} {'mean':>9} {'SD':>9}")
print(f"{'keep the zeros (wrong)':>28} {ins_all.mean():>9.1f} {ins_all.std():>9.1f}")
print(f"{'drop them':>28} {real.mean():>9.1f} {real.std():>9.1f}")
print(f"{'impute the mean':>28} {imputed.mean():>9.1f} {imputed.std():>9.1f}")
print("\\nMean imputation keeps the mean and shrinks the SD: it invents precision.")

# Is the missingness related to the outcome?
rate_missing = dia.loc[dia.Insulin == 0, "Outcome"].mean()
rate_present = dia.loc[dia.Insulin > 0, "Outcome"].mean()
print(f"\\ndiabetes rate where insulin is MISSING : {rate_missing:.3f}")
print(f"diabetes rate where insulin is present  : {rate_present:.3f}")
print("If those differ, the missingness carries information and dropping rows changes the population.")""")

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


nb.write("Code_Unit06_Causal_and_Provenance.ipynb")

# =====================================================================
# HOMEWORK
# =====================================================================
hw = HW(6, "Causal Claims and Where the Data Came From",
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

hw.problem(2, """*Real data: the effect of smoking on medical costs.* Use `ins`. An insurer wants
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

hw.problem(3, """*Simulation lab: designs, bias, and missingness.* Treat the full `rent` dataset as
the population, so you always know the right answer.""")
hw.part("a", """Compute the population mean `Rent`. Then simulate 600 replications each of four
designs at roughly 100 listings: simple random, convenience (only units at or below median
`Size`), cluster (2 random cities, 50 each), and stratified by city in proportion to city size.
Report bias, SD, and RMSE for each.""")
hw.part("b", """Which designs are unbiased? Which is merely noisy, and which is actually wrong?
Explain the difference in 2 to 3 sentences, and say which error a bigger budget can fix.""", "written")
hw.part("c", """Show that bias does not shrink: for a true proportion of 0.50 with a 4-point
systematic tilt, plot RMSE against $n$ on log-log axes for the biased and unbiased processes.
Report the random sample size that matches the biased sample of any size.""")
hw.part("d", """At $n = 1{,}000{,}000$ from the biased process, compute the reported 95% confidence
interval and state whether it contains the truth. Explain why this is the most dangerous case
rather than the safest.""")
hw.part("e", """**Missingness mechanisms.** Simulate 5,000 people with a true mean income. Create
three versions. First, values missing completely at random. Second, missing at random given age,
where older people skip the question and you recorded age. Third, missing not at random, where
high earners skip it. For
each, report the mean after dropping missing rows and compare to the truth.""")
hw.part("f", """For the missing-at-random case in Part e, show that including `age` in a model
recovers the right answer while a simple mean does not. Explain why the third case cannot be
fixed from the data alone.""")

hw.problem(4, """*Real data: missing values in disguise.* Use `dia`.""")
hw.part("a", """For `Glucose`, `BloodPressure`, `SkinThickness`, `Insulin`, and `BMI`, report the
count and percentage of zeros. Which are physiologically impossible?""")
hw.part("b", """Compute the mean and SD of `Insulin` three ways: keeping zeros, dropping them, and
mean-imputing them. Report all six numbers and explain why imputation preserves the mean but
shrinks the SD.""")
hw.part("c", """Test whether the missingness is informative: compare the diabetes rate among rows
with `Insulin == 0` and `Insulin > 0`, with a test of the difference. What missingness mechanism
does this suggest?""")
hw.part("d", """Fit two logistic regressions of `Outcome` on `Glucose`, `BMI`, and `Insulin`: one
dropping the zero-insulin rows, and one keeping all rows with an added `insulin_missing`
indicator. Compare the coefficients, the sample sizes, and the indicator's own coefficient.""")
hw.part("e", """Which model would you report, and what would you say in the methods section about
the zeros? Answer in 3 to 4 sentences.""", "written")

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


hw.write("Stat_220_HW_Unit06_Causal_and_Provenance.ipynb")
