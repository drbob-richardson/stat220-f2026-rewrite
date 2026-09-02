#!/usr/bin/env python3
"""Unit 2 --- Probability and Random Variables: code companion + homework."""
from nblib import CodeNB, HW

# =====================================================================
# CODE COMPANION
# =====================================================================
nb = CodeNB(2, "Probability and Random Variables",
            "The simulations behind the slides: why real randomness clumps, what independence "
            "buys you and what it costs when it fails, Bayes by counting people, and why the "
            "average is the wrong number to plan on.")

nb.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(220)
plt.rcParams["figure.figsize"] = (7, 3.5)""")

nb.section("1. Real randomness clumps",
           "The fake-a-coin demo, settled by simulation. We measure the longest run of the same "
           "side in a sequence of honest flips.")
nb.code("""def longest_run(seq):
    best = run = 1
    for i in range(1, len(seq)):
        run = run + 1 if seq[i] == seq[i-1] else 1
        best = max(best, run)
    return best

runs = np.array([longest_run(rng.integers(0, 2, 50)) for _ in range(20_000)])
print(f"50 honest flips: mean longest run = {runs.mean():.2f}, "
      f"median = {np.median(runs):.0f}, 90th pct = {np.percentile(runs, 90):.0f}")
print(f"P(longest run <= 3) = {(runs <= 3).mean():.3f}   <-- where most invented sequences live")

plt.hist(runs, bins=np.arange(1.5, 15.5), color="#4878a8", edgecolor="white")
plt.xlabel("longest streak in 50 flips"); plt.ylabel("sequences")
plt.title("People almost never invent a streak this long"); plt.show()""")

nb.section("1b. The detector, so you can try to fool it",
           "Same 120 reference sequences the slides use. Type your invented sequence into "
           "`check()` and it will tell you whether a person wrote it.")
nb.code("""REF_SEED, N_FLIPS, N_REF = 20260817, 50, 120
ref_rng = np.random.default_rng(REF_SEED)
reference = ["".join("HT"[b] for b in ref_rng.integers(0, 2, N_FLIPS)) for _ in range(N_REF)]

def switch_rate(seq):
    return sum(seq[i] != seq[i-1] for i in range(1, len(seq))) / (len(seq) - 1)

ref_runs = np.array([longest_run(s) for s in reference])
ref_switch = np.array([switch_rate(s) for s in reference])
print(f"reference: {N_REF} real sequences of {N_FLIPS} flips")
print(f"  longest run  mean {ref_runs.mean():.2f}, range {ref_runs.min()} to {ref_runs.max()}")
print(f"  P(longest run <= 4) = {(ref_runs <= 4).mean():.2f}")
print(f"  switch rate  mean {ref_switch.mean():.2f}")""")

nb.code("""def check(raw):
    seq = "".join(c for c in raw.upper() if c in "HT01").replace("0", "T").replace("1", "H")
    run, sw = longest_run(seq), switch_rate(seq)
    flags = []
    if run <= 4:
        flags.append(f"longest run of {run}: only {100*(ref_runs <= run).mean():.0f}% of real "
                     f"sequences are that short")
    if sw >= 0.60:
        flags.append(f"alternates {100*sw:.0f}% of the time, real coins sit near 50%")
    print(f"{len(seq)} flips, {seq.count('H')} heads, longest run {run}, "
          f"alternates {100*sw:.0f}%")
    print("VERDICT: a person wrote this" if flags else "VERDICT: could be a real coin")
    for f in flags:
        print("   -", f)

check("HTHTTHTHHTHTTHTHHTHTTHTHHTHTTHTHHTHTTHTHHTHTTHTHHT")   # a typical human attempt
print()
check(reference[0])                                            # a real one""")
nb.md("Try your own. The two tells are independent of each other, so a sequence has to get "
      "*both* right to pass, which is why almost nobody does it on the first attempt.")

nb.section("2. Rare events stop being rare when you get many chances")
nb.code("""p_day = 0.01
for days in [1, 7, 30, 90, 365]:
    print(f"{days:4d} days: P(at least one outage) = {1 - (1-p_day)**days:.3f}")""")

nb.section("3. What false independence costs you",
           "Three data centers, each with a 1% monthly failure rate. The only thing that changes "
           "between the two worlds is whether they share a common shock.")
