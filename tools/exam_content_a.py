#!/usr/bin/env python3
"""Midterm A: multiple choice, and the urgent care clinic analysis."""

DATA_URL = "https://drbob-richardson.github.io/stat220/F2026/data"

MC = [
 ("A clinic compares wait times on two days and gets $p = 0.21$. What has it shown?",
  ["That the two days have the same average wait.",
   "That a difference this size is unsurprising if nothing is going on.",
   "That the sample was too small for the test to work.",
   "That the difference is real, but it is not large enough to matter."],
  1, "A p-value says how surprising this result would be if nothing were going on. It does not "
     "establish that nothing is going on, and it says nothing about size."),

 ("Which of these does a 95\\% confidence interval for a difference in means tell you?",
  ["The range of differences the data leaves as plausible.",
   "The range that contains 95\\% of individual patients.",
   "The probability that the true difference is zero.",
   "The range of values the sample difference would take 95\\% of the time."],
  0, "It is a statement about an estimate: the differences that are reasonably consistent with "
     "this data. It is not about individuals, and it is not a probability for the truth."),

 ("A study with 40{,}000 patients finds a 0.3 minute difference in wait time with $p < 0.001$. "
  "What should you conclude?",
  ["The effect is real and worth acting on, since the p-value is tiny.",
   "The test must be wrong, since such a small difference cannot be significant.",
   "The difference is real but far too small to matter operationally.",
   "The sample is too large for the p-value to be meaningful."],
  2, "With enough data, tiny differences become statistically detectable. Significance and "
     "importance are separate questions, and 0.3 minutes is not a difference a clinic can feel."),

 ("Which power statement is correct?",
  ["Power is the chance of seeing a real effect when one is there.",
   "Power is the chance that the null hypothesis is true.",
   "Power rises as the significance cutoff is made stricter.",
   "Power does not depend on the size of the effect you are looking for."],
  0, "Power is the probability of detecting an effect that is genuinely present. It grows with "
     "sample size and with effect size, and shrinks as the cutoff gets stricter."),

 ("A manager tests 20 unrelated operational changes at the 0.05 cutoff and finds one "
  "significant. What is the most likely explanation?",
  ["That change is the only one that worked.",
   "The other 19 tests were underpowered.",
   "The data must have been collected incorrectly for the other 19.",
   "On 20 useless tests, one significant result is expected by chance."],
  3, "At a 5\\% cutoff, one in twenty useless tests clears the bar on average. A single "
     "significant result out of twenty is what pure chance looks like."),

 ("The outcome is whether a patient leaves before being seen, yes or no. Which family fits?",
  ["Linear regression, since the outcome is coded 0 and 1.",
   "Logistic regression, which returns a probability between 0 and 1.",
   "Poisson regression, since the outcome is a count of patients.",
   "A random forest, since the outcome is not continuous."],
  1, "A yes/no outcome calls for a model that returns a probability. Linear regression on 0/1 "
     "produces values below 0 and above 1, which cannot be probabilities."),

 ("Which is the strongest reason to prefer a regression over a random forest when the question "
  "is whether a new kiosk changed wait times?",
  ["A forest cannot handle categorical predictors like severity.",
   "A forest will always predict less accurately than a regression does.",
   "A regression reports a coefficient with an interval, which is the answer.",
   "A forest requires far more data than a regression does."],
  2, "The question asks for an effect with its uncertainty. A regression reports exactly that. "
     "A forest can predict well and still have nothing to say about the size of an effect."),

 ("What does AIC do that $R^2$ does not?",
  ["It measures how well the model predicts a new case.",
   "It charges the model for each predictor it uses.",
   "It works for any model that makes a prediction.",
   "It tests whether the coefficients are different from zero."],
  1, "AIC balances fit against the number of parameters, so adding a useless predictor can make "
     "it worse. $R^2$ cannot go down when you add a column, so it cannot choose."),

 ("A regression of wait time on number of patients ahead gives a slope of 4.3. What does that "
  "mean?",
  ["Each extra patient ahead is associated with about 4.3 more minutes of wait.",
   "Wait time is about 4.3 times the number of patients ahead.",
   "About 4.3\\% of the variation in wait time is explained by patients ahead.",
   "The model's predictions are off by about 4.3 minutes on a typical visit."],
  0, "A slope is a rate, in minutes per patient, and it describes an association in this data "
     "rather than what would happen if you intervened."),

 ("In \\texttt{minutes $\\sim$ patients\\_ahead + staff\\_on\\_shift}, what does the coefficient "
  "on staffing mean?",
  ["The effect of staffing, ignoring how busy the clinic is.",
   "The total effect of staffing, including its effect through patient volume.",
   "The effect of staffing among visits with the same number of patients ahead.",
   "The correlation between staffing and wait time."],
  2, "Every coefficient in a multi-predictor model is read with the other predictors held "
     "fixed. Saying that phrase out loud is what separates a right reading from a wrong one."),

 ("A categorical predictor with four levels appears in the output with three coefficients. Why?",
  ["One level was dropped for being statistically insignificant.",
   "One level is the baseline, folded into the intercept.",
   "The fourth coefficient is always zero and is omitted.",
   "Three is the maximum number of levels a model can estimate."],
  1, "One level sits inside the intercept and every other coefficient is read against it. "
     "Changing which level is the baseline changes all the numbers but no prediction."),

 ("A coefficient on a treatment flips from positive to negative when a second predictor is "
  "added. What is the most reasonable conclusion?",
  ["One of the two models is misspecified and should be discarded.",
   "The sign flip means the data contains an error.",
   "Both are correct, and they answer different questions.",
   "The flip is noise, since coefficients move around between models."],
  2, "The first model answers a question about raw comparison, the second about comparison at "
     "fixed values of the added variable. Which one you want depends on the question."),

 ("A residual plot shows a clear U shape. What does that say?",
  ["The relationship bends, so a straight line is the wrong shape.",
   "The residuals are not normal, so the outcome should be transformed.",
   "There are outliers that should be removed before refitting.",
   "The predictors are too highly correlated with each other."],
  0, "Structure left in the residuals is structure the model missed, and a U specifically means "
     "curvature. Adding a squared term or transforming the predictor usually fixes it."),

 ("A clinic wants to tell one arriving patient how long they should expect to wait. Which "
  "interval do they need?",
  ["The confidence interval for the fitted mean.",
   "The prediction interval for a new case.",
   "Either one, since both come from the same model.",
   "The confidence interval, because it is narrower and more precise."],
  1, "One patient is a single case, so the answer must include the visit-to-visit variation "
     "that a confidence interval for the average leaves out."),

 ("As you collect far more data, what happens to the prediction interval for one new case?",
  ["It narrows toward zero width.",
   "It narrows a little, then levels off near the spread of cases.",
   "It stays exactly the same width.",
   "It widens, because more unusual cases turn up in a bigger sample."],
  1, "More data pins down the line, which is only part of the width. The rest is the spread of "
     "individual outcomes, which no amount of data removes."),

 ("What makes error measured on the rows a model was fitted on too optimistic?",
  ["Those rows usually contain fewer recording mistakes than later ones.",
   "The coefficients were chosen to make those rows' residuals small.",
   "The sample is always smaller than the population.",
   "The software computes it before the fit has converged."],
  1, "Fitting optimizes the residuals for the rows in front of it. Measuring on the same rows "
     "grades the model on work it already did."),

 ("Which is a fair description of what 5-fold cross-validation produces?",
  ["A guarantee of how the model will do next month.",
   "A p-value for whether the model beats a baseline.",
   "An error estimate averaged over five held-out pieces of the data.",
   "A larger training set, which makes the model more accurate."],
  2, "Each fifth is held out once and predicted by a model fitted on the rest. Averaging those "
     "five errors gives a steadier estimate than a single split."),

 ("A model includes \\texttt{kiosk}, \\texttt{severity} and their interaction. What does the "
  "coefficient on \\texttt{kiosk} by itself now mean?",
  ["The kiosk effect averaged over the three severity levels.",
   "The kiosk effect for visits at the baseline severity level.",
   "The kiosk effect with severity held at its average value.",
   "The kiosk effect among urgent visits only."],
  1, "Once an interaction is in the model, the plain coefficient is the effect in the group "
     "coded zero, here the baseline severity. Quoting it as the overall kiosk effect reports "
     "one group's answer as if it applied to everyone."),

 ("Two predictors are correlated at 0.97. What should you expect?",
  ["Each will have a tiny p-value, since both predict the outcome well enough.",
   "They explain little more than either alone, and both coefficients wobble.",
   "The model will refuse to fit.",
   "Dropping either one will sharply reduce predictive accuracy."],
  1, "Near-duplicates split the credit between them. The pair adds little over one of them, and "
     "small changes in the data can swing the coefficients."),

 ("A model predicts wait times well. Management asks whether adding a third nurse would shorten "
  "waits. What is the right answer?",
  ["Yes, if the staffing coefficient is negative and significant.",
   "Yes, since the model predicts accurately.",
   "No, because the model's $R^2$ is not high enough to support that.",
   "The data is observational, so it is a comparison, not an intervention."],
  3, "Predicting well and estimating what a change would do are different jobs. Shifts with "
     "more staff may differ in other ways, and nothing here was assigned."),
]

