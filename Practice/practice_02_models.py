#!/usr/bin/env python3
"""Unit 2 practice, multiple choice with answers inline. STUDENT-FACING.

Every option carries its own reasoning. The key is not systematically longest and
is spread over A, B, C and D.
"""
from build_questions import build_mc

build_mc("Models", "A Map of Models",
"""Practice on what separates a probability model from a non-probability one, what each lets you
ask, and how the job you were given narrows the choice. No computer needed.""",
[
("What makes something a probability model rather than a non-probability one?",
 ["It states a distribution the outcome is drawn from, which is what produces a likelihood.",
  "It uses probability somewhere inside the fitting procedure rather than plain arithmetic.",
  "Its predictions are guaranteed to fall between 0 and 1, so they can be read as chances.",
  "It was fitted by maximum likelihood rather than by minimizing squared error directly."],
 0,
 "A probability model commits to where the data came from: normal around a line, Bernoulli with "
 "some probability, Poisson with some rate. That commitment produces a likelihood, and the "
 "likelihood is what standard errors, p-values, confidence intervals and AIC are all made of. "
 "Option D names a fitting method, which comes after the distribution rather than instead of it."),

("A colleague asks for the p-value on the most important variable in a random forest.",
 ["It is in the model output, and you just have to ask the library to print it for you.",
  "Bootstrap the forest a thousand times and read the p-value off the spread of the importances.",
  "There isn't one, because the forest never states a distribution for the outcome.",
  "It works out to roughly one divided by the number of trees you grew in the forest."],
 2,
 "No distribution means no likelihood, and a p-value would have nothing to be computed from. The "
 "quantity does not exist rather than being hidden somewhere. Resampling will tell you how much "
 "an importance score wobbles, which is worth knowing, but that is a stability check and not a "
 "test of any hypothesis."),

("You want to compare a linear regression against a gradient boosted model. Which comparison "
 "actually works?",
 ["Adjusted R-squared on the training data, which already corrects for the number of predictors.",
  "Cross-validated error, provided both models are scored on exactly the same folds.",
  "AIC, since it exists precisely to compare models against each other on the same data.",
  "Neither, because the two are different kinds of model and cannot be put on one scale."],
 1,
 "AIC needs a likelihood, so boosting is not eligible for it. Out-of-sample error works on "
 "anything that produces a prediction, which is why it is the general-purpose answer. The "
 "condition in the second half matters: both models must face identical folds, or you are partly "
 "measuring which one drew the easier split."),

("Which of these does fitting the model decide, rather than you deciding it beforehand?",
 ["How deep the tree is allowed to grow before it has to stop splitting.",
  "How many folds to divide the data into when you cross-validate.",
  "Where the tree puts its split points, and what value it predicts inside each one.",
  "How large a penalty to place on the size of the coefficients."],
 2,
 "Fitting settles the parts the data has an opinion about: split points, slopes, weights. Depth, "
 "fold count and penalty size are settings you fix in advance, and no amount of fitting will "
 "choose them for you. Unit 4 covers how to make those choices without fooling yourself."),

("Your outcome is a yes or no. What does that fact by itself rule out?",
 ["Random forests, which are built for numeric outcomes and cannot handle categories.",
  "Boosting, which works on counts and continuous outcomes but not on binary ones.",
  "Nothing at all, since every model on the menu can take any type of outcome you hand it.",
  "Linear regression, which has no way to keep its predictions inside 0 and 1."],
 3,
 "The outcome type eliminates probability models one at a time, and eliminates nothing on the "
 "other side, because trees, forests and boosting all have a classification mode. So when you "
 "decide against a forest, the reason is never the outcome. It is that somebody needs to read a "
 "number out of the model."),

("A lasso keeps 12 of 200 candidate variables. You report those coefficients with their p-values.",
 ["Nothing is wrong, since the lasso reports valid standard errors alongside its coefficients.",
  "They were shrunk toward zero on purpose, and the 12 were picked by looking at the data.",
  "Ridge would have been the correct choice here, since it keeps every variable in the model.",
  "Twelve survivors out of 200 is too few for the resulting model to be worth reporting at all."],
 1,
 "Two things break at once. The penalty biases every coefficient toward zero by design, so the "
 "printed numbers are not estimating what they appear to. And these 12 won a 200-way search while "
 "the inference is computed as though the model had been settled in advance. Treat what survives "
 "as a shortlist worth investigating."),

("A regulator will review every loan rejection your model produces. What does that fact alone "
 "tell you?",
 ["You need a probability model, because somebody will read a coefficient and ask you to defend "
  "it.",
  "You need as much training data as you can gather, since regulators expect large samples.",
  "Accuracy is what matters most here, so you should pick whichever model predicts best.",
  "A neural network is the right choice, since lending rules are complicated and interacting."],
 0,
 "The audience settled this before anyone looked at a row of data. A boosted model might predict "
 "default better and still be unusable, because the algorithm said so is not a defence. This is "
 "the deployment job, and it constrains the choice more tightly than accuracy does."),

("You have 300 rows and 80 candidate columns. What should you rule out straight away?",
 ["Cross-validation, since splitting 300 rows five ways leaves folds too small to score on.",
  "Nothing yet, since any model can be fitted at any sample size and then judged on its error.",
  "Forests and boosting, since 300 rows cannot pay for that much flexibility.",
  "Linear regression, which cannot be fitted at all once you have more columns than you want."],
 2,
 "Flexibility is bought with sample size. At 300 rows and 80 columns a flexible model fits "
 "beautifully and predicts badly, because most of what it is fitting is noise. Regularized "
 "regression is the sensible move, used to cut 80 columns down to a few you can defend."),

("Your forest beats your regression by five points of cross-validated error. What do you do next?",
 ["Ship the forest, since it won the comparison on the measure you agreed to use.",
  "Average the two models together, which usually beats either one on its own.",
  "Ship the regression anyway, because a simpler model is the safer choice in every case.",
  "Find out what the forest is using that the regression is missing."],
 3,
 "A gap that size is information rather than a verdict. Usually the forest has found an "
 "interaction or a threshold you can name, and once you add it to the regression the gap closes "
 "and you ship the model you can explain. If it does not close, you have learned the structure is "
 "genuinely complicated, which is also worth knowing."),

("A depth-10 tree scores 0.44 training error and 13.19 cross-validated. A straight line scores "
 "11.59 and 12.23. Which model is better?",
 ["The tree, since 0.44 is by a wide margin the lowest error anywhere on the table.",
  "The line, because the column that counts is the one scored on rows the model never saw.",
  "Neither, since a tree and a line are different kinds of model and cannot be compared.",
  "The tree, since having more flexibility available can only help once it is tuned properly."],
 1,
 "Training error measures how well a model reproduces rows it has already seen, and a flexible "
 "model drives that toward zero by memorizing. On the honest column the tree loses to a straight "
 "line. Both sat on the same rows and were scored the same way, which is what makes them "
 "comparable at all."),

("A model predicting daily revenue reports a cross-validated MSE of 140. What do you tell the "
 "owner?",
 ["That it explains about 140 percent of the day-to-day variation in what the shop takes.",
  "That it is off by roughly 140 dollars on a typical day, which is the meaning of the number.",
  "That MSE is an internal diagnostic and cannot sensibly be translated into dollars at all.",
  "That it is off by roughly 12 dollars on a typical day."],
 3,
 "MSE is in squared units, so 140 means 140 squared dollars, which nobody can picture. The square "
 "root is about 12, which is back in dollars and is a sentence the owner can act on. Quote the "
 "RMSE to people, and keep the MSE for ranking models against each other."),

("A model has to run nightly for two years, and any single output may be queried. What does that "
 "push you toward?",
 ["Whichever model scored best in testing, since that is the only objective criterion available.",
  "The most flexible model your data can support, retuned each month as new data arrives.",
  "The simplest model that clears the accuracy bar you actually need.",
  "A model with several tuned settings, so it can be adjusted as conditions change over time."],
 2,
 "Accuracy is one requirement among several, and this job is mostly the others. A model with six "
 "tuned settings is six things that can drift as the data moves, and each is something you would "
 "have to explain. Choosing simplicity on purpose reads as judgement. Defaulting to it because "
 "you never tried anything else does not."),
])