nb.code("""n_sims = 500_000

# World 1: truly independent failures.
indep = rng.random((n_sims, 3)) < 0.01

# World 2: same 1% marginal rate, but part of the risk is a shared regional shock.
shock = rng.random(n_sims) < 0.004                      # hits everything at once
local = rng.random((n_sims, 3)) < 0.006                 # independent local causes
corr = local | shock[:, None]

for name, arr in [("independent", indep), ("shared shock", corr)]:
    marg = arr.mean()
    all_three = arr.all(axis=1).mean()
    print(f"{name:>14}: per-site rate = {marg:.4f}   P(all three down) = {all_three:.6f}")

print(f"\\nThe naive answer 0.01^3 = {0.01**3:.6f}")
print("Same per-site risk. The joint risk differs by orders of magnitude.")""")
nb.md("This is the 2008 mortgage problem in eight lines. Every marginal probability is identical. "
      "Only the dependence changed. Any model that priced the joint risk from the marginals alone "
      "would have called the second world impossible.")

nb.section("4. Bayes by counting people",
           "Never manipulate the formula under pressure. Build the table.")
nb.code("""def screening_table(prevalence, sensitivity, specificity, population=10_000):
    sick = population * prevalence
    well = population - sick
    tp, fn = sick * sensitivity, sick * (1 - sensitivity)
    fp, tn = well * (1 - specificity), well * specificity
    ppv = tp / (tp + fp)
    print(f"population {population:,}, prevalence {prevalence:.1%}")
    print(f"  sick     : {sick:8.0f}  ->  {tp:7.0f} test positive, {fn:7.0f} missed")
    print(f"  healthy  : {well:8.0f}  ->  {fp:7.0f} FALSE positives")
    print(f"  P(sick | positive) = {tp:.0f}/({tp:.0f}+{fp:.0f}) = {ppv:.1%}\\n")
    return ppv

screening_table(0.01, 0.99, 0.95)
screening_table(0.30, 0.99, 0.95)""")
nb.code("""prev = np.logspace(-4, -0.3, 200)
ppv = 0.99*prev / (0.99*prev + 0.05*(1-prev))
plt.semilogx(prev*100, ppv*100, color="#4878a8", lw=2.5)
plt.xlabel("how common the condition is (%)"); plt.ylabel("P(sick | positive)  (%)")
plt.title("The same 99%-accurate test, across base rates"); plt.grid(alpha=.3); plt.show()""")
nb.md("The test never changed. Only the population did. This single curve explains why a fraud "
      "model that looks brilliant on a balanced test set floods the review queue in production.")

nb.section("5. Linearity, and why variance is different",
           "Expectations always add. Variances only add when the pieces are independent.")
nb.code("""# Expected daily revenue for a call center, by simulation and by linearity.
calls, p_buy, basket = 400, 0.06, 85.0
sim = rng.binomial(calls, p_buy, size=200_000) * basket
print(f"simulated mean revenue : ${sim.mean():,.2f}")
print(f"linearity says         : ${calls * p_buy * basket:,.2f}")
print(f"simulated SD           : ${sim.std():,.2f}")
print(f"formula sqrt(n p (1-p)) * basket = ${np.sqrt(calls*p_buy*(1-p_buy))*basket:,.2f}")""")
nb.code("""# Averaging n cases: independent vs correlated.
def sd_of_average(n, rho):
    base = rng.normal(size=(20_000, n))
    common = rng.normal(size=(20_000, 1))
    x = np.sqrt(1-rho)*base + np.sqrt(rho)*common     # each has SD 1, pairwise corr rho
    return x.mean(axis=1).std()

print(f"{'n':>6} {'independent':>13} {'rho=0.2':>10}")
for n in [1, 10, 100, 1000]:
    print(f"{n:>6} {sd_of_average(n, 0.0):>13.3f} {sd_of_average(n, 0.2):>10.3f}")
print(f"\\nfloor for rho=0.2 is sqrt(0.2) = {np.sqrt(0.2):.3f}: more data never gets below it")""")

nb.section("6. The flaw of averages, with real demand",
           "Daily bike rentals. Suppose each bike costs $3 for the day and each rental earns $9.")
nb.code("""bikes = pd.read_csv("https://richardson.byu.edu/220/bikes.csv")
demand = bikes["Count"].values

def profit(fleet, d):
    return 9*np.minimum(d, fleet) - 3*fleet

mean_demand = int(round(demand.mean()))
print(f"mean demand                          : {demand.mean():.0f} bikes")
print(f"profit IF demand equalled the mean   : ${profit(mean_demand, mean_demand):,.0f}")
print(f"ACTUAL average profit at that fleet  : ${profit(mean_demand, demand).mean():,.0f}")

fleets = np.arange(0, demand.max()+1, 5)
avg_profit = np.array([profit(f, demand).mean() for f in fleets])
best = fleets[avg_profit.argmax()]
print(f"profit-maximizing fleet              : {best} bikes  (${avg_profit.max():,.0f})")

plt.plot(fleets, avg_profit, color="#4878a8", lw=2.5)
plt.axvline(mean_demand, color="#7f8c8d", ls="--", label="mean demand")
plt.axvline(best, color="#2e8b57", lw=2, label="optimal fleet")
plt.xlabel("fleet size"); plt.ylabel("average daily profit ($)")
plt.legend(); plt.title("Planning at the average is not planning optimally"); plt.show()""")
nb.md("Two lessons in one plot. The profit you *predict* by plugging in average demand is far "
      "above what you actually earn, and the *best* fleet is not the average demand either. It "
      "sits where the cost of an idle bike balances the cost of a missed rental.")

