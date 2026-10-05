#!/usr/bin/env python3
"""Midterm B: multiple choice, and the bicycle repair shop analysis."""

DATA_URL = "https://drbob-richardson.github.io/stat220/F2026/data"

MC = [
 ("A shop compares repair times for two months and gets $p = 0.54$. What follows?",
  ["The two months had the same average repair time.",
   "There is no difference worth looking for.",
   "A difference this size is unsurprising if nothing changed.",
   "The comparison needs a larger sample before it can be run."],
  2, "A large p-value means the data is unsurprising under the assumption of no difference. It "
     "is not evidence that no difference exists, which is why the interval matters."),

 ("A 95\\% interval for a difference in repair time runs from $-1.8$ to $+0.4$ days. What is "
  "the right reading?",
  ["The difference is zero, since the interval contains zero.",
   "A 1.8 day gain and a slight worsening are both still consistent.",
   "There is a 95\\% chance the true difference is in that range.",
   "The study failed and should be repeated."],
  1, "The interval reports the range the data leaves open. Containing zero means no difference "
     "is consistent with it, not that no difference is established, and a 1.8 day gain is also "
     "consistent."),

 ("Which change would most increase the power of a comparison?",
  ["Using a stricter significance cutoff.",
   "Collecting more repair jobs in each group.",
   "Reporting a confidence interval alongside the test.",
   "Adding more predictors to the model."],
  1, "Power grows with sample size and with the size of the effect. A stricter cutoff lowers "
     "it, and reporting style changes nothing about it."),

 ("A technician looks at 30 possible predictors of repair time and reports the three with "
  "$p < 0.05$. What is wrong?",
  ["Three predictors is too few for a useful model.",
   "The p-values should have been computed before the fitting began.",
   "Nothing, as long as those three really are below 0.05.",
   "Those three won a search, so their p-values are not what they seem."],
  3, "Looking at 30 columns and keeping the best is a search. About one or two of 30 useless "
     "columns clear 0.05 by chance, and the reported values do not account for the looking."),

 ("The outcome is the number of parts a repair needs. Which family fits best?",
  ["Logistic regression, since parts are counted in whole numbers.",
   "Poisson regression, which is built for counts.",
   "Linear regression, which handles any numeric outcome equally well.",
   "A classification tree, since the counts are small."],
  1, "A count outcome calls for a count model. A linear model can predict negative parts and "
     "assumes a spread that does not grow with the mean, which counts usually do."),

 ("The shop wants to know whether a new supplier shortened repairs, and also wants to quote "
  "customers a turnaround time. What does that imply?",
  ["One model can answer both, since both use the same data.",
   "One asks for an effect with uncertainty, the other for a prediction.",
   "Both questions require a causal design before anything can be said.",
   "The second question cannot be answered without an experiment."],
  1, "Explaining and predicting are different jobs. The first wants a coefficient and its "
     "interval, the second wants a predicted value and a prediction interval."),

 ("What is the main thing a random forest cannot hand back?",
  ["A prediction of turnaround for a new repair job.",
   "A measure of which predictors it leaned on most.",
   "An accurate fit when the predictors interact.",
   "A coefficient with an interval and a p-value."],
  3, "A forest has no probability model for the outcome, so there is no likelihood to build "
     "intervals or p-values from. It predicts, and it can rank variables, but it cannot do that."),

 ("A regression of repair days on parts needed gives a slope of 0.69. What does it mean?",
  ["Repairs take about 0.69 days on average.",
   "About 69\\% of repair time is explained by the number of parts.",
   "Each additional part is associated with about 0.69 more days.",
   "The typical prediction is off by about 0.69 days."],
  2, "A slope is a rate: days per part. The units are what make it meaningful, and it is an "
     "association in this data."),

 ("In \\texttt{days $\\sim$ parts\\_needed + tech\\_years}, the coefficient on experience is "
  "$-0.16$. What is the correct phrase?",
  ["Each extra year of experience shortens a repair by 0.16 days.",
   "Among repairs needing the same parts, each extra year goes with 0.16 fewer days.",
   "Experience explains 16\\% of the variation in repair time.",
   "Each extra year of experience causes repairs to take 0.16 fewer days each."],
  1, "Coefficients in a multi-predictor model are conditional on the others, and this data is "
     "observational, so association rather than causation."),

 ("Bike type has four levels and the output shows three coefficients, with commuter missing. "
  "How do you read the electric coefficient?",
  ["Electric bikes compared with the average of all four types.",
   "Electric bikes compared with commuter bikes.",
   "Electric bikes compared with zero.",
   "The share of repair time attributable to electric bikes."],
  1, "The missing level is the baseline, and every other coefficient compares its level with "
     "that one."),

 ("A supplier coefficient is near zero in a raw comparison and clearly negative once parts "
  "needed is added. What is the explanation?",
  ["The new supplier took the jobs needing more parts, which masked the gain.",
   "The raw comparison was computed incorrectly.",
   "Adding predictors always moves coefficients away from zero.",
   "The sample is too small for the raw comparison to be at all reliable."],
  0, "If the new supplier handled harder jobs, those jobs take longer for reasons that have "
     "nothing to do with the supplier, which hides the improvement until you hold difficulty "
     "fixed."),

 ("What should you look at before trusting any of the summary numbers from a fit?",
  ["The p-value on the largest coefficient.",
   "The number of observations.",
   "Plots of the data and of what the model missed.",
   "Whether $R^2$ is above a standard threshold."],
  2, "Every summary assumes the shape you fitted is roughly right. A plot catches curvature, a "
     "single point driving the fit, and spread that grows, none of which show up in the "
     "coefficient table."),

 ("A shop quotes one customer a turnaround time. Which interval belongs in the quote?",
  ["The prediction interval for a single repair.",
   "The confidence interval for the average repair.",
   "Whichever is narrower, to keep the quote competitive.",
   "Neither; a point prediction is what a quote needs."],
  0, "One customer is one case. The prediction interval includes the job-to-job variation that "
     "the confidence interval for an average leaves out."),

 ("A model reports $R^2 = 0.97$ on the repairs it was fitted on and typical error three times "
  "larger on next month's repairs. What is happening?",
  ["Underfitting, so more predictors are needed.",
   "Overfitting: the model followed noise in the rows it was fitted on.",
   "Nothing unusual, since the two numbers measure the same thing.",
   "The new month's data must have been recorded differently."],
  1, "A near-perfect fit on its own rows beside poor performance on new ones is the signature "
     "of a model with enough flexibility to bend around individual points."),

 ("What does holding rows back from fitting accomplish?",
  ["It makes the model more accurate on the rows it keeps.",
   "It gives an error the fitting was not allowed to optimize.",
   "It reduces the number of predictors the model needs.",
   "It removes outliers from the training data."],
  1, "The point is an honest measurement. Error on held-out rows is not something the fitting "
     "was allowed to minimize."),

 ("\\texttt{parts\\_cost} is 18 times \\texttt{parts\\_needed} plus noise. What happens if both "
  "go into the model?",
  ["The fit improves substantially, since two predictors beat one.",
   "They add little over either alone, and the coefficients wobble.",
   "The model cannot be fitted at all.",
   "Their coefficients will both be close to the true combined effect."],
  1, "Near-duplicate columns split the credit. The pair explains barely more than one of them, "
     "and the individual coefficients can swing with small changes in the data."),

 ("Which comparison can AIC not be used for?",
  ["Two linear regressions on the same rows with different predictors.",
   "A linear regression against a random forest.",
   "A model with three predictors against one with five.",
   "A model with a squared term against one without."],
  1, "AIC is built from a likelihood, which a forest does not have. Comparing those two "
     "requires held-out error instead."),

 ("A full second-order model on 5 predictors has how many terms, counting main effects, "
  "squares and pairwise products?",
  ["10", "15", "20", "25"],
  2, "Five main effects, five squares and ten pairwise products. Twenty coefficients is a lot "
     "of flexibility to support from a small sample."),

 ("Lasso with the penalty chosen by cross-validation sets \\texttt{quarter} to exactly zero. "
  "What does that establish?",
  ["Quarter of the year has no relationship with repair time.",
   "Quarter would also be insignificant in an ordinary regression.",
   "The column did not earn its keep against the penalty here.",
   "The column is uncorrelated with every other predictor."],
  2, "A zero is the result of a penalty choice in this sample with these other columns. Change "
     "any of those and the variable can return."),

 ("The shop asks whether switching all repairs to the new supplier will cut turnaround by the "
  "amount your model estimated. What is the honest answer?",
  ["Yes, that is what the coefficient estimates.",
   "Yes, provided the coefficient is statistically significant.",
   "No, the coefficient only applies to the bikes already in the data.",
   "The data is observational, so it describes a comparison, not a switch."],
  3, "Jobs were not assigned to suppliers at random. The adjusted comparison is much better "
     "than the raw one, but a full switch is an intervention the data does not directly speak to."),
]

