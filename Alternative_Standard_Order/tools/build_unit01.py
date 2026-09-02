#!/usr/bin/env python3
"""Unit 1 --- Statistical Inference: code companion + homework."""
from nblib import CodeNB, HW

# =====================================================================
# CODE COMPANION
# =====================================================================
nb = CodeNB(1, "Statistical Inference",
            "Five short simulations behind the slides: what 'just guessing' looks like, where the "
            "standard error comes from, what p-values do under the null, what power buys you, and "
            "the two ways a t-test quietly lies to you.")

nb.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(220)
plt.rcParams["figure.figsize"] = (7, 3.5)""")

nb.section("1. The Coke test: what 'just guessing' looks like",
           "A guesser calling 10 cups is 10 coin flips. Before you can call a score impressive, "
           "you need the distribution of scores a guesser produces.")
nb.code("""k = np.arange(0, 11)
pmf = stats.binom.pmf(k, 10, 0.5)

for cutoff in [7, 8, 9, 10]:
    print(f"P(guesser gets >= {cutoff:2d} right) = {stats.binom.sf(cutoff-1, 10, 0.5):.4f}")

plt.bar(k, pmf, color=["#c0392b" if v >= 8 else "#4878a8" for v in k])
plt.xlabel("cups called correctly out of 10"); plt.ylabel("probability")
plt.title("What a pure guesser produces"); plt.show()""")

nb.md("**Try it:** change 10 cups to 20. How many must they get right for the result to be "
      "surprising at the same 5% level? Is it more or less than double?")

nb.section("2. Two tasters: how far apart can luck put them?",
           "The gap between two guessers is the two-sample question in miniature.")
nb.code("""sims = rng.binomial(10, 0.5, size=(200_000, 2))
gap = np.abs(sims[:, 0] - sims[:, 1])
for g in [3, 4, 5, 6]:
    print(f"P(gap >= {g}) = {(gap >= g).mean():.3f}")""")

nb.section("3. Where the standard error comes from",
           "Draw the same study over and over and watch the estimate move. The spread of those "
           "estimates *is* the standard error. The formula sigma/sqrt(n) only predicts it.")
nb.code("""sigma = 12.0
for n in [10, 40, 160, 640]:
    means = rng.normal(50, sigma, size=(20_000, n)).mean(axis=1)
    print(f"n = {n:4d}   SD of the sample means = {means.std():5.2f}   "
          f"sigma/sqrt(n) = {sigma/np.sqrt(n):5.2f}")""")
nb.md("Four times the data cuts the noise in half, not to a quarter. That square root is the "
      "entire economics of sample size, and it is why 'just collect more data' gets expensive fast.")

nb.section("4. What p-values do when nothing is going on",
           "This is the single most clarifying simulation in the course. Run studies where the "
           "truth is *no difference at all*, and look at the p-values you get.")
nb.code("""def run_studies(n_studies=5000, n=30, true_diff=0.0, sd=1.0):
    a = rng.normal(0, sd, size=(n_studies, n))
    b = rng.normal(true_diff, sd, size=(n_studies, n))
    return stats.ttest_ind(a, b, axis=1, equal_var=False).pvalue

p_null = run_studies(true_diff=0.0)
print(f"fraction of NULL studies with p < 0.05: {(p_null < 0.05).mean():.3f}  (should be ~0.05)")

