#!/usr/bin/env python3
r"""The second multiple-choice midterm: 35 questions on Units 1 through 5.

Entries are (stem, options, answer_index, why, unit, kind) with an optional
seventh element (figure file, width, how many questions it covers) when the
question introduces a figure.

The first paper went out as practice, so about half of these are deliberately
close to one of its questions or to a practice-guide item: a student who
worked the practice should recognise the shape. The rest are new, and ten of
them are read off a plot.

Figures come from tools/make_mc_exam_figs.py.
"""

QUESTIONS = [
# =====================================================================
# UNIT 1
# =====================================================================
(r"A 95\% confidence interval for a difference runs from $-2.0$ to $+6.4$. Which reading is "
 r"correct?",
 ["The difference is zero, since the interval contains zero.",
  "There is a 95\\% probability the true difference is in that range.",
  "Everything from a small harm to a gain of 6.4 is still consistent.",
  "The study was underpowered and should be repeated before use."],
 2, "An interval reports the range the data leaves open. Containing zero means no difference is "
    "among the possibilities, not that it has been established, and a gain of 6.4 is equally "
    "among them.", 1, "echo"),

(r"A study reports $p = 0.02$ and a colleague says there is a 2\% chance the treatment does "
 r"nothing. What is wrong?",
 ["Nothing at all, since that is exactly what a p-value measures.",
  "The p-value assumes nothing is going on and asks how surprising the data is.",
  "The figure applies to one tail only and should be doubled.",
  "A p-value describes only the sample, so it can say nothing about any treatment."],
 1, "The p-value is computed under the assumption of no effect. It is the probability of data "
    "this extreme given that assumption, not the probability that the assumption holds.",
 1, "echo"),

(r"A marketing team runs 40 tests and reports the one that came back at $p = 0.04$. How much "
 r"should that interest you?",
 ["A good deal, since 0.04 sits comfortably below the usual cutoff.",
  "Not much: at a 0.05 cutoff, 40 tests of nothing produce about two of these.",
  "A good deal, as long as every one of the 40 tests was randomised properly.",
  "Not much, because 40 tests is too few to find a real effect."],
 1, "Two false positives are the expected yield from 40 tests of nothing. One winner out of 40 "
    "is what noise looks like, so the finding has to be confirmed on fresh data before anyone "
    "acts on it.", 1, "echo"),

(r"A trial on 11 patients reports $p = 0.44$ and concludes the drug does not work. What are the "
 r"two situations that both produce this?",
 ["The drug does nothing, or the trial was too small to detect what it does.",
  "The drug does nothing, or the cutoff was set too low to begin with.",
  "The sample was biased, or the outcome was measured with some error.",
  "The drug is harmful, or its benefit is confined to a subgroup."],
 0, "A large p-value is consistent with no effect and with a real effect the study had no power "
    "to find. Eleven patients cannot separate those, which is why the interval is the thing to "
    "report rather than a verdict.", 1, "echo"),

(r"Two labs study the same drug and estimate the same effect size. Lab A has 50 patients and "
 r"reports $p = 0.07$; Lab B has 5,000 and reports $p < 0.001$. A colleague says they disagree. "
 r"Do they?",
 ["Yes: one found an effect and the other did not.",
  "Yes: the larger study overrules the smaller one.",
  "No: they agree on the estimate and differ only in precision.",
  "No, but only if both used the same significance cutoff."],
 2, "The estimate is the finding; the p-value reports how firmly the data pins it down. Same "
    "estimate at two sample sizes is agreement, and the smaller study's wider interval will "
    "contain the larger study's answer.", 1, "new"),

(r"Which change would most increase the power of a comparison?",
 ["Lowering the significance cutoff from 0.05 to 0.01.",
  "Reporting a confidence interval alongside the test.",
  "Measuring more subjects in each group.",
  "Running the test one-sided rather than two-sided."],
 2, "Power rises with sample size and with the size of the effect. A stricter cutoff lowers it, "
    "and how the result is reported changes nothing about it.", 1, "new"),

# =====================================================================
# UNIT 2
# =====================================================================
(r"What makes a model a probability model?",
 ["Its predictions are constrained to lie between 0 and 1.",
  "It states a distribution for the outcome, so uncertainty follows from it.",
  "It is fitted by maximising a likelihood rather than minimising error.",
  "Its predictors are required to be independent of one another."],
 1, "A probability model says what distribution the outcome follows. That assumption is what "
    "produces standard errors, intervals, p-values and AIC. Methods without one can predict "
    "well and simply cannot hand you those.", 2, "echo"),

(r"A manager asks for the p-value on the top variable in a random forest. What do you tell them?",
 ["It appears in the forest output, under variable importance.",
  "It can be recovered by refitting the forest on bootstrap samples.",
  "A forest states no distribution for the outcome, so there is no p-value.",
  "Only variables that appear in most of the trees have p-values."],
 2, "Importance scores rank how heavily the forest leaned on a column. They are not effects and "
    "carry no uncertainty. A question that needs a p-value needs a model that has one.",
 2, "echo"),

(r"Which pair can AIC legitimately compare?",
 ["A regression against a boosted tree on the same rows.",
  "A regression fitted on 400 rows against that same regression on 900 rows.",
  "A regression on $y$ against the same regression on $\\log(y)$.",
  "A regression with two predictors against one with six, on the same rows."],
 3, "AIC is a penalised likelihood, so both models need a likelihood, the same rows, and the "
    "same outcome on the same scale. Change the scale or the rows and the numbers stop being "
    "comparable.", 2, "echo"),

(r"Your outcome is the number of claims a policy files in a year, and most policies file none. "
 r"What does that rule out?",
 ["Any model that mixes categorical and numeric predictors together.",
  "Ordinary linear regression, which can predict a negative count.",
  "Tree-based methods, which need a continuous outcome.",
  "Any model reporting a coefficient rather than a rate."],
 1, "A count outcome bounded below at zero, with a spread that grows with the mean, is what "
    "count models are built for. A straight line will predict $-0.4$ claims without complaint.",
 2, "new"),

(r"A model will be rerun every night for two years, and any single prediction may be queried by "
 r"a customer. What does that push you toward?",
 ["The model with the lowest cross-validated error, whatever its form.",
  "A model whose output you can explain for one case.",
  "A forest, because it is the most stable under retraining.",
  "Whichever model has the fewest predictors to maintain."],
 1, "An output that has to be defended one case at a time needs to be explainable one case at a "
    "time. That is a constraint on the model family, and it is often worth some accuracy.",
 2, "new"),

# =====================================================================
# UNIT 3  (three of these read off the residual panels)
# =====================================================================
(r"Which panel shows a model whose coefficients you could read as they stand?",
 ["Panel 1", "Panel 2", "Panel 3", "Panel 4"],
 1, "Panel 2 is a shapeless band around zero, which is what a residual plot looks like when the "
    "shape you fitted was about right. Panel 1 bends, panel 3 fans, and panel 4 has one case "
    "far from the rest.", 3, "new", ("fig_mc_resid_four.pdf", "0.96", 4)),

(r"Which panel is telling you to add a squared term, or to transform the predictor?",
 ["Panel 1", "Panel 2", "Panel 3", "Panel 4"],
 0, "Panel 1 is an arc: the fit sits above the data in the middle and below it at both ends, "
    "which is what happens when the truth curves and a straight line cannot follow it. More "
    "data will not fix a wrong shape.", 3, "new"),

(r"In panel 4, what should you do first?",
 ["Delete the point and refit, since one case should not drive a model.",
  "Find out what that case is before doing anything to it.",
  "Take the log of the outcome to pull it back toward the others.",
  "Add a predictor that explains why that case is unusual."],
 1, "It could be a data entry error, which gets fixed, or a real and unusual case, which gets "
    "reported with and without. Neither is decided from the plot, and a point does not get "
    "deleted for being inconvenient.", 3, "new"),

(r"Which panel is the one a log of the outcome is meant to fix?",
 ["Panel 1", "Panel 2", "Panel 3", "Panel 4"],
 2, "Panel 3 fans: the spread grows with the fitted value, which is the signature of an outcome "
    "that varies by a percentage rather than a fixed amount. Logging turns a percentage into a "
    "distance and usually flattens the band.", 5, "echo"),

(r"A regression of delivery cost on distance returns a slope of 1.35. What does it mean?",
 ["Deliveries cost about \\$1.35 each on average.",
  "About 135\\% of cost is accounted for by distance.",
  "Each extra mile goes with about \\$1.35 more cost.",
  "A typical prediction is off by about \\$1.35."],
 2, "A slope is a rate, in outcome units per predictor unit: dollars per mile. Stating the "
    "units is most of the interpretation.", 3, "echo"),

(r"A model uses department, which has six levels, and the output shows five coefficients. What "
 r"happened to the sixth?",
 ["It was dropped for being statistically insignificant in the fit.",
  "It is the baseline, and the other five are measured against it.",
  "It was absorbed into the intercept along with the rest.",
  "Its coefficient is exactly zero, so it is not printed."],
 1, "One level has to serve as the reference or the columns would be redundant. Every printed "
    "coefficient compares its level with that one, holding the other predictors fixed.",
 3, "echo"),

(r"House price on lot size gives a slope of $+320$. Add square footage and it becomes $-45$, "
 r"both with small p-values. What is the explanation?",
 ["One of the two fits must have been computed wrongly somewhere.",
  "A sign flip of that size means the sample is too small.",
  "Big lots tend to carry big houses; the first slope was comparing house sizes.",
  "Lot size turns out to have no real relationship with price once you look closely."],
 2, "The two slopes answer different questions. The first compares all houses, the second "
    "compares houses of the same floor area. When the omitted variable relates to both, "
    "adjusting for it can move a coefficient through zero.", 3, "echo"),

(r"In \texttt{sales $\sim$ ads * region}, with \texttt{region} coded 0 or 1, the interaction "
 r"coefficient is $-0.6$. What does it say?",
 ["On average region 1 sells about 0.6 units less per store than region 0.",
  "A dollar of advertising returns 0.6 less in region 1 than in region 0.",
  "Region accounts for 60\\% of the variation in sales.",
  "Advertising and region together explain 0.6 of the model."],
 1, "An interaction coefficient is a difference between slopes, not between levels. The return "
    "on advertising in region 0 is the \\texttt{ads} coefficient; in region 1 it is that minus "
    "0.6. The level difference is the \\texttt{region} coefficient.", 3, "new"),

(r"Residuals against fitted values look fine, but plotted against the order the rows were "
 r"collected they drift steadily upward. What does that mean?",
 ["The relationship bends with the fitted value, so it needs a squared term.",
  "The rows are not independent, so the reported standard errors are wrong.",
  "The outcome should be logged, since it is growing.",
  "Nothing: residuals drift whenever they are sorted by anything."],
 1, "Rows collected near each other resemble each other, so the data carries less information "
    "than its row count suggests and every interval is narrower than it should be. Recognising "
    "it is the part you are responsible for.", 3, "new"),

# =====================================================================
# UNIT 4  (two read off the interval bands)
# =====================================================================
(r"You quote one customer a delivery time. Which band belongs in the quote?",
 ["Band 1, the wider one.",
  "Band 2, the narrower one.",
  "Whichever is narrower at that value of $x$.",
  "Neither; a quote should be a single number."],
 0, "Band 1 is the prediction interval, which includes the case-to-case variation a single "
    "customer is subject to. Band 2 is the confidence interval for the average and is far too "
    "narrow to quote to one person.", 4, "echo", ("fig_mc_intervals.pdf", "0.62", 2)),

(r"You collect ten times as much data and redraw the same picture. What happens to the two "
 r"bands?",
 ["Both shrink toward zero width at about the same rate.",
  "Band 2 keeps narrowing; band 1 narrows a little and then levels off.",
  "Band 1 keeps narrowing; band 2 levels off at the spread of the data.",
  "Neither moves, since the fitted line is unchanged."],
 1, "More data pins down where the line sits, so the confidence band keeps narrowing. The "
    "prediction band also contains the spread of individual cases around the line, which more "
    "data does not remove, so it levels off near that spread.", 4, "new"),

(r"Why is the error a model reports on the rows it was fitted on too small?",
 ["Those rows were cleaner than rows collected later.",
  "The coefficients were chosen to make those residuals small.",
  "Any sample is smaller than the population it came from.",
  "The error is reported before the fitting has converged."],
 1, "Fitting selects the coefficients that minimise the residuals on the rows in front of it, so "
    "measuring there grades the model on the quantity it optimised. A new case gets no such "
    "treatment.", 4, "echo"),

(r"Adding four columns of random noise raises $R^2$ from 0.704 to 0.709. What does that tell "
 r"you?",
 ["The four columns carry a small amount of real signal.",
  "Nothing: $R^2$ cannot fall when a column is added.",
  "The model was underfitted before they were added.",
  "The columns should be kept, since the fit improved."],
 1, "$R^2$ is non-decreasing in the number of predictors, so a rise is not evidence of anything "
    "at all. AIC, or error on rows the model has not seen, is what can tell you a column was "
    "not worth its cost.", 4, "echo"),

(r"A lasso sends the coefficient on \texttt{store\_size} to exactly zero. What does that "
 r"establish?",
 ["Store size has no relationship with the outcome.",
  "Store size would also be insignificant in an ordinary regression.",
  "Store size did not earn its keep against this penalty in this sample.",
  "Store size is uncorrelated with the other predictors."],
 2, "A zero is the product of one penalty strength, this sample, and the other columns present. "
    "Change any of the three and the variable can come back.", 4, "echo"),

(r"A colleague tunes a model on the cross-validation folds, then reports the cross-validated "
 r"error as the final number. What is wrong?",
 ["Nothing, since cross-validation already holds out every row exactly once.",
  "The folds should have been re-randomised before the second pass.",
  "The tuning used those folds, so the score is a best-of rather than an estimate.",
  "Cross-validation cannot be used on a model with tuning parameters."],
 2, "Once the folds have chosen something, the score on them flatters the winner. Tuning is "
    "fine; reporting the tuned score as the final estimate is not. Keep a slice nothing "
    "touched.", 4, "new"),

(r"Two candidate models have cross-validated errors of 4.40 and 4.37 minutes, using 6 and 24 "
 r"predictors. Which do you ship?",
 ["The 24-predictor model, since its error is lower.",
  "Neither, since a gap that small means the comparison is unreliable.",
  "The 6-predictor model, since the gain is tiny for 18 more columns.",
  "Whichever of the two has the higher $R^2$ on the full data."],
 2, "Two seconds of accuracy against eighteen more columns to collect, explain and maintain. "
    "When the scores are this close, everything other than the score is the tie-breaker.",
 4, "new"),

(r"Every predictor for a new case sits inside its own range in the data. Is a prediction for it "
 r"safe?",
 ["Yes: checking each range is what guards against extrapolation.",
  "Yes, provided the model's $R^2$ is comfortably high enough.",
  "Not necessarily: that combination of values may never have occurred.",
  "Not necessarily, but only if the predictors are uncorrelated."],
 2, "Correlated predictors fill a narrow band rather than a box. A case can be ordinary on every "
    "axis and still sit where nothing was ever observed, and a one-variable-at-a-time check "
    "never sees it.", 4, "echo"),

# =====================================================================
# UNIT 5  (five read off plots)
# =====================================================================
(r"What changed between the left panel and the right one?",
 ["The model gained predictors, so the residuals shrank.",
  "The outcome was logged, and the spread is now even across the range.",
  "The most extreme cases were removed before the model was refitted.",
  "The residuals were standardised, which rescales the axis."],
 1, "The left panel fans; the right one does not. Logging the outcome turns a multiplicative "
    "spread into a constant one, which is the assumption every interval and p-value in the "
    "output rests on.", 5, "new", ("fig_mc_fan_fix.pdf", "0.80", 2)),

(r"In the right-hand model the coefficient on $x$ is $0.18$. What does it say?",
 ["$y$ rises by about 0.18 for each unit of $x$.",
  "$y$ rises by about 18\\% for each unit of $x$.",
  "$x$ accounts for about 18\\% of the variation in $y$.",
  "$y$ rises by about 0.18\\% for each 1\\% more $x$."],
 1, "On a logged outcome a coefficient is a percentage: $e^{0.18}-1$ is about 0.20, so roughly "
    "20\\%, and 18\\% is the usual quick reading. Only the predictor being logged too would make "
    "it a percentage for a percentage.", 5, "echo"),

(r"Which depth would you choose from this figure?",
 ["Depth 1, since the two curves are closest there.",
  "Depth 4, where the held-back error is lowest.",
  "Depth 10, since the error on its own rows is still falling.",
  "Depth 14, the deepest shown."],
 1, "The lower curve can always be driven down by letting the tree memorise, so it cannot choose "
    "anything. The held-back curve measures prediction on rows the tree has not seen, and its "
    "minimum is the honest answer.", 5, "echo", ("fig_mc_depth.pdf", "0.62", 1)),

(r"The tree in this figure was grown on $x$ between 1 and 8. What does it predict beyond the "
 r"dashed line?",
 ["It extends the upward trend it found among the largest cases.",
  "It returns the average of the rows in its right-most region, unchanged.",
  "It returns an error, since the value is outside the training range.",
  "It returns the overall average of all the training rows."],
 1, "A tree is flat outside its range by construction: the case falls into the right-most leaf "
    "and gets that leaf's average. It will not run away the way a line does, and it will not use "
    "the extra $x$ at all, with nothing in the output to say so.",
 5, "new", ("fig_mc_tree_steps.pdf", "0.62", 1)),

(r"What does a single split in a regression tree do?",
 ["It fits a separate straight line on each side of the cut.",
  "It tests the two groups and keeps the split when $p < 0.05$.",
  "It cuts the rows in two and predicts each group's average.",
  "It locates the point of steepest change in the outcome."],
 2, "A split chooses one variable and one cut point and predicts the average of the rows on each "
    "side. The machine tries every variable and every cut and keeps whichever leaves the two "
    "groups most alike inside. No test, and no line.", 5, "echo"),

(r"A tree splits on \texttt{weekend} inside the high-volume branch and not inside the low-volume "
 r"branch. What does that suggest adding?",
 ["A squared term in the volume column.",
  "An indicator flag for the high-volume days.",
  "The weekend variable on its own.",
  "An interaction between weekend and volume."],
 3, "A split that appears in one branch and not the other is the tree writing an interaction in "
    "its own notation: the effect of one variable depends on the value of another. The "
    "regression then puts a coefficient and an interval on it.", 5, "new"),

(r"A tree splits a continuous predictor at exactly 100, a round number. What should you suspect?",
 ["The tree is chasing noise, since the cut point it picks is arbitrary.",
  "Something real changes at 100, and it is worth asking what.",
  "The predictor should be logged and the tree grown again from scratch.",
  "The tree was grown too deep and should be pruned back."],
 1, "A continuous variable gives no reason to prefer a round number, so a cut landing on one is "
    "worth asking about. Thresholds in a business, a price list or a regulation are real, and a "
    "smooth model cannot represent the step that follows from them.", 5, "new"),
]
