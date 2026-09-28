#!/usr/bin/env python3
"""Unit 4 practice, multiple choice with answers inline. STUDENT-FACING."""
from build_questions import build_mc

build_mc("Prediction", "Prediction and Choosing Predictors",
"""Practice on predicting a new case, putting the right interval on it, measuring error honestly,
and deciding which predictors belong. No computer needed.""",
[
("A dispatcher asks how many hours to block on the schedule for one specific move. Which interval "
 "should you give them?",
 ["The confidence interval, since it is the interval the software reports first.",
  "The prediction interval, because the question is about one job rather than an average.",
  "Either one, since both are built from the same fitted model and the same data.",
  "The confidence interval, because a narrower interval is a more useful answer."],
 1,
 "The confidence interval describes where the average outcome sits for jobs like this one. The "
 "dispatcher is scheduling a single crew on a single Tuesday, so the job-to-job variation is "
 "part of their question. That variation is exactly what the prediction interval includes and "
 "the confidence interval leaves out."),

("You collect ten times as much data and refit. What happens to the two intervals?",
 ["Both shrink toward zero width at about the same rate.",
  "Both stay about the same, since the model has not changed.",
  "The confidence interval shrinks, and the prediction interval stays wide.",
  "The prediction interval shrinks, and the confidence interval stays wide."],
 2,
 "More data pins down where the line sits, so the confidence interval keeps narrowing. The "
 "prediction interval also contains the spread of individual cases around the line, and no "
 "amount of data removes that. It settles toward the residual spread and stops."),

("Why is the error a model reports on the rows it was fitted on too small?",
 ["Because the rows used for fitting are cleaner than the ones collected later.",
  "Because the software reports the error before the fitting has converged.",
  "Because the coefficients were chosen to make the residuals small on those rows.",
  "Because any sample is smaller than the population that it was drawn from."],
 2,
 "Fitting picks the coefficients that minimize the residuals for the rows in front of it, so "
 "measuring on those same rows grades the model on the work it optimized. A new job gets no "
 "such treatment. The gap between the two widens as the model gains flexibility."),

("What does 5-fold cross-validation give you that a single train/test split does not?",
 ["An average over five splits, so the estimate rests less on a lucky division.",
  "A guarantee that the model will perform the same way on data collected later.",
  "A larger training set, which by itself produces a more accurate final model.",
  "A p-value for whether the model predicts better than nothing at all."],
 0,
 "One split gives one number, and that number moves depending on which rows happened to land in "
 "the test set. Five folds average over that, and every row is held out exactly once. It is a "
 "steadier estimate of the same quantity, not a guarantee about the future."),

("You try twenty models, keep the one with the lowest held-out error, and report that error as "
 "your final number. What is wrong with doing that?",
 ["Nothing at all, since the error was measured on data held out from the fitting.",
  "Twenty models is far too many to compare against any one held-out sample.",
  "It is the best of twenty, so it flatters the model the way training error does.",
  "Held-out error is only valid when the models are nested inside each other."],
 2,
 "Choosing with held-out data is fine and normal. Reporting the winner's score as your estimate "
 "is not, because you picked the model that did best on those particular rows. If the choice "
 "mattered, keep a slice you never touched, or say plainly that the number came from the same "
 "data you chose with."),

("A model has an $R^2$ of 0.98 on its own rows and a typical error four times larger on new "
 "data. What is going on?",
 ["The model is underfitting, and adding more predictors would close the gap.",
  "The newer data must have been collected or recorded incorrectly.",
  "This is ordinary, since the two numbers describe the same quantity.",
  "The model is overfitting: it followed noise in the rows it was fitted on."],
 3,
 "A nearly perfect fit on its own rows next to poor performance on new ones is the signature of "
 "overfitting. The model has enough flexibility to bend around individual points, and those "
 "bends do not repeat in the next sample. Fewer predictors or less flexibility is the fix."),

("The same ladder of models is fitted twice, once on 60 jobs and once on 600. On 60 the best "
 "choice is five plain predictors; on 600 it is those five plus their squared terms. Why?",
 ["The larger sample has less noise in it, so curvature becomes easier to see.",
  "More data supports more complexity, so the squared terms become affordable.",
  "The relationship genuinely changes shape once you collect more of the data.",
  "The smaller sample must have been drawn in some unrepresentative way."],
 1,
 "The truth is the same in both: the relationship really does bend. With 60 jobs there is not "
 "enough data to estimate the extra coefficients well, so the squared terms cost more in wobble "
 "than they return in shape. With 600 the same terms pay for themselves. How much complexity "
 "you can afford is a fact about your sample size, not only about the world."),

("Polynomial regression fits $y$ on $x$, $x^2$, and $x^3$. Is it still linear regression?",
 ["No, because the curve that it fits is no longer a straight line.",
  "Yes, because it is linear in the coefficients, and powers are just columns.",
  "No, because least squares no longer applies once powers are involved.",
  "Yes, but only when the degree of the polynomial is 2 or lower."],
 1,
 "Linear regression means linear in the coefficients, not in the predictors. Each power is "
 "computed and handed to the same fitting procedure as an ordinary column, and least squares "
 "neither knows nor cares that one column is the square of another."),

("With 5 predictors, how many terms does a full second-order model have, counting main effects, "
 "squares, and pairwise products?",
 ["10, which is the five main effects plus their five squares.",
  "15, which is the five main effects plus the ten products.",
  "25, which is the five predictors multiplied by five again.",
  "20, five main effects, five squares, and ten products."],
 3,
 "Five main effects, five squares, and ten pairwise products, which is 5 choose 2. Each is an "
 "ordinary column. The count matters because twenty coefficients estimated from a small sample "
 "is a lot of flexibility, and that is where the fit starts chasing noise."),

("Adding three useless columns raises $R^2$ from 0.9233 to 0.9246. What does that tell you?",
 ["The columns carry a small amount of real information worth keeping.",
  "Nothing useful, because $R^2$ cannot fall when you add a column.",
  "The model was underfitting before, so the additions helped.",
  "The sample is too small for $R^2$ to be computed reliably."],
 1,
 "$R^2$ never decreases when you add a predictor, even one made of random numbers, because the "
 "fit can always use it a little. That is why the rise tells you nothing on its own. Adjusted "
 "$R^2$, AIC, BIC, or cross-validated error will all charge you for the extra columns."),

("A colleague ran stepwise selection over 65 columns, kept the 11 with $p < 0.05$, and reports "
 "that every predictor in the final model is significant. What is the problem?",
 ["Nothing at all, as long as every p-value in the final model is below 0.05.",
  "The p-values should have been computed before the final model was fitted.",
  "Each p-value assumes the variable was chosen in advance, and these won a search.",
  "Eleven predictors is too many for a model of this kind to be trustworthy."],
 2,
 "A p-value answers how often a result this strong would appear if the variable did nothing, and "
 "that question assumes you picked the variable without looking. Picking the best of 65 "
 "guarantees extreme-looking results, so the reported values understate how easily noise could "
 "produce them."),

("What is the practical difference between ridge and lasso?",
 ["Ridge shrinks coefficients toward zero but keeps every predictor; lasso can zero them out.",
  "Ridge works on correlated predictors, while lasso requires them to be independent.",
  "Ridge is for prediction problems, while lasso is only for explaining an effect.",
  "Ridge needs the predictors scaled first, and lasso can be run on the raw columns."],
 0,
 "Both add a charge for the size of the coefficients, and both need the predictors on a common "
 "scale first. The difference is the shape of the charge: lasso can drive a coefficient to "
 "exactly zero, which drops the variable, while ridge shrinks everything and keeps it. When two "
 "predictors carry nearly the same information, ridge tends to split the credit between them."),

("A lasso fit sends the coefficient on `weekend` to exactly zero. What does that establish?",
 ["That weekends have no effect at all on how long one of these jobs takes.",
  "That an ordinary regression would also put the weekend coefficient at zero.",
  "That weekends are unrelated to each of the other predictors in the model.",
  "That the column did not earn its keep against the penalty, beside these others."],
 3,
 "A zero from lasso is a decision, not a finding. Change the penalty, the sample, or the other "
 "columns in the model and the same variable can come back. It says the column was not worth "
 "its cost here, which is a much narrower claim than having no effect."),

("Every predictor for a new case is inside its own range in the data. Is the prediction safe?",
 ["Not necessarily, since the combination of values may never have occurred.",
  "Yes, that check is exactly what guards against extrapolation.",
  "Yes, as long as the model's $R^2$ is reasonably high.",
  "Not necessarily, but only if the predictors are uncorrelated with each other."],
 0,
 "A 900 cubic foot move is ordinary and 35 boxes is ordinary, but if no job has ever had both, "
 "the model is filling that gap with nothing but the shape you assumed. Correlated predictors "
 "make this worse: the pairs off the diagonal are empty, and a one-variable check never sees it."),

("You are choosing between a model with 5 predictors and one with 20. Their cross-validated "
 "errors are 0.84 and 0.83 hours. Which do you ship?",
 ["The 20-predictor model, since it came out with the lower error of the two.",
  "Neither, since a difference that small means the comparison was done wrong.",
  "The 5-predictor model, since the gain is tiny and it costs less to live with.",
  "Whichever of the two turns out to have the higher $R^2$ on the full data."],
 2,
 "A hundredth of an hour is thirty-six seconds, against fifteen extra columns to collect, "
 "explain, and maintain. When the scores are this close the tie-breaker is everything other than "
 "the score. A smaller model is also less exposed to a column that changes meaning next year."),
])
