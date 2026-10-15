#!/usr/bin/env python3
r"""The second multiple-choice midterm: 35 questions on Units 1 through 5.

Entries are (stem, options, answer_index, why, unit, kind) with an optional
seventh element (figure file, width, how many questions it covers).

Written to be read in context: most questions carry a scenario, coefficients
are written as equations rather than as code, and the options are long enough
to say what they mean. Six figures carry twelve questions between them, none
of them a picture from the slides.
"""

QUESTIONS = [
# =====================================================================
# UNIT 1
# =====================================================================
(r"A hospital trials a new discharge checklist and estimates that it changes the 30-day "
 r"readmission rate by $+2.2$ percentage points, with a 95\% interval from $-2.0$ to $+6.4$. "
 r"The board asks what the study has established about the checklist.",
 ["That the checklist makes no difference, since the interval contains zero.",
  "That the checklist raises readmissions by about 2.2 points, since that is the best estimate the study produced and it is what the board should plan around.",
  "That the data cannot separate a modest improvement from a sizeable worsening, so the board "
  "should not adopt the checklist on this evidence alone.",
  "That there is a 95\\% probability the true change lies between $-2.0$ and $+6.4$ points."],
 2, "The interval runs from a two-point improvement to a six-point worsening, so the study has "
    "not settled the direction, let alone the size. An interval covering zero does not establish "
    "that nothing is happening, and the 95\\% describes the procedure across repeated samples "
    "rather than this one interval.", 1, "echo"),

(r"A drug trial reports $p = 0.02$. A journalist writes that there is a 2\% chance the drug does "
 r"nothing. What is wrong with that sentence?",
 ["Nothing at all, since that is exactly what a p-value measures.",
  "The p-value is computed assuming the drug does nothing, and reports how surprising the data "
  "would be in that case.",
  "The figure describes one tail of the distribution and should have been doubled first.",
  "A p-value is a property of the sample in hand, so it cannot be turned into a statement about the drug in either direction."],
 1, "The p-value starts from the assumption that there is no effect and asks how unusual data "
    "like this would be under it. Turning it around into the probability that the assumption "
    "holds is a different quantity, and the data alone cannot supply it.", 1, "echo"),

(r"A retailer tests 40 different email subject lines, each as its own experiment against the "
 r"same control, each with its own p-value. Thirty-nine come back above 0.05. The fortieth comes "
 r"back at $p = 0.04$ and the team wants to roll that one out. What should you tell them?",
 ["Roll it out: 0.04 is below the usual cutoff, and the other 39 are irrelevant to it.",
  "Running 40 separate tests on subject lines that do nothing would be expected to turn up about "
  "two results under 0.05 by chance alone, so this one needs confirming first.",
  "Roll it out, provided every one of the 40 experiments was randomised properly.",
  "Do not roll it out, because 40 experiments sharing a single control group is too few for any one of them to detect a difference as small as this, whatever its p-value came out at."],
 1, "At a 0.05 cutoff, each test of a subject line that does nothing has a one in twenty chance "
    "of clearing the bar, so 40 of them yield about two winners from noise alone. One winner out "
    "of 40 is what you would expect to see if none of them worked. Confirm it in a fresh "
    "experiment before acting.", 1, "echo"),

(r"A clinic trials a new physiotherapy protocol on 11 patients and reports $p = 0.44$. The "
 r"write-up concludes that the protocol does not work. Which statement best describes what this "
 r"study actually supports?",
 ["The protocol does nothing, since a p-value that large rules out an effect of any size.",
  "The protocol works, but the significance cutoff was set too strictly for it to show.",
  "Either the protocol does nothing, or it does something that a trial of 11 patients had little "
  "chance of detecting, and this study cannot tell those two apart.",
  "The result is uninformative, because 11 patients recruited at a single clinic are almost certainly biased in ways the write-up does not describe anywhere."],
 2, "A large p-value says the data is unsurprising if there were no effect. It is equally "
    "unsurprising if there were a real effect that 11 patients could not resolve. The honest "
    "output of a study this small is a wide interval, not a verdict of no effect.", 1, "echo"),

(r"Two labs test the same drug and both estimate that it lowers blood pressure by about 4 mmHg. "
 r"Lab A has 50 patients and reports $p = 0.07$; Lab B has 5,000 patients and reports "
 r"$p < 0.001$. A colleague says the two studies contradict each other. Do they?",
 ["Yes: one study found an effect and the other failed to find one.",
  "Yes: the larger study is the reliable one and it overturns the smaller.",
  "No: both estimate the same 4 mmHg, and they differ only in how precisely they pin it down.",
  "No, but only if both labs used the same significance cutoff and the same statistical test."],
 2, "The estimate is the finding and the p-value reports how firmly the data pins it down. Both "
    "labs landed on 4 mmHg. Lab A's interval is wide enough to include zero and Lab B's is not, "
    "which is a difference in precision rather than a disagreement about the drug.", 1, "new"),

(r"A company runs an A/B test on a new checkout page with a cutoff of 0.05. The new page is in "
 r"truth slightly better than the old one, but the test returns $p = 0.21$ and the team keeps the "
 r"old page. What has happened?",
 ["A Type I error: they rejected a true null hypothesis.",
  "A Type II error: there was a real effect and the test failed to detect it.",
  "Nothing went wrong, since a p-value above the cutoff proves there is no effect.",
  "The test had high power, which is why it was able to detect no difference here."],
 1, "A Type I error is calling something real when it is not. A Type II error is missing "
    "something that is real, which is what happened here. Power is the probability of avoiding a "
    "Type II error, and the fix for a test like this is more data, not a looser cutoff.",
 1, "new"),

# =====================================================================
# UNIT 2
# =====================================================================
(r"What makes a model a probability model rather than a non-probability one?",
 ["Its predictions are constrained to lie between 0 and 1.",
  "It states a distribution for the outcome, which is what standard errors, intervals and AIC "
  "are then derived from.",
  "It is fitted by maximising a likelihood function rather than by minimising a sum of squared errors across the rows.",
  "It requires that the predictors be independent of one another before it can be fitted."],
 1, "The distributional assumption is the thing that generates uncertainty. Methods without one "
    "can predict very well and simply have no standard errors, intervals, p-values or AIC to "
    "offer, because there is no likelihood to compute them from.", 2, "echo"),

(r"A manager asks for the p-value on the most important variable in a random forest. What do you "
 r"tell them?",
 ["It is in the forest's output already, reported under variable importance.",
  "It can be recovered by refitting the forest on several bootstrap samples.",
  "A forest states no distribution for the outcome, so there is no p-value for it to report.",
  "Only those variables that appear in a clear majority of the forest's trees have one attached."],
 2, "Importance scores rank how heavily the forest leaned on each column. They are not effects, "
    "they carry no units, and nothing in them is an estimate of uncertainty. A question that "
    "needs a p-value needs a model built on a probability statement.", 2, "echo"),

(r"Two regressions are fitted to the same 400 rows with the same outcome on the same scale. "
 r"Model A has five predictors and AIC 1842. Model B has those five plus four more and AIC 1831. "
 r"What does this support?",
 ["Model B is preferred: AIC already charges for the extra parameters, and it still came out 11 "
  "lower.",
  "Model A is preferred, because AIC rewards simplicity and model A has fewer predictors in it.",
  "Model B fits better, but AIC cannot say whether the four extra predictors were worth adding.",
  "Neither is preferred, because a difference of 11 in AIC is too small to be meaningful here."],
 0, "AIC is a likelihood penalised by the number of parameters, so the four extra columns have "
    "already been paid for in the 1831. A lower AIC on the same rows and the same outcome is "
    "evidence the additions earned their place; a difference of 11 is a substantial one.",
 2, "echo"),

(r"You are modelling how many insurance claims each policy files in a year. Most policies file "
 r"none, a few file one or two, and a handful file more. What does the nature of this outcome "
 r"rule out?",
 ["Any model that mixes categorical predictors with numeric ones in the same fit.",
  "Ordinary linear regression, which will happily predict a negative number of claims and "
  "assumes a spread that does not grow with the average.",
  "Tree-based methods, which need a continuous outcome and cannot handle whole numbers.",
  "Any model that reports a coefficient, since counts have to be modelled as rates per unit of exposure and a coefficient cannot be read on a count scale."],
 1, "A count is a whole number bounded below at zero, and its spread usually rises with its "
    "mean. A straight line will predict $-0.4$ claims for a safe policy without complaint, and "
    "its intervals assume a constant spread the data does not have. Trees handle counts fine.",
 2, "new"),

(r"A model will be rerun every night for two years, and any single prediction it makes may be "
 r"queried by the customer it concerns. What does that fact alone push you toward?",
 ["Whichever model has the lowest cross-validated error, whatever form it takes.",
  "A model whose output for one case can be explained to the person it is about.",
  "A random forest, because averaging many trees makes it the most stable under retraining.",
  "Whichever model has the fewest predictors, since fewer columns are easier to maintain."],
 1, "An output that has to be defended one case at a time has to be explainable one case at a "
    "time. That is a constraint on the family of model you choose, and it is often worth giving "
    "up some accuracy to satisfy it.", 2, "new"),

# =====================================================================
# UNIT 3  (four questions on the fertilizer figure)
# =====================================================================
(r"An agronomist has 280 plots and fits $\text{yield} = \beta_0 + \beta_1\,\text{fertilizer} + "
 r"\varepsilon$ by least squares. Both panels come from that fit. What is wrong?",
 ["Nothing is wrong here; the residuals are centred on zero all the way across the fitted range.",
  "The spread of the residuals grows as the fitted yield grows.",
  "The relationship bends and a straight line cannot follow it, which the arc in the residuals "
  "shows.",
  "A small number of plots at the high end are pulling the fitted line upward."],
 2, "The left panel shows yield rising, flattening and then falling, and the straight line cuts "
    "through it. The right panel is the same fact stated as residuals: negative at both ends and "
    "positive in the middle, which is the signature of a curve the line could not follow.",
 3, "new", ("fig_mc_yield_curve.pdf", "0.94", 4)),

(r"The co-op wants a prediction of yield for a plot given 240 kg of fertilizer per hectare. What "
 r"will this fitted line do at that value?",
 ["It will predict too high, because the residuals at the top of the fitted range are negative.",
  "It will predict too low, because the residuals at the top of the fitted range are positive.",
  "It will be about right, since the line passes through the middle of the data overall.",
  "It cannot predict there at all, because 240 kg lies outside the range of the data."],
 0, "At the right-hand end of the residual plot the points sit below zero, which means the "
    "actual yields there fall short of what the line predicts. The bend has turned downward and "
    "the line is still climbing, so its prediction at 240 kg is too optimistic.", 3, "new"),

(r"Which model would you fit instead?",
 [r"$\text{yield} = \beta_0 + \beta_1\,\text{fertilizer} + \beta_2\,\text{fertilizer}^2 + "
  r"\varepsilon$, which can rise and then fall.",
  r"$\log(\text{yield}) = \beta_0 + \beta_1\,\text{fertilizer} + \varepsilon$, which handles a "
  r"spread that grows.",
  r"The same straight line, fitted only on the plots given less than 150 kg per hectare.",
  r"$\text{yield} = \beta_0 + \beta_1\,\text{fertilizer} + \varepsilon$ with the most extreme "
  r"plots removed first."],
 0, "A squared term lets the fitted curve rise, flatten and come back down, which is the shape "
    "the data has. Logging the outcome addresses a growing spread and this is not that. "
    "Restricting the range or deleting points hides the problem rather than modelling it.",
 3, "new"),

(r"A colleague suggests modelling $\log(\text{yield})$ instead of adding a squared term. What "
 r"would settle which of the two to use?",
 ["Whichever model has the higher $R^2$ on these 280 plots.",
  "Whichever model has fewer parameters, since both are attempts at the same thing.",
  "Fit both and compare the residual plots: the version that leaves no pattern behind is the one "
  "that matched the shape.",
  "Neither can be chosen from this data, because the two models have different outcomes and so cannot be compared at all."],
 2, "The residual plot is what diagnosed the problem, so it is what judges the fix. $R^2$ cannot "
    "settle it here, since the two models have different outcomes and their $R^2$ values are not "
    "comparable. Subject knowledge helps too: fertilizer that eventually harms yield is a peak, "
    "not a flattening.", 5, "echo"),

(r"A regression of delivery cost on distance gives $\widehat{\text{cost}} = 4.10 + "
 r"1.35\,\text{miles}$. What does the 1.35 mean?",
 ["Deliveries cost about \\$1.35 each on average across the whole fleet.",
  "About 135\\% of the variation in cost is accounted for by the distance driven.",
  "Each additional mile is associated with about \\$1.35 more cost.",
  "A typical prediction from this model is off by about \\$1.35 in either direction."],
 2, "A slope is a rate, in outcome units per predictor unit: dollars per mile. Stating the units "
    "is most of the interpretation, and the \\$4.10 intercept is the part that does not depend "
    "on distance at all.", 3, "echo"),

(r"A model of employee salary includes department, which has six levels, and the output lists "
 r"five department coefficients. What happened to the sixth?",
 ["It was dropped from the model for being statistically insignificant.",
  "It is the baseline: the five printed coefficients each compare their department with it.",
  "It was absorbed into the intercept along with the other five departments.",
  "Its coefficient came out as exactly zero, so the software leaves it out of the printed table."],
 1, "One level has to serve as the reference or the six columns would be redundant with the "
    "intercept. Each printed coefficient is the difference between its department and that "
    "reference, holding the other predictors fixed.", 3, "echo"),

(r"An analyst regresses house price on lot size alone and gets a slope of $+\$320$ per hundred "
 r"square feet of lot. Adding interior floor area to the model changes the lot-size slope to "
 r"$-\$45$. Both coefficients have small p-values. What is the best explanation?",
 ["One of the two fits must have been computed incorrectly somewhere along the way.",
  "A sign flip of this size shows the sample is too small for either fit to be trusted.",
  "Larger lots tend to carry larger houses, so the first slope was partly measuring floor area; "
  "the second compares houses that have the same floor area.",
  "Lot size turns out to have no real relationship with price once the size of the house standing on it is accounted for, so the first slope was simply wrong."],
 2, "The two slopes answer different questions. The first compares all houses, big lots against "
    "small. The second compares houses of the same interior size, where a bigger lot means a "
    "smaller house on it. When the omitted variable is related to both, adjusting for it can "
    "move a coefficient a long way, including through zero.", 3, "echo"),

(r"A utility models monthly electricity use for 500 homes, where $\text{pool}$ is 1 if the home "
 r"has a swimming pool and 0 otherwise: "
 r"$\widehat{\text{kWh}} = 420 + 0.38\,\text{sqft} + 215\,\text{pool}$. "
 r"What does the 215 say?",
 ["Homes with pools use about 215 kWh a month in total.",
  "A home with a pool uses about 215 kWh a month more than a home of the same size without one.",
  "About 215\\% more electricity is used by homes with pools than by comparable homes without.",
  "Adding a pool to a home causes its monthly use to rise by about 215 kWh."],
 1, "The coefficient on a 0/1 predictor is the gap between the two groups with the other "
    "predictors held fixed, so it is a comparison at equal floor area. It is a comparison and not "
    "a consequence: homes with pools may differ in other ways this model never measured.",
 3, "new"),

(r"The same team refits the model and allows the effect of size to differ: "
 r"$\widehat{\text{kWh}} = 455 + 0.33\,\text{sqft} + 90\,\text{pool} + "
 r"0.07\,(\text{sqft} \times \text{pool})$. "
 r"For a home with a pool, how much does an extra square foot add?",
 ["0.07 kWh, which is the coefficient on the product term.",
  "0.33 kWh, since that is the coefficient on floor area.",
  "0.40 kWh, the floor-area coefficient plus the product term.",
  "0.33 kWh for the first 90 square feet and 0.40 kWh after that."],
 2, "Set $\\text{pool}=1$ and collect the terms in sqft: $0.33 + 0.07 = 0.40$. With no pool the "
    "rate is 0.33. The 90 is the gap between the two groups at zero square feet, which is why an "
    "interaction changes what the main effect means.", 3, "new"),

# =====================================================================
# UNIT 4
# =====================================================================
(r"A courier quotes one customer a delivery time for their single parcel. Which band belongs in "
 r"the quote?",
 ["Band 1, the wider one.",
  "Band 2, the narrower one.",
  "Whichever of the two is narrower at that particular value of $x$.",
  "Neither of them, since a quote to a customer should be a single number."],
 0, "One customer is one case, so the parcel-to-parcel variation is part of what they are "
    "asking about. Band 2 describes where the average sits and is far too narrow to promise to "
    "any individual.", 4, "echo", ("fig_mc_intervals.pdf", "0.62", 2)),

(r"Why is band 1 wider than band 2 at every value of $x$?",
 ["Band 1 was drawn at a higher confidence level than band 2.",
  "Band 2 covers only the uncertainty about where the line sits; band 1 also covers how far an "
  "individual case falls from the line.",
  "Band 1 is wider only because this particular sample is small; with enough data collected the two bands would eventually coincide.",
  "Band 2 leaves out the uncertainty in the slope, which band 1 includes."],
 1, "There are two sources of error and the bands count different ones. Both have to allow for "
    "the fitted line being in slightly the wrong place. Only the prediction band also has to "
    "allow for the scatter of individual cases about it, which is why more data shrinks band 2 "
    "toward the line and leaves band 1 near the spread of the data.", 4, "new"),

(r"A team reports that their delivery-time model is typically off by 3.2 minutes, measured by "
 r"5-fold cross-validation. The operations manager asks whether next month's deliveries will "
 r"really be off by about 3.2 minutes. What is the honest answer?",
 ["Yes: cross-validation measures error on held-out rows, so it applies to any future delivery.",
  "Yes, provided the model is refitted on the full dataset before next month begins.",
  "It estimates the error on new deliveries drawn from the same process, and it carries no "
  "promise if routes, staffing or demand change.",
  "No: cross-validation measures how well the model fits rather than how well it predicts, so it says nothing at all about next month."],
 2, "Held-out error is an honest estimate for cases like the ones already seen. It is not a "
    "guarantee about a month in which the thing being modelled has changed, and saying so is "
    "part of reporting the number.", 4, "new"),

(r"Adding four columns of random numbers to a model raises the in-sample $R^2$ from 0.704 to "
 r"0.709. What does that tell you?",
 ["The four columns must carry a small amount of real signal after all, even if not very much.",
  "Nothing: in-sample $R^2$ cannot fall when a column is added, whatever the column contains.",
  "The model was underfitted before the four columns were put in.",
  "The columns should be kept, since the fit to the data improved."],
 1, "In-sample $R^2$ is non-decreasing in the number of predictors, so a rise is not evidence "
    "about anything. AIC charges for the extra parameters, and error on rows the model has not "
    "seen asks the question that matters.", 4, "echo"),

(r"A lasso fit, with its penalty chosen by cross-validation, sends the coefficient on "
 r"\texttt{store\_size} to exactly zero. What does that establish?",
 ["That store size has no relationship with the outcome.",
  "That store size would also come out insignificant in an ordinary regression on the same rows and the same outcome.",
  "That store size did not earn its keep against this penalty, in this sample, beside these "
  "other columns.",
  "That store size is uncorrelated with the other predictors in the model."],
 2, "A zero is the product of one penalty strength, one sample, and the particular set of other "
    "columns present. Change any of the three and the variable can come back. It is a decision "
    "about this fit, not a finding about the world.", 4, "echo"),

(r"A retail chain fits a model of monthly revenue across 240 stores. The executive team uses it "
 r"to decide where to open next and how heavily to staff. Which two predictors does this data "
 r"fail to distinguish from no effect at all?",
 ["Parking spaces and loyalty members.",
  "Staff on duty and parking spaces.",
  "Competitor within 1 mile and loyalty members.",
  "Floor area and staff on duty."],
 0, "Those are the two whose intervals cross the dashed zero line: parking spaces runs from "
    "$-0.62$ to $+0.86$ and loyalty members from $-0.54$ to $+1.46$. The other three intervals "
    "sit entirely on one side of zero.", 4, "new", ("fig_mc_coefplot.pdf", "0.72", 2)),

(r"The team is deciding whether to pay a premium for sites with more parking. What does this "
 r"model support?",
 ["Parking does not affect revenue, so they should not pay a premium for it.",
  "Parking adds about \\$120 a month per space, so a small premium for a site with more of them is justified.",
  "The data cannot resolve what a parking space is worth: anything from a modest loss to a "
  "modest gain is still on the table.",
  "Parking should be dropped from the model entirely before any decision about new sites is taken on the basis of it."],
 2, "An interval straddling zero means the study could not pin the effect down, which is "
    "different from showing there is none. For a decision with money attached, that is the "
    "finding to report, together with what it would take to answer the question properly.",
 4, "new"),

(r"In this chain's data, floor area runs from 1,800 to 9,400 square feet and staff on duty runs "
 r"from 3 to 14. A proposed new store would have 2,100 square feet and 13 staff. Both values sit "
 r"inside their own ranges. Is a prediction for it safe?",
 ["Yes: checking that each predictor falls inside its own observed range is exactly what guards against extrapolation, and both of these values pass that check.",
  "Yes, provided the model's $R^2$ is comfortably high.",
  "Not necessarily: small stores are unlikely to have been staffed that heavily, so that "
  "combination may never have occurred even though each value is ordinary on its own.",
  "Not necessarily, but only if the two predictors turn out to be uncorrelated."],
 2, "Correlated predictors fill a narrow band rather than a rectangle. A 2,100 square foot store "
    "with 13 staff may be a combination the chain has never operated, and the model's prediction "
    "there rests on the shape that was assumed rather than on any store it has seen.",
 4, "echo"),

# =====================================================================
# UNIT 5
# =====================================================================
(r"Both panels come from the same 320 repair jobs. The left fits "
 r"$\text{cost} = \beta_0 + \beta_1\,\text{size} + \varepsilon$ and the right fits "
 r"$\log(\text{cost}) = \beta_0 + \beta_1\,\text{size} + \varepsilon$. What could explain the "
 r"difference between them?",
 ["The largest jobs were dropped before the second model was fitted.",
  "Repair cost varies by a percentage of the job rather than by a fixed number of dollars, and "
  "the log turns that multiplicative spread into a constant one.",
  "The second model has more predictors in it, so less variation is left over to show up in the residuals, which is why the band looks tighter.",
  "The residuals in the right panel were standardised, which rescales the vertical axis."],
 1, "On the raw scale a big job's error is big in dollars and a small job's is small, which is "
    "the fan in the left panel. Taking logs makes a 10\\% miss the same distance everywhere, so "
    "the band evens out. Every interval and p-value from the fit assumes the even version.",
 5, "new", ("fig_mc_fan_fix.pdf", "0.80", 2)),

(r"In the right-hand model the coefficient on job size is $0.18$. Which is the correct "
 r"interpretation?",
 ["Each extra unit of job size adds about \\$0.18 to the repair cost.",
  "Each extra unit of job size adds about 20\\% to the repair cost.",
  "Job size accounts for about 18\\% of the variation in repair cost.",
  "Each 1\\% increase in job size adds about 0.18\\% to the repair cost."],
 1, "The outcome is logged and the predictor is not, so the coefficient is a percentage change "
    "per unit: $e^{0.18}-1$ is about 0.20. Option D would be right only if job size had been "
    "logged too, and option A reads a logged coefficient as if it were in dollars.", 5, "echo"),

(r"A dispatcher has 2,600 deliveries, with the time written down by the driver on arrival, "
 r"against a 30 minute promise to the customer. Before fitting anything, what does this picture "
 r"tell you?",
 ["That most deliveries arrive on time, which is the key fact for the model.",
  "That delivery time should be logged, since the distribution is skewed to the right.",
  "That the recorded time is not the true time near 30 minutes, so a model of this column will "
  "inherit whatever the drivers did when they were close to the promise.",
  "That deliveries recorded at over 30 minutes should be dropped, since they are clearly a "
  "different population and will distort any model fitted to all of them."],
 2, "A pile just under the promise and a dip just over it is a fact about how the number was "
    "written down, not about how long the trips took. Anything fitted to this column estimates "
    "recorded time, and the gap between that and real time is widest exactly where the business "
    "cares most.", 5, "new", ("fig_mc_threshold.pdf", "0.70", 1)),

(r"This tree was grown on jobs with $x$ between 1 and 8. What does it predict to the right of "
 r"the dashed line?",
 ["It extends the upward trend it found among the largest jobs it saw.",
  "It returns the average of the training rows in its right-most region, unchanged, however far "
  "out you go.",
  "It returns an error, since the value lies outside the range it was grown on.",
  "It returns the overall average of all the training rows, since no region of the tree matches."],
 1, "A tree is flat outside its range by construction. The case falls into the right-most leaf "
    "and receives that leaf's average, so the extra $x$ does nothing at all. A line would at "
    "least keep going; neither is trustworthy, and the tree gives no sign that it has run out of "
    "data.", 5, "new", ("fig_mc_tree_steps.pdf", "0.62", 1)),

(r"What does a single split in a regression tree do?",
 ["It fits a separate straight line on each side of the cut point.",
  "It tests whether the two groups differ and keeps the split when $p < 0.05$.",
  "It divides the rows into two groups and predicts each group's own average.",
  "It locates the point at which the outcome changes direction most sharply."],
 2, "A split picks one variable and one cut point and predicts the average of the rows on each "
    "side. The machine tries every variable and every cut and keeps whichever leaves the two "
    "groups most alike inside. There is no test involved, and no line.", 5, "echo"),

(r"A tree is fitted to restaurant wait times. Its first split is on party size, at six people. "
 r"Among parties of six or more it then splits on whether the booking was on a weekend. Among "
 r"parties smaller than six it never asks about the weekend at all. What does that suggest "
 r"adding to a regression?",
 [r"A squared term in party size, $\text{size}^2$.",
  r"An indicator for parties of six or more.",
  r"The weekend indicator on its own, since the tree clearly made use of it somewhere.",
  r"A product term $\text{weekend} \times \text{size}$, so the weekend effect can differ with "
  r"party size."],
 3, "The tree used the weekend only inside one branch, which is its way of saying that what the "
    "weekend does depends on the size of the party. A product term lets the regression estimate "
    "that, and unlike the tree it returns a coefficient with an interval and a p-value.",
 5, "new"),

(r"A utility has five years of monthly bills for 8,000 households, with floor area, number of "
 r"occupants, heating type, and whether the home has solar panels. They want to estimate how much "
 r"solar reduces a household's bill, with a number they can defend. In what order would you work?",
 ["Plot the bills against the main predictors; fit the model; check the residuals and repair the shape if it is wrong; report the solar coefficient with its interval, and what it does not settle.",
  "Fit the model; report the solar coefficient with its interval, and what it does not settle; plot the bills against the main predictors; check the residuals and repair the shape if it is wrong.",
  "Fit the model; plot the bills against the main predictors; check the residuals and repair the shape if it is wrong; report the solar coefficient with its interval, and what it does not settle.",
  "Plot the bills against the main predictors; fit the model; report the solar coefficient with its interval, and what it does not settle; check the residuals and repair the shape if it is wrong."],
 0, "Looking first tells you what shape to fit and what is odd about the data. Checking the "
    "residuals before reporting is what tells you whether the interval you are about to quote "
    "means anything. Reporting first and checking later means the number is already out in the "
    "world when you find out it was wrong.", 5, "new"),
]
