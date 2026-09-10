#!/usr/bin/env python3
"""Unit 4 practice, multiple choice with answers inline. STUDENT-FACING."""
from build_questions import build_mc

build_mc("Model_Building", "Building and Trusting a Model",
"""Practice on many predictors, overfitting, honest evaluation, and how much flexibility your data
can actually pay for. No computer needed.""",
[
("A teammate adds 40 variables and training $R^2$ rises from 0.62 to 0.95. How impressed should "
 "you be?",
 ["Very. That is a large improvement in fit.",
  "Not at all by itself. In-sample $R^2$ can only go up when you add variables, even useless "
  "ones, so the jump is expected rather than evidence.",
  "Somewhat. It depends on whether the 40 variables were significant.",
  "Not impressed, because 0.95 is suspiciously high and the data must be wrong."],
 1,
 "Adding a column can never reduce the fit on the data you fitted, so training $R^2$ is a "
 "ratchet. The number that would mean something is error on rows the model never saw. Ask for "
 "that, and ask how the 40 were chosen."),

("Why does the error curve have a minimum when neither of its two parts does?",
 ["Because cross-validation introduces randomness.",
  "Because bias falls with complexity while variance rises, and only their sum turns around.",
  "Because the training error eventually starts rising.",
  "Because of the central limit theorem."],
 1,
 "Bias measures being wrong in the same direction every time, and it decreases the whole way as "
 "the model gains flexibility. Variance measures being different every refit, and it increases "
 "the whole way. Neither curve has a bottom. Their sum does, and finding it is what "
 "cross-validation is for."),

("What moves the best model complexity toward more flexibility?",
 ["More noise in the outcome.",
  "More candidate predictors to search through.",
  "More rows of data.",
  "A stronger need to explain a coefficient."],
 2,
 "Data buys down variance, which is the cost of flexibility, so more rows make a complicated "
 "model affordable. The other three all push the other way. More noise means more of what you "
 "would fit is noise, searching more candidates is itself a form of fitting, and needing to "
 "defend a number rules out models whose parameters mean nothing."),

("Cross-validated errors for a depth-3 tree and a depth-7 tree are within one standard error of "
 "each other. What does the one-standard-error rule say?",
 ["Take the depth-7 tree, since its mean was lower.",
  "Take the depth-3 tree, since the two are not distinguishable on this data.",
  "Try depths 4, 5 and 6 to break the tie.",
  "Collect more data."],
 1,
 "A cross-validated score is an estimate and carries noise of its own. Inside that noise, "
 "choosing the lower mean is choosing at random. The simpler model is more stable over time, "
 "easier to explain, and less likely to break under a shift in the data, and none of those are "
 "consolation prizes."),

("A model predicting hospital readmission achieves 0.99 AUC in testing. What is your first "
 "thought?",
 ["Excellent, ship it.",
  "Suspicion. Check whether a variable in the model encodes the answer.",
  "The test set was too small.",
  "The model is underfitting."],
 1,
 "Near-perfect performance on a genuinely hard problem usually means leakage: something in the "
 "feature set is a consequence of the outcome rather than a predictor of it. A discharge code "
 "recorded at readmission, or a date field that only exists for readmitted patients. Real "
 "prediction problems are hard, and 0.99 is a claim that this one was not."),

("What is wrong with running cross-validation after scaling the entire dataset?",
 ["Nothing, scaling is a standard preprocessing step.",
  "The scaling used the held-out rows, so information leaked from the test folds into training.",
  "Scaling makes coefficients uninterpretable.",
  "Cross-validation cannot be used with scaled data."],
 1,
 "The mean and standard deviation used for scaling were computed with the held-out rows "
 "included, so every fold's training set has already peeked at its test set. The effect is "
 "usually small but it is in the optimistic direction, and it is free to avoid by scaling inside "
 "the pipeline so it is refit on each fold's training portion."),

("Two predictors correlate at 0.95. What happens to their coefficients?",
 ["Both become significant, since they share signal.",
  "The coefficients become unstable and each can look insignificant, even though together the "
  "pair clearly matters.",
  "The model refuses to fit.",
  "One is automatically dropped."],
 1,
 "The model cannot tell which twin deserves the credit, so it splits it in a way that swings "
 "wildly between refits, and the standard errors inflate. The tell is that each looks "
 "unimportant on its own while dropping both hurts badly. Insignificant here means "
 "indistinguishable from its twin, not unimportant."),

("You search 200 predictors against an outcome that is pure noise. Roughly what does the best one "
 "look like?",
 ["Nothing, since the outcome is noise.",
  "Weakly correlated but not significant.",
  "Correlated around 0.4 and significant at $p<0.01$ if you report it without mentioning the "
  "search.",
  "Perfectly correlated, since one of 200 will match by chance."],
 2,
 "The maximum of 200 noisy correlations is a large number by construction. Reporting it as though "
 "it were the only thing you tried is the mechanism behind a great many findings that fail to "
 "replicate. If the variables were chosen by looking at the data, the printed $p$-values assume "
 "something that is not true."),

("What does stepwise selection by $p$-value do to the coefficients that survive?",
 ["Nothing, they are unbiased.",
  "It shrinks them toward zero.",
  "It biases them away from zero, because surviving required looking large.",
  "It makes them all significant by construction."],
 2,
 "Survival was conditional on clearing a threshold, so the survivors are enriched for estimates "
 "that happened to land high. The reported intervals and $p$-values are computed as if the model "
 "had been fixed in advance, which it was not. Report out-of-sample performance instead, or "
 "validate on fresh data."),

("When is a simpler model the right choice even though it predicts worse?",
 ["Never, prediction accuracy is the goal.",
  "When someone will have to defend an individual output, or maintain it for years.",
  "Only when the difference is under 1\\%.",
  "When the dataset is small."],
 1,
 "Accuracy is one requirement among several. A model whose outputs get challenged by a regulator, "
 "a customer, or a colleague has to be explainable, and one that runs nightly for two years has "
 "to be stable. Choosing simplicity for a stated reason reads as judgment. Defaulting to it "
 "because you never tried anything else reads as inexperience, and the difference is whether you "
 "can say what you ruled out."),
])