SETUP = f'''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score

repairs = pd.read_csv("{DATA_URL}/repair_jobs.csv")
folds = KFold(5, shuffle=True, random_state=0)
repairs.head()'''

TASKS = [
 ("Look at the data first",
  r"Make \textbf{two} plots that matter for the question the shop is asking. Then write two or "
  r"three sentences on anything you notice that a later step will have to deal with.",
  10,
  "Any two sensible plots: days against parts needed, days by supplier, a histogram of days, or "
  "days by bike type. Full credit needs a real observation. The useful ones: parts needed "
  "drives repair time and the relationship bends slightly; the two supplier groups look almost "
  "identical in raw averages; the new supplier's jobs need more parts."),

 ("The comparison the owner already made",
  r"The owner compared average repair time with the old and new supplier, saw almost no "
  r"difference, and is ready to drop the new supplier. Carry out that comparison: report both "
  r"averages, the difference, a test, and a 95\% interval. Then say in two or three sentences "
  r"what it does and does not establish.",
  12,
  "About 3.28 days with the new supplier against 3.37 with the old, a difference near $-0.09$ "
  "days with $p$ about 0.54 and an interval covering zero comfortably. Full credit says a "
  "non-significant result is not evidence of no difference, and points at the interval, which "
  "still allows a meaningful improvement in either direction."),

 ("Put the obvious predictor in the model",
  r"Fit a model for \texttt{days} using the supplier indicator together with the predictors "
  r"that plainly belong. Report the supplier coefficient with its 95\% interval, interpret it "
  r"in a sentence that says what is held fixed, and explain in two or three sentences why it "
  r"differs from Task 2.",
  14,
  "With parts needed, technician experience and bike type in the model, the supplier "
  "coefficient is about $-0.85$ days, interval roughly $[-1.07, -0.64]$. Interpretation must "
  "hold the others fixed: among repairs needing the same parts, by technicians of the same "
  "experience, on the same type of bike, the new supplier ran about 0.85 days faster. The "
  "explanation: the new supplier was used on harder jobs (correlation about $+0.34$ with parts "
  "needed), which hid the gain in the raw comparison."),

 ("Which predictors to keep",
  r"Compare at least two candidate sets of predictors and say which you would use. Justify it "
  r"with something other than $R^2$, and say in a sentence what that number measures.",
  12,
  "Any defensible comparison on cross-validated error, AIC or BIC. The sensible set gives "
  "cross-validated error about 1.63 days; adding \\texttt{ticket\\_number}, "
  "\\texttt{shop\\_rating} and \\texttt{quarter} does not help and worsens AIC (about 3046 "
  "against 3051). \\texttt{parts\\_cost} is a near-copy of parts needed (correlation 0.98) and "
  "adds nothing. Naming the criterion and what it measures is required."),

 ("A number for one customer",
  r"A customer brings in a commuter bike needing 4 parts, assigned to a technician with 2 "
  r"years of experience, using the new supplier. Produce a prediction, give the interval you "
  r"would quote the customer, and say in a sentence why that interval rather than the other.",
  8,
  "Prediction about 3.5 days. The prediction interval is roughly $[0.7, 6.3]$ days against a "
  "confidence interval of about $[3.3, 3.7]$. A quote is for one repair, so the prediction "
  "interval is the one that belongs in it."),

 ("What you would tell the owner",
  r"Write \textbf{four to six sentences} to the shop owner. Say what you found, how confident "
  r"you are, and what they can and cannot do with it. Write it for a reader who has not taken "
  r"this course.",
  4,
  "Should report that the new supplier is associated with faster repairs once job difficulty is "
  "accounted for, give the number with its uncertainty, explain why the raw averages hid it, "
  "and stop short of promising the same gain from switching everything over. Deduct for a bare "
  "coefficient with no caveat, or for claiming the raw comparison was simply wrong."),
]

EXAM = dict(
    tag="B",
    title="Turnaround time at a bicycle repair shop",
    blurb=(r"A repair shop switched to a new parts supplier for some jobs this year. The owner "
           r"compared average turnaround before and after, saw no real difference, and is about "
           r"to go back to the old supplier. They have asked you to check."),
    dataset=r"\texttt{repair\_jobs.csv}: 800 completed repairs.",
    columns=[("days", "days to finish the repair, the outcome"),
             ("parts\\_needed", "parts the repair required"),
             ("parts\\_cost", "what those parts cost"),
             ("tech\\_years", "the technician's years of experience"),
             ("bike\\_type", "commuter, road, mountain, or electric"),
             ("new\\_supplier", "1 if the parts came from the new supplier"),
             ("ticket\\_number, shop\\_rating, quarter", "also recorded")],
    setup_code=SETUP,
    mc=MC,
    tasks=TASKS,
    data_note=(r"Load it with \texttt{pd.read\_csv(\"" + DATA_URL +
               r"/repair\_jobs.csv\")}. Put each piece of work in the space provided."),
)
