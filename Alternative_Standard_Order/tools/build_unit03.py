#!/usr/bin/env python3
"""Unit 3 --- The Normal Distribution and the CLT: code companion + homework."""
from nblib import CodeNB, HW

# =====================================================================
# CODE COMPANION
# =====================================================================
nb = CodeNB(3, "The Normal Distribution and the CLT",
            "The sticky-note demo, run 20,000 times: watch a badly skewed population turn into a "
            "bell curve once you average it, find out how big n really has to be, and check "
            "whether a 95% interval actually covers 95% of the time.")

nb.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(220)
plt.rcParams["figure.figsize"] = (7, 3.5)""")

nb.section("1. The CLT, watched happening",
           "Start from a population that looks nothing like a bell curve, then average it.")
nb.code("""population = rng.exponential(1.0, 400_000) ** 1.6      # badly right-skewed
print(f"population: mean {population.mean():.2f}, median {np.median(population):.2f}, "
      f"skewness {stats.skew(population):.2f}")

fig, axes = plt.subplots(1, 4, figsize=(12, 2.8))
for ax, n in zip(axes, [1, 2, 10, 50]):
    means = population[rng.integers(0, len(population), size=(20_000, n))].mean(axis=1)
    ax.hist(means, bins=60, color="#4878a8", edgecolor="white", density=True)
    ax.set_title(f"n = {n}   skew {stats.skew(means):+.2f}", fontsize=10)
    ax.set_yticks([]); ax.set_xlim(0, np.percentile(means, 99.5))
plt.tight_layout(); plt.show()""")
nb.md("Track the skewness number, not the picture. It starts near 4 and collapses toward 0. "
      "The CLT is not a claim that the data changes. It is a claim about what happens to the "
      "*average* of the data.")

nb.section("2. Standard deviation is not standard error")
nb.code("""sample = population[rng.integers(0, len(population), 900)]
print(f"SD of the individual values (describes people)   : {sample.std(ddof=1):.3f}")
print(f"SE of the mean = SD/sqrt(n) (describes estimate) : {sample.std(ddof=1)/np.sqrt(900):.3f}")
print()
print("Same data, two questions:")
print(f"  'how different are two random cases?'  -> use the SD  ({sample.std(ddof=1):.2f})")
print(f"  'how well do we know the average?'     -> use the SE  ({sample.std(ddof=1)/30:.2f})")""")

nb.section("3. How big does n have to be? It depends on the shape.",
           "The honest test of the CLT is not 'does the histogram look bell-shaped' but 'does a "
           "95% confidence interval actually cover the truth 95% of the time?'")
nb.code("""def coverage(draw, truth, n, reps=4000):
    x = draw((reps, n))
    m, s = x.mean(axis=1), x.std(axis=1, ddof=1)
    tcrit = stats.t.ppf(0.975, n-1)
    lo, hi = m - tcrit*s/np.sqrt(n), m + tcrit*s/np.sqrt(n)
    return ((lo <= truth) & (truth <= hi)).mean()

cases = {
    "normal        ": (lambda sz: rng.normal(0, 1, sz), 0.0),
    "mildly skewed ": (lambda sz: rng.exponential(1, sz), 1.0),
    "badly skewed  ": (lambda sz: rng.lognormal(0, 1.8, sz), np.exp(1.8**2/2)),
    "rare event 1% ": (lambda sz: (rng.random(sz) < 0.01).astype(float), 0.01),
}
print(f"{'population':>15} " + "".join(f"{('n='+str(n)):>9}" for n in [5, 30, 100, 1000]))
for name, (draw, truth) in cases.items():
    print(f"{name:>15} " + "".join(f"{coverage(draw, truth, n):>9.3f}" for n in [5, 30, 100, 1000]))
print("\\n(every cell should be 0.95 if the interval is honest)")""")
nb.md("This table is the real answer to 'is n=30 enough?'. For symmetric data even n=5 is nearly "
      "fine. For a badly skewed population, n=30 intervals cover well below 95%, so you are "
      "overconfident far more often than you think. For a 1% rare event, n=30 is hopeless: most "
      "samples contain zero events, the SD is estimated as 0, and the interval collapses.")

nb.section("4. Real data: what actually happens with rent")
nb.code("""rent = pd.read_csv("https://richardson.byu.edu/220/rent.csv")
r = rent["Rent"].values
print(f"n = {len(r)},  mean = {r.mean():,.0f},  median = {np.median(r):,.0f},  SD = {r.std():,.0f}")

