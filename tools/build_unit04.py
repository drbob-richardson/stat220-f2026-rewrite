#!/usr/bin/env python3
"""Unit 4 --- Estimation, Likelihood, and the Bootstrap: code companion + homework."""
from nblib import CodeNB, HW

# =====================================================================
# CODE COMPANION
# =====================================================================
nb = CodeNB(4, "Estimation, Likelihood, and the Bootstrap",
            "Score estimators against a truth you control, watch a likelihood sharpen as data "
            "arrives, and build confidence intervals for statistics that have no formula.")

nb.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(220)
plt.rcParams["figure.figsize"] = (7, 3.5)""")

nb.section("1. The estimator contest",
           "The serial-number problem: N items numbered 1..N, you see n of them, estimate N. "
           "Three rules, scored by how they behave across many samples.")
nb.code("""N_TRUE, n, reps = 500, 8, 20_000
samples = np.array([rng.choice(np.arange(1, N_TRUE+1), size=n, replace=False)
                    for _ in range(reps)])

estimators = {
    "largest seen":          samples.max(axis=1),
    "2*mean - 1":            2*samples.mean(axis=1) - 1,
    "max*(n+1)/n - 1":       samples.max(axis=1)*(n+1)/n - 1,
}

print(f"truth N = {N_TRUE}, sample size n = {n}\\n")
print(f"{'estimator':>18} {'bias':>8} {'SD':>8} {'RMSE':>8}")
for name, est in estimators.items():
    bias = est.mean() - N_TRUE
    rmse = np.sqrt(((est - N_TRUE)**2).mean())
    print(f"{name:>18} {bias:>8.1f} {est.std():>8.1f} {rmse:>8.1f}")""")
nb.md("Notice the ranking. 'Largest seen' has the worst bias but not the worst RMSE. '2*mean-1' is "
      "perfectly unbiased and still loses, because it is so variable. **Unbiased is not the same "
      "as accurate**, and RMSE is the column that matters when you only get one sample.")

nb.section("2. Bias, variance, and why shrinkage wins",
           "Estimating a rate for a group with very little data. Pull the estimate toward a "
           "sensible prior and watch the total error fall.")
nb.code("""true_rate, prior_guess, n_obs, reps = 0.35, 0.20, 12, 40_000
raw = rng.binomial(n_obs, true_rate, reps) / n_obs

weights = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
rows = []
for w in weights:
    est = (1-w)*raw + w*prior_guess
    rows.append((w, est.mean()-true_rate, est.std(), np.sqrt(((est-true_rate)**2).mean())))
best_w = min(rows, key=lambda r: r[3])[0]

print(f"{'shrink toward prior':>20} {'bias':>8} {'SD':>8} {'RMSE':>8}")
for w, bias, sd, rmse in rows:
    print(f"{w:>20.1f} {bias:>8.3f} {sd:>8.3f} {rmse:>8.3f}"
          + ("  <-- lowest total error" if w == best_w else ""))""")
nb.md("Shrinking a little makes the estimate *biased on purpose* and still lowers total error. "
      "This is the same trade that justifies regularization later in the course.")

nb.section("3. Likelihood: same estimate, different confidence")
nb.code("""p = np.linspace(0.001, 0.999, 800)
for k, n_trials, style in [(3, 10, ":"), (30, 100, "--"), (300, 1000, "-")]:
    loglik = k*np.log(p) + (n_trials-k)*np.log(1-p)
    lik = np.exp(loglik - loglik.max())
    plt.plot(p, lik, style, lw=2, label=f"{k} of {n_trials}")
    se = np.sqrt((k/n_trials)*(1-k/n_trials)/n_trials)
    print(f"{k:>4} of {n_trials:>5}:  p-hat = {k/n_trials:.2f},  SE = {se:.4f}")
plt.xlim(0, 0.8); plt.xlabel("conversion rate p"); plt.ylabel("likelihood (scaled)")
plt.legend(); plt.title("All three peak at 0.30. Only one is convincing."); plt.show()""")
nb.md("The width of the peak *is* the standard error, and the numbers confirm it: each tenfold "
      "increase in data narrows the curve by about a factor of three, matching the sqrt(n) rule. "
      "When software prints a huge standard error, it is telling you this curve is flat.")

nb.section("4. The bootstrap, on real data",
           "Medical charges. We want intervals for a mean, a median, and a 90th percentile. "
           "Only one of those has a formula anyone remembers.")
nb.code("""ins = pd.read_csv("https://richardson.byu.edu/220/insurance_all.csv")
charges = ins["charges"].values

def boot(x, stat, B=5000):
    idx = rng.integers(0, len(x), size=(B, len(x)))
    return stat(x[idx], axis=1)

