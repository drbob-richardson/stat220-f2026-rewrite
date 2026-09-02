#!/usr/bin/env python3
"""Unit 10 --- Bayesian Reasoning and Decisions: code companion + homework."""
from nblib import CodeNB, HW

nb = CodeNB(10, "Bayesian Reasoning and Decisions",
            "Update a belief step by step, watch a prior stop mattering as data arrives, and turn "
            "a posterior into a decision with a price attached.")

nb.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(220)
plt.rcParams["figure.figsize"] = (7, 3.5)""")

nb.section("1. The two-bag game, in odds form",
           "Bag A is 70% red, Bag B is 30% red. Each red chip multiplies the odds for A by "
           "0.7/0.3, and each white chip divides by the same.")
nb.code("""draws = ["red", "red", "white", "red", "red"]
odds = 1.0                                   # 50/50 to start
print(f"{'draw':>7} {'odds for A':>12} {'P(bag A)':>10}")
print(f"{'start':>7} {odds:>12.3f} {odds/(1+odds):>10.3f}")
for d in draws:
    odds *= (0.7/0.3) if d == "red" else (0.3/0.7)
    print(f"{d:>7} {odds:>12.3f} {odds/(1+odds):>10.3f}")""")
nb.md("Notice the third row: one white chip undoes exactly one red chip. Evidence against counts "
      "as much as evidence for, which is the part people's intuition gets wrong when they are "
      "attached to a hypothesis.")

nb.section("2. Updating a rate: the conjugate shortcut",
           "A Beta(a,b) prior plus s successes and f failures gives a Beta(a+s, b+f) posterior. "
           "The prior behaves like imaginary prior observations.")
nb.code("""a, b = 2, 8                                   # prior: about 20%, worth 10 observations
stages = [(0, 0, "prior"), (2, 8, "10 visitors"), (12, 38, "50 visitors"), (48, 152, "200 visitors")]

print(f"{'after':>14} {'posterior':>18} {'mean':>7} {'95% interval':>20}")
p = np.linspace(0, 1, 600)
for s, f, label in stages:
    post = stats.beta(a+s, b+f)
    lo, hi = post.ppf([0.025, 0.975])
    print(f"{label:>14} {'Beta(%d, %d)' % (a+s, b+f):>18} {post.mean():>7.3f} "
          f"{'[%.3f, %.3f]' % (lo, hi):>20}")
    plt.plot(p, post.pdf(p), lw=2, label=label)
plt.xlim(0, .6); plt.xlabel("conversion rate"); plt.legend(); plt.title("Belief sharpening"); plt.show()""")

nb.section("3. When does the prior stop mattering?")
nb.code("""priors = {"flat Beta(1,1)": (1, 1), "skeptical Beta(2,8)": (2, 8), "bullish Beta(20,5)": (20, 5)}
for label, (s, f) in [("small data: 3 of 10", (3, 7)), ("large data: 150 of 500", (150, 350))]:
    print(f"\\n{label}")
    for name, (a0, b0) in priors.items():
        post = stats.beta(a0+s, b0+f)
        lo, hi = post.ppf([0.025, 0.975])
        print(f"   {name:>22}: mean {post.mean():.3f}  95% [{lo:.3f}, {hi:.3f}]")""")
nb.md("With 10 observations the three priors give three different answers, and honesty requires "
      "reporting which one you used. With 500 they agree to two decimals. The prior is an "
      "assumption exactly when the data is thin, which is exactly when you needed one.")

nb.section("4. A Bayesian A/B test, with the decision attached")
nb.code("""a_s, a_n = 84, 1000
b_s, b_n = 104, 1000
post_a = stats.beta(1 + a_s, 1 + a_n - a_s)
post_b = stats.beta(1 + b_s, 1 + b_n - b_s)
da, db = post_a.rvs(200_000, random_state=1), post_b.rvs(200_000, random_state=2)

p_better = (db > da).mean()
loss_ship_b = np.maximum(da - db, 0).mean()
loss_ship_a = np.maximum(db - da, 0).mean()

from statsmodels.stats.proportion import proportions_ztest
_, pval = proportions_ztest([b_s, a_s], [b_n, a_n])

