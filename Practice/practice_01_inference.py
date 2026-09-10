#!/usr/bin/env python3
"""Unit 1 practice, multiple choice with answers inline. STUDENT-FACING.

Distractor discipline: the key is not systematically the longest option, and it
is spread across A, B, C and D. Reasoning lives in the explanation.
"""
from build_questions import build_mc

build_mc("Inference", "Statistical Inference",
"""Practice on signal against noise, p-values, confidence intervals, power, and the assumptions a
t-test rests on. No computer and no tables. Where a number is needed it is small enough to reason
about in your head.""",
[
("An A/B test on 40 users per arm reports a 60 percent lift, $p = 0.04$. Why wait before "
 "shipping?",
 ["The p-value is above the usual 0.01 bar.",
  "A one-sided test would have been the right call.",
  "At that sample size, only lucky results clear the bar.",
  "A 60 percent lift is impossible, so the data is wrong."],
 2,
 "This is the winner's curse. When power is low, the only estimates that reach significance are "
 "the ones that happened to land high, so the reported effect is biased upward. Ask for the "
 "confidence interval and a replication. Option A invents a threshold and option D throws out "
 "data for being inconvenient."),

("A trial reports $p = 0.04$. A journalist writes that there is a 4 percent chance the drug does "
 "not work. What is wrong?",
 ["The p-value assumes the drug does nothing.",
  "It should have been doubled for a two-sided test.",
  "Nothing, that is what a p-value measures.",
  "It is fine if patients were randomized."],
 0,
 "The p-value is computed assuming the null is true, so it cannot also be the probability that "
 "the null is true. That reverses the conditional. The honest reading: if the drug did nothing, "
 "results this extreme would turn up about 4 percent of the time. Getting the probability of a "
 "hypothesis needs a prior, which is Unit 12."),

("Study A: a 10-point drop, $\\mathrm{SE} = 8$. Study B: a 2-point drop, $\\mathrm{SE} = 0.5$. "
 "Which is stronger evidence?",
 ["A, since a bigger standard error means more data.",
  "B, at four standard errors from zero.",
  "Neither until they are pooled.",
  "A, since a 10-point drop is five times larger."],
 1,
 "Evidence is the estimate measured against its own noise. Ten over eight is 1.25, and two over "
 "half is 4. Study A's interval comfortably includes zero, so it is consistent with the drug "
 "doing nothing. Option A has the standard error backwards, since more data makes it smaller."),

("Five million users, a 0.4 second difference, $p < 10^{-8}$. Your manager calls it major.",
 ["Agree, a p-value that small is as strong as it gets.",
  "The test is invalid at that sample size.",
  "Disagree, it is almost certainly a false positive.",
  "It is real and probably trivial."],
 3,
 "A tiny p-value at huge n is a statement about the sample size, not about importance, since the "
 "t-statistic grows with the square root of n. Move the conversation to the effect size and "
 "whether 0.4 seconds is worth anyone's engineering time. Note that C goes wrong in the opposite "
 "direction: large samples make false positives less likely."),

("Twenty page colours are tested. Green comes back at $p = 0.04$ and the rest show nothing.",
 ["Excited, it cleared the 0.05 bar.",
  "Not excited, since 0.04 is too near 0.05 to trust.",
  "Excited, since 19 nulls make green stand out.",
  "Not excited, that is what noise looks like."],
 3,
 "Each test carries its own 5 percent false-alarm budget, so across 20 the chance of at least one "
 "hit is about 64 percent. A lone significant result out of 20 is roughly what pure noise "
 "produces. Option B is a different mistake, treating 0.05 as a cliff where 0.04 and 0.06 mean "
 "opposite things."),

("A study on 10 people reports $p = 0.40$ and concludes there is no effect.",
 ["Correct, a high p-value shows something does not work.",
  "Wrong, that p-value actually supports a large effect.",
  "Underpowered, so ask for the interval.",
  "Right, though a one-sided test would have been better."],
 2,
 "Failing to reject is not the same as showing the effect is zero. At n = 10 the study could miss "
 "a large real effect entirely. The confidence interval separates the two cases: running from "
 "minus 3 to plus 12 percent means inconclusive, while a narrow interval hugging zero would "
 "genuinely support no meaningful effect."),

("Which statement describes a 95 percent confidence interval?",
 ["About 95 percent of the observed data falls inside it.",
  "95 percent of such intervals cover the truth.",
  "There is a 95 percent chance the truth is in this one.",
  "It holds the sample mean 95 percent of the time."],
 1,
 "The 95 percent describes the long-run behaviour of the procedure, not this one interval. Once "
 "computed, the interval either contains the true value or it does not. Option C is the most "
 "common misstatement and actually describes a credible interval, which needs a prior. Option A "
 "confuses it with the spread of the data, which is far wider."),

("Conversion moves from 2.0 to 2.4 percent week over week. What do you check?",
 ["Announce it, a 20 percent relative gain is large.",
  "Run a t-test on the two percentages.",
  "Counts, then the denominator, then the tracking.",
  "Compare with the same week last year."],
 2,
 "Work outward from the most boring explanation. On a small base, 2.0 to 2.4 can easily be noise. "
 "If it is not, a shift in traffic mix or a change in how conversion is recorded explains far "
 "more dashboard movement than real behaviour does. Hunting for causes before ruling those out is "
 "how teams end up explaining artifacts."),

("Someone watches a live A/B dashboard and stops the moment $p$ drops below 0.05.",
 ["It only matters when the sample is small.",
  "It makes the test more conservative.",
  "Nothing, as long as p is below 0.05 at the end.",
  "Every look is another chance to cross."],
 3,
 "Optional stopping is multiplicity in disguise. An experiment with no real effect will wander "
 "across the line eventually if you keep watching, and stopping right then guarantees you record "
 "it. The true false-positive rate climbs well above 5 percent, easily to 20 or 30 with frequent "
 "checks. Fix the sample size in advance, or use a method built for repeated looks."),

("Two cities are compared by pooling 400,000 sessions, giving $t = 31$. First concern?",
 ["Nothing, more data is better.",
  "A t that large means a computational error.",
  "The sessions are not 400,000 independent facts.",
  "It should have been a paired test."],
 2,
 "Sessions from the same user, and users within the same city, are correlated. The standard error "
 "divides by the square root of n, so counting correlated rows as independent ones makes it far "
 "too small and inflates t. Aggregate to the level that is genuinely independent, the user or the "
 "city, and analyse those numbers instead."),

("(a) 30 people measured before and after training. (b) 30 trained compared with 30 untrained.",
 ["Both unpaired, each compares two sets of numbers.",
  "(a) unpaired, (b) paired.",
  "Both paired, both involve the training.",
  "(a) paired, (b) unpaired."],
 3,
 "Pairing is about whether the two numbers are linked at the level of one individual. In (a) they "
 "are, so take each person's difference and run a one-sample test, which also strips out "
 "person-to-person variation and gains power. In (b) no particular trained person is linked to "
 "any particular untrained one."),

("Group A: 2,000 observations, small spread. Group B: 80 observations, large spread.",
 ["Welch's test.",
  "The pooled Student test, which has more power.",
  "A paired test, to handle the different sizes.",
  "No test until the groups are the same size."],
 0,
 "The pooled test forces one common spread onto two groups that plainly do not share one, and "
 "with lopsided group sizes it reports more certainty than it has earned. Welch costs essentially "
 "nothing and fixes it, which is why it is a sensible default even when you are unsure whether "
 "the variances differ."),

("A t-test on 18 revenue figures, one of them enormous, gives $p = 0.02$. Which assumptions are "
 "strained?",
 ["Independence and equal variance.",
  "Random assignment and blinding of the analyst.",
  "None of them, since n = 18 is fine for a t-test.",
  "Normality of the estimate, and no one point dominating."],
 3,
 "At n = 18 the average of a heavily skewed variable is still skewed, so the reference "
 "distribution is wrong. The single huge purchase moves the mean and inflates s at the same time. "
 "Two checks you can run in your head: ask what happens to the conclusion if that observation "
 "goes, and compare the mean against the median."),

("Rank these by how much damage their failure does: equal variance, independence, normality of "
 "the raw data, outliers.",
 ["Normality first, the t-test is built on it.",
  "Independence, then outliers, then variance, then normality.",
  "Equal variance first, unequal spread biases the estimate.",
  "All four do about the same damage."],
 1,
 "Independence is worst because its failure leaves no trace in any plot and it makes you more "
 "confident rather than less. Outliers come next, since one point moves both the estimate and the "
 "spread. Unequal variance is nearly free to fix with Welch. Normality of the raw data matters "
 "least for means at moderate n, because the CLT works on the average."),

("Why are p-values uniform between 0 and 1 when the null is true?",
 ["Because of the central limit theorem at large n.",
  "Because the null is true about half the time.",
  "Because the sample is large.",
  "It is the null distribution's own tail area."],
 3,
 "Under the null the test statistic follows a known distribution, and the p-value is that "
 "distribution's tail area at the observed value. Feeding a distribution back through itself "
 "gives a flat result. So p below 0.05 happens in exactly 5 percent of null studies by "
 "construction: the 5 percent is a budget you chose, not evidence you found."),

("A manager says the result was not significant, so stop investigating.",
 ["Non-significance always means too small a sample.",
  "No effect, or no power. The interval separates them.",
  "Correct, a non-significant result means no effect.",
  "Wrong, the test should have been one-sided."],
 1,
 "A narrow interval sitting tightly around zero genuinely supports the claim that any effect is "
 "too small to matter. A wide interval spanning large positive and negative values means the "
 "study could not resolve the question, and the honest summary is that you still do not know. "
 "Both give the same p-value."),
])