nb.write("Code_Unit02_Probability.ipynb")


# =====================================================================
# HOMEWORK
# =====================================================================
hw = HW(2, "Probability and Random Variables",
        """Answer each problem in the cell(s) provided. Replace *Your answer* with your response
for written parts, and put code in the empty code cells.

The first problem is a **simulation lab** where you know the truth in advance. The next three
apply the same ideas to **real data with a decision attached**. The last asks what your analysis
does and does not establish.

A correct number with a wrong interpretation earns very little here.

**Data** (all real):

- `https://richardson.byu.edu/220/diabetes.csv`: clinical measurements with a diagnosis.
- `https://richardson.byu.edu/220/insurance_all.csv`: annual medical charges per person.
- `https://richardson.byu.edu/220/product_sales_complaint_data.csv`: units sold and complaints
  per batch.
- `https://richardson.byu.edu/220/bikes.csv`: daily bike-rental counts.""")

hw.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(220)
dia = pd.read_csv("https://richardson.byu.edu/220/diabetes.csv")
ins = pd.read_csv("https://richardson.byu.edu/220/insurance_all.csv")
comp = pd.read_csv("https://richardson.byu.edu/220/product_sales_complaint_data.csv")
bikes = pd.read_csv("https://richardson.byu.edu/220/bikes.csv")
print(dia.shape, ins.shape, comp.shape, bikes.shape)""")

# ---------------- P1: simulation lab ----------------
hw.problem(1, """*Simulation lab: independence, and what it is worth.* You control the truth here,
so you can check every claim from lecture.""")
hw.part("a", """Simulate 20,000 sequences of 50 fair coin flips and record the longest run of the
same side in each. Report the mean and the 10th and 90th percentiles, and plot the distribution.
Then report $P(\\text{longest run} \\le 3)$.""")
hw.part("b", """A classmate hands you an invented sequence whose longest run is 3. Using your
answer to Part a, how suspicious should you be? Answer with a probability, and say in one sentence
what you would conclude and how confident you could be from a single sequence.""")
hw.part("c", """Three services each fail independently with probability 0.02 in a given month.
Compute $P(\\text{at least one fails})$ and $P(\\text{all three fail})$ exactly, then confirm both
by simulation.""")
hw.part("d", """Now break independence. Build a simulation in which each service still fails about
2% of the time, but part of that risk comes from a **shared** regional outage that takes down all
three at once. (For example: a shared shock with probability 0.008 plus independent local causes
with probability 0.012.) Verify the per-service rate is still about 2%, then report
$P(\\text{all three fail})$ and compare it to your Part c answer.""")
hw.part("e", """By what factor did the joint failure probability change between Parts c and d,
while every individual failure rate stayed the same? Write 2 to 3 sentences explaining what this
means for a company that buys three redundant servers from the same cloud region.""", "written")
hw.part("f", """Verify the $1/\\sqrt{n}$ rule and its limit: for $n = 1, 10, 100, 1000$, simulate
the standard deviation of the average of $n$ variables that are (i) independent and (ii) pairwise
correlated at $\\rho = 0.2$. Present a table and describe what happens to each as $n$ grows.""")

# ---------------- P2: real screening ----------------
hw.problem(2, """*Real data: a cheap screening rule and its base rate.* Use `dia`. Treat the rule
**Glucose > 140** as a screening test for diabetes (`Outcome == 1`). A clinic wants to use it to
decide who gets an expensive confirmatory test.""")
hw.part("a", """Report the base rate of diabetes in this dataset. Then build the 2x2 table of the
rule against the truth and compute the **sensitivity** and the **specificity**.""")
hw.part("b", """Compute the positive predictive value, $P(\\text{diabetes} \\mid \\text{test}^+)$,
directly from the table. Explain in two sentences why it differs from the sensitivity.""")
hw.part("c", """Write a function `ppv(prevalence, sensitivity, specificity)` that returns the
positive predictive value implied by a 100,000-person table. Using **your estimated sensitivity
and specificity**, plot the PPV as prevalence ranges from 0.1% to 40%.""")
hw.part("d", """This dataset over-represents diabetes relative to the general population. Read off
your curve the PPV at a realistic community prevalence of 8%, and report how many false positives
the clinic would generate per 1,000 people screened.""")
hw.part("e", """The clinic asks whether they should adopt the rule. Answer in 4 to 5 sentences using
your numbers. Address the base rate, the cost of a false positive, the cost of a miss, and one
thing about this dataset that limits how far your answer should be trusted.""", "written")

# ---------------- P3: real expectation & pooling ----------------
hw.problem(3, """*Real data: expectation, spread, and pooling.* Use `ins`, where `charges` is one
person's annual medical cost. You are advising a small insurer.""")
hw.part("a", """Report the mean, median, and standard deviation of `charges`, and plot the
distribution. Which of the mean and median is the right number for setting a premium that must
cover total payouts, and why?""")
hw.part("b", """Compute the expected charge separately for smokers and non-smokers. How much extra
would a smoker's premium need to be just to break even on expected cost?""")
hw.part("c", """Risk, not just cost: for pool sizes $n = 10, 50, 100, 500, 1000$, simulate 2,000
pools by sampling $n$ people with replacement and record the standard deviation of the **average
charge per person**. Plot it against $n$ and check it against the $1/\\sqrt{n}$ rule.""")
hw.part("d", """Using your Part c results, state how large a pool the insurer needs for the
average cost per person to be within \\$1,000 of its expectation about 95% of the time. Show your
reasoning.""")
hw.part("e", """Now break the independence: suppose a bad flu season raises *everyone's* charges
by a common random amount. Modify your simulation so each pool gets a shared shock (say, a common
multiplier drawn around 1.0) on top of individual variation. Redo the $n = 1000$ case and report
what happens to the SD of the average.""")
hw.part("f", """In 3 to 4 sentences, explain to the insurer why "we have 50,000 policyholders, so
our average cost is essentially certain" is only true under an assumption that catastrophes
violate.""", "written")