print(f"P(B better than A)          : {p_better:.1%}")
print(f"frequentist p-value          : {pval:.3f}   <-- 'not significant'")
print(f"expected loss if we ship B   : {loss_ship_b*100:.4f} percentage points")
print(f"expected loss if we ship A   : {loss_ship_a*100:.4f} percentage points")
print(f"\\nAt 200,000 visitors a year, shipping B risks about "
      f"{loss_ship_b*200_000:.0f} conversions and stands to gain {loss_ship_a*200_000:.0f}.")""")
nb.md("Both numbers are correct. They answer different questions. The p-value asks how surprising "
      "this data would be if the two were identical. The posterior asks what we should now believe "
      "and what it costs to be wrong, which is what the person deciding actually needs.")

nb.section("5. Shrinkage, checked against the truth",
           "Small groups get pulled toward the overall rate. Here we can verify that this is not "
           "just conservative, it is more accurate.")
nb.code("""credit = pd.read_csv("https://richardson.byu.edu/220/credit_risk.csv")
truth = credit.groupby("loan_intent")["loan_status"].mean()
sample = credit.sample(400, random_state=5)
g = sample.groupby("loan_intent")["loan_status"].agg(["sum", "count"])
overall = sample["loan_status"].mean()

print(f"{'k':>6} {'total squared error':>22}")
for k in [0, 5, 20, 40, 100, 400]:
    est = (g["sum"] + k*overall) / (g["count"] + k)
    sse = ((est - truth[est.index])**2).sum()
    label = "raw (no shrinkage)" if k == 0 else ""
    print(f"{k:>6} {sse:>22.5f}  {label}")""")

nb.section("6. What is a study worth?",
           "Information has a computable price: how much better your decision gets because you "
           "bought it.")
nb.code("""COST, GOOD, P_GOOD = 400_000, 1_000_000, 0.60

ev_blind = P_GOOD*GOOD - COST
print(f"expected profit, launch blind          : ${ev_blind:,.0f}")

ev_perfect = P_GOOD*(GOOD - COST)          # with perfect info you only launch when good
print(f"expected profit, perfect information   : ${ev_perfect:,.0f}")
print(f"value of perfect information           : ${ev_perfect - ev_blind:,.0f}")

# An imperfect study: right 80% of the time in each direction.
n = 200_000
good = rng.random(n) < P_GOOD
says_good = np.where(good, rng.random(n) < 0.8, rng.random(n) < 0.2)
profit = np.where(says_good, np.where(good, GOOD - COST, -COST), 0)
print(f"expected profit, 80%-accurate study    : ${profit.mean():,.0f}")
print(f"value of the imperfect study           : ${profit.mean() - ev_blind:,.0f}")""")
nb.md("If a study cannot change your decision, its value is zero no matter how interesting it is. "
      "That is the question to ask before commissioning one.")

nb.write("Code_Unit10_Bayesian.ipynb")


hw = HW(10, "Bayesian Reasoning and Decisions",
        """Answer each problem in the cell(s) provided. Replace *Your answer* with your response
for written parts, and put code in the empty code cells.

The first problem is a **simulation lab** on updating and priors. The next three apply it to
**real data and a real decision**. The last asks what your posterior entitles you to claim.

**Data** (all real):

- `https://richardson.byu.edu/220/credit_risk.csv`: loans with a default indicator.
- `https://richardson.byu.edu/220/fish.csv`: 159 fish of 7 species with unequal group sizes.""")

hw.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest

rng = np.random.default_rng(220)
credit = pd.read_csv("https://richardson.byu.edu/220/credit_risk.csv")
fish = pd.read_csv("https://richardson.byu.edu/220/fish.csv", encoding="utf-8-sig")
print(credit.shape, fish.shape)""")

hw.problem(1, """*Simulation lab: updating, priors, and coverage.*""")
hw.part("a", """Bag A is 70% red, Bag B is 30% red, starting at 50/50. Compute the posterior
probability of Bag A after the sequence red, red, white, red, red, showing the value after each
draw. Do it with the odds form and print a table.""")
hw.part("b", """Explain, using your table, why one white chip exactly cancels one red chip.""", "written")
hw.part("c", """With a Beta(2,8) prior, plot the posterior for the conversion rate after 2 of 10,
12 of 50, and 48 of 200 conversions. Report the posterior mean and 95% credible interval at each
stage.""")
hw.part("d", """Repeat the 3-of-10 case under three priors: Beta(1,1), Beta(2,8), Beta(20,5).
Report the three posterior means and intervals. Then repeat with 150 of 500. Summarize in one
sentence when the prior matters.""")
hw.part("e", """**Do credible intervals cover?** Simulate 5,000 experiments where the true rate is
drawn from Beta(2,8) and then 20 trials are observed. Compute the 95% credible interval from a
Beta(2,8) prior each time and report the fraction containing the true rate.""")
hw.part("f", """Repeat Part e but draw the true rate from Beta(20,5) while still analyzing with the
Beta(2,8) prior. Report the coverage now, and explain what this shows about a prior that disagrees
with reality.""")