SETUP = f'''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score

visits = pd.read_csv("{DATA_URL}/clinic_visits.csv")
folds = KFold(5, shuffle=True, random_state=0)
visits.head()'''

TASKS = [
 ('Which kind of model, and why',
  'Before you fit anything, decide what kind of model this question calls for. Name the family, say why it suits this outcome, and say what you need from it that a random forest could not give you.',
  6,
  'Linear regression: the outcome is a continuous number of minutes, and the question is about the size of an effect, so the model has to return a coefficient with an interval. A forest would predict wait times without saying anything about the size of the kiosk effect or its uncertainty. Credit any answer that names a family fitting a continuous outcome and ties the choice to needing an effect rather than a prediction.'),

 ('Look at the data first',
  "Make two plots that bear on the clinic's question. Then, in two or three sentences, say what you see that a later step will have to account for.",
  8,
  'Any two sensible plots: minutes against patients ahead, minutes by kiosk group, a histogram of minutes, or minutes by severity. Full credit needs a real observation, not a description of the axes. The useful ones: the relationship with patients ahead is strong and bends slightly; kiosk visits look \\emph{longer} in the raw data; the clinic was busier during the kiosk period.'),

 ('The comparison management already made',
  'Management compared average wait times with and without the kiosk and decided the kiosk made things worse. Run that comparison yourself. Report both averages, the difference, a test, and a 95\\% interval. Then say in two or three sentences what it does and does not establish.',
  10,
  'Kiosk visits average about 54.4 minutes against 43.4 without, a gap of roughly +11 minutes, with $p$ around $2\\times10^{-16}$ and an interval well away from zero. The gap is real in the sense that chance does not explain it. It does not establish that the kiosk caused longer waits, because the two groups of visits differ in other ways. Credit the word association, or naming a variable that differs between the groups.'),

 ('Put the obvious predictors in the model',
  'Now fit a model for wait time that includes the kiosk indicator along with the predictors that obviously belong. Report the kiosk coefficient and its 95\\% interval, and interpret it in a sentence that names what is being held fixed. Then explain, in two or three sentences, why it came out different from Task 3.',
  12,
  'With patients ahead, staffing and severity in the model, the kiosk coefficient is about $-5.6$ minutes, 95\\% interval roughly $[-7.3, -3.9]$: the sign flips. The interpretation must hold the other predictors fixed, for example: among visits with the same number of patients ahead, the same staffing and the same severity, kiosk visits ran about 5.6 minutes shorter. The explanation should say the kiosk period was busier (correlation about $+0.5$ between kiosk and patients ahead), so the raw gap was mostly volume.'),

 ('The category in the model',
  'Severity has three levels. Report its coefficients, say which level is the baseline and how you can tell, and write the sentence that interprets one of the others. Then say what would change, and what would not, if a different level were the baseline.',
  6,
  'Baseline is \\texttt{minor}, the level with no coefficient of its own. Moderate is about $+10.5$ minutes and urgent about $+22$ minutes, each read against a minor visit with the other predictors held fixed. Changing the baseline changes every coefficient and the intercept but no fitted value and no prediction.'),

 ('Does the kiosk help some visits more than others?',
  'Management thinks the kiosk helps most on urgent visits. Fit a model that lets the kiosk effect differ by severity, say what you find, and decide whether to keep the extra terms. Back that decision with a number.',
  8,
  'The interaction terms come out with $p$ around 0.99 and 0.79, and AIC gets worse, about 6933 against 6930 without them. Full credit says the data gives no sign the kiosk effect differs by severity and keeps the simpler model, citing the p-values, AIC, or held-out error. A student who keeps the interaction anyway can still earn most of the credit if they say the terms did not earn their place and explain why they kept them.'),

 ('A number for one patient',
  'A patient is checking in now: 8 people ahead of them, 3 staff on shift, a moderate case, and the kiosk in use. Predict how long this visit will take, give the interval the front desk should quote, and say in one sentence why that interval rather than the other.',
  6,
  'Prediction about 51 minutes. The prediction interval is roughly $[29, 74]$ minutes, against a confidence interval of about $[50, 53]$. The front desk is talking to one patient, so the prediction interval is the honest one; quoting the narrow interval would promise precision the model does not have.'),

 ('What you would tell management',
  'Write four to six sentences to the clinic manager. Say what you found, how sure you are, and what they can and cannot do with it. Assume they have not taken this course.',
  4,
  'Should say the kiosk is associated with shorter visits once volume and severity are accounted for, give a number with its uncertainty, note that the raw comparison pointed the other way and why, and avoid a flat causal claim about what rolling it out further would do. Deduct for a bare restatement of the coefficient with no caveat, or for promising a guaranteed time saving.'),

]

EXAM = dict(
    tag="A",
    title="Wait times at an urgent care clinic",
    blurb=(r"A walk-in clinic installed a self check-in kiosk partway through the year. "
           r"Management looked at average wait times before and after, concluded the kiosk made "
           r"things worse, and is about to remove it. They have asked you to check."),
    dataset=r"\texttt{clinic\_visits.csv}: 900 completed visits.",
    columns=[("minutes", "how long the patient was in the clinic, the outcome"),
             ("patients\\_ahead", "patients waiting when this one arrived"),
             ("waiting\\_room\\_count", "a second count taken by the front desk"),
             ("staff\\_on\\_shift", "clinicians working, 2 to 4"),
             ("severity", "minor, moderate, or urgent"),
             ("kiosk", "1 if the visit used the self check-in kiosk"),
             ("room\\_number, front\\_desk\\_rating, month", "also recorded")],
    setup_code=SETUP,
    mc=MC,
    tasks=TASKS,
    data_note=(r"Load it with \texttt{pd.read\_csv(\"" + DATA_URL +
               r"/clinic\_visits.csv\")}. Put each piece of work in the space provided."),
)
