#!/usr/bin/env python3
"""Unit 6 practice, multiple choice with answers inline. STUDENT-FACING."""
import random

from build_questions import build_mc


def spread(questions, seed=6):
    """Move the correct option around so it is not B seven times out of ten.

    Swapping two options changes nothing about a question. Written straight
    through, the answer lands wherever the first plausible phrasing put it,
    which here was B.
    """
    pool = [i % 4 for i in range(len(questions))]
    rng = random.Random(seed)
    while True:
        rng.shuffle(pool)
        letters = ["ABCD"[t] for t in pool]
        runs = max(len(list(g)) for _, g in __import__("itertools").groupby(letters))
        if runs < 3:
            break
    out = []
    for (stem, opts, ans, why), target in zip(questions, pool):
        o = list(opts)
        o[target], o[ans] = o[ans], o[target]
        out.append((stem, o, target, why))
    return out


build_mc("Resampling", "Inference Without a Formula",
"""Practice on reading an importance score, building an interval by resampling, and knowing what
resampling can and cannot repair. No computer needed.""",
spread([
("A random forest reports that \\texttt{account\\_number} is the third most important variable, "
 "using the importance the software returns by default. What should you suspect first?",
 ["That account number is secretly encoding something real, such as signup order.",
  "That the default importance favors columns with many distinct values, and an id has one per row.",
  "That the forest was grown too deep and has memorized the training rows.",
  "That account number is correlated with a variable that genuinely matters here."],
 1, "Impurity importance credits a column for the splits it wins, and a column with a distinct "
    "value in every row gets a candidate cut point between every pair of rows. It wins splits by "
    "having more chances. Rerun with permutation importance before investigating the column "
    "itself; an id can encode something real, but that is the second thing to check."),

("What does a permutation importance of 0.21 for one column actually measure?",
 ["The share of the outcome's variation that this column accounts for on its own.",
  "The change in the outcome for a one-unit change in that column, holding others fixed.",
  "How much worse the model predicts on held-out rows when that column is shuffled.",
  "The proportion of the forest's splits that were made on that column."],
 2, "It is a drop in predictive performance, measured by breaking the column's relationship with "
    "the outcome and nothing else. It has no units anyone can name, no direction, and it is not "
    "comparable to a regression coefficient."),

("Permutation importance comes out at $-0.004$ for one column. What does a negative value mean?",
 ["The column has a negative relationship with the outcome.",
  "The calculation has gone wrong and should be rerun with more repeats.",
  "Shuffling the column happened to help slightly, which is what a useless column looks like.",
  "The column should be removed, since it is actively harming the model."],
 2, "If a column carries nothing, shuffling it changes predictions only by chance, and chance "
    "sometimes improves them a little. A small negative score is the signature of a column doing "
    "nothing. Importance has no sign to read."),

("Two columns have permutation importances of 0.40 and 0.20. What follows?",
 ["The first has about twice the effect on the outcome that the second has.",
  "The model leaned on the first more; the ratio is not an effect size.",
  "The first is statistically significant and the second is not.",
  "Dropping the first would cost about twice as much accuracy as dropping the second."],
 1, "Importance ranks how much this fitted model relied on each column. It is not on a scale "
    "where twice the number means twice the effect, and it carries no claim about significance. "
    "Correlated columns can also share credit in ways that make the ratio meaningless."),

("You want a 95\\% interval for the median of a sample. What does one bootstrap resample consist "
 "of?",
 ["A random half of the rows, with the other half held back.",
  "The same number of rows as the original, drawn with replacement.",
  "The same rows in a different random order.",
  "A random subset of about 63\\% of the rows, drawn without replacement."],
 1, "Same size, with replacement, so some rows appear more than once and some not at all. About "
    "63\\% of the original rows turn up in any given resample, but that is a consequence rather "
    "than the rule. Reordering the same rows gives the same median every time."),

("Having drawn 2,000 resamples and computed the median on each, how do you get the interval?",
 ["Take the mean of the 2,000 medians, plus and minus two standard deviations.",
  "Take the 2.5th and 97.5th percentiles of the 2,000 medians.",
  "Take the smallest and largest of the 2,000 medians.",
  "Take the median of the 2,000 medians, plus and minus the standard error of the sample."],
 1, "The percentile interval reads the middle 95\\% straight off the resamples, which is what "
    "makes the method work for quantities with no formula. The minimum and maximum of 2,000 "
    "numbers are the worst two draws and get further apart the more resamples you take."),

("You bootstrap a regression coefficient that already has a textbook standard error, and the two "
 "intervals come out almost identical. What has that shown?",
 ["That the bootstrap was unnecessary and the formula should be used instead.",
  "That the resampling is working, which is the reason to trust it where no formula exists.",
  "That the sample is large enough for the coefficient to be normally distributed.",
  "That the model's assumptions have been checked and hold."],
 1, "Agreement on a case you can check is the argument for using the method on a median, a "
    "ratio, or an importance score, where there is nothing to check it against. It is a "
    "calibration, not a redundancy."),

("A sample of 40 patients was recruited at one clinic. A bootstrap interval for the treatment "
 "effect is narrow. What does that interval cover?",
 ["How much the answer would move across patients drawn the same way from that clinic.",
  "How much the answer would move across patients drawn from the wider population.",
  "The range within which the true effect lies, with 95\\% probability.",
  "Both the sampling variation and the risk that the clinic is unrepresentative."],
 0, "Resampling treats your sample as a stand-in for the population it came from. If the clinic "
    "is unusual, every resample is unusual in the same way, and the interval is tight around the "
    "wrong number. A narrow interval is not evidence that the sample was the right one to take."),

("Several rental listings come from the same building. You resample rows to build an interval. "
 "What goes wrong?",
 ["Nothing, as long as the building is recorded as a column in the data.",
  "The interval comes out too narrow, because the rows carry less information than their count.",
  "The interval comes out too wide, because buildings add variation between resamples.",
  "The resampling fails, because the same listing can be drawn more than once."],
 1, "Listings in one building resemble each other, so 20 of them are not 20 independent pieces "
    "of evidence. Resampling rows assumes they are, and the resulting spread is smaller than the "
    "truth. Resampling whole buildings instead is the usual repair."),

("You bootstrap permutation importance by resampling the whole dataset, then splitting each "
 "resample into training and test rows. Every column, including one you added as noise, comes "
 "back with an interval above zero. What happened?",
 ["The forest needs more trees before the importances settle down.",
  "Resampling with replacement put the same row in both the training and the test set.",
  "The noise column turned out to be correlated with a real predictor.",
  "The number of resamples was too small for the intervals to be reliable."],
 1, "A duplicated row can land on both sides of the split, so the forest has already seen part "
    "of the test set. Shuffling any column then disturbs rows it memorized, and everything "
    "scores as important. Resample the training rows and score against a test set you never "
    "resampled. Nothing errors, and the result looks like a finding."),
]))
