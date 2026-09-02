#!/usr/bin/env python3
"""Unit 8 --- Categorical Outcomes: code companion + homework."""
from nblib import CodeNB, HW

# =====================================================================
# CODE COMPANION
# =====================================================================
nb = CodeNB(8, "Categorical Outcomes",
            "Rates with honest intervals, a chi-square you can compute by hand, Simpson's paradox "
            "reproduced from the real Berkeley data, and a classifier whose threshold is chosen by "
            "money instead of by habit.")

nb.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.proportion import proportion_confint, proportions_ztest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve

rng = np.random.default_rng(220)
plt.rcParams["figure.figsize"] = (7, 3.5)""")

nb.section("1. A percentage is an estimate too",
           "Every rate on every dashboard has a standard error. Most dashboards do not show it.")
nb.code("""for x, n in [(12, 300), (120, 3000), (2, 20), (0, 50)]:
    p = x/n
    lo, hi = proportion_confint(x, n, method="wilson")
    print(f"{x:>4}/{n:<5} = {p:6.2%}   95% CI [{lo:6.2%}, {hi:6.2%}]   width {hi-lo:6.2%}")

print("\\nNote the last row: 0 out of 50 does NOT mean 'never'.")
print(f"The rule of three says the rate could plausibly be as high as 3/50 = {3/50:.1%}")""")

nb.section("2. The same difference, three ways",
           "A campaign moves conversion from 2.0% to 2.4%. Watch how differently the same fact "
           "can be reported.")
nb.code("""p1, p2 = 0.020, 0.024
odds = lambda p: p/(1-p)
print(f"absolute difference : {100*(p2-p1):+.1f} percentage points")
print(f"relative difference : {100*(p2/p1 - 1):+.0f}%")
print(f"odds ratio          : {odds(p2)/odds(p1):.2f}")
print("\\nAll three are true. They will produce three different meetings.")

# And whether it is even distinguishable from noise:
for n in [500, 5_000, 50_000]:
    count1, count2 = int(p1*n), int(p2*n)
    stat, pval = proportions_ztest([count2, count1], [n, n])
    print(f"n = {n:>6} per arm: p-value = {pval:.3f}")""")
nb.md("The effect never changed. Only the sample size did. A '20% lift' is a headline, a p-value "
      "is a statement about sample size, and neither one tells you whether to ship.")

nb.section("3. Chi-square, computed by hand and then by library")
nb.code("""credit = pd.read_csv("https://richardson.byu.edu/220/credit_risk.csv")
tab = pd.crosstab(credit["loan_intent"], credit["loan_status"])
print(tab, "\\n")
print("default rate by purpose:")
print((tab[1]/(tab[0]+tab[1])).sort_values().round(3), "\\n")

expected = np.outer(tab.sum(axis=1), tab.sum(axis=0)) / tab.values.sum()
chi2_hand = ((tab.values - expected)**2 / expected).sum()
dof_hand = (tab.shape[0]-1)*(tab.shape[1]-1)
chi2, p, dof, exp = stats.chi2_contingency(tab)
print(f"by hand : chi2 = {chi2_hand:.2f}, df = {dof_hand}")
print(f"library : chi2 = {chi2:.2f}, df = {dof}, p = {p:.2e}")

resid = (tab.values - expected)/np.sqrt(expected)
print("\\nstandardized residuals (which cells drive it):")
print(pd.DataFrame(resid, index=tab.index, columns=["repaid", "defaulted"]).round(2))""")
nb.md("The p-value says 'not independent.' The *residuals* say which purposes are unusual and in "
      "which direction, and the rate table says how big the difference is. Report all three. The "
      "p-value alone is the least informative of them.")

nb.section("4. Simpson's paradox, from the real 1973 Berkeley data")
nb.code("""dept = ["A", "B", "C", "D", "E", "F"]
men_app = np.array([825, 560, 325, 417, 191, 373]); men_adm = np.array([512, 353, 120, 138, 53, 22])
wom_app = np.array([108,  25, 593, 375, 393, 341]); wom_adm = np.array([ 89,  17, 202, 131, 94, 24])

