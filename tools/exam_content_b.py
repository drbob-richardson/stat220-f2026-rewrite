#!/usr/bin/env python3
"""Midterm B, the take-home: the bicycle repair shop analysis.

Thirteen tasks, 100 points, covering Units 1 through 5. The multiple-choice
half of the midterm is a separate paper now, in exam_content_mc.py.

Every number in the answer key below was measured off Exams/data/repair_jobs.csv
as built by tools/make_exam_data.py. Rebuild the data and these move.
"""

DATA_URL = "https://drbob-richardson.github.io/stat220/F2026/data"

SETUP = f'''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from scipy import stats
from sklearn.tree import DecisionTreeRegressor, export_text
from sklearn.model_selection import train_test_split

repairs = pd.read_csv("{DATA_URL}/repair_jobs.csv")
repairs.head()'''

TASKS = [
 # ---------------- Unit 2: choosing a family ----------------
 ('Which kind of model, and why',
  'Before you fit anything, decide what kind of model this question calls for. Name the family, '
  'say why it suits this outcome, and say what you need back from it that a random forest could '
  'not give you.',
  6,
  'Linear regression on repair time, a continuous positive number, and the question asks for the '
  'size of an effect, so the model has to return a coefficient with an interval. A forest would '
  'predict turnaround without saying anything about the supplier effect or its uncertainty. '
  'Credit a student who notices the outcome is skewed and proposes working on the log scale, '
  'which is Task 8.'),

 # ---------------- Unit 3: look first ----------------
 ('Look at the data first',
  "Make two plots that bear on the shop's question. Then, in two or three sentences, say what you "
  'see that a later step will have to account for.',
  8,
  'Any two sensible plots: days against parts needed, days by supplier, a histogram of days, or '
  'days by bike type. Full credit needs a real observation. The useful ones: repair time is '
  'strongly right skewed (median 1.59 days, mean 1.98, maximum 12.12, skew 2.03); parts needed '
  'drives it; the two supplier groups look almost identical in raw averages; the new supplier\'s '
  'jobs need more parts (3.43 against 2.20).'),

 # ---------------- Unit 1: the comparison already made ----------------
 ('The comparison the owner already made',
  'The owner compared average repair time under the old and the new supplier, saw almost no '
  'difference, and is ready to drop the new one. Run that comparison. Report both averages, the '
  'difference, a test, and a 95\\% interval, then say in two or three sentences what it does and '
  'does not establish.',
  10,
  'About 1.94 days with the old supplier against 2.02 with the new, a difference near $+0.08$ '
  'days with $p$ about 0.39 and a 95\\% interval of roughly $[-0.10, +0.26]$. Full credit says a '
  'non-significant result is not evidence of no difference, and points at the interval, which '
  'still leaves a meaningful improvement in either direction on the table.'),

 # ---------------- Unit 3: adjust ----------------
 ('Put the obvious predictors in the model',
  'Now fit a model for repair time that includes the supplier indicator along with the predictors '
  'that obviously belong. Report the supplier coefficient with its interval, interpret it in a '
  'sentence that names what is held fixed, and explain in two or three sentences why it differs '
  'from Task 3.',
  8,
  'With parts needed, technician experience and bike type in the model, the supplier coefficient '
  'is about $-0.43$ days, 95\\% interval roughly $[-0.57, -0.28]$, $p \\approx 10^{-8}$, '
  '$R^2 = 0.455$. The interpretation must hold the others fixed: among repairs needing the same '
  'parts, by technicians of the same experience, on the same type of bike, the new supplier ran '
  'about 0.43 days faster. The explanation: the new supplier was given the harder jobs, which hid '
  'the gain in the raw comparison.'),

 # ---------------- Unit 4: the near-duplicate ----------------
 ('A column that adds nothing',
  'Add \\texttt{parts\\_cost} to the model from Task 4 and look at what happens. Report the '
  '$R^2$ before and after, and the coefficient on \\texttt{parts\\_needed} and its standard error '
  'before and after. Explain in two or three sentences what is going on and what you would do.',
  6,
  '$R^2$ does not move at all: 0.4548 either way. The coefficient on parts needed goes from '
  '$+0.467$ to $+0.436$, and its standard error blows up from 0.020 to 0.105, a factor of five. '
  'The two columns carry nearly the same information ($r = 0.98$), so the fit cannot tell which '
  'one deserves the credit and the individual estimates become unstable. Drop one. Full credit '
  'names the near-duplication and uses the standard error, not just the $R^2$, as the evidence.'),

 # ---------------- Unit 3: categorical ----------------
 ('The category in the model',
  'Bike type has four levels. Report its coefficients, say which level is the baseline and how '
  'you can tell, and write the sentence that interprets one of the others. Say what would change '
  'if a different level were the baseline.',
  6,
  'Baseline is \\texttt{commuter}, the level with no coefficient of its own. Against a commuter '
  'bike with the other predictors held fixed: electric $+0.75$ days, mountain $+0.15$, road '
  '$-0.10$. Changing the baseline changes every coefficient and the intercept, but no fitted '
  'value and no prediction.'),

 # ---------------- Unit 5: read the residuals ----------------
 ('Read the residual plot',
  'Plot the residuals of the Task 4 model against its fitted values. Name what you see, and back '
  'it with a number: report the standard deviation of the residuals on the upper half of the '
  'fitted values divided by the standard deviation on the lower half. Say what this does to the '
  'intervals you reported in Task 4.',
  8,
  'The residuals fan out. The ratio is about 2.1, so the errors on slow repairs are roughly twice '
  'the size of the errors on fast ones. Full credit names the fan rather than just saying the '
  'plot looks bad, gives the ratio, and says that equal spread is an assumption behind every '
  'interval and p-value in Task 4, so those are not trustworthy as they stand. Credit a student '
  'who also notes the mild bend.'),

 # ---------------- Unit 5: the log ----------------
 ('Fix it on the log scale',
  'Fit the model again with the log of repair days as the outcome. Report the same spread ratio '
  'for the new residuals, say which model you would use and why, and write the sentence that '
  'interprets the supplier coefficient on the log scale. A coefficient of $b$ on a logged outcome '
  'is roughly a $100(e^{b}-1)\\%$ change.',
  10,
  'The ratio falls from about 2.1 to about 1.1, so the fan is gone. The supplier coefficient is '
  'about $-0.226$, a reduction of roughly 20\\%, 95\\% interval about 15\\% to 25\\% faster. Full '
  'credit needs the before-and-after comparison, a choice with a reason, and a percentage reading '
  'rather than a reading in days. Do not give credit for choosing the log model only because '
  '$R^2$ rose; it barely moves (0.455 to 0.469) and the two are not comparable across different '
  'outcome scales anyway.'),

 # ---------------- Unit 5: grow a tree ----------------
 ('Grow a tree and read it',
  'Fit a decision tree of depth 3 predicting log repair days from parts needed, technician '
  'experience, bike type and supplier. Print it. Then describe in plain words the kind of repair '
  'that lands in the slowest leaf and the kind that lands in the fastest, and say what the first '
  'split is and where it falls.',
  10,
  'The first split is \\texttt{parts\\_needed} at 4.5, that is, five parts or more against four '
  'or fewer. Slowest leaf: five or more parts, electric bike, technician with more than 1.5 '
  'years. Fastest: two or fewer parts with an experienced technician. Full credit reads the tree '
  'as rules in words and locates the first cut. Credit a student who remarks that the tree also '
  'splits on supplier inside the middle branches, which is the effect the regression is '
  'estimating.'),

 # ---------------- Unit 5: how deep ----------------
 ('How deep should it go',
  'Split the rows into a training set and a held-out set. For depths 1 through 12, report the '
  'error on the rows the tree was fitted on and the error on the rows held back. Say which depth '
  'you would use and why, and say what the first column alone would have told you.',
  6,
  'Error on its own rows falls at every depth, 0.502 down to about 0.358. Held-out error falls to '
  'about 0.466 at depth 5 and then climbs back to about 0.50 by depth 10. Depth 5 is the answer. '
  'Full credit says the first column can always be driven down by letting the tree memorise, so '
  'it cannot choose anything, and that only the held-out column is measuring prediction.'),

 # ---------------- Unit 5: tree as scout ----------------
 ('Put what the tree found into the regression',
  'The tree cut \\texttt{parts\\_needed} at 4.5, which is not something a smooth model can '
  'produce. Add an indicator for repairs needing five or more parts to your log model from Task 8. '
  'Report its coefficient, its p-value, and the AIC before and after. Then fit a third model that '
  'uses a squared term in \\texttt{parts\\_needed} instead of the indicator, and say which of the '
  'three you would keep and why. Finally, say what you would ask the shop about this threshold.',
  10,
  'The indicator is about $+0.276$, a repair needing five or more parts runs roughly 32\\% longer '
  'than the smooth trend predicts, $p \\approx 10^{-5}$. AIC improves from about 934 to 916, a '
  'gain of 18. The squared term does not help at all: AIC about 935, no better than the model '
  'without it. Keep the indicator. Full credit explains why: a threshold is a jump, and a '
  'polynomial is smooth, so a curve cannot reproduce a step. The question to ask the shop is '
  'whether something changes at five parts, and the answer in this shop is that those repairs '
  'have to be special-ordered from the warehouse. Credit a student who notes the supplier '
  'coefficient barely moves ($-0.223$, still about 20\\% faster), so the threshold is a separate '
  'finding rather than an explanation of the supplier effect.'),

 # ---------------- Unit 4: predict one case ----------------
 ('A number for one customer',
  'A customer brings in a commuter bike needing 4 parts, going to a technician with 2 years of '
  'experience, with parts from the new supplier. Predict the turnaround from the model you '
  'settled on, give the interval you would quote them, and say in one sentence why that interval '
  'rather than the other.',
  6,
  'About 1.73 days, with a prediction interval of roughly $[0.75, 4.0]$ days against a confidence '
  'interval of about $[1.61, 1.86]$. A quote is for one repair, so the prediction interval belongs '
  'in it. Note this job needs 4 parts, so the Task 11 indicator is 0. Credit a student who works '
  'on the untransformed scale as long as they use a prediction interval and say so. Credit, but do '
  'not require, noticing that exponentiating a fitted log value returns a median rather than a '
  'mean.'),

 # ---------------- communication ----------------
 ('What you would tell the owner',
  'Write six to eight sentences to the shop owner. Cover what you found about the supplier, what '
  'you found about big jobs, how sure you are of each, and what they can and cannot do with it. '
  'Assume they have not taken this course.',
  6,
  'Should report that the new supplier is associated with repairs roughly 20\\% faster once job '
  'difficulty is accounted for, give the uncertainty, explain why the raw averages hid it, report '
  'the five-part threshold as a separate and actionable finding, and stop short of promising the '
  'same gain from switching every job over, since jobs were not assigned to suppliers at random. '
  'Deduct for a bare coefficient with no caveat, for reporting the log coefficient in days, or '
  'for claiming the owner\'s raw comparison was simply computed wrong.'),
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
    tasks=TASKS,
    data_note=(r"Load it with \texttt{pd.read\_csv(\"" + DATA_URL +
               r"/repair\_jobs.csv\")}. Put each piece of work in the space provided."),
)
