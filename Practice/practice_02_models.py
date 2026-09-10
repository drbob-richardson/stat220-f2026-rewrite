#!/usr/bin/env python3
"""Unit 2 practice, multiple choice with answers inline. STUDENT-FACING."""
from build_questions import build_mc

build_mc("Models", "A Map of Models",
"""Practice on what separates a probability model from an algorithmic one, what each lets you ask,
and how the job you were given narrows the choice. No computer needed.""",
[
("What makes something a probability model rather than an algorithmic one?",
 ["It uses probability somewhere in the fitting procedure.",
  "It writes down a distribution for the outcome, so the data has a stated origin.",
  "It produces predictions between 0 and 1.",
  "It was fit with maximum likelihood rather than least squares."],
 1,
 "A probability model says where the data came from: `mpg ~ Normal(b0 + b1*weight, sigma^2)`. "
 "That single sentence is what produces a likelihood, and the likelihood is what standard errors, "
 "p-values, confidence intervals and AIC are all built out of. Option D describes a fitting "
 "method, which is downstream of the distribution, not the thing that defines it."),

("Your colleague asks for the $p$-value on the most important variable in a random forest. What "
 "do you tell them?",
 ["It is in the model output, you just have to request it.",
  "You can get one by bootstrapping the forest 1,000 times.",
  "There isn't one. A forest states no distribution, so there is no likelihood and no $p$-value "
  "to report.",
  "The $p$-value is 1 divided by the number of trees."],
 2,
 "The quantity does not exist rather than being hidden. You can certainly resample to see how "
 "much an importance score wobbles, which is worth doing, but that is a stability check and not a "
 "test of a null hypothesis. There is no null hypothesis here to test."),

("You want to compare a linear regression against a gradient boosted model. Which comparison "
 "works?",
 ["AIC, since it is designed for comparing models.",
  "Adjusted $R^2$ on the training data.",
  "Cross-validated error, using the same folds for both.",
  "Neither can be compared, they are different kinds of model."],
 2,
 "AIC needs a likelihood, so boosting is not eligible. Out-of-sample error works for anything "
 "that can produce a prediction, which is why it is the general-purpose answer. The catch is that "
 "both models have to face identical folds, otherwise you are partly measuring which model got "
 "the easier split."),

("Which of these is a hyperparameter?",
 ["The slope on square footage in a rent model.",
  "The maximum depth of a decision tree.",
  "The residual standard deviation in a linear regression.",
  "The predicted value for a new house."],
 1,
 "A parameter comes out of fitting. A hyperparameter you set before fitting, and no amount of "
 "fitting will discover it. Depth, the lasso penalty, and $k$ in nearest neighbours are all "
 "choices. The honest way to make them is cross-validation on folds fixed in advance, not trying "
 "values until the result looks agreeable."),

("A listings site shows an estimated rent on every apartment page. Which interval belongs next to "
 "that number?",
 ["A confidence interval, because it is the standard thing to report.",
  "A prediction interval, because the user is asking about one specific apartment.",
  "Either one, they are the same width in large samples.",
  "Neither, intervals confuse users."],
 1,
 "A confidence interval covers the average rent for apartments like this one, and it keeps "
 "shrinking as you collect more data. A prediction interval covers the next single apartment, and "
 "it stays wide no matter how much data you have, because individual apartments genuinely differ. "
 "The user is standing in one apartment, so the second is the honest range."),

("You run a lasso on 200 candidate variables, 12 survive, and you report their coefficients with "
 "$p$-values. What is wrong?",
 ["Nothing, the lasso reports valid standard errors.",
  "The lasso shrinks every coefficient toward zero on purpose, so the printed values are not "
  "describing what they claim, and the variables were chosen by looking at the data.",
  "You should have used ridge instead, which does report valid $p$-values.",
  "The problem is only that 12 is too few survivors to be meaningful."],
 1,
 "Two things are broken at once. The penalty deliberately biases the coefficients, and the "
 "selection step means these 12 are the winners of a 200-way search, so their inference is "
 "computed as if the model had been chosen in advance when it was not. Use the lasso to screen, "
 "then refit an ordinary regression on the survivors if you need a defensible number, and say "
 "that you did."),

("A regulator will review every loan rejection your model produces. What does that fact alone "
 "tell you about the model choice?",
 ["Nothing, accuracy is what matters and you should pick the most accurate model.",
  "You need a probability model, because somebody will read a coefficient and you must be able "
  "to defend it.",
  "You need the largest possible training set.",
  "You should use a neural network, since they handle complex rules."],
 1,
 "The audience decided this before you looked at a single row. A boosted model might predict "
 "default better and still be unusable, because 'the algorithm said so' is not a defense. This "
 "is the fifth job from the unit, deployment, and it constrains the choice more tightly than "
 "accuracy does."),

("You have 300 rows and 80 candidate columns. What do you rule out immediately?",
 ["Linear regression, because 80 columns is too many for it.",
  "Flexible models like forests and boosting, because there is not enough data to pay for that "
  "much freedom.",
  "Nothing, all models work at any sample size.",
  "Cross-validation, because the folds would be too small."],
 1,
 "Flexibility is bought with sample size. With 300 rows and 80 columns a flexible model will fit "
 "the data beautifully and predict new cases badly, because most of what it is fitting is noise. "
 "Regularized regression is the sensible move here, used to cut 80 columns down to a handful "
 "chosen for a reason."),

("Your forest beats your regression by five points of cross-validated error. What should you do "
 "next?",
 ["Ship the forest, it won.",
  "Ship the regression, simpler is always better.",
  "Find out what the forest is using that the regression is not, then decide.",
  "Average the two models together."],
 2,
 "A gap that size is information rather than a verdict. Usually the forest has found an "
 "interaction or a threshold you can name, and once you put it in the regression the gap closes. "
 "Then you ship the model you can explain. If the gap does not close, you have learned that the "
 "structure is genuinely complicated, which is also worth knowing."),

("Two models are within one standard error of each other on cross-validation. What does that "
 "justify?",
 ["Reporting the one with the lower mean, since it is still better.",
  "Taking the simpler one, because on this data the two are not distinguishable.",
  "Collecting more data before deciding anything.",
  "Averaging their predictions."],
 1,
 "A cross-validated score is itself an estimate with noise around it. When two models fall inside "
 "that noise, choosing the lower mean is choosing on a coin flip. Taking the simpler model is a "
 "decision you can defend, and it usually buys you stability and a clearer story as well."),
])