# Fit a normal by moments and ask it something absurd.
p_negative = stats.norm.cdf(0, r.mean(), r.std())
print(f"\\nA normal with this mean and SD says {p_negative:.1%} of listings have NEGATIVE rent.")
print("The variable is not normal. That does not stop us estimating its MEAN with normal theory:")
print(f"  SE of the mean = {r.std(ddof=1)/np.sqrt(len(r)):,.0f}")
print(f"  95% CI for mean rent = [{r.mean() - 1.96*r.std(ddof=1)/np.sqrt(len(r)):,.0f}, "
      f"{r.mean() + 1.96*r.std(ddof=1)/np.sqrt(len(r)):,.0f}]")""")
nb.code("""fig, axes = plt.subplots(1, 2, figsize=(11, 3.4))
axes[0].hist(r[r < 200_000], bins=80, color="#4878a8", edgecolor="white")
axes[0].set_title("Rent: the raw data is nowhere near normal"); axes[0].set_yticks([])
stats.probplot(np.log(r), dist="norm", plot=axes[1])
axes[1].set_title("log(Rent): much closer to a straight line")
plt.tight_layout(); plt.show()""")

nb.section("5. Where averaging stops working",
           "The CLT needs a finite variance. Heavy-tailed data can violate that, and then no "
           "sample size saves you.")
nb.code("""fig, axes = plt.subplots(1, 2, figsize=(11, 3.2))
for ax, draws, title in [
        (axes[0], rng.normal(0, 1, 5000), "well behaved: the average settles"),
        (axes[1], rng.standard_cauchy(5000), "heavy tail: it never settles")]:
    ax.plot(np.cumsum(draws)/np.arange(1, len(draws)+1), color="#4878a8", lw=1.2)
    ax.axhline(0, color="#c0392b", ls="--"); ax.set_title(title); ax.set_xlabel("observations")
plt.tight_layout(); plt.show()""")

nb.section("6. Dependence: when n is not n",
           "The CLT assumes independent draws. Real data is full of repeated measurements.")
nb.code("""def ar1(n, rho, reps):
    \"\"\"Each observation is correlated with the previous one.\"\"\"
    e = rng.normal(size=(reps, n))
    x = np.zeros((reps, n))
    x[:, 0] = e[:, 0]
    for t in range(1, n):
        x[:, t] = rho*x[:, t-1] + np.sqrt(1-rho**2)*e[:, t]
    return x

for rho in [0.0, 0.3, 0.6, 0.9]:
    x = ar1(200, rho, 4000)
    m, s = x.mean(axis=1), x.std(axis=1, ddof=1)
    lo, hi = m - 1.96*s/np.sqrt(200), m + 1.96*s/np.sqrt(200)
    cover = ((lo <= 0) & (0 <= hi)).mean()
    eff_n = 200 * (1-rho)/(1+rho)
    note = "independent, so n really is 200" if rho == 0 else f"effective n is about {eff_n:.0f}, not 200"
    print(f"correlation {rho:.1f}: 95% CI actually covers {cover:5.1%}   ({note})")""")
nb.md("At a correlation of 0.6 your '95%' interval covers about two-thirds of the time. Nothing "
      "in the output warns you: the code runs, the number is small, and the conclusion is wrong. "
      "This is why the first question about any dataset is *what is one independent observation?*")

nb.write("Code_Unit03_Normal_CLT.ipynb")


# =====================================================================
# HOMEWORK
# =====================================================================
hw = HW(3, "The Normal Distribution and the CLT",
        """Answer each problem in the cell(s) provided. Replace *Your answer* with your response
for written parts, and put code in the empty code cells.

The first problem is a **simulation lab** where you know the right answer in advance, so you can
test claims instead of believing them. The next three use **real data with a decision attached**.
The last asks what your results do and do not license you to say.

**Data** (all real):

- `https://richardson.byu.edu/220/rent.csv`: 4,743 rental listings across six cities.
- `https://richardson.byu.edu/220/cars.csv`: fuel economy for 392 cars.
- `https://richardson.byu.edu/220/bikes.csv`: 365 consecutive days of rental counts.""")

hw.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(220)
rent = pd.read_csv("https://richardson.byu.edu/220/rent.csv")
cars = pd.read_csv("https://richardson.byu.edu/220/cars.csv").dropna()
bikes = pd.read_csv("https://richardson.byu.edu/220/bikes.csv")
print(rent.shape, cars.shape, bikes.shape)""")

# ---------------- P1: simulation lab ----------------
hw.problem(1, """*Simulation lab: does the CLT actually deliver?* The claim from lecture is that
sample means become normal and that 95% intervals cover 95% of the time. Test it.""")
hw.part("a", """Create a badly skewed population (for example `rng.exponential(1, 400_000)**1.6`).
Report its mean, median, and skewness, and plot it.""")
hw.part("b", """For $n = 1, 2, 10, 50$, draw 20,000 samples of that size and plot the four
histograms of sample means. Report the **skewness** of the sample means at each $n$, and describe
what happens to both the shape and the width.""")
hw.part("c", """Confirm the width rule: for each $n$ above, compare the standard deviation of your
sample means to $\\sigma/\\sqrt{n}$ computed from the population. Present a small table.""")
hw.part("d", """Now the honest test. Write a function `coverage(draw, truth, n, reps=4000)` that
builds a standard 95% $t$-interval from each simulated sample and returns the fraction that
contain the true mean. Run it for $n = 5, 30, 100, 1000$ on four populations: normal, exponential,
a heavily skewed lognormal, and a 1%-rare binary event. Present the results as a table.""")
hw.part("e", """Interpret your table in 4 to 5 sentences. For which populations is $n = 30$ adequate?
Where is a "95%" interval badly overconfident, and what does that mean for someone who reports one
without checking?""", "written")
hw.part("f", """The rare-event column should look especially bad. Explain what goes wrong
mechanically when a sample of 30 contains zero or one events.""", "written")

