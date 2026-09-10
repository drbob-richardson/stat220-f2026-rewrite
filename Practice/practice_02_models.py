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
 "choices you make before the data gets a say. How to make them without fooling yourself is "
 "Unit 4."),

("A hospital dataset has a yes/no outcome. Which of these does that fact rule out?",
 ["Random forests, since they are built for numeric outcomes.",
  "Linear regression, because it cannot keep its predictions between 0 and 1.",
  "Gradient boosting, which only works on counts.",
  "Nothing. Every model can handle any outcome type."],
 1,
 "The type of the outcome rules out probability models, one at a time: linear regression genuinely "
 "cannot take a yes/no, and Poisson genuinely cannot take a continuous number. It rules out nothing "
 "on the algorithmic side, because trees, forests and boosting all have a classification mode. So "
 "when you decide against a forest, the reason is never the outcome. It is that somebody needs to "
 "read a number out of the model."),

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
 "computed as if the model had been chosen in advance when it was not. Treat what survives as "
 "a shortlist worth looking into, and say that a search produced it."),

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

("A depth-10 tree has a training error of 0.44 and a cross-validated error of 13.19. A straight "
 "line has 11.59 and 12.23. Which is the better model?",
 ["The tree, since 0.44 is by far the lowest number on the table.",
  "The line, because the tree only looks good on the rows it was fitted to.",
  "Neither, the two cannot be compared.",
  "The tree, because it has more flexibility available."],
 1,
 "Training error measures how well a model reproduces data it has already seen, and a flexible "
 "model can drive that near zero by memorizing. The honest column is the other one, and there the "
 "tree is worse than a straight line. Notice also that the two models sit on the same rows and are "
 "scored the same way, which is what makes the comparison mean anything."),

("A model predicting daily revenue reports a cross-validated MSE of 140. What should you tell the "
 "owner?",
 ["The model is off by about \\$140 on a typical day.",
  "The model is off by about \\$12 on a typical day, since $\\sqrt{140} \\approx 12$.",
  "The model explains 140\\% of the variation.",
  "MSE cannot be translated into dollars."],
 1,
 "MSE is in squared units, so 140 is 140 squared dollars, which means nothing to anyone. Taking "
 "the square root puts it back into dollars, and about \\$12 a day is a sentence the owner can "
 "actually use. Quote the RMSE for that reason, and keep the MSE for comparing models to each "
 "other."),

("Which of these is decided by fitting the model, rather than by you?",
 ["How deep to let a tree grow.",
  "How many folds to use in cross-validation.",
  "Where a tree puts its split points.",
  "How large a penalty to put on the coefficients."],
 2,
 "Fitting is the part the data decides: the split points, the slopes, the weights. Depth, the "
 "number of folds and the size of a penalty are all settings you choose beforehand, and no amount "
 "of fitting will choose them for you. Unit 4 covers how to make those choices without fooling "
 "yourself."),
])
