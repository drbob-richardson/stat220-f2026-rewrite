#!/usr/bin/env python3
"""Unit 3 practice, multiple choice with answers inline. STUDENT-FACING."""
from build_questions import build_mc

build_mc("Regression", "Linear Regression",
"""Practice on reading a fitted line, what a slope does and does not mean, and what happens to a
coefficient when the model around it changes. No computer needed.""",
[
("A model of house price on square footage returns a slope of 152. What does that number mean?",
 ["Houses are worth 152 times their square footage.",
  "Each additional square foot is associated with about \\$152 more in predicted price.",
  "Square footage explains 152\\% of the variation in price.",
  "The model is off by about \\$152 on a typical house."],
 1,
 "A slope is a rate: the change in the predicted outcome per one-unit change in the predictor, "
 "with the other predictors held fixed. It is meaningless until you attach both units, dollars "
 "per square foot here. Note the word associated. Whether an extra square foot would cause the "
 "price to rise is a different question this model cannot answer."),

("What does least squares actually minimize?",
 ["The number of points that fall off the line.",
  "The sum of the vertical distances from the points to the line.",
  "The sum of the squared vertical distances from the points to the line.",
  "The largest distance from any point to the line."],
 2,
 "Squaring is the whole reason a few far-off points can drag the line toward themselves. A point "
 "twice as far away contributes four times as much to the total being minimized, so outliers get "
 "a vote out of proportion to their number. That is worth remembering before you trust a fit on "
 "skewed data."),

("A regression reports $R^2 = 0.04$ and a slope with $p < 0.001$. Is the model useful?",
 ["No. A low $R^2$ means the relationship is not real.",
  "Yes. A tiny $p$-value means the model fits well.",
  "The relationship is real but explains almost none of the variation, so it depends entirely on "
  "what you wanted the model for.",
  "The two numbers contradict each other, so something was computed wrong."],
 2,
 "The two answer different questions and there is no contradiction. The $p$-value asks whether "
 "the slope could be zero, and with enough rows even a tiny slope clears that bar. $R^2$ asks how "
 "tightly the points hug the line. For explaining one effect, a real slope with a small $R^2$ can "
 "be exactly what you wanted. For predicting individual cases, it is nearly useless."),

("In `price ~ sqft + garage`, where `garage` is coded 1 or 0, the coefficient on `garage` is "
 "18{,}000. What does that say?",
 ["Garages cost about \\$18{,}000 to build.",
  "Among houses of the same square footage, having a garage is associated with about \\$18{,}000 "
  "more in predicted price.",
  "18{,}000 houses in the data have garages.",
  "The garage variable explains \\$18{,}000 of the variation."],
 1,
 "A 0/1 predictor shifts the line up or down without tilting it, so its coefficient is the gap "
 "between two parallel lines. The phrase holding square footage fixed is doing real work: without "
 "it you would be comparing garage houses to non-garage houses that also differ in size."),

("You add an interaction term `group * x` to a model that already had `group` and `x`. What "
 "changes about the coefficient on `x`?",
 ["Nothing, it still means the effect of $x$.",
  "It now means the effect of $x$ in the group coded 0, not the overall effect.",
  "It becomes the average effect of $x$ across both groups.",
  "It becomes uninterpretable."],
 1,
 "This is the most common misreading of an interaction model. With the interaction in, the two "
 "groups get different slopes: $b_1$ for the baseline group and $b_1 + b_3$ for the other. "
 "Quoting $b_1$ as the overall slope silently reports one group's answer as if it applied to "
 "everyone."),

("Fuel economy regressed on acceleration time gives a slope of $+1.20$. Add horsepower to the "
 "model and it becomes $-0.61$, with both $p$-values under $10^{-6}$. What happened?",
 ["One of the two models must be misspecified, and the second one is wrong.",
  "The sign flip means the data contains an error.",
  "Both are correct. They answer different questions, because the first absorbed the effect of "
  "the horsepower it left out.",
  "This is noise, since sign flips happen randomly."],
 2,
 "Leaving out a variable does not remove its influence, it redistributes it onto whatever stayed "
 "in. Slow cars have small engines, so acceleration was partly standing in for horsepower. The "
 "first model asks whether slower cars get better mileage across all cars, and yes. The second "
 "asks whether they do among cars of equal power, and no, because a car that is sluggish at fixed "
 "power is heavy."),

("Before trusting a fitted line, what should you look at first?",
 ["The $p$-value on the slope.",
  "The $R^2$.",
  "A plot of the data and of what the model missed.",
  "The number of observations."],
 2,
 "Every summary number assumes the shape you fitted is roughly the shape that is there. A plot "
 "catches a curve fitted with a straight line, a single point dragging the whole fit, and a "
 "variance that grows with $x$. None of those announce themselves in the coefficient table, and "
 "all of them change what the numbers mean."),

("A colleague reports that a regression on observational sales data shows advertising raises "
 "revenue by \\$2.10 per dollar spent. What is the first thing you say?",
 ["Ask for the $R^2$ to see if the model fits.",
  "Ask what else differs between the high-advertising and low-advertising periods, since the "
  "slope is a comparison and not an experiment.",
  "Ask whether the residuals were normally distributed.",
  "Congratulate them, since the return is clearly positive."],
 1,
 "Advertising spend is not assigned at random. It goes up before holidays, after good quarters, "
 "and when a new product launches, all of which also move revenue. The regression is doing what "
 "it was asked, comparing periods that differ in advertising and in everything correlated with "
 "it. Unit 6 gives you the vocabulary for this."),

("You fit `y ~ x` and the residual plot shows a clear U shape. What does that tell you?",
 ["The errors are not normally distributed, so you should transform $y$.",
  "The relationship bends, and a straight line is the wrong shape for it.",
  "There are outliers you should remove.",
  "The sample size is too small."],
 1,
 "Residuals should look like a shapeless cloud. Structure left in them is structure the model "
 "failed to capture, and a U specifically says the true relationship curves. Adding a squared "
 "term or transforming the predictor usually fixes it. This is not an outlier problem and it is "
 "not primarily about normality."),

("When does adding a predictor to a regression make a coefficient you already had more "
 "trustworthy, rather than less?",
 ["Whenever it raises $R^2$.",
  "When the new variable is a confounder, meaning it affects both the predictor of interest and "
  "the outcome.",
  "When the new variable is significant.",
  "Adding predictors always improves a model."],
 1,
 "Controlling for a genuine confounder removes a distortion that was sitting inside your "
 "coefficient. But adding variables is not free and not always right: controlling for something "
 "that sits on the causal path between your predictor and the outcome removes part of the effect "
 "you were trying to measure. $R^2$ rises either way, which is why it cannot be your guide."),
])