print(f"OVERALL: men {men_adm.sum()/men_app.sum():.1%} admitted, "
      f"women {wom_adm.sum()/wom_app.sum():.1%} admitted\\n")
print(f"{'dept':>5} {'men rate':>10} {'women rate':>12} {'women favored?':>16} {'dept selectivity':>18}")
for i, d in enumerate(dept):
    mr, wr = men_adm[i]/men_app[i], wom_adm[i]/wom_app[i]
    sel = (men_adm[i]+wom_adm[i])/(men_app[i]+wom_app[i])
    print(f"{d:>5} {mr:>10.1%} {wr:>12.1%} {str(wr > mr):>16} {sel:>18.1%}")

print("\\nWhere did women apply? Share of each department's applicants who were women:")
for i, d in enumerate(dept):
    share = wom_app[i]/(wom_app[i]+men_app[i])
    sel = (men_adm[i]+wom_adm[i])/(men_app[i]+wom_app[i])
    print(f"  dept {d}: {share:5.1%} women, and the department admits {sel:5.1%} of applicants")""")
nb.md("Women were admitted at similar or higher rates in most departments, yet lower overall, "
      "because they applied disproportionately to the departments that admit almost nobody. The "
      "pooled number is a weighted average with the wrong weights.")

nb.section("5. A classifier, and the threshold that actually pays",
           "Predicting diabetes. The model is the easy part. The threshold is the decision.")
nb.code("""dia = pd.read_csv("https://richardson.byu.edu/220/diabetes.csv")
feats = ["Glucose", "BMI", "Age", "Pregnancies", "BloodPressure"]
X, y = dia[feats].values, dia["Outcome"].values
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.35, random_state=220, stratify=y)
model = LogisticRegression(max_iter=5000).fit(Xtr, ytr)
p_hat = model.predict_proba(Xte)[:, 1]

print("odds ratios (per one unit of the predictor):")
for name, coef in zip(feats, model.coef_[0]):
    print(f"  {name:<15} {np.exp(coef):.3f}")

base = yte.mean()
print(f"\\nbase rate in the test set          : {base:.1%}")
print(f"accuracy of always predicting 'no' : {1-base:.1%}   <-- the number to beat")
print(f"accuracy of the model at 0.5       : {((p_hat >= .5) == yte).mean():.1%}")
print(f"AUC                                : {auc(*roc_curve(yte, p_hat)[:2]):.3f}")""")
nb.code("""COST_MISS, COST_FALSE_ALARM = 500, 60
thresholds = np.linspace(0.02, 0.98, 200)
costs = [(((p_hat < t) & (yte == 1)).sum()*COST_MISS +
          ((p_hat >= t) & (yte == 0)).sum()*COST_FALSE_ALARM)/len(yte) for t in thresholds]
best = thresholds[int(np.argmin(costs))]

plt.plot(thresholds, costs, color="#4878a8", lw=2)
plt.axvline(0.5, ls="--", color="#7f8c8d", label="default 0.5")
plt.axvline(best, color="#2e8b57", lw=2, label=f"cost-minimizing {best:.2f}")
plt.xlabel("threshold"); plt.ylabel("expected cost per patient ($)"); plt.legend(); plt.show()

cost_at = lambda t: (((p_hat < t) & (yte == 1)).sum()*COST_MISS +
                     ((p_hat >= t) & (yte == 0)).sum()*COST_FALSE_ALARM)/len(yte)
print(f"cost at 0.50 : ${cost_at(0.5):.2f} per patient")
print(f"cost at {best:.2f} : ${cost_at(best):.2f} per patient")
print(f"rule of thumb threshold = cost_FP/(cost_FP+cost_FN) = "
      f"{COST_FALSE_ALARM/(COST_FALSE_ALARM+COST_MISS):.2f}")

tn, fp, fn, tp = confusion_matrix(yte, (p_hat >= best).astype(int)).ravel()
print(f"\\nAt the chosen threshold: flag {tp+fp} of {len(yte)} patients; "
      f"{tp/(tp+fp):.0%} of those flagged have diabetes; we catch {tp/(tp+fn):.0%} of real cases.")""")

nb.section("6. Is a predicted 30% really 30%?")
nb.code("""bins = np.linspace(0, 1, 11)
idx = np.digitize(p_hat, bins) - 1
print(f"{'predicted':>12} {'actual':>10} {'n':>5}")
xs, ys = [], []
for b in range(10):
    m = idx == b
    if m.sum() >= 8:
        xs.append(p_hat[m].mean()); ys.append(yte[m].mean())
        print(f"{p_hat[m].mean():>12.2f} {yte[m].mean():>10.2f} {m.sum():>5}")

