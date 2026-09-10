#!/usr/bin/env python3
"""Unit 5 practice, multiple choice with answers inline. STUDENT-FACING."""
from build_questions import build_mc

build_mc("Prediction", "Prediction and Its Uncertainty",
"""Practice on where prediction error comes from, which parts shrink with data and which do not,
and the ways a good model still produces a bad number. No computer needed.""",
[
("Which source of prediction error does collecting more data not reduce?",
 ["Uncertainty about the coefficients.",
  "The irreducible noise in the outcome itself.",
  "Error from having chosen the wrong model shape.",
  "Error from a small training set."],
 1,
 "Two identical houses sell for different prices. That spread is a property of the world, not of "
 "your sample, so no amount of data removes it. Coefficient uncertainty does shrink with $n$. "
 "Model-shape error shrinks only if you change the shape, and distribution shift is not about "
 "sample size at all."),

("Why is a prediction interval wider than a confidence interval at the same point?",
 ["Because it uses a higher confidence level.",
  "Because it covers where a single new case lands, which includes the noise around the mean, "
  "not just uncertainty about where the mean is.",
  "Because it accounts for outliers in the training data.",
  "They are the same width once the sample is large."],
 1,
 "The confidence interval covers the average outcome for cases like this one, and it shrinks "
 "toward zero width as $n$ grows. The prediction interval covers one actual case, so it carries "
 "the irreducible spread as well and stays wide forever. Quoting the first when someone asked "
 "about one case is the most common version of this mistake."),

("Your 90\\% prediction intervals contain the truth about 60\\% of the time on new data. What is "
 "wrong?",
 ["Nothing, 60\\% is close enough.",
  "The intervals are too narrow, so the model is overconfident.",
  "The intervals are too wide.",
  "The model has too much bias."],
 1,
 "Coverage below the nominal level means the stated uncertainty is smaller than the real "
 "uncertainty. Usually the interval was built from in-sample residuals, which are optimistic "
 "because the model was fitted to them, or the world has shifted since training. Sizing intervals "
 "from held-out errors fixes the first cause."),

("A model trained on 2019 data performs badly in 2021. Which layer of error is this?",
 ["Irreducible noise.",
  "Estimation uncertainty.",
  "Distribution shift.",
  "Overfitting."],
 2,
 "The relationship the model learned stopped holding. This is the layer that no amount of "
 "cross-validation catches, because cross-validation resamples within the same period and "
 "therefore assumes the world holds still. The only defenses are monitoring performance over time "
 "and knowing when a shift is plausible."),

("A model predicts house prices well for homes between 800 and 3{,}000 square feet. You ask it "
 "about a 12{,}000 square foot mansion. What is the danger?",
 ["The prediction will be too low.",
  "You are extrapolating, so the fitted shape is being trusted far outside the range where "
  "anything checked it.",
  "The confidence interval will be too narrow to compute.",
  "There is no danger, since the model is linear."],
 1,
 "Inside the data, a straight line can be a good approximation to a curve. Outside it, nothing "
 "constrained the fit and nothing tested it. The model will still return a number with an "
 "interval attached, and both will look as confident as any other output, which is what makes "
 "this dangerous rather than merely wrong."),

("Your worst-performing stores got an intervention and improved the next quarter. Your best stores "
 "got nothing and declined. What is the most likely explanation?",
 ["The intervention worked and the best stores became complacent.",
  "Regression to the mean, since both groups were selected on an extreme result that was partly "
  "luck.",
  "Seasonal effects.",
  "The measurements were wrong."],
 1,
 "Selecting on an extreme value selects partly for genuine performance and partly for luck, and "
 "luck does not repeat. Both groups drift toward the middle on their own. The untouched top group "
 "declining is the giveaway, because nothing was done to them and they moved anyway. Any "
 "evaluation of the intervention needs a control group."),

("How should you size a prediction interval in practice?",
 ["From the standard errors in the model summary.",
  "From the percentiles of errors on data the model was not fitted to.",
  "As twice the training residual standard deviation.",
  "From the range of the training outcomes."],
 1,
 "Held-out errors already include everything that goes wrong in practice: noise, coefficient "
 "uncertainty, and the ways your model shape is imperfect. Training residuals miss the last two, "
 "because the model was bent to fit those particular rows, so intervals built from them come out "
 "too narrow."),

("Your model reports 94\\% accuracy on a problem where 94\\% of cases are negative. What have you "
 "learned?",
 ["The model is performing well.",
  "Essentially nothing, since predicting the majority class every time achieves the same score.",
  "The model is overfitting.",
  "The test set was too small."],
 1,
 "Accuracy on an imbalanced problem is dominated by the majority class, so a model that has "
 "learned nothing at all matches it. You need measures that look at the rare class specifically, "
 "and you need to know what each kind of error costs, since those costs are rarely equal."),

("A stakeholder asks for one number and no interval. What is the right response?",
 ["Give the point estimate, since that is what was asked for.",
  "Give the point estimate together with a short statement of how wrong it could plausibly be.",
  "Refuse until they accept an interval.",
  "Give the interval only."],
 1,
 "A bare point estimate invites a decision that assumes it is exact. You do not need to teach "
 "anyone about intervals to fix this, you need one extra sentence: our estimate is 420, and "
 "realistically it could be anywhere from 380 to 465. That is the information they need to act, "
 "in a form nobody has to be trained to read."),

("Which of these would you check before trusting a model's prediction for a specific new case?",
 ["Only the model's overall out-of-sample error.",
  "Whether the case falls inside the range of the training data, and whether conditions have "
  "changed since training.",
  "Only whether the coefficients are significant.",
  "The training $R^2$."],
 1,
 "Overall error is an average across cases, and the case in front of you may be nothing like the "
 "average one. Two questions catch most single-prediction failures: is this case inside the "
 "region the model actually learned, and does the world still look like the world the model was "
 "trained on."),
])