for name, stat in [("mean", np.mean), ("median", np.median),
                   ("90th pct", lambda a, axis: np.percentile(a, 90, axis=axis))]:
    b = boot(charges, stat)
    lo, hi = np.percentile(b, [2.5, 97.5])
    print(f"{name:>10}: estimate {stat(charges[None, :], axis=1)[0]:9,.0f}   "
          f"SE {b.std():7,.0f}   95% CI [{lo:8,.0f}, {hi:8,.0f}]")""")
nb.code("""# Sanity check: for the mean, the bootstrap should agree with the textbook formula.
b = boot(charges, np.mean)
print(f"bootstrap SE of the mean : {b.std():,.1f}")
print(f"formula  s/sqrt(n)       : {charges.std(ddof=1)/np.sqrt(len(charges)):,.1f}")""")

nb.section("5. Where the bootstrap breaks",
           "It can only reshuffle values you already saw, so it cannot see past the largest one.")
nb.code("""x = rng.uniform(0, 100, 60)
bmax = boot(x, np.max)
print(f"true maximum of the distribution : 100.0")
print(f"largest value in the sample      : {x.max():.1f}")
print(f"bootstrap 95% CI for the maximum : [{np.percentile(bmax, 2.5):.1f}, "
      f"{np.percentile(bmax, 97.5):.1f}]  <-- cannot exceed the sample max")

plt.hist(bmax, bins=30, color="#4878a8", edgecolor="white")
plt.axvline(100, color="#c0392b", lw=2, label="the truth, which is unreachable")
plt.legend(); plt.title("The bootstrap cannot invent values it never saw"); plt.show()""")

nb.section("6. Resampling the right unit",
           "The most common bootstrap error in industry, with the damage measured.")
nb.code("""# 60 customers, 40 sessions each. Customers differ; sessions within a customer are alike.
n_cust, per_cust = 60, 40
cust_mean = rng.normal(30, 8, n_cust)
sessions = rng.normal(cust_mean[:, None], 3, size=(n_cust, per_cust))
flat = sessions.ravel()

wrong = boot(flat, np.mean)                       # resample sessions: WRONG
cust_means = sessions.mean(axis=1)
right = boot(cust_means, np.mean)                 # resample customers: RIGHT

print(f"resampling {len(flat):,} sessions : SE = {wrong.std():.3f}")
print(f"resampling {n_cust} customers    : SE = {right.std():.3f}")
print(f"\\nthe wrong unit understates the uncertainty by {right.std()/wrong.std():.1f}x")""")

nb.write("Code_Unit04_Estimation.ipynb")


# =====================================================================
# HOMEWORK
# =====================================================================
hw = HW(4, "Estimation, Likelihood, and the Bootstrap",
        """Answer each problem in the cell(s) provided. Replace *Your answer* with your response
for written parts, and put code in the empty code cells.

The first problem is a **simulation lab** in a world where you know the truth. The next three are
**real estimation problems with a decision attached**. The last asks what your intervals mean.

**Data** (all real):

- `https://richardson.byu.edu/220/insurance_all.csv`: annual medical charges per person.
- `https://richardson.byu.edu/220/fish.csv`: 159 fish of 7 species, with very unequal group
  sizes.
- `https://richardson.byu.edu/220/rent.csv`: rental listings clustered within six cities.""")

hw.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(220)
ins = pd.read_csv("https://richardson.byu.edu/220/insurance_all.csv")
fish = pd.read_csv("https://richardson.byu.edu/220/fish.csv", encoding="utf-8-sig")
rent = pd.read_csv("https://richardson.byu.edu/220/rent.csv")
print(ins.shape, fish.shape, rent.shape)""")

# ---------------- P1: simulation lab ----------------
hw.problem(1, """*Simulation lab: scoring estimators.* A competitor ships products with serial
numbers $1, \\ldots, N$ and you observe a random sample of $n$ of them without replacement. Take
the truth to be $N = 500$.""")
hw.part("a", """Write three estimators of $N$: the sample maximum, $2\\bar{x} - 1$, and
$\\text{max}\\cdot(n+1)/n - 1$. Simulate 20,000 samples of size $n = 8$ and report the bias,
standard deviation, and RMSE of each in a table.""")
hw.part("b", """Plot the three sampling distributions on common axes with a line at the truth.
Which estimator would you actually use, and why is it not simply the one with the smallest
bias?""")
hw.part("c", """Repeat for $n = 3$ and $n = 30$. Describe how the ranking changes, and explain why
the unbiased estimator's disadvantage shrinks as $n$ grows.""")
hw.part("d", """Now the bias-variance trade directly. A group has a true rate of 0.35 and you
observe only 12 trials. For shrinkage weights $w = 0, 0.2, \\ldots, 1.0$ toward a prior guess of
0.20, simulate the bias, SD, and RMSE of $(1-w)\\hat{p} + w(0.20)$. Report the table and identify
the RMSE-minimizing weight.""")
hw.part("e", """Your Part d table should show a biased estimator beating the unbiased one. Explain
in 3 to 4 sentences why this is not cheating, and what you would have to believe about the prior
guess for it to backfire.""", "written")
hw.part("f", """Verify the link between likelihood and standard error: for $(k, n)$ equal to
$(3, 10)$, $(30, 100)$, and $(300, 1000)$, plot the scaled likelihood of $p$ on common axes and
compute $\\sqrt{\\hat{p}(1-\\hat{p})/n}$ for each. Explain the relationship between the width of
each curve and its standard error.""")