plt.plot([0, 1], [0, 1], "--", color="#7f8c8d", label="perfect calibration")
plt.plot(xs, ys, "o-", color="#4878a8", lw=2, label="this model")
plt.xlabel("predicted probability"); plt.ylabel("observed frequency"); plt.legend(); plt.show()""")
nb.md("If these points sit near the diagonal you may multiply the probabilities by dollars. If "
      "they do not, the model may still *rank* well, but any expected-cost calculation built on "
      "its numbers is fiction.")

nb.write("Code_Unit08_Categorical.ipynb")


# =====================================================================
# HOMEWORK
# =====================================================================
hw = HW(8, "Categorical Outcomes",
        """Answer each problem in the cell(s) provided. Replace *Your answer* with your response
for written parts, and put code in the empty code cells.

The first problem is a **simulation lab** where you construct the paradoxes yourself. The next
three are **real categorical problems with a decision attached**. The last asks what your rates and
thresholds actually justify.

**Data** (all real):

- `https://richardson.byu.edu/220/credit_risk.csv`: consumer loans with a default indicator.
- `https://richardson.byu.edu/220/diabetes.csv`: clinical measurements with a diagnosis.
- `https://richardson.byu.edu/220/insurance_all.csv`: medical charges with smoker and region.""")

hw.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.proportion import proportion_confint, proportions_ztest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve

rng = np.random.default_rng(220)
credit = pd.read_csv("https://richardson.byu.edu/220/credit_risk.csv")
dia = pd.read_csv("https://richardson.byu.edu/220/diabetes.csv")
ins = pd.read_csv("https://richardson.byu.edu/220/insurance_all.csv")
print(credit.shape, dia.shape, ins.shape)""")

# ---------------- P1: simulation lab ----------------
hw.problem(1, """*Simulation lab: build the paradoxes yourself.* Each part constructs a situation
where you know the truth, so the illusion becomes visible.""")
hw.part("a", """Simulate 2,000 A/B tests where both arms have a true conversion rate of exactly
3%, with 800 visitors per arm. Report the fraction where a two-proportion test gives $p < 0.05$,
and the largest "lift" (relative difference) you observe among those significant results.""")
hw.part("b", """Using your Part a results, explain in 2 to 3 sentences why a reported "35% lift, $p =
0.04$" from a small test should not be taken at face value.""", "written")
hw.part("c", """**Build a Simpson's paradox from scratch.** Construct a two-department admissions
scenario where each department admits women at a *higher* rate than men, but the pooled rate is
higher for men. Print the department-level table and the pooled table, and state exactly what
feature of your construction produced the reversal.""")
hw.part("d", """**The rare-event classifier.** Simulate 100,000 cases where 0.5% are fraud, and a
detector that catches 90% of fraud with a 3% false-positive rate. Report the accuracy of the
detector, the accuracy of "predict never," precision, and recall.""")
hw.part("e", """Using Part d, explain why accuracy is nearly useless here, and compute how many
cases a reviewer must examine to find one real fraud.""")
hw.part("f", """Sweep the false-positive rate from 0.1% to 10% in your Part d simulation and plot
precision against it, holding recall fixed. Describe how sensitive the reviewer's workload is to
that one number.""")