# ---------------- P4: distributions & the flaw of averages ----------------
hw.problem(4, """*Real data: choosing a distribution, and planning with it.* Two short studies.""")
hw.part("a", """Use `comp`. Compute the overall complaint rate per unit sold, the mean and
variance of `complaints`, and the correlation between `complaints` and `products_sold`.""")
hw.part("b", """A colleague proposes a Poisson model for `complaints`. What relationship between
the mean and variance does Poisson force? Compare it to what you found, and say whether the data
supports the assumption.""")
hw.part("c", """Reason from the **generating story** instead: each unit sold either produces a
complaint or does not, out of a known number of units. Which distribution does that imply? Using
the average `products_sold` and your estimated rate, compute the variance that story predicts and
compare it to the observed variance.""")
hw.part("d", """Compute $P(\\text{a batch has} \\ge 10 \\text{ complaints})$ three ways: under
Poisson, under your Part c model, and empirically. Which model describes the tail better, and what
would you have concluded about staffing if you had used the wrong one?""")
hw.part("e", """Now `bikes`. Each bike deployed costs \\$3 for the day and each rental earns \\$9,
and you cannot rent more bikes than you deploy. Compute (i) the profit you would *predict* by
assuming demand equals its mean, and (ii) the actual average profit of that same fleet size across
the real daily demands. Report both and explain the gap.""")
hw.part("f", """Sweep fleet sizes and report the profit-maximizing fleet. Is it above or below
mean demand? Explain why in terms of the two costs, and compute how much money per day the
"plan for the average" fleet leaves on the table.""")

# ---------------- P5: what can we say ----------------
hw.problem(5, """*What can and cannot be said.* Written answers, drawing on the work above.""")
hw.part("a", """Your Part 2 analysis produced a positive predictive value. State clearly what
population that number applies to, and name two reasons it would be wrong if the clinic applied it
to walk-in patients at a health fair.""", "written")
hw.part("b", """In Part 3 you estimated the extra expected cost of a smoker. Can the insurer
conclude that *smoking causes* those extra costs? Explain what the number does establish, and what
kind of evidence a causal claim would require. (We return to this in Unit 9.)""", "written")
hw.part("c", """In Part 4 you chose a distribution from the generating story rather than the shape
of the histogram. Give one situation where the story-based choice would be wrong and the data
should override it, and say what you would look for.""", "written")
hw.part("d", """A manager reads your Part 4 fleet recommendation and asks for "the number, not a
range." Write the 3 to 4 sentence answer you would actually give: the recommendation, what it
assumes about next season's demand, and the one condition under which you would revisit it.""", "written")
hw.part("e", """Across this assignment, you used simulation to check three things you could also
have derived algebraically. Name one place where simulation was clearly the better tool and one
where the formula was, and explain the difference in a few sentences.""", "written")

hw.write("Stat_220_HW_Unit02_Probability.ipynb")