plt.hist(p_null, bins=20, color="#4878a8", edgecolor="white")
plt.xlabel("p-value"); plt.ylabel("studies")
plt.title("Under the null, p-values are uniform: every value equally likely"); plt.show()""")
nb.md("Read that histogram carefully. When nothing is happening, a p-value below 0.05 is not "
      "rare or strange, it happens in exactly 5% of studies **by construction**. That is what "
      "the 5% means. It is a false-alarm rate you chose, not evidence you discovered.")

nb.section("5. Power: what happens when something *is* going on")
nb.code("""print(f"{'true effect':>12} {'n':>5} {'power':>8}")
for eff in [0.2, 0.5, 0.8]:
    for n in [15, 30, 100]:
        power = (run_studies(n=n, true_diff=eff) < 0.05).mean()
        print(f"{eff:>12} {n:>5} {power:>8.2f}")""")
nb.md("A real effect of 0.2 with n=15 is caught about 1 time in 10. If you run that study and "
      "get nothing, you have learned almost nothing about the world, only about your sample size.")

nb.section("6. The winner's curse",
           "When power is low, the only results that reach significance are the ones that got "
           "lucky and large. So 'significant' effects come out systematically overstated.")
nb.code("""n, true_effect = 15, 0.3
a = rng.normal(0, 1, size=(20_000, n))
b = rng.normal(true_effect, 1, size=(20_000, n))
res = stats.ttest_ind(a, b, axis=1, equal_var=False)
est = b.mean(axis=1) - a.mean(axis=1)
sig = res.pvalue < 0.05

print(f"true effect                       : {true_effect}")
print(f"average estimate, all studies     : {est.mean():.3f}")
print(f"average estimate, SIGNIFICANT only: {est[sig].mean():.3f}   <-- inflated {est[sig].mean()/true_effect:.1f}x")
print(f"power                             : {sig.mean():.2f}")""")

nb.section("7. Two ways the t-test lies: peeking, and dependence")
nb.code("""# (a) PEEKING: test repeatedly as data arrive, stop the moment p < 0.05.
def peek_experiment(max_n=500, checks=25):
    a = rng.normal(0, 1, max_n); b = rng.normal(0, 1, max_n)   # NO real difference
    for n in np.linspace(20, max_n, checks).astype(int):
        if stats.ttest_ind(a[:n], b[:n], equal_var=False).pvalue < 0.05:
            return True
    return False

false_alarms = np.mean([peek_experiment() for _ in range(2000)])
print(f"false-positive rate when you peek 25 times: {false_alarms:.3f}  (you asked for 0.05)")""")
nb.code("""# (b) DEPENDENCE: 40 users, 50 sessions each. The rows are not independent.
n_users, per_user = 40, 50
user_effect = rng.normal(0, 1.0, size=(2, n_users, 1))          # each user has a personality
sessions = user_effect + rng.normal(0, 1.0, size=(2, n_users, per_user))

t_rows, p_rows = stats.ttest_ind(sessions[0].ravel(), sessions[1].ravel(), equal_var=False)
t_user, p_user = stats.ttest_ind(sessions[0].mean(axis=1), sessions[1].mean(axis=1), equal_var=False)
print(f"treating all {2*n_users*per_user} SESSIONS as independent: t = {t_rows:6.2f}, p = {p_rows:.4f}")
print(f"aggregating to {2*n_users} USERS (the real unit)        : t = {t_user:6.2f}, p = {p_user:.4f}")""")
nb.md("Run that cell a few times. The session-level test is not just noisier, it is *wrong*: it "
      "reports far more confidence than the data contains, because 2,000 rows from 40 people is "
      "not 2,000 independent pieces of information.")

nb.section("7c. Two things the homework needs: group summaries and a picture",
           "Every real comparison starts by describing the groups and looking at them, not by "
           "running a test.")
nb.code("""bikes = pd.read_csv("https://richardson.byu.edu/220/bikes.csv")

# per-group summaries: count, mean, SD, median
summary = bikes.groupby("Holiday")["Count"].agg(["count", "mean", "std", "median"]).round(1)
print(summary, "\\n")

# mean vs median is the quick skew check
for name, g in bikes.groupby("Holiday"):
    print(f"{name:>12}: mean {g.Count.mean():6.1f}, median {g.Count.median():6.1f}, "
          f"gap {g.Count.mean() - g.Count.median():+6.1f}")

fig, axes = plt.subplots(1, 2, figsize=(11, 3.2))
bikes.boxplot(column="Count", by="Holiday", ax=axes[0])
axes[0].set_title("side by side"); axes[0].set_xlabel(""); plt.suptitle("")
for name, g in bikes.groupby("Holiday"):
    axes[1].hist(g.Count, bins=25, alpha=.55, label=name, density=True)
