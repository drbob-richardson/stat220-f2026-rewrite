#!/usr/bin/env python3
"""Unit 1 practice, multiple choice with answers inline. STUDENT-FACING.

Every option carries its own reasoning, so choosing is a judgement rather than a
length comparison. The key is not systematically longest and is spread over ABCD.
"""
from build_questions import build_mc

build_mc("Inference", "Statistical Inference",
"""Practice on signal against noise, p-values, confidence intervals, power, and the assumptions a
t-test rests on. No computer and no tables. Where a number is needed it is small enough to reason
about in your head.""",
[
("An A/B test on 40 users per arm reports a 60 percent lift with $p = 0.04$, and your colleague "
 "wants to ship today. What is the strongest reason to wait?",
 ["With 40 per arm the test had little power, so anything big enough to reach significance "
  "probably got there partly on luck.",
  "A p-value of 0.04 clears 0.05 but not the stricter 0.01 bar that A/B tests normally use, so "
  "the result does not meet the team's own standard.",
  "A 60 percent lift is far larger than these tests usually produce, so the data is probably "
  "mismeasured.",
  "The team should have run a one-sided test, which would have given a smaller p-value here."],
 0,
 "This is the winner's curse. When power is low, the estimates that clear significance are the "
 "ones that landed high, so the reported effect is biased upward. Ask for the interval and a "
 "replication. Option B invents a threshold, and option D chases a smaller p-value rather than a "
 "better answer."),

("A drug trial reports $p = 0.04$. A journalist writes that there is only a 4 percent chance the "
 "drug does not work. What is wrong with that sentence?",
 ["The p-value is one-sided, so the correct figure to quote to readers would be 8 percent.",
  "Nothing is wrong. A p-value of 0.04 is the probability that the null hypothesis is true.",
  "The number is computed assuming the drug does nothing, so it cannot also be the chance that "
  "the drug does nothing.",
  "The sentence is acceptable as long as patients were randomly assigned, since randomization "
  "is what licenses a probability statement about the drug."],
 2,
 "The journalist reversed the conditional. A p-value is the probability of data this extreme "
 "given the null, not the probability of the null given the data. The honest reading is that if "
 "the drug did nothing, results this extreme would appear about 4 percent of the time. Getting "
 "the probability of a hypothesis needs a prior, which is Unit 12."),

("Study A finds a 10-point drop with $\\mathrm{SE} = 8$. Study B finds a 2-point drop with "
 "$\\mathrm{SE} = 0.5$. Which is stronger evidence of a real effect?",
 ["Study A, since a 10-point drop is five times the size of a 2-point drop.",
  "Study B, whose estimate sits four standard errors from zero while Study A's sits at 1.25.",
  "Neither on its own. The two have to be pooled before either can be interpreted.",
  "Study A, because a larger standard error indicates the study collected more observations."],
 1,
 "Evidence is the estimate measured against its own noise, not the raw size of the estimate. Ten "
 "over eight is 1.25, and two over one half is 4. Study A's interval comfortably includes zero, "
 "so it is consistent with the drug doing nothing at all. Option D has the standard error "
 "backwards, since more data makes it smaller."),

("An experiment on 5 million users finds a 0.4 second difference in session time with "
 "$p < 10^{-8}$, and your manager calls it a major finding.",
 ["Agree, since a p-value that small is about as strong as statistical evidence ever gets.",
  "Disagree, since with 5 million users a result this extreme is almost certainly a false alarm.",
  "Disagree, since the t-test stops being valid once the sample runs into the millions and the "
  "normal approximation it leans on breaks down.",
  "The effect is real and probably trivial, because the t-statistic grows with the square root "
  "of the sample size."],
 3,
 "A tiny p-value at huge n is a statement about sample size rather than importance. Move the "
 "conversation to the effect size and whether 0.4 seconds is worth anyone's engineering time. "
 "Note that option B fails in the opposite direction: large samples make false positives less "
 "likely, not more."),

("A team tests 20 page colours against conversion. Green comes back at $p = 0.04$ and the other "
 "19 show nothing. How excited should you be?",
 ["Excited. Nineteen colours showing nothing is what makes the green result stand out.",
  "Not excited. Running 20 tests on nothing gives about a 64 percent chance of at least one hit "
  "under 0.05.",
  "Excited, since the result cleared the 0.05 bar the field has agreed to use, and the other 19 "
  "colours were tested independently of it.",
  "Not excited, because 0.04 sits too close to 0.05 for the result to be worth anything."],
 1,
 "Each test carries its own 5 percent false-alarm budget, so one significant result out of 20 is "
 "roughly what pure noise produces. Fix it with a multiplicity adjustment, or decide on the one "
 "test you care about in advance. Option D is a different mistake, treating 0.05 as a cliff where "
 "0.04 and 0.06 mean opposite things."),

("A study on 10 participants reports $p = 0.40$, and the authors conclude the treatment has no "
 "effect. What is the problem?",
 ["No problem. A large p-value is how you demonstrate that a treatment does not work, and 0.40 "
  "sits far above any threshold in common use.",
  "The conclusion is backwards, since a p-value of 0.40 is evidence that the effect is large.",
  "The study is badly underpowered at $n = 10$, so ask for the confidence interval before "
  "concluding anything.",
  "The conclusion is fine, though a one-sided test would have been the better choice here."],
 2,
 "Failing to reject is not the same as showing the effect is zero. At n = 10 the study could miss "
 "a large real effect. The interval separates the cases: one running from minus 3 to plus 12 "
 "percent means inconclusive, while a narrow interval hugging zero would genuinely support no "
 "meaningful effect."),

("Which statement correctly describes what a 95 percent confidence interval means?",
 ["Roughly 95 percent of the observations in the sample fall inside the interval's endpoints.",
  "There is a 95 percent probability that the true value lies inside this particular interval.",
  "The interval contains the sample mean in about 95 percent of the studies you might run, "
  "which is why the mean sits near its centre.",
  "If the study were repeated many times, about 95 percent of intervals built this way would "
  "contain the truth."],
 3,
 "The 95 percent describes the long-run behaviour of the procedure, not this one interval. Once "
 "computed, the interval either contains the true value or it does not. Option B is the most "
 "common misstatement and describes a credible interval, which needs a prior. Option A confuses "
 "it with the spread of the data, which is far wider."),

("A dashboard shows conversion rising from 2.0 to 2.4 percent week over week. What should you "
 "check before anyone explains why?",
 ["Announce it. On these numbers a 20 percent relative gain is large enough to act on.",
  "Compare the week against the same week a year ago and draw the conclusion from that.",
  "The counts and the interval, then whether traffic mix changed, then whether tracking changed.",
  "Run a two-sample t-test on the two percentages and report whether it clears 0.05, which is "
  "the standard way to compare two rates."],
 2,
 "Work outward from the most boring explanation. On a small base, 2.0 to 2.4 can easily be noise. "
 "If it is not, a change in the denominator or in how conversion is recorded explains far more "
 "dashboard movement than real behaviour does. Hunting for causes before ruling those out is how "
 "teams end up explaining artifacts."),

("A colleague watches an A/B test on a live dashboard and stops it the moment $p$ drops below "
 "0.05. What does that do?",
 ["Nothing, provided the p-value really is below 0.05 at the moment the test is stopped and the "
  "sample size was reasonable by then.",
  "It makes the procedure more conservative, so the false-positive rate ends up under 5 percent.",
  "It matters only for small experiments, where a few observations can swing the result.",
  "Every look is another chance to cross the line, so the real false-positive rate climbs well "
  "past 5 percent."],
 3,
 "Optional stopping is multiplicity in disguise. An experiment with no real effect will wander "
 "across the line if you watch long enough, and stopping right then guarantees you record it. "
 "With frequent checks the true rate reaches 20 or 30 percent. Fix the sample size in advance, or "
 "use a method built for repeated looks."),

("You compare conversion between two cities by pooling all 400,000 individual sessions and obtain "
 "$t = 31$. What is your first concern?",
 ["No concern. More observations give a more reliable estimate, which is what the large t "
  "reflects.",
  "Sessions from one user, and users in one city, are related, so there are far fewer independent "
  "observations than rows.",
  "A t statistic above 30 indicates an arithmetic error somewhere, since values that large do "
  "not occur with real behavioural data.",
  "The two cities should have been compared with a paired test rather than an unpaired one."],
 1,
 "This is the unit-of-analysis problem. The standard error divides by the square root of n, so "
 "counting correlated rows as independent facts makes it far too small and inflates t. Aggregate "
 "to the level that is genuinely independent, the user or the city, and analyse those numbers "
 "instead."),

("Two studies of a training program. Study 1 measures 30 people before and after. Study 2 "
 "compares 30 who trained against 30 who did not. Which test does each call for?",
 ["Study 1 unpaired and Study 2 paired, since Study 2 has the larger total sample.",
  "Both unpaired, because in each case you are comparing one set of numbers against another.",
  "Study 1 paired, since the two numbers come from one person, and Study 2 unpaired.",
  "Both paired, because both studies are measuring the effect of the same training program."],
 2,
 "Pairing is about whether the two numbers being compared are linked at the level of the "
 "individual. In Study 1 they are, so take each person's difference and run a one-sample test, "
 "which also removes person-to-person variation and gains power. In Study 2 no particular trained "
 "person is linked to any particular untrained one."),

("Group A has 2,000 observations with a small spread. Group B has 80 observations with a large "
 "spread. Which two-sample test should you reach for?",
 ["Welch's test, since unequal variances together with unequal group sizes is where the pooled "
  "version misfires.",
  "The pooled Student test, which uses both groups to estimate one spread and so has more power "
  "here.",
  "A paired test, which is the standard way to handle groups of very different sizes by "
  "matching each large-group row to a small-group one.",
  "No test is appropriate until the two groups have been trimmed to the same number of rows."],
 0,
 "The pooled test forces a single common spread onto two groups that plainly do not share one, "
 "and with lopsided sizes it claims more certainty than it has earned. Welch costs essentially "
 "nothing and fixes it, which is why it is a sensible default even when you are unsure whether "
 "the variances differ."),

("A researcher runs a t-test on 18 revenue observations, one of which is an enormous purchase, "
 "and reports $p = 0.02$. Which assumptions are under the most strain?",
 ["Independence of the observations, and equality of the variances across the two groups.",
  "Random assignment to conditions, and blinding of whoever recorded the revenue figures.",
  "None of them. At $n = 18$ the central limit theorem has already done its work.",
  "Normality of the estimate at small n, and the condition that no single point dominates."],
 3,
 "At n = 18 the average of a heavily skewed variable is still skewed, so the reference "
 "distribution is wrong. The single huge purchase moves the mean and inflates s at the same time. "
 "Two checks you can run without a computer: ask what happens if that observation goes, and "
 "compare the mean against the median."),

("Rank the failure of these four t-test assumptions by how much damage each does: equal "
 "variances, independence, normality of the raw data, no extreme outliers.",
 ["Normality first, since the t-test is built on the normal distribution in the first place.",
  "Independence first, then outliers, then equal variance, and normality of the raw data last.",
  "Equal variances first, since unequal spread biases the estimate of the difference itself.",
  "They do roughly equal damage, so the order you check them in does not really matter."],
 1,
 "Independence is worst because its failure leaves no trace in any plot and it makes you more "
 "confident rather than less. Outliers come next, since one point moves both the estimate and the "
 "spread. Unequal variance is nearly free to fix with Welch. Normality of the raw data matters "
 "least for means at moderate n, since the CLT works on the average."),

("Why are p-values uniformly distributed between 0 and 1 when the null hypothesis is true?",
 ["Because the central limit theorem makes the test statistic normal at any reasonable "
  "sample size.",
  "Because across many published studies the null hypothesis turns out to be true about half the "
  "time.",
  "Because the p-value is the tail area of the test statistic's own null distribution, evaluated "
  "at the statistic.",
  "Because the sample is large enough that the sampling distribution of the p-value flattens "
  "out as the number of observations grows."],
 2,
 "Under the null the statistic follows a known distribution, and the p-value is that "
 "distribution's own tail area at the observed value. Feeding a distribution back through itself "
 "gives a flat result. So p below 0.05 happens in exactly 5 percent of null studies by "
 "construction. The 5 percent is a budget you chose, not evidence you found."),

("A manager says the result was not significant, so the team can stop investigating. What are the "
 "two situations that could have produced it?",
 ["Only one situation is possible, since a result that is not significant means there is no "
  "effect.",
  "Either the effect is genuinely small, or the study lacked power, and the interval width tells "
  "them apart.",
  "Either the test was one-sided when it should have been two-sided, or the sample was too small.",
  "Either the sample was too small, or the wrong test was used for this design, and rerunning "
  "with the right one would settle it."],
 1,
 "A narrow interval sitting tightly around zero genuinely supports the claim that any effect is "
 "too small to matter. A wide interval spanning large positive and negative values means the "
 "study could not resolve the question, and the honest summary is that you do not yet know. Both "
 "produce the same p-value."),
])
