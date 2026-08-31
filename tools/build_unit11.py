#!/usr/bin/env python3
"""Unit 11 --- Where the Data Comes From: code companion + homework."""
from nblib import CodeNB, HW

nb = CodeNB(11, "Where the Data Comes From",
            "Sample the same population four ways and watch which designs are merely noisy and "
            "which are wrong, measure why a huge biased sample loses to a small clean one, and "
            "find the missing values hiding as zeros in a real clinical dataset.")

nb.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(220)
plt.rcParams["figure.figsize"] = (7, 3.5)

rent = pd.read_csv("https://richardson.byu.edu/220/rent.csv")
TRUTH = rent["Rent"].mean()
print(f"treating this dataset as the population: true mean rent = {TRUTH:,.0f}")""")

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

nb.section("4. Nonresponse bends the answer, and weighting only partly fixes it")
nb.code("""groups = ["very satisfied", "satisfied", "neutral", "dissatisfied", "very dissatisfied"]
true_share = np.array([0.15, 0.30, 0.30, 0.17, 0.08])
score = np.array([5, 4, 3, 2, 1])
resp_rate = np.array([0.45, 0.20, 0.08, 0.15, 0.40])     # extremes reply

observed = true_share*resp_rate
observed = observed/observed.sum()
print(f"true mean satisfaction      : {(true_share*score).sum():.3f}")
print(f"observed (survey) mean      : {(observed*score).sum():.3f}")

weights = true_share/observed          # weight back to the known population mix
print(f"weighted back to population : {(observed*weights*score).sum():.3f}   <-- exact, because")
print("we knew the true composition AND the only distortion was on that variable.")

x = np.arange(len(groups))
plt.bar(x-0.2, true_share, 0.4, label="population", color="#4878a8")
plt.bar(x+0.2, observed, 0.4, label="respondents", color="#c0392b")
plt.xticks(x, groups, fontsize=8); plt.legend(); plt.show()""")

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

nb.write("Code_Unit11_Data_Provenance.ipynb")


hw = HW(11, "Where the Data Comes From",
        """Answer each problem in the cell(s) provided. Replace *Your answer* with your response
for written parts, and put code in the empty code cells.

The first problem is a **simulation lab** on sampling and missingness. The next three interrogate
**real datasets you have already modeled**, asking where they came from and who is missing. The
last is the provenance write-up you would attach to a report.

**Data** (all real):

- `https://richardson.byu.edu/220/rent.csv`: rental listings across six cities.
- `https://richardson.byu.edu/220/diabetes.csv`: clinical measurements with disguised
  missing values.
- `https://richardson.byu.edu/220/credit_risk.csv`: **approved** loans only.""")

hw.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm

rng = np.random.default_rng(220)
rent = pd.read_csv("https://richardson.byu.edu/220/rent.csv")
dia = pd.read_csv("https://richardson.byu.edu/220/diabetes.csv")
credit = pd.read_csv("https://richardson.byu.edu/220/credit_risk.csv")
print(rent.shape, dia.shape, credit.shape)""")

hw.problem(1, """*Simulation lab: designs, bias, and missingness.* Treat the full `rent` dataset as
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

hw.problem(2, """*Real data: what population is `rent` actually about?* Use `rent`.""")
hw.part("a", """Report the number of listings per city and per `AreaType`. Then describe, in
2 to 3 sentences, the population these listings plausibly represent and at least two groups of
renters who would not appear.""", "written")
hw.part("b", """Compute the mean rent overall, and then the mean weighting each city equally.
Report both, and explain which question each one answers.""")
hw.part("c", """Simulate the effect of a listing platform that under-represents cheap units:
resample the data with probability proportional to `Rent`, and report the resulting mean rent.
By how much would a platform like that overstate the market?""")
hw.part("d", """Compute the standard error of mean rent two ways, treating listings as independent
and treating cities as the unit. Report both and say which you would publish.""")
hw.part("e", """A city council wants "the average rent in the city" for a policy decision. List the
three questions you would ask before handing over any number.""", "written")

hw.problem(3, """*Real data: missing values in disguise.* Use `dia`.""")
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

hw.problem(4, """*Real data: the sample you cannot see.* Use `credit`, which contains only loans
that were **approved** under some earlier policy.""")
hw.part("a", """Report the overall default rate and explain why it is implausible as a real
portfolio rate. What was probably done to this dataset before you received it?""", "written")
hw.part("b", """Fit a default model on this data and report its AUC on a held-out split. Then
report the average predicted probability of default and compare it to a realistic portfolio rate
of 5%.""")
hw.part("c", """Down-sample the defaults to create a test set with a 5% default rate, and
re-evaluate accuracy, precision, and recall at a 0.5 threshold. Which metrics moved most?""")
hw.part("d", """Explain specifically how a model trained on approved-only loans would mislead a
credit team deciding whom to approve next, and name the region of applicant space about which the
data is silent.""", "written")
hw.part("e", """Propose a concrete data-collection change that would fix the selection problem,
including what it would cost the lender and why they might do it anyway.""", "written")

hw.problem(5, """*The provenance write-up.* Written answers.""")
hw.part("a", """Write the data-provenance paragraph you would put at the top of a report using
`credit`: what population it represents, what is missing, what is measured by proxy, and two
conclusions it cannot support.""", "written")
hw.part("b", """Do the same, in three sentences, for `diabetes`.""", "written")
hw.part("c", """A colleague says: "we have 12 million rows of app telemetry, so we don't need to
worry about sampling." Write the two-sentence rebuttal, and name the specific groups the telemetry
misses.""", "written")
hw.part("d", """Pick any model you built in an earlier unit. Name the measurement in it that is
furthest from the concept it stands for, and describe what would happen if that measure became a
target people optimized.""", "written")
hw.part("e", """Write the seven-question checklist you would run on any new dataset before
modeling it, in the order you would ask them, with one sentence on why each question comes where
it does.""", "written")

hw.write("Stat_220_HW_Unit11_Data_Provenance.ipynb")