axes[1].legend(); axes[1].set_title("overlaid, scaled to compare")
plt.tight_layout(); plt.show()""")

nb.section("7d. Power for a comparison you actually have",
           "The power table earlier used equal groups and SD 1. Real groups are lopsided, so "
           "simulate with the sizes and spreads you really have.")
nb.code("""def power_for(n1, n2, sd1, sd2, true_diff, reps=4000, alpha=0.05):
    a = rng.normal(0, sd1, size=(reps, n1))
    b = rng.normal(true_diff, sd2, size=(reps, n2))
    return (stats.ttest_ind(a, b, axis=1, equal_var=False).pvalue < alpha).mean()

reg = bikes.loc[bikes.Holiday == "No Holiday", "Count"]
hol = bikes.loc[bikes.Holiday == "Holiday", "Count"]
print(f"observed: {len(reg)} regular days (SD {reg.std():.0f}), "
      f"{len(hol)} holidays (SD {hol.std():.0f})")
print(f"power to detect a 150-rental difference as it stands: "
      f"{power_for(len(reg), len(hol), reg.std(), hol.std(), 150):.2f}")

print("\\nhow many holidays would we need?")
for n_hol in [18, 40, 80, 150, 300]:
    print(f"  {n_hol:>4} holidays -> power {power_for(len(reg), n_hol, reg.std(), hol.std(), 150):.2f}")""")

nb.section("7e. Measuring dependence, and what it costs you",
           "The clustered example above used made-up users. Here is the same problem in the real "
           "bike data, plus a simulation of the damage.")
nb.code("""print(f"lag-1 autocorrelation of daily Count: {bikes['Count'].autocorr(1):.3f}")
print("A day looks like the day before it, so 365 days is not 365 independent facts.\\n")

def ar1_groups(n, rho, reps=2000):
    # Two groups of correlated "days" with NO real difference between them.
    def series(reps, n):
        e = rng.normal(size=(reps, n)); x = np.zeros((reps, n)); x[:, 0] = e[:, 0]
        for t in range(1, n):
            x[:, t] = rho*x[:, t-1] + np.sqrt(1-rho**2)*e[:, t]
        return x
    a, b = series(reps, n), series(reps, n)
    return (stats.ttest_ind(a, b, axis=1, equal_var=False).pvalue < 0.05).mean()

for rho in [0.0, 0.3, 0.5, 0.8]:
    print(f"correlation {rho:.1f} between neighbouring days -> "
          f"false positives {ar1_groups(200, rho):.1%}  (you asked for 5%)")""")
nb.md("At the 0.50 correlation the real bike data shows, a test that should cry wolf 5% of the "
      "time does it far more often. Nothing in the output warns you.")

nb.section("8. A real comparison, end to end",
           "Daily bike rentals: does ridership differ on holidays? A real operational question "
           "with a real staffing decision behind it.")
nb.code("""bikes = pd.read_csv("https://richardson.byu.edu/220/bikes.csv")
hol = bikes.loc[bikes.Holiday == "Holiday", "Count"]
reg = bikes.loc[bikes.Holiday == "No Holiday", "Count"]

t, p = stats.ttest_ind(reg, hol, equal_var=False)
diff = reg.mean() - hol.mean()
se = np.sqrt(reg.var(ddof=1)/len(reg) + hol.var(ddof=1)/len(hol))
print(f"regular days: n = {len(reg):3d}, mean = {reg.mean():6.1f}")
print(f"holidays    : n = {len(hol):3d}, mean = {hol.mean():6.1f}")
print(f"difference  : {diff:.1f} rentals   t = {t:.2f}   p = {p:.3f}")
print(f"95% CI for the difference: [{diff - 1.96*se:.0f}, {diff + 1.96*se:.0f}]")""")
nb.md("The p-value is nowhere near 0.05, but look at that interval before you say 'no "
      "difference.' With only 18 holidays in the data, the study is consistent with anything "
      "from a large drop to a large increase. That is an *inconclusive* result, not a negative "
      "one, and the honest report says so.")

nb.write("Code_Unit01_Inference.ipynb")


# =====================================================================
# HOMEWORK
# =====================================================================
hw = HW(1, "Statistical Inference",
        """Answer each problem in the cell(s) provided. Replace *Your answer* with your response