# ---------------- P2: real proportions ----------------
hw.problem(2, """*Real data: default rates that a lender will act on.* Use `credit`.""")
hw.part("a", """Compute the default rate and count for each `person_home_ownership` level, with a
95% confidence interval for each. Plot the rates with intervals.""")
hw.part("b", """One group is very small. Report its interval and explain what the width tells a
lender who wants to write a policy about that group.""", "written")
hw.part("c", """Compare the highest- and lowest-rate groups with a formal two-proportion test.
Report the difference in percentage points, the relative difference, the odds ratio, and the
p-value.""")
hw.part("d", """Build the `loan_intent` by `loan_status` contingency table. Compute the expected
counts and chi-square statistic **by hand** (not with `chi2_contingency`), then confirm with the
library. Report the standardized residuals and name the two cells that drive the result.""")
hw.part("e", """Repeat the chi-square test on only the first 150 rows. Report the new p-value and
explain what changed and what did not, and what that demonstrates about significance and sample
size.""")
hw.part("f", """Write the two-sentence summary a lending manager could act on, reporting both the
absolute and relative comparison and one caveat.""", "written")

# ---------------- P3: denominators and Simpson in real data ----------------
hw.problem(3, """*Real data: a regional ranking that reverses.* Use `ins`. Define a "high-cost
person" as one with `charges` above \\$16,000.""")
hw.part("a", """Compute the proportion of high-cost people in each `region`, with intervals. Which
region looks worst?""")
hw.part("b", """Compute the smoking rate in each region. Then compute the high-cost proportion
**within** smokers and within non-smokers, by region.""")
hw.part("c", """Does the regional ranking survive the split? Explain the role of the smoking rate
using the language of lurking variables and weighted averages.""", "written")
hw.part("d", """Standardize: compute what each region's high-cost rate *would* be if every region
had the overall smoking rate. Report the standardized rates and compare the ranking to Part a.""")
hw.part("e", """Write the 3 to 4 sentence explanation you would give the manager of the
worst-looking region.""", "written")

# ---------------- P4: classification and thresholds ----------------
hw.problem(4, """*Real data: a screening model, and the threshold that pays for itself.* Use `dia`
with a train/test split. A missed case costs \\$500 in later complications and an unnecessary
follow-up costs \\$60.""")
hw.part("a", """Fit a logistic regression of `Outcome` on `Glucose`, `BMI`, `Age`, `Pregnancies`,
and `BloodPressure`. Report the coefficients as odds ratios and interpret the `Glucose` one for a
physician.""")
hw.part("b", """On the test set, report the base rate, the accuracy of predicting "no" for
everyone, the model's accuracy at threshold 0.5, and the AUC. Comment on which of those numbers
actually tells you the model is useful.""")
hw.part("c", """Plot the ROC curve and the precision-recall curve with a line at the base rate.
Explain what the base-rate line represents and when the PR curve is the more honest picture.""")
hw.part("d", """Sweep the threshold and plot expected cost per patient. Report the cost-minimizing
threshold, the cost there, the cost at 0.5, and the savings per 1,000 patients screened. Compare
your answer to the rule of thumb $t^* \\approx c_{FP}/(c_{FP}+c_{FN})$.""")
hw.part("e", """State the operating point in plain language for a hospital administrator: how many
patients get flagged, what share of them truly have diabetes, and what share of true cases you
catch.""", "written")
hw.part("f", """Produce a calibration plot. Are the predicted probabilities trustworthy enough to
multiply by dollars? If not, say what you would do before using them in the cost calculation you
just performed.""")

# ---------------- P5: what can we say ----------------
hw.problem(5, """*What can and cannot be said.* Written answers.""")
hw.part("a", """Your Problem 2 analysis found renters default more often. Write the claim the data
supports, and the causal claim it does not, and explain what a lender risks by confusing them.""", "written")
hw.part("b", """The `credit` dataset has a default rate near 50%, far above any real portfolio.
Explain what was probably done to it, and how that distorts (i) the model's predicted probabilities
and (ii) the threshold you chose in Problem 4 if you applied the same logic to lending.""", "written")
hw.part("c", """In Problem 3 the regional ranking changed after adjusting for smoking. Can you now
say which region is "actually worst"? State precisely what standardization does and does not
establish.""", "written")
hw.part("d", """Your Problem 4 threshold came from two cost numbers. Describe how you would obtain
those numbers in a real hospital, and what you would do if stakeholders disagreed about them.""", "written")
hw.part("e", """A vendor pitches a fraud model with 99.4% accuracy and an AUC of 0.995. Write the
four questions you would ask, and say what answer to each would make you walk away.""", "written")

hw.write("Stat_220_HW_Unit08_Categorical.ipynb")
