#!/usr/bin/env python3
r"""The multiple-choice midterm: 35 questions on Units 1 through 5.

Each entry is (stem, options, answer_index, why, unit, kind).

`kind` is "echo" for a question a student who worked the practice guides will
recognize as the same idea in new clothes, and "new" for one that asks them to
put two ideas together or read a result they have not been handed before.
Fifteen echoes, twenty new. The builder prints the tally so the balance is
visible rather than claimed.
"""

QUESTIONS = [
# =====================================================================
# UNIT 1: inference
# =====================================================================
(r"Which statement correctly describes what a 95\% confidence interval means?",
 ["There is a 95\\% probability that the true value lies inside this interval.",
  "95\\% of the observations in the sample fall inside this interval.",
  "Intervals built this way capture the true value 95\\% of the time.",
  "The true value is within the interval unless the sample was unusual."],
 2, "The 95\\% is a property of the procedure across repeated samples, not of this one interval. "
    "Once computed, this interval either contains the true value or it does not.", 1, "echo"),

(r"A trial reports $p = 0.03$. A reporter writes that there is a 3\% chance the treatment does "
 r"nothing. What is wrong?",
 ["Nothing, since that is what a p-value measures.",
  "The p-value assumes nothing is going on and asks how surprising the data is.",
  "The figure should have been doubled, since the test was two-sided.",
  "The p-value is about the sample, so it says nothing about any treatment."],
 1, "A p-value is computed under the assumption that there is no effect; it is the probability of "
    "data this extreme given that assumption, not the probability the assumption is true.",
 1, "echo"),

(r"A team tests 25 subject lines against open rate. One comes back at $p = 0.03$ and the other 24 "
 r"show nothing. How much should that interest you?",
 ["A good deal, since 0.03 clears the usual cutoff comfortably.",
  "Not much: with 25 tests, about one false positive is expected.",
  "A good deal, provided the 24 others were properly randomized.",
  "Not much, because open rate is too noisy to test this way."],
 1, "At a 0.05 cutoff, 25 tests of nothing produce about 1.25 results under 0.05 by chance. One "
    "winner out of 25 is what pure noise looks like. Confirm it on fresh data before acting.",
 1, "echo"),

(r"A study of 14 patients reports $p = 0.31$ and the authors conclude the treatment does not "
 r"work. Which two situations would both produce this result?",
 ["The treatment does nothing, or the study was too small to detect what it does.",
  "The treatment does nothing, or the significance cutoff was set far too low.",
  "The sample was biased, or the outcome was measured with error.",
  "The treatment harms patients, or it helps them by a very small amount."],
 0, "A large p-value is consistent with no effect and with a real effect the study had no power "
    "to find. Fourteen patients cannot tell those apart, which is why the interval, not the "
    "verdict, is the thing to report.", 1, "new"),

(r"An experiment on 3 million sessions finds a 0.2 second difference in load time with "
 r"$p < 10^{-9}$. The manager calls it a breakthrough. What do you say?",
 ["The p-value is so small the result must be a computational error.",
  "Nothing, since that p-value settles the question beyond any doubt.",
  "At this sample size a tiny difference is detectable; ask whether 0.2 seconds matters.",
  "The test is not valid, since the sample is far larger than these formulas assume."],
 2, "Enough data makes any non-zero difference statistically significant. The p-value answers "
    "whether the difference is real, not whether it is worth anything. The effect size and its "
    "units are the business question.", 1, "new"),

(r"Output for a two-sample comparison reads: difference $= 1.4$, SE $= 0.9$, $t = 1.56$, "
 r"$p = 0.12$, 95\% CI $[-0.4, 3.2]$. The manager asks how large the effect could plausibly be. "
 r"Which number answers that?",
 ["The p-value of 0.12, which measures the strength of the evidence.",
  "The upper end of the interval, 3.2.",
  "The difference of 1.4, which is the best single estimate.",
  "The t-statistic of 1.56, which scales the difference."],
 1, "The question is about the range the data leaves open, which is what the interval reports. "
    "The data is consistent with anything from a small harm to a gain of 3.2, and that spread is "
    "the honest answer to how large the effect could be.", 1, "new"),

# =====================================================================
# UNIT 2: a map of models
# =====================================================================
(r"What makes something a probability model rather than a non-probability one?",
 ["It produces predictions that fall between 0 and 1.",
  "It was fitted by maximizing a likelihood rather than minimizing an error.",
  "It states a distribution for the outcome, so uncertainty can be derived.",
  "It requires the predictors to be independent of one another."],
 2, "A probability model says what distribution the outcome follows. That assumption is what "
    "produces standard errors, intervals, p-values and AIC. A method without one can still "
    "predict well; it just cannot hand you those.", 2, "echo"),

(r"A colleague asks for the p-value on the most important variable in a random forest. What do "
 r"you tell them?",
 ["It is in the output, under variable importance.",
  "A forest has no probability model, so there is no p-value to give.",
  "It can be obtained by refitting the forest on bootstrap samples.",
  "Only the top three variables in a forest have p-values."],
 1, "Importance scores rank how much the forest leaned on a column; they are not effects and "
    "carry no uncertainty. If the question needs a p-value, it needs a model that has one.",
 2, "echo"),

(r"Which pair of models can AIC legitimately compare?",
 ["A linear regression against a gradient boosted tree fitted on the same rows.",
  "A regression on 600 rows against the same regression on 900 rows.",
  "A regression predicting $y$ against one predicting $\\log(y)$.",
  "A regression with three predictors against one with seven, on the same rows."],
 3, "AIC is a likelihood penalised for the number of parameters, so both models need a "
    "likelihood, the same rows, and the same outcome on the same scale. Nested or not does not "
    "matter; the scale and the rows do.", 2, "new"),

(r"Your outcome is whether a customer renewed, yes or no. What does that fact alone rule out?",
 ["Any model that uses categorical predictors.",
  "Ordinary linear regression, which can predict below 0 and above 1.",
  "Tree-based methods, which require a numeric outcome.",
  "Any model that reports a coefficient rather than a probability."],
 1, "A yes/no outcome needs a model whose predictions are probabilities. A straight line will "
    "happily predict $-0.3$ and 1.4, and assumes a spread that a binary outcome does not have. "
    "Trees handle this outcome fine.", 2, "new"),

(r"The question is which of five store features most affects sales, with a number attached to "
 r"the answer. Three colleagues propose a linear regression, a random forest, and a single "
 r"depth-3 tree. Which serves the question?",
 ["The forest, because it will rank the five features by importance.",
  "The depth-3 tree, because its splits can be read off directly.",
  "The regression, because only it attaches an interval to the number.",
  "Any of the three, since all three use the same five features."],
 2, "The ask is an effect with uncertainty. A forest ranks but does not quantify, and a tree's "
    "splits are not effects. Only the regression returns a coefficient with an interval. The "
    "other two are useful for finding what to put in it.", 2, "new"),
(r"A model of repair cost on labour hours returns a slope of 84. What does that number mean?",
 ["Repairs cost about \\$84 on average.",
  "About 84\\% of the variation in cost is explained by labour hours.",
  "Each additional labour hour goes with about \\$84 more cost.",
  "A typical prediction is off by about \\$84."],
 2, "A slope is a rate, in outcome units per predictor unit: dollars per hour. Giving the units "
    "is most of the interpretation.", 3, "echo"),

(r"A regression uses region, which has five levels, and the output lists four coefficients. What "
 r"happened to the fifth?",
 ["It was dropped for being statistically insignificant.",
  "It is the baseline, and the other four are measured against it.",
  "It was merged into the intercept along with the other four.",
  "Its coefficient is exactly zero and so is not printed."],
 1, "One level has to be the reference, or the columns would be redundant. Every printed "
    "coefficient is its level against that baseline, with the other predictors held fixed.",
 3, "echo"),

(r"Fuel economy on acceleration time gives a slope of $+1.2$. Add engine power and the slope "
 r"becomes $-0.5$, both with small p-values. What is the explanation?",
 ["One of the two fits must have been computed incorrectly.",
  "The sign flip shows the sample is too small for either fit to be reliable.",
  "Slow cars tend to be small; the first slope was comparing engine sizes.",
  "Acceleration time has no real relationship with fuel economy."],
 2, "The two slopes answer different questions. The first compares all cars; the second compares "
    "cars of the same engine power. When the omitted variable relates to both, adjusting for it "
    "can move a coefficient a long way, including through zero.", 3, "echo"),

(r"Residuals against fitted values look shapeless, but residuals plotted against the week the "
 r"job was recorded drift slowly upward across the year. What does that indicate?",
 ["The relationship with the predictors bends and needs a squared term.",
  "The rows are not independent, so the reported standard errors are wrong.",
  "The outcome should be logged, since the drift suggests growth.",
  "Nothing: residuals are expected to drift when sorted by any column."],
 1, "Nearby weeks resemble each other, so the rows carry less information than their count "
    "suggests and every interval is narrower than it should be. Unit 5 names this: it needs a "
    "model built for time, and recognizing it is the part you are responsible for.", 3, "new"),
(r"Two fits on the same rows. \texttt{y $\sim$ x} gives a slope of 3.1 with SE 0.4. "
 r"\texttt{y $\sim$ x + z} gives 3.0 with SE 1.9. Here $x$ and $z$ correlate at 0.95. What is "
 r"going on?",
 ["Adding $z$ revealed that the slope on $x$ was biased all along.",
  "The second fit is wrong, since a standard error cannot grow that much.",
  "$z$ duplicates $x$, so the fit cannot tell which deserves the credit.",
  "The slope barely moved, so the two fits are equally informative."],
 2, "The estimate hardly moved but its precision collapsed, which is the signature of two columns "
    "carrying the same information. Keep one. A coefficient that moves is confounding; a "
    "coefficient that merely gets noisier is duplication.", 3, "new"),
(r"In \texttt{price $\sim$ sqft * waterfront}, with \texttt{waterfront} coded 0 or 1, the "
 r"interaction coefficient is $+85$. What does it mean?",
 ["Waterfront houses cost about \\$85 more than inland ones.",
  "A square foot is worth about \\$85 more on waterfront than inland.",
  "Waterfront houses cost about 85\\% more than comparable inland ones.",
  "The model gains about \\$85 of accuracy from the interaction."],
 1, "An interaction coefficient is a difference between slopes, not a difference between levels. "
    "The inland rate is the coefficient on \\texttt{sqft}; waterfront earns that plus 85 per "
    "square foot. The level difference is the \\texttt{waterfront} coefficient.", 3, "new"),
(r"Two regressions on the same rows: model A has $R^2 = 0.62$, model B has $R^2 = 0.64$ and four "
 r"more predictors. What settles the choice?",
 ["Model B, since a higher $R^2$ means a better fit to this data.",
  "Model A, since fewer predictors is always the safer choice.",
  "AIC, or error on rows neither model was fitted on.",
  "The p-values on the four extra predictors in model B."],
 2, "$R^2$ cannot fall when predictors are added, so a rise of 0.02 over four columns is not "
    "evidence of anything. AIC charges for the extra parameters, and held-out error asks the "
    "question that matters, which is how each does on rows it has not seen.", 3, "new"),
(r"What does least squares actually minimize?",
 ["The sum of the vertical distances from the points to the line.",
  "The sum of the squared vertical distances from the points to the line.",
  "The sum of the perpendicular distances from the points to the line.",
  "The largest distance from any point to the line."],
 1, "Squaring makes the penalty grow faster than the error, which is why a single far-off point "
    "can pull the line toward itself, and why you look at a residual plot before trusting the "
    "fit.", 3, "echo"),

# =====================================================================
# UNIT 4: prediction and choosing predictors
# =====================================================================
(r"A customer asks how long their one repair will take. Which interval belongs in the answer?",
 ["The prediction interval for a single repair.",
  "The confidence interval for the average repair.",
  "Whichever is narrower, so the quote stays competitive.",
  "Neither; a quote should be a single number."],
 0, "One customer is one case, so the job-to-job variation is part of their question. The "
    "confidence interval is about where the average sits and is far too narrow to quote.",
 4, "echo"),

(r"Why is the error a model reports on the rows it was fitted on too small?",
 ["Because those rows were cleaner than rows collected later.",
  "Because the coefficients were chosen to make those residuals small.",
  "Because any sample is smaller than the population it came from.",
  "Because the error is reported before the fitting has converged."],
 1, "Fitting picks the coefficients that minimize the residuals on the rows in front of it, so "
    "measuring there grades the model on the quantity it optimised. A new case gets no such "
    "treatment.", 4, "echo"),

(r"Adding one indicator to a model moves AIC from 934 to 916. A colleague reports that the "
 r"indicator explains 18\% more of the outcome. What is wrong?",
 ["Nothing, provided the two models were fitted on the same rows.",
  "AIC is a score for comparing models, not a share of anything.",
  "The change should have been divided by 934 to get a percentage.",
  "AIC went down, so the indicator made the model worse."],
 1, "AIC has no units anyone can interpret and no scale from 0 to 100; only differences between "
    "models on the same rows and the same outcome mean anything. A drop of 18 is strong evidence "
    "the indicator earns its parameter, and it is not a percentage of anything.", 4, "new"),

(r"A lasso fit sends the coefficient on \texttt{weekend} to exactly zero. What does that "
 r"establish?",
 ["Weekend has no relationship with the outcome.",
  "Weekend would also come out insignificant in an ordinary regression.",
  "Weekend did not earn its keep against this penalty, in this sample.",
  "Weekend is uncorrelated with the other predictors."],
 2, "A zero is the result of one penalty strength, this sample, and these other columns. Change "
    "any of the three and the variable can come back.", 4, "echo"),

(r"You cross-validate a model, then use the same folds to tune a cutoff, then report that "
 r"cross-validated error as your final number. What is wrong?",
 ["Nothing, since cross-validation holds out every row exactly once.",
  "The folds should have been re-randomized between the two steps.",
  "The cutoff was chosen using those folds, so the error is optimistic.",
  "Cross-validation cannot be used on a model with a tunable cutoff."],
 2, "Once the folds have been used to choose something, the score on them is a best-of rather "
    "than an estimate. Tuning is fine; reporting the tuned score as the final number is not. Keep "
    "a slice that nothing touched.", 4, "new"),
(r"For one new case the prediction interval is $[2.1, 9.8]$ and the confidence interval is "
 r"$[5.4, 6.1]$. The manager says the model is useless because the first is so wide. What do you "
 r"say?",
 ["They are right, since an interval that wide carries no useful information.",
  "The two measure different things; the wide one is the honest one for a case.",
  "The prediction interval should be recomputed at a lower confidence level.",
  "The model needs more predictors until the wide interval narrows."],
 1, "The narrow interval is about where the average sits, and more data shrinks it. The wide one "
    "includes the case-to-case variation, which is real and does not shrink. For a single case "
    "the wide interval is the truthful answer, not a defect.", 4, "new"),
(r"Two models have cross-validated errors of 0.84 and 0.83 days. The first uses 5 predictors, "
 r"the second 20. Which do you ship?",
 ["The 20-predictor model, since its cross-validated error came out lower.",
  "Neither: a gap that small means the comparison was done wrong.",
  "The 5-predictor model, since the gain is tiny and it costs less to live with.",
  "Whichever turns out to have the higher $R^2$ on the full data."],
 2, "A hundredth of a day is about fifteen minutes, against fifteen extra columns to collect, "
    "explain and maintain. When scores are this close the tie-breaker is everything other than "
    "the score.", 4, "new"),

(r"Forward selection picks \texttt{est\_boxes} first, and then never uses it again once "
 r"\texttt{volume} has entered. What does that tell you?",
 ["The two columns largely carry the same information.",
  "Boxes matter on their own but not in combination with anything.",
  "The search should be rerun backward to confirm the ordering.",
  "Boxes have a non-linear relationship with the outcome."],
 0, "A greedy search takes the best column available at each step. Once volume is in, anything "
    "that mostly repeats volume has nothing left to add. Being chosen first and then dropped is "
    "about overlap, not about importance.", 4, "new"),
(r"A residual plot shows a narrow band on the left widening steadily to the right. What is the "
 r"first thing to try?",
 ["Dropping the points on the right, which are the ones producing the wide residuals.",
  "Modeling the log of the outcome, since the spread grows with the prediction.",
  "Adding predictors, since the unexplained variation is still large.",
  "Nothing: least squares does not assume equal spread."],
 1, "Spread growing with the fitted value is the signature of an outcome that varies by a "
    "percentage rather than a fixed amount. Logging turns a percentage into a distance and "
    "usually flattens the band.", 5, "echo"),

(r"In a model of $\log(\text{price})$ on $\log(\text{weight})$, the coefficient on log weight is "
 r"$1.9$. What does that say?",
 ["An item 10\\% heavier costs about 19\\% more.",
  "An item one unit heavier costs about 1.9 units more.",
  "Weight explains about 190\\% of the variation in price.",
  "An item 10\\% heavier costs about 1.9\\% more."],
 0, "Both sides logged makes the coefficient a percentage for a percentage, which economists "
    "call an elasticity: 10\\% more weight buys about $10 \\times 1.9$, or 19\\% more price.",
 5, "echo"),

(r"Four repairs take 1, 2, 8 and 10 hours. A tree scores a cut by adding the squared distances "
 r"from each group's own average. What does it score for the cut that puts $\{1,2\}$ against "
 r"$\{8,10\}$?",
 ["0.0, since each group is predicted by its own average.",
  "2.5",
  "12.5",
  "41.0, the total spread around the overall average."],
 1, "The group averages are 1.5 and 9. The squared distances are $0.25 + 0.25$ on the left and "
    "$1 + 1$ on the right, so the score is 2.5. A tree tries every cut of every variable and "
    "keeps whichever total is smallest; 41.0 is what no split at all would leave.", 5, "new"),

(r"As a tree is allowed to go deeper, error on the rows it was fitted on keeps falling while "
 r"error on held-back rows falls, bottoms out, then rises. Which depth do you choose?",
 ["The deepest, since it fits the data best.",
  "The shallowest, since simpler models generalize more reliably.",
  "The depth where the two curves are closest together.",
  "The depth where the held-back error is lowest."],
 3, "The first curve can always be driven to zero by giving every row its own leaf, so it cannot "
    "choose anything. The held-out curve is the one measuring prediction on cases the tree has "
    "not seen.", 5, "echo"),

(r"A tree grown on repairs needing 0 to 8 parts is asked about a repair needing 15. What comes "
 r"back?",
 ["The average of the rows in the leaf holding the largest jobs it saw.",
  "An error, since the value is outside the range it was grown on.",
  "A prediction extended along the slope it found among the large jobs.",
  "The overall average, since the case matches no leaf."],
 0, "The case falls down the rightmost branch into an existing leaf and gets that leaf's average. "
    "A tree is flat outside its range: it will not run away the way a line does, but it will not "
    "use the extra size at all, and it gives no sign that it has run out of data.", 5, "new"),

(r"A tree splits on \texttt{supplier} inside the many-parts branch and not inside the few-parts "
 r"branch. What does that suggest adding to the regression?",
 ["A squared term in parts needed.",
  "An indicator for jobs that need an unusually large number of parts.",
  "The supplier variable on its own.",
  "An interaction between supplier and parts needed."],
 3, "A split that appears in one branch and not the other is the tree writing an interaction in "
    "its own notation: the effect of one variable depends on the value of another. The regression "
    "then puts a coefficient, an interval and a p-value on it.", 5, "new"),

(r"Your tree predicts better than your regression, and the owner asks how much the new supplier "
 r"saves per repair. What do you report?",
 ["The tree's prediction, since it has the lower held-out error.",
  "The regression's coefficient and interval, from a tree-informed model.",
  "The raw difference in average repair time between the two suppliers.",
  "Both numbers, and let the owner decide which to believe."],
 1, "A tree gives predictions, not effects: there is no supplier coefficient in it and no "
    "interval around one. The question asks for an effect holding other things fixed, which is "
    "what the regression is built to answer. Use the tree to find what belongs in the model.",
 5, "new"),

(r"A model of $\log(\text{days})$ gives a supplier coefficient of $-0.22$. What does that say on "
 r"the original scale?",
 ["Repairs run about 0.22 days shorter with the new supplier.",
  "The supplier accounts for about 22\\% of the variation in repair time.",
  "Repairs run about 20\\% shorter with the new supplier.",
  "Repairs run about 22 days shorter on the longest jobs."],
 2, "A coefficient on a logged outcome is a multiplicative change: $e^{-0.22} \\approx 0.80$, so "
    "about 20\\% shorter. The percentage applies to a quick repair and a slow one alike, which is "
    "what makes the log scale natural here.", 5, "new"),
]