for written parts, and put code in the empty code cells.

The first problem is a **simulation lab**: you build a world where you already know the truth, so
you can watch the machinery work. The next three are **real data with real decisions attached**.
The last one asks what you are and are not entitled to conclude.

Throughout, a correct number with a wrong interpretation earns very little. Say what the number
means, and say what it does not mean.

**Data** (real, all from the course server):

- `https://richardson.byu.edu/220/bikes.csv`: 365 days of bike-rental counts with weather.
- `https://richardson.byu.edu/220/rent.csv`: 4,743 rental listings across six cities.""")

hw.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(220)
bikes = pd.read_csv("https://richardson.byu.edu/220/bikes.csv")
rent = pd.read_csv("https://richardson.byu.edu/220/rent.csv")
print(bikes.shape, rent.shape)
bikes.head()""")

# ---------------- Problem 1: simulation lab ----------------
hw.problem(1, """*Simulation lab: what a p-value is.* Here you control the truth, so you can check
what the machinery does. Use `rng` for everything.""")
hw.part("a", """Write a function `run_studies(n_studies, n, true_diff, sd=1.0)` that simulates
`n_studies` experiments. Each experiment draws two independent groups of size `n` from normal
distributions whose means differ by `true_diff`, runs a Welch two-sample $t$-test, and returns the
array of p-values.""")
hw.part("b", """Run 5,000 studies with `true_diff = 0` and $n = 30$, so that **nothing is really
going on**. Plot a histogram of the p-values, and report the fraction below 0.05.""")
hw.part("c", """The histogram should look flat. Explain in 2 to 3 sentences why the p-values are
uniform when the null is true, and what that implies about the meaning of "$p < 0.05$".""", "written")
hw.part("d", """Now set `true_diff = 0.5` and compute the fraction of studies that reach $p<0.05$
for $n = 10, 30, 100, 400$. This fraction is the **power**. Present the four numbers in a small
table and describe the pattern.""")
hw.part("e", """Keep $n = 15$ and `true_diff = 0.3`. Among only the studies that reached
significance, compute the average estimated difference. Compare it to the true 0.3 and explain the
phenomenon you have just measured, and why it makes small significant studies untrustworthy.""")
hw.part("f", """Simulate the peeking problem: run experiments with **no real effect** where you
test after every 20 new observations up to $n = 500$ and stop the moment $p < 0.05$. Across 2,000
such experiments, what fraction produce a "significant" result? Explain the gap between that
number and 0.05.""")

# ---------------- Problem 2: real, underpowered ----------------
hw.problem(2, """*Real data: do holidays change bike ridership?* Use `bikes`. The operations team
wants to know whether to staff differently on holidays. `Count` is the day's rentals and `Holiday`
marks the day type.""")
hw.part("a", """Report the number of days, mean, and standard deviation of `Count` for each level
of `Holiday`. Plot the two distributions side by side (boxplot or overlaid histograms).""")
hw.part("b", """Run a Welch two-sample $t$-test comparing the two groups. Report the difference in
means, the $t$-statistic, the p-value, and a 95% confidence interval for the difference.""")
hw.part("c", """The result is not significant. Your manager writes: *"Confirmed, holidays make no difference. Staff them normally."* Using your confidence interval, explain in 3 to 4 sentences
why that conclusion is not supported, and what the data actually establishes.""", "written")
hw.part("d", """Quantify the problem: by simulation, estimate the power this comparison would have
to detect a true difference of 150 rentals per day, given the group sizes and standard deviations
you observed. (Simulate from normals with those parameters and count how often $p<0.05$.) What
does the number tell you?""")
hw.part("e", """How many holidays would you need in the data to reach 80% power against a
150-rental difference? Find it by simulating a range of holiday counts. Given that a year contains
a fixed number of holidays, what does your answer imply about ever settling this question with one
year of data?""")