# ---------------- P2: real bootstrap ----------------
hw.problem(2, """*Real data: intervals for things without formulas.* Use `ins`. An insurer needs
several different summaries of `charges`, and only one of them has a formula anyone remembers.""")
hw.part("a", """Write a bootstrap function and use it to produce estimates, standard errors, and
95% percentile intervals for the **mean**, the **median**, and the **90th percentile** of
`charges`. Present the three results in one table.""")
hw.part("b", """Check your bootstrap against theory where theory exists: compare the bootstrap SE
of the mean to $s/\\sqrt{n}$. Report both, and say what agreement here tells you about the
bootstrap's validity for the *other* two statistics.""")
hw.part("c", """The median's interval should be much narrower than the mean's. Explain why, in
terms of what each statistic does with the long right tail.""", "written")
hw.part("d", """The insurer must (i) budget total payouts for 10,000 members and (ii) tell a
prospective member what someone like them typically pays. State which statistic answers each
question and give the number with its interval.""", "written")
hw.part("e", """Bootstrap the **maximum** charge and plot the result. Explain what is wrong with
this distribution and why no amount of resampling can fix it.""")

# ---------------- P3: shrinkage on real groups ----------------
hw.problem(3, """*Real data: small groups and honest rankings.* Use `fish`, where `Weight` is an
individual fish's weight and `Species` has seven levels with very unequal sample sizes.""")
hw.part("a", """Report the mean `Weight`, standard deviation, and count for each species, sorted
by mean. Note the sample size of the heaviest species.""")
hw.part("b", """Bootstrap a 95% interval for each species' mean weight and plot the seven intervals
side by side. Which species are genuinely distinguishable, and which overlap so much that ranking
them is meaningless?""")
hw.part("c", """Build shrunken estimates: a weighted average of each species mean and the overall
mean, with weight $n_i/(n_i + 10)$ on the species mean. Report raw and shrunken side by side and
describe which species moved most, and why.""")
hw.part("d", """A supplier wants to advertise "the heaviest species we sell." Using your intervals
and shrunken estimates, write the 3 to 4 sentence answer you would give, including why the raw
leaderboard is a biased way to pick a winner.""", "written")
hw.part("e", """Show the winner's-curse effect directly: by simulation, draw seven groups that all
have the *same* true mean but the sample sizes from this dataset, and record how often the
group with the highest sample mean is a small group. Report the fraction.""")

# ---------------- P4: the resampling unit ----------------
hw.problem(4, """*Real data: what is one observation?* Use `rent`, where listings cluster within
six cities.""")
hw.part("a", """Bootstrap the mean `Rent` by resampling **individual listings**. Report the SE and
the 95% interval.""")
hw.part("b", """Now bootstrap by resampling **whole cities** (draw six cities with replacement and
pool all their listings each time). Report the SE and interval.""")
hw.part("c", """Report the ratio of the two standard errors. Which one would you defend in a
meeting, and what question determines the answer?""", "written")
hw.part("d", """Demonstrate the same effect where you control the truth: simulate 60 customers with
40 sessions each, where customers differ substantially but sessions within a customer are similar.
Bootstrap the mean session value by resampling sessions and by resampling customers, and report
how badly the wrong unit understates the uncertainty.""")
hw.part("e", """Give a rule, in one or two sentences, that a junior analyst could apply to any
dataset to choose the resampling unit correctly.""", "written")

# ---------------- P5: what can we say ----------------
hw.problem(5, """*What can and cannot be said.* Written answers.""")
hw.part("a", """You reported a bootstrap 95% interval for median charges. Write the sentence you
would put in a report, and then write the *incorrect* version that most people would write
instead, and explain the difference.""", "written")
hw.part("b", """Your shrunken species estimates are deliberately biased. Explain to a skeptical
colleague why you would still prefer them for a public leaderboard, and name the situation in
which they would mislead.""", "written")
hw.part("c", """The bootstrap needs one assumption to work at all. State it, and describe a
realistic dataset where it fails badly enough that you would not trust the interval.""", "written")
hw.part("d", """Compare what you learned from the simulation lab (Problem 1) with what you learned
from the real data (Problems 2 to 4). Name one thing the simulation could establish that the real
data could not, and one thing the real data revealed that no simulation would have.""", "written")
hw.part("e", """Your manager asks: "just give me the number, I don't need the interval." Write the
3 to 4 sentence reply you would actually send, giving them a usable number while making the
uncertainty impossible to ignore.""", "written")

hw.write("Stat_220_HW_Unit04_Estimation.ipynb")