hw.problem(2, """*Real data: an A/B test with a decision attached.* Variant A converts 84 of 1,000
visitors. Variant B converts 104 of 1,000.""")
hw.part("a", """With flat priors, draw 200,000 samples from each posterior and estimate
$P(\\text{B better than A})$. Plot the posterior of the difference.""")
hw.part("b", """Run the frequentist two-proportion test on the same counts and report the p-value.
Explain in 2 to 3 sentences why the two numbers seem to conflict and why both are correct.""", "written")
hw.part("c", """Compute the expected loss of shipping B and of shipping A. Convert both into
expected conversions gained or lost per 200,000 annual visitors.""")
hw.part("d", """Implementing B costs \\$20,000 of engineering time, and each extra conversion is
worth \\$15. Compute the posterior probability that shipping B is profitable over a year, and give
your recommendation in two sentences.""")
hw.part("e", """Your team wants to stop the test now because $P(\\text{B better}) > 90\\%$. Explain
what is and is not protected by using a Bayesian stopping rule, and propose a rule you would
actually adopt.""", "written")

hw.problem(3, """*Real data: shrinkage that you can check.* Use `credit`, grouping by
`loan_intent`. Treat the full dataset's group rates as the truth, and a 400-row sample as your
data.""")
hw.part("a", """Draw `credit.sample(400, random_state=5)`. Report the raw default rate and count
per loan purpose in the sample, alongside the true rates from the full data.""")
hw.part("b", """Build shrunken estimates $(\\text{successes} + k\\bar{p})/(n + k)$ for
$k = 5, 20, 40, 100, 400$. For each $k$, compute the total squared error against the truth, and
plot error against $k$.""")
hw.part("c", """Report the best $k$ and the error at $k = 0$. By what factor did shrinkage reduce
the error? Explain what happens at both extremes of $k$.""")
hw.part("d", """Repeat the whole exercise with 40 different random samples of 400 rows, and report
how often the shrunken estimate beats the raw one. Is the advantage reliable or occasional?""")
hw.part("e", """Now do it on `fish`: build a shrunken estimate of mean `Weight` per species using
the other species as prior information. Report raw and shrunken means and say which you would
publish, and why.""")

hw.problem(4, """*A decision, priced.* Written and computational.""")
hw.part("a", """You must decide whether to launch in a new city. Launching costs \\$400,000. Your
posterior gives a 60% chance of a \\$1,000,000 return and a 40% chance of \\$0. Compute the
expected profit and state whether you launch.""")
hw.part("b", """Compute the expected profit if you had perfect information about which case you
are in, and derive the maximum you should pay for a perfect study.""")
hw.part("c", """Now simulate an imperfect study that is right 80% of the time in each direction.
Estimate the expected profit of "buy the study, launch only if it is positive," and report the
value of the study.""")
hw.part("d", """Find the accuracy at which the study becomes worthless (its value drops to zero) by
sweeping the accuracy from 0.5 to 1.0 and plotting the value. Report the break-even accuracy.""")
hw.part("e", """Give one realistic example from business or engineering where an expensive,
accurate study would still be worth nothing, and explain why.""", "written")

hw.problem(5, """*What can and cannot be said.* Written answers.""")
hw.part("a", """State precisely what your Problem 2 posterior probability means, and then write the
sentence a careless colleague would write instead, explaining the difference.""", "written")
hw.part("b", """Your Problem 3 shrunken estimates are deliberately biased. Explain why you would
still publish them, and describe the situation in which they would mislead.""", "written")
hw.part("c", """A skeptic says your analysis is unscientific because you chose a prior. Write the
reply you would give, including what you would show them to make the objection testable.""", "written")
hw.part("d", """Bayes' rule assumes your model is right, not just your prior. Give a concrete
example where the prior was reasonable, the arithmetic was correct, and the answer was still
badly wrong.""", "written")
hw.part("e", """A VP asks: "just tell me, does the new feature work?" Write the 3 to 4 sentence answer
you would say out loud, given a posterior of 94%, an expected monthly gain of \\$140,000 if right,
and an expected monthly cost of \\$8,000 if wrong. Include the one caveat that would change your
recommendation.""", "written")

hw.write("Stat_220_HW_Unit10_Bayesian.ipynb")
