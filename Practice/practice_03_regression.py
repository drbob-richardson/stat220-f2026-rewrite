#!/usr/bin/env python3
"""Unit 3 practice, multiple choice with answers inline. STUDENT-FACING."""
from build_questions import build_mc

build_mc("Regression", "Linear Regression",
"""Practice on reading a fitted line, what a slope does and does not mean, and what happens to a
coefficient when the model around it changes. No computer needed.""",
[
("A model of house price on square footage returns a slope of 152. What does that number mean?",
 ["Each additional square foot is associated with about \\$152 more in predicted price.",
  "A house is worth about 152 times whatever its square footage happens to be.",
  "Square footage accounts for about 152\\% of the variation in the price of a house.",
  "The model's prediction for a typical house misses the actual price by about \\$152."],
 0,
 "A slope is a rate: the change in the predicted outcome per one-unit change in the predictor. It "
 "means nothing until you attach both units, dollars per square foot here. Note the word "
 "associated. Whether an extra square foot would cause the price to rise is a different question, "
 "and this model cannot answer it."),

("What does least squares actually minimize?",
 ["The number of points that fall some distance off the fitted line.",
  "The sum of the vertical distances from the points to the fitted line.",
  "The largest vertical distance between any single point and the fitted line.",
  "The sum of the squared vertical distances from the points to the line."],
 3,
 "Squaring is the reason a few far-off points can drag the line toward themselves. A point twice "
 "as far away contributes four times as much to the total being minimized, so outliers get a vote "
 "out of proportion to their number. Worth remembering before you trust a fit on skewed data."),

("A regression reports $R^2 = 0.04$ and a slope with $p < 0.001$. Is the model any good?",
 ["No, because an $R^2$ that low means the relationship is not a real one.",
  "The relationship is real but explains very little, so it depends what you wanted it for.",
  "Yes, because a $p$-value that small is evidence the line fits the points closely.",
  "Neither number can be right, since the two of them directly contradict each other."],
 1,
 "The two numbers answer different questions and there is no contradiction. The $p$-value asks "
 "whether the slope could be zero, and with enough rows even a tiny slope clears that bar. $R^2$ "
 "asks how tightly the points hug the line. For explaining one effect, a real slope with a small "
 "$R^2$ can be exactly what you wanted. For predicting individual cases, it is nearly useless."),

("In `price ~ sqft + garage`, where `garage` is 1 or 0, the coefficient on `garage` is 18,000. "
 "What does that say?",
 ["Roughly 18,000 of the houses in this data were sold with a garage attached.",
  "The garage variable accounts for about \\$18,000 of the total variation in price.",
  "Among houses of the same size, a garage is associated with about \\$18,000 more in price.",
  "A garage costs a builder in this market about \\$18,000 to add to a house of ordinary size."],
 2,
 "A 0/1 predictor shifts the line up or down without tilting it, so its coefficient is the gap "
 "between two parallel lines. The phrase holding square footage fixed is doing real work here. "
 "Without it you would be comparing garage houses to non-garage houses that also differ in size."),

("A regression uses region with four levels, and the output lists coefficients for only three of "
 "them. What happened to the fourth?",
 ["It is the baseline, folded into the intercept, and the others compare to it.",
  "The software dropped it because it was not statistically significant at the usual 5\\% level.",
  "Its coefficient is zero, meaning that region has no relationship with the outcome at all.",
  "It was collinear with the others, so the model could not estimate anything for it."],
 0,
 "One level always sits inside the intercept, and every other coefficient is read against it. If "
 "you forget which level is the baseline, every interpretation you give is wrong. Changing the "
 "baseline changes all the numbers without changing the model or a single prediction."),

("You add an interaction `group * x` to a model that already had `group` and `x`. What happens to "
 "the coefficient on `x`?",
 ["It becomes the average of the two groups' slopes, weighted by their sizes.",
  "Nothing changes, since it still reports the effect of $x$ across the whole sample.",
  "It becomes the effect of $x$ within the group coded 0, not an overall effect.",
  "It stops being interpretable on its own, so nobody should report it at all."],
 2,
 "This is the most common misreading of an interaction model. With the interaction in, the two "
 "groups get different slopes: $b_1$ for the baseline group and $b_1 + b_3$ for the other. "
 "Quoting $b_1$ as the overall slope reports one group's answer as if it applied to everyone."),

("Fuel economy on acceleration time gives a slope of $+1.20$. Add horsepower and it becomes "
 "$-0.61$, both with $p$-values under $10^{-6}$. What happened?",
 ["The sign flip is a sign that something in the data was recorded incorrectly.",
  "Sign flips like this happen by chance often enough that it is probably noise.",
  "One of the two models has to be wrong, and it is the second one with the extra variable.",
  "Both are right, about different questions. The first absorbed the horsepower it left out."],
 3,
 "Leaving out a variable does not remove its influence, it redistributes it onto whatever stayed "
 "in. Slow cars have small engines, so acceleration was partly standing in for horsepower. The "
 "first model asks whether slower cars get better mileage across all cars, and they do. The "
 "second asks whether they do among cars of equal power, and there the answer is no."),

("A fitted line on homes of 800 to 3,000 square feet is used to price a 12,000 square foot "
 "mansion. What is wrong with that?",
 ["Nothing, as long as the slope was statistically significant in the original fit.",
  "The prediction is an extrapolation, and nothing in the data says the line continues out there.",
  "The intercept becomes meaningless once you predict that far from the center of the data.",
  "The error would be fixed by refitting the model with the mansion included in the data."],
 1,
 "A line describes the relationship inside the range you observed. Out past the edge of the data "
 "the model still returns a number, confidently and with no warning, and that number rests on an "
 "assumption nobody checked. The honest answer is that this sale is outside what the data covers."),

("Before trusting a fitted line, what should you look at first?",
 ["The $p$-value on the slope, which tells you whether the relationship is real.",
  "The number of observations, since a large sample makes the other numbers dependable.",
  "The $R^2$, which summarizes how much of the outcome the model has accounted for.",
  "A plot of the data, and a plot of what the model missed."],
 3,
 "Every summary number assumes the shape you fitted is roughly the shape that is there. A plot "
 "catches a curve fitted with a straight line, a single point dragging the whole fit, and spread "
 "that grows with $x$. None of those announce themselves in the coefficient table, and each one "
 "changes what the numbers mean."),

("You fit `y ~ x` and the residual plot shows a clear U shape. What is that telling you?",
 ["The relationship bends, so a straight line is the wrong shape for it.",
  "The residuals are not normally distributed, which calls for transforming $y$.",
  "There are outliers at both ends that ought to be dropped before refitting.",
  "The sample is too small for the standard errors to be trustworthy."],
 0,
 "Residuals should look like a shapeless cloud. Structure left in them is structure the model "
 "failed to capture, and a U says specifically that the true relationship curves. Adding a "
 "squared term or transforming the predictor usually fixes it. This is not an outlier problem, "
 "and it is not mainly about normality."),

("A colleague reports that on observational sales data, advertising raises revenue by \\$2.10 per "
 "dollar spent. What is the first thing you say?",
 ["Ask for the $R^2$, since a low one would mean the effect is not worth acting on.",
  "Ask whether the residuals were normally distributed before trusting the coefficient.",
  "Congratulate them, since a return above a dollar for every dollar spent is clearly good news.",
  "Ask what else differs between high and low advertising periods, since this is not an "
  "experiment."],
 3,
 "Advertising spend is not assigned at random. It rises before holidays, after good quarters, and "
 "when a product launches, all of which move revenue too. The regression is doing exactly what it "
 "was asked, comparing periods that differ in advertising and in everything that travels with it. "
 "Unit 6 gives you the vocabulary for this."),

("When does adding a predictor make a coefficient you already had more trustworthy rather than "
 "less?",
 ["Whenever the addition raises $R^2$, which means the model improved.",
  "When the new variable is a confounder, driving both the predictor and the outcome.",
  "Whenever the new variable turns out to be statistically significant in the larger model.",
  "Almost always, since a model with more information in it is the better model."],
 1,
 "Controlling for a genuine confounder removes a distortion that was sitting inside your "
 "coefficient. But adding variables is not free. Controlling for something on the causal path "
 "between your predictor and the outcome removes part of the very effect you were trying to "
 "measure. $R^2$ goes up either way, which is why it cannot be your guide."),
])