# ---------------- Problem 3: real, significant but confounded ----------------
hw.problem(3, """*Real data: furnished apartments rent for more.* Use `rent`. A property manager
asks how much extra to charge for furnishing a unit.""")
hw.part("a", """Compare `Rent` for `FurnishingStatus == "Furnished"` versus `"Unfurnished"`.
Report both sample sizes, both means, the difference, the $t$-statistic, and the p-value.""")
hw.part("b", """The p-value is astronomically small. Explain what that does and does not tell you.
In particular, state whether it says anything about **how much** furnishing is worth.""", "written")
hw.part("c", """Report a 95% confidence interval for the difference in mean rent, and compare the
information it carries to the p-value from Part a. Which would you put in a memo, and why?""")
hw.part("d", """Furnished units are not otherwise identical to unfurnished ones. Compare the two
groups on `Size`, `BHK`, and `City` composition. Report at least two ways they differ.""")
hw.part("e", """Repeat the furnished-versus-unfurnished comparison **within a single city and a
single `BHK` level** (choose ones with enough listings). Report the difference and its interval.
How does it compare to the raw difference from Part a, and what does that tell the property
manager about the number they should actually use?""")

# ---------------- Problem 4: assumptions ----------------
hw.problem(4, """*When the test is quietly wrong.* Both datasets violate a $t$-test assumption.
Find the damage.""")
hw.part("a", """Plot `Rent` and describe its shape. Then compare the mean and median. Which
assumption of the $t$-test is under strain here, and does the sample size rescue it?""")
hw.part("b", """Redo the Problem 3a comparison three ways, all of them $t$-tests: on the raw
`Rent`, on $\\log(\\text{Rent})$, and on the raw rents after dropping the most extreme 1% of
listings. Report all three and explain what each one is actually estimating, and why they do not
answer quite the same question. (We get a fourth and better way, the bootstrap, in Unit 4.)""")
hw.part("c", """Now the `bikes` data. Compute the lag-1 autocorrelation of `Count` across the
year (`bikes["Count"].autocorr(1)`). Report it and explain what it means about the independence
assumption behind Problem 2.""")
hw.part("d", """Demonstrate the damage by simulation: generate two groups of 200 "days" each with
**no real difference** but with each day correlated with the previous one (for example
$x_t = 0.5x_{t-1} + \\varepsilon_t$). Across 2,000 such experiments, what fraction produce
$p < 0.05$? Compare it to the 5% you asked for.""")
hw.part("e", """In 2 to 3 sentences, state which of the two problems, skew or dependence, you would worry about more in a real analysis, and why.""", "written")

# ---------------- Problem 5: what can we say ----------------
hw.problem(5, """*What can and cannot be said.* No new computation is required here. This is the part that
separates an analyst from a calculator.""")
hw.part("a", """Write the two-sentence result statement you would send the operations team about
holidays and bike ridership (Problem 2). It must be honest about both what you found and what
remains unknown.""", "written")
hw.part("b", """Write the two-sentence statement you would send the property manager about
furnishing (Problem 3), including the number you would recommend and the caveat attached to it.""", "written")
hw.part("c", """For each of the following claims, say whether your analyses support it, and if
not, what evidence would be required. (i) *Holidays do not affect ridership.* (ii) *Furnishing a
unit causes rent to rise by the amount you found in Problem 3a.* (iii) *The furnishing result is
more trustworthy than the holiday result because its p-value is smaller.*""", "written")
hw.part("d", """A colleague proposes settling the holiday question by testing every weather
variable, day type, and season in the dataset and reporting whichever comparisons come out
significant. Explain what is wrong with this, and estimate roughly how many "significant" results
they would find by chance if they ran 40 such tests on pure noise.""", "written")
hw.part("e", """Across this assignment you used p-values, confidence intervals, effect sizes, and
power. Rank them by how useful they were for making an actual decision, and defend your
ranking in 3 to 4 sentences.""", "written")

hw.write("Stat_220_HW_Unit01_Inference.ipynb")