# ---------------- P2: real, non-normal data ----------------
hw.problem(2, """*Real data: rent is not normal, and that is usually fine.* Use `rent`.""")
hw.part("a", """Plot `Rent` and report its mean, median, and standard deviation. Then fit a normal
distribution using that mean and SD and compute the probability it assigns to a **negative** rent.
Report the number.""")
hw.part("b", """Given Part a, is it defensible to report a normal-theory 95% confidence interval
for the *mean* rent? Compute the interval, and explain in 2 to 3 sentences why the answer to this
question is different from the answer to "is rent normally distributed?".""")
hw.part("c", """Produce a Q-Q plot of `Rent` and of $\\log(\\text{Rent})$. Describe what each shows,
and say what the log transformation suggests about how rents are generated.""")
hw.part("d", """Estimate how large a sample you would need for the sample mean of `Rent` to be
trustworthy: resample from the observed rents at $n = 10, 30, 100, 500$ and report the coverage of
the standard 95% interval at each size (treat the full dataset's mean as the truth).""")
hw.part("e", """A colleague reports "mean rent is 35,000 with SD 78,000, so about 95% of listings
fall between $-121{,}000$ and $191{,}000$." Identify both errors in that sentence and give the
correct way to describe the middle 95% of listings.""", "written")

# ---------------- P3: real, roughly normal data ----------------
hw.problem(3, """*Real data: when the normal model does work.* Use `cars`, variable `mpg`.""")
hw.part("a", """Plot `mpg` with a fitted normal density overlaid, and produce a Q-Q plot. Describe
how well the normal model fits.""")
hw.part("b", """Compute the fraction of cars within 1, 2, and 3 standard deviations of the mean and
compare to 68%, 95%, and 99.7%. Report the three comparisons.""")
hw.part("c", """A regulator proposes a standard at 15 mpg. Using the normal model, estimate the
fraction of cars below it. Then compute the actual fraction. Report both and explain the
difference.""")
hw.part("d", """Compute a 95% confidence interval for mean `mpg`, and separately report the range
covering the middle 95% of individual cars. Explain in two sentences which one answers "how good
is the typical car" and which answers "how well do we know the fleet average".""")
hw.part("e", """Repeat Part d separately for `origin == "American"` and `origin == "Japanese"`.
Report both intervals and state whether the two fleet averages are distinguishable.""")

# ---------------- P4: dependence ----------------
hw.problem(4, """*Real data: when your sample size is a lie.* Use `bikes`, which is 365
**consecutive** days.""")
hw.part("a", """Compute the lag-1 autocorrelation of `Count`. Plot `Count` against day index.
Describe what the plot and the number tell you about independence.""")
hw.part("b", """Compute the naive 95% confidence interval for mean daily rentals using
$s/\\sqrt{365}$. Then estimate an effective sample size using
$n_{\\text{eff}} = n(1-\\rho)/(1+\\rho)$ and recompute the interval. Report both.""")
hw.part("c", """Demonstrate the damage with a simulation: generate AR(1) series with
$\\rho = 0, 0.3, 0.6, 0.9$ where the true mean is 0, and report how often the nominal 95% interval
actually contains 0. Present the four coverage numbers.""")
hw.part("d", """`rent` has a different dependence problem: listings cluster within cities. Compute
the mean rent two ways, first treating all listings as independent and then treating each of
the six cities as one observation. Report the standard error each way.""")
hw.part("e", """In 3 to 4 sentences, explain which of the two datasets' dependence problems is more
dangerous in practice and why. Refer to the direction of the error in each case.""", "written")

# ---------------- P5: what can we say ----------------
hw.problem(5, """*What can and cannot be said.* Written answers.""")
hw.part("a", """Write one sentence that correctly uses the standard **deviation** of rent, and one
that correctly uses the standard **error** of the mean rent. Then write a sentence that misuses
one for the other, and explain who would be misled and how.""", "written")
hw.part("b", """State the central limit theorem in your own words, including both conditions it
requires. Then name the two situations from this assignment where those conditions failed.""", "written")
hw.part("c", """A colleague runs a normality test on 4,743 rents, gets $p < 10^{-50}$, and
concludes the analysis is invalid. Explain what is wrong with both the test's role here and the
conclusion drawn from it.""", "written")
hw.part("d", """Your Problem 3 analysis of `mpg` used data collected in the 1970s and early 1980s.
List two conclusions it can support today and two it cannot, and explain the difference.""", "written")
hw.part("e", """Suppose you must report mean daily bike rentals to a city council that will use it
to plan next year's fleet budget. Write the 3 to 4 sentence statement you would give, including the
interval you would quote, which dependence issue you accounted for, and the assumption that would
most threaten the number.""", "written")

hw.write("Stat_220_HW_Unit03_Normal_CLT.ipynb")
