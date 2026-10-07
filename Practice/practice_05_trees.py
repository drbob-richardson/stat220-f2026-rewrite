#!/usr/bin/env python3
"""Unit 5 practice, multiple choice with answers inline. STUDENT-FACING."""
from build_questions import build_mc

build_mc("Trees", "When a Line Is Not Enough",
"""Practice on reading a residual plot, fixing what it shows, growing and reading a decision
tree, and using a tree to improve a regression. No computer needed.""",
[
("A residual plot shows a narrow band on the left that widens steadily to the right. What is the "
 "first thing to try?",
 ["Drop the rows on the right, since those are the ones producing the wide residuals.",
  "Take the log of the outcome, since the spread is growing with the prediction.",
  "Add more predictors, since the unexplained variation is clearly still large.",
  "Nothing, since least squares does not require the residuals to have equal spread."],
 1,
 "Spread that grows with the fitted value is the signature of an outcome that varies by a "
 "percentage rather than by a fixed amount. Logging the outcome turns a percentage into a "
 "distance, and the band usually flattens out. Least squares still gives sensible coefficients "
 "here, but every interval and p-value it reports is built on the equal-spread assumption."),

("A residual plot shows a clear arc: negative at both ends and positive in the middle. What does "
 "that mean?",
 ["The outcome has outliers at both extremes of the predictor's range.",
  "The predictor and the outcome are uncorrelated over most of the range.",
  "The model has too many predictors and is fitting noise at the edges.",
  "The relationship bends, and a straight line cannot follow the bend."],
 3,
 "A line can only go up or down at a constant rate. If the truth curves, the line sits above the "
 "data in the middle and below it at the ends, or the reverse, and the residuals trace out the "
 "shape the line could not follow. The fixes are a squared term or a log on the predictor."),

("In a model of $\\log(\\text{rent})$ on $\\log(\\text{size})$, the coefficient on log size is "
 "0.26. What does that say?",
 ["An apartment 10\\% larger rents for about 2.6\\% more, everything else held fixed.",
  "An apartment 10 square feet larger rents for about 0.26\\% more.",
  "An apartment one square foot larger rents for about 26 rupees more.",
  "Size explains about 26\\% of the variation in rent across these listings."],
 0,
 "Both sides are logged, so the coefficient is a percentage for a percentage, which economists "
 "call an elasticity. Ten percent more size buys about $10 \\times 0.26$, or 2.6 percent more "
 "rent. Reporting it in rupees per square foot is the usual mistake: once both sides are "
 "logged, the coefficient is not in the units of the outcome any more."),

("Your outcome is a count of complaints, and many stores had zero. A colleague suggests "
 "$\\log(y+1)$ because $\\log(y)$ returned an error. What should you say?",
 ["Use it, since adding one is the standard correction for counts that include zero.",
  "Use it, since the plus one is negligible once the counts are large enough.",
  "The plus one was chosen to stop an error, not because it fits the problem.",
  "Drop the stores with zero complaints and log the rest of the data as usual."],
 2,
 "There is nothing wrong with the arithmetic, but the constant is doing real work on the small "
 "counts and nobody chose its value for a reason. Counts with zeros usually want a model built "
 "for counts. Dropping the zeros is worse, since those stores are often the interesting ones."),

("What does a single split in a regression tree actually do?",
 ["It fits a separate straight line on each side of the cut point.",
  "It cuts the rows into two groups and predicts each group's average.",
  "It tests whether the two groups differ, and keeps the split if $p < 0.05$.",
  "It finds the point where the outcome changes direction most sharply."],
 1,
 "A split chooses one variable and one cut point, and the prediction on each side is just the "
 "average of the rows that land there. The machine tries every variable and every cut and keeps "
 "whichever pair leaves the two groups as alike inside as possible. There is no test and no "
 "line, which is why a tree's prediction is a staircase rather than a slope."),

("As you let a tree go deeper, the error on the rows it was fitted on keeps falling while the "
 "error on held-back rows falls, bottoms out, and rises. Which depth do you pick?",
 ["The deepest one, since it has the lowest error on the rows it was fitted on.",
  "The shallowest one, since simpler models always generalize more reliably.",
  "The depth where the two curves are closest together.",
  "The depth where the held-back error is at its lowest."],
 3,
 "The first curve can always be driven to zero by giving every row its own leaf, so it cannot "
 "choose anything. The held-back error is the one measuring prediction on rows the tree has "
 "never seen, and its minimum is the honest answer. The gap between the curves tells you how "
 "much the tree is memorizing, but closing the gap is not the goal."),

("A tree was grown on houses from 800 to 4,000 square feet. You ask it to predict for a 9,000 "
 "square foot house. What comes back?",
 ["The average of the largest houses it saw, with no adjustment for the extra size.",
  "An error, since the value falls outside the range the tree was grown on.",
  "A prediction extended along the slope the tree found among the large houses.",
  "The overall average of all the houses, since the case matches no leaf."],
 0,
 "The case falls down the rightmost branch and lands in the leaf holding the largest houses in "
 "the training data, and that leaf's prediction is its average. A tree is flat outside its range "
 "by construction, so it will not run away the way a line does, but it also will not use the "
 "extra size at all. Neither answer is trustworthy; the honest response is that the question is "
 "outside what the data can speak to."),

("A tree never splits on `square_footage`, which you know matters. What does that tell you?",
 ["Square footage has no relationship with the outcome in this dataset.",
  "The tree was grown too shallow to reach the variable at all.",
  "Some other variable it did split on may be carrying the same information.",
  "The variable should be dropped from the regression model as well."],
 2,
 "Trees are greedy: once bedrooms are in, a variable that largely repeats bedrooms has nothing "
 "left to add and will never be chosen. Absence from the tree is a reason to look at the "
 "correlations, not a verdict on the variable. It is a candidate for dropping only after you "
 "have checked what it overlaps with."),

("A tree splits on `slope` inside the large-lot branch and not inside the small-lot branch. What "
 "should you add to the regression?",
 ["A squared term in lot size, since the effect of size is clearly not constant.",
  "An indicator for large lots, since that is where the second split appeared.",
  "The slope variable on its own, since the tree has shown that it matters.",
  "An interaction between slope and lot size, since slope matters only on big lots."],
 3,
 "A split that shows up in one branch and not the other is the tree writing an interaction in "
 "its own notation: the effect of one variable depends on the value of another. Adding slope "
 "alone forces it to have the same effect everywhere, which is exactly what the tree said is "
 "false. The regression then gives the interaction a coefficient, an interval, and a p-value."),

("Your tree predicts better than your regression. The client wants to know how much a gated "
 "property adds to the time a job takes. What do you report?",
 ["The regression's coefficient on gated, with its interval, from a tree-informed model.",
  "The tree's prediction, since it is the model with the better held-out error.",
  "The difference in average time between gated and ungated jobs in the raw data.",
  "Both numbers, side by side, and let the client decide which one they prefer."],
 0,
 "A tree gives predictions, not effects: it has no coefficient for gated and no interval around "
 "one. The question asked is about an effect holding other things fixed, which is what the "
 "regression is built to answer. Use the tree as a scout to find what belongs in the model, then "
 "let the regression say how much and how sure. The raw difference ignores everything else that "
 "differs between gated and ungated properties."),
])
