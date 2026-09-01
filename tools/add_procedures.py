#!/usr/bin/env python3
"""Add two frames to every unit deck.

1. A step-by-step procedure frame: how you actually carry the method out.
2. A closing table of what a student should be able to produce with software and
   an AI assistant, with the function they would reach for. Syntax is not the
   thing being examined; knowing which procedure to run and what the output means
   is.
"""
from pathlib import Path

SLIDES = Path(__file__).resolve().parents[1] / "Slides"

UNITS = {
"Unit_01_Inference": dict(
  proc_title="Running a two-group comparison, start to finish",
  steps=[
    r"\textbf{Write down $\Hzero$, $\Hone$, and $\alpha$ before you look.} One-sided or two-sided is decided here, not later.",
    r"\textbf{Check the design.} Independent groups, or the same subjects measured twice? Paired data goes to a one-sample test on the differences.",
    r"\textbf{Plot both groups} before any test. Look for skew, outliers, and whether the groups are even comparable.",
    r"\textbf{Report $n$, mean, and SD} for each group.",
    r"\textbf{Run Welch's test}, which does not assume equal variances: \texttt{stats.ttest\_ind(a, b, equal\_var=False)}.",
    r"\textbf{Compute the CI for the difference}, $(\xbar_A-\xbar_B) \pm t^{*}\se$, because that is the number you will actually report.",
    r"\textbf{Report all four:} the effect size in real units, the interval, the $p$-value, and $n$.",
  ],
  software=[
    ("One-sample $t$-test against a claimed value", r"\texttt{stats.ttest\_1samp}"),
    ("Two independent groups (Welch, the default choice)", r"\texttt{stats.ttest\_ind(..., equal\_var=False)}"),
    ("Before-and-after on the same subjects", r"\texttt{stats.ttest\_rel}"),
    ("Confidence interval for a mean or a difference", r"\texttt{stats.t.ppf} with $s/\sqrt{n}$"),
    ("Critical value or a $p$-value from $t$", r"\texttt{stats.t.ppf}, \texttt{stats.t.sf}"),
    ("Power, and the $n$ you would need", r"\texttt{statsmodels.stats.power.TTestIndPower}"),
    ("Simulate the null to check any of the above", r"\texttt{rng.normal}, then loop"),
  ]),

"Unit_02_Probability_and_Random_Variables": dict(
  proc_title="Turning a probability question into arithmetic",
  steps=[
    r"\textbf{Name the events in words} and write which conditional you were given.",
    r"\textbf{Ask which one you were asked for.} If it is the other direction, you need Bayes.",
    r"\textbf{Find the base rate.} If nobody stated one, that is your missing input.",
    r"\textbf{Build a table of 10{,}000 cases}: prevalence splits the column, sensitivity and specificity split each row.",
    r"\textbf{Read the answer off the table} as a ratio of counts, not a formula.",
    r"\textbf{Check any multiplication} you did for a shared cause before trusting independence.",
    r"\textbf{If it is a quantity rather than an event}, report a mean \emph{and} an SD, and simulate rather than plugging in averages.",
  ],
  software=[
    ("Simulate any event and estimate its probability", r"\texttt{rng.random}, \texttt{rng.integers}"),
    ("Exact binomial probabilities and tails", r"\texttt{stats.binom.pmf}, \texttt{.cdf}, \texttt{.sf}"),
    ("Counts over a window (Poisson)", r"\texttt{stats.poisson.pmf}, \texttt{.sf}"),
    ("Waiting times", r"\texttt{stats.expon}"),
    ("A natural-frequency screening table", "a few lines of arithmetic, no library"),
    ("Mean and SD of a simulated quantity", r"\texttt{.mean()}, \texttt{.std(ddof=1)}"),
    ("Expected cost or profit under uncertainty", "simulate the scenarios, then average"),
  ]),

"Unit_03_Normal_and_the_CLT": dict(
  proc_title="Deciding whether a normal-based answer is safe",
  steps=[
    r"\textbf{Name the estimate}, not the data: a mean, a difference, a proportion?",
    r"\textbf{Plot the raw data once} to see skew, gaps, and outliers. Do not run a normality test.",
    r"\textbf{Count the informative observations}, which for a proportion means successes and failures, not rows.",
    r"\textbf{Ask what one independent observation is}, and reduce $n$ to that.",
    r"\textbf{Convert to a $z$-score} when you need to compare across units: $z=(x-\mu)/\sigma$.",
    r"\textbf{If in doubt, simulate.} Resample your own data and look at the shape of the estimate.",
    r"\textbf{Report the SE and the interval}, and say which assumption is carrying the weight.",
  ],
  software=[
    ("Normal probabilities and percentiles", r"\texttt{stats.norm.cdf}, \texttt{stats.norm.ppf}"),
    ("Standardize a value", r"\texttt{(x - mean) / sd}"),
    ("Check normality by eye", r"\texttt{stats.probplot}, plus a histogram"),
    ("Build a sampling distribution yourself", r"\texttt{rng.integers} to resample, then \texttt{.mean(axis=1)}"),
    ("Standard error of a mean", r"\texttt{s / np.sqrt(n)}"),
    ("Check whether an interval really covers 95\\%", "simulate many samples and count"),
    ("Measure dependence in a series", r"\texttt{Series.autocorr(1)}"),
  ]),

"Unit_04_Estimation_and_the_Bootstrap": dict(
  proc_title="Estimating anything, with an interval",
  steps=[
    r"\textbf{Write the target in words and units}, for example ``median revenue per active user.''",
    r"\textbf{Identify the independent unit}: users, stores, or weeks. This sets your real $n$.",
    r"\textbf{Choose the statistic from the decision}, not from convenience.",
    r"\textbf{Compute the estimate.}",
    r"\textbf{Resample with replacement} a few thousand times, recomputing the statistic each time.",
    r"\textbf{Take the SD of those values} for the standard error and the 2.5 and 97.5 percentiles for the interval.",
    r"\textbf{Shrink toward a sensible prior} if any group has a small sample, then report estimate, interval, and the shakiest assumption.",
  ],
  software=[
    ("Resample rows with replacement", r"\texttt{rng.integers(0, n, size=(B, n))}"),
    ("Bootstrap SE and percentile interval", r"\texttt{boot.std()}, \texttt{np.percentile(boot, [2.5, 97.5])}"),
    ("Bootstrap a median, a percentile, or a ratio", "the same loop, a different statistic"),
    ("Resample clusters instead of rows", "sample the group labels, then pool their rows"),
    ("Maximum likelihood for a simple model", r"\texttt{scipy.optimize.minimize} on the negative log-likelihood"),
    ("Bias, variance, and MSE of an estimator", "simulate from a known truth and compare"),
    ("Shrunken group estimates", r"\texttt{(sum + k*overall) / (n + k)}"),
  ]),

"Unit_05_Regression_as_Reasoning": dict(
  proc_title="Fitting and reading a regression",
  steps=[
    r"\textbf{Plot $y$ against $x$ first.} A line on a curved cloud is a wrong answer with a good $p$-value.",
    r"\textbf{Fit it:} \texttt{sm.OLS(y, sm.add\_constant(X)).fit()}, then read \texttt{.summary()}.",
    r"\textbf{Read the slope with its units}, and rescale to something a human feels (per 1{,}000 lbs, not per lb).",
    r"\textbf{Check the slope against its SE}, which is the same estimate-over-noise ratio as always.",
    r"\textbf{Get the interval}, \texttt{.conf\_int()}, and report it rather than the $p$-value alone.",
    r"\textbf{Plot residuals against fitted values} to check the straight-line and constant-spread assumptions.",
    r"\textbf{State the range of $x$ the data covers}, and refuse to predict outside it.",
  ],
  software=[
    ("Simple and multiple regression", r"\texttt{sm.OLS(y, sm.add\_constant(X)).fit()}"),
    ("Formula interface with categories", r"\texttt{smf.ols(\"y \textasciitilde\ x + C(group)\", data)}"),
    ("An interaction", r"\texttt{smf.ols(\"y \textasciitilde\ x * group\", data)}"),
    ("Coefficient intervals", r"\texttt{fit.conf\_int()}"),
    ("Residual diagnostics", r"\texttt{fit.resid} against \texttt{fit.fittedvalues}"),
    ("Correlation between predictors", r"\texttt{df[cols].corr()}"),
    ("Transform a skewed variable", r"\texttt{np.log(y)}, then interpret on the log scale"),
  ]),

"Unit_06_Building_and_Trusting_a_Model": dict(
  proc_title="Building a model you can defend",
  steps=[
    r"\textbf{Split first.} Hold out a test set and do not touch it again until the end.",
    r"\textbf{Fit the simple model} as your benchmark, and always compare against predicting the mean.",
    r"\textbf{Put every preprocessing step inside a pipeline} so it is refit within each fold.",
    r"\textbf{Cross-validate:} \texttt{cross\_val\_score(pipe, X, y, cv=KFold(5, shuffle=True))}.",
    r"\textbf{Tune complexity on the CV curve}, and take the simplest model within one standard error of the best.",
    r"\textbf{Compare candidates on the same folds}, and look at the fold-to-fold spread before declaring a winner.",
    r"\textbf{Touch the test set once} and report that number.",
  ],
  software=[
    ("Train/test split", r"\texttt{train\_test\_split}"),
    ("Cross-validation on the same folds", r"\texttt{KFold(5, shuffle=True, random\_state=...)}"),
    ("Preprocessing that cannot leak", r"\texttt{make\_pipeline(StandardScaler(), model)}"),
    ("Ridge and lasso with the penalty chosen for you", r"\texttt{RidgeCV}, \texttt{LassoCV}"),
    ("A tree, and a forest", r"\texttt{DecisionTreeRegressor}, \texttt{RandomForestRegressor}"),
    ("Feature importance, with its caveats", r"\texttt{model.feature\_importances\_}"),
    ("The one-standard-error rule", "CV mean plus \\texttt{scores.std()/sqrt(k)}"),
  ]),

"Unit_07_Prediction_and_Its_Uncertainty": dict(
  proc_title="Producing a prediction with honest error bars",
  steps=[
    r"\textbf{Name the target and the decision.} What will someone do with this number?",
    r"\textbf{Fit on training data, predict on held-out data}, and keep those residuals.",
    r"\textbf{Take the 5th and 95th percentiles of the held-out residuals} and attach them to the point prediction.",
    r"\textbf{Check coverage} on data used for neither fitting nor calibration: do the 90\% intervals catch 90\%?",
    r"\textbf{Ask which layer dominates}: noise, estimation, model structure, or shift.",
    r"\textbf{Check whether you are extrapolating} past the range of the training data.",
    r"\textbf{Report the point, the interval, and one sentence on when it stops being valid.}",
  ],
  software=[
    ("Predictions from a fitted model", r"\texttt{model.predict(X\_new)}"),
    ("Held-out residuals", r"\texttt{y\_test - model.predict(X\_test)}"),
    ("An empirical prediction interval", r"\texttt{np.percentile(resid, [5, 95])}"),
    ("Confidence versus prediction band in OLS", r"\texttt{fit.get\_prediction(X).conf\_int(obs=True)}"),
    ("Coverage check", "count how often the truth lands inside"),
    ("Estimation wobble via resampling", "refit on bootstrap samples and spread the predictions"),
    ("Turn a predictive distribution into a decision", "simulate outcomes, then average the cost"),
  ]),

"Unit_08_Categorical_Outcomes": dict(
  proc_title="From a rate to a decision",
  steps=[
    r"\textbf{Write the rate as a fraction} and say out loud what the denominator is.",
    r"\textbf{Attach an interval} to every rate you plan to compare: \texttt{proportion\_confint(x, n, method=\"wilson\")}.",
    r"\textbf{Compare two rates} with \texttt{proportions\_ztest}, and report the absolute difference, the relative change, and the odds ratio.",
    r"\textbf{For a table}, compute expected counts and run \texttt{stats.chi2\_contingency}, then read the residuals to see which cells drive it.",
    r"\textbf{Disaggregate} by the obvious lurking variable before publishing a pooled number.",
    r"\textbf{For a model}, fit \texttt{LogisticRegression} and exponentiate the coefficients to get odds ratios.",
    r"\textbf{Choose the threshold from the two error costs}, then report the operating point in plain language.",
  ],
  software=[
    ("Interval for a single proportion", r"\texttt{proportion\_confint(x, n, method=\"wilson\")}"),
    ("Compare two proportions", r"\texttt{proportions\_ztest([x1, x2], [n1, n2])}"),
    ("Contingency table and chi-square", r"\texttt{pd.crosstab}, \texttt{stats.chi2\_contingency}"),
    ("Logistic regression and odds ratios", r"\texttt{LogisticRegression}, then \texttt{np.exp(coef)}"),
    ("Confusion matrix, precision, recall", r"\texttt{confusion\_matrix}, \texttt{classification\_report}"),
    ("ROC, AUC, and precision-recall", r"\texttt{roc\_curve}, \texttt{auc}, \texttt{precision\_recall\_curve}"),
    ("Sweep the threshold on cost", "loop over thresholds and total the two error costs"),
  ]),

"Unit_09_Causal_Thinking": dict(
  proc_title="Answering ``does X cause Y?''",
  steps=[
    r"\textbf{State the intervention precisely.} Who gets what, instead of what?",
    r"\textbf{Name the comparison group.} If there is none, stop.",
    r"\textbf{Draw the diagram} and classify every candidate control as confounder, collider, or mediator.",
    r"\textbf{Ask how treatment was assigned}: randomized, self-selected, or by a rule?",
    r"\textbf{Choose the design that matches the assignment}, and write down the assumption it buys.",
    r"\textbf{Check that assumption explicitly}, for example by plotting pre-treatment trends.",
    r"\textbf{Report the estimate, its uncertainty, and the confounder you could not measure.}",
  ],
  software=[
    ("Adjusted comparison", r"\texttt{smf.ols(\"y \textasciitilde\ treat + covariates\", data)}"),
    ("Estimates within strata", r"\texttt{pd.qcut} then \texttt{groupby}"),
    ("Difference in differences", "four group means, then the difference of the differences"),
    ("Check parallel pre-trends", "plot both series for several periods before treatment"),
    ("Randomized assignment for a rollout", r"\texttt{rng.integers(0, 2, n)} on the unit of assignment"),
    ("Simulate a confounder or a collider", "generate the data yourself and compare estimates"),
    ("Logistic version for a binary outcome", r"\texttt{smf.logit}"),
  ]),

"Unit_10_Bayesian_Reasoning_and_Decisions": dict(
  proc_title="From prior to decision",
  steps=[
    r"\textbf{Write the unknown in words} and say what decision depends on it.",
    r"\textbf{State a prior} from past data, and say where it came from.",
    r"\textbf{Update.} For a rate, a Beta$(a,b)$ prior with $s$ successes and $f$ failures becomes Beta$(a+s,\,b+f)$.",
    r"\textbf{Summarize the posterior}: the mean, and a credible interval from the 2.5 and 97.5 percentiles.",
    r"\textbf{Answer the question actually asked}, such as $\PR{\text{B beats A}}$, by drawing from both posteriors and comparing.",
    r"\textbf{Attach costs} and compute the expected loss of each action.",
    r"\textbf{Re-run under a skeptical and an optimistic prior} and report whether the decision changes.",
  ],
  software=[
    ("Posterior for a rate", r"\texttt{stats.beta(a+s, b+f)}"),
    ("Credible interval", r"\texttt{posterior.ppf([0.025, 0.975])}"),
    ("Draw from a posterior", r"\texttt{posterior.rvs(200\_000)}"),
    ("Probability one variant beats another", r"\texttt{(draws\_b > draws\_a).mean()}"),
    ("Expected loss of a decision", r"\texttt{np.maximum(a - b, 0).mean()}"),
    ("Shrunken group estimates", r"\texttt{(successes + k*p\_bar) / (n + k)}"),
    ("Value of a study", "simulate deciding with and without it, and difference the profits"),
  ]),

"Unit_11_Where_the_Data_Comes_From": dict(
  proc_title="The audit to run before you model anything",
  steps=[
    r"\textbf{Name the population} the decision concerns, and the frame the rows actually came from.",
    r"\textbf{Ask who is missing because of the outcome} you are studying.",
    r"\textbf{Count the missing values per column}, and look for them in disguise: 0, $-1$, 999, empty strings.",
    r"\textbf{Compare rows with missing values to complete rows} on the outcome. If they differ, dropping them changes the population.",
    r"\textbf{Ask what each column really measures}, who recorded it, and when.",
    r"\textbf{Check for breaks over time} in the instrument, the definition, or the pipeline.",
    r"\textbf{Write down what you could not fix}, and put it in the report.",
  ],
  software=[
    ("Missingness by column", r"\texttt{df.isna().sum()}, and \texttt{(df[col] == 0).mean()}"),
    ("Compare responders to non-responders", r"\texttt{groupby} on a missingness indicator"),
    ("A missing-value indicator as a feature", r"\texttt{df[\"x\_missing\"] = df.x.isna().astype(int)}"),
    ("Multiple imputation rather than the mean", r"\texttt{sklearn.impute.IterativeImputer}"),
    ("Stratified and cluster sampling", r"\texttt{groupby(...).sample}"),
    ("Reweight to a known population mix", "weights = population share / sample share"),
    ("Cluster-aware standard errors", "resample the cluster, not the row"),
  ]),

"Unit_12_Putting_It_Together": dict(
  proc_title="The whole workflow, in order",
  steps=[
    r"\textbf{Pin the question} to a decision somebody will make.",
    r"\textbf{Interrogate the data's origin} before you open it: population, frame, who is missing.",
    r"\textbf{Look at the data}: distributions, missingness, outliers, and what one observation is.",
    r"\textbf{Choose the simplest method the question needs}, and say why that one.",
    r"\textbf{Estimate with uncertainty}, using a bootstrap when no formula applies.",
    r"\textbf{Check the assumption most likely to break}, out of sample.",
    r"\textbf{Translate into a recommendation} with the risk and one caveat attached.",
  ],
  software=[
    ("Everything from Units 1 through 11, on demand", "you should not need to be told which"),
    ("Load, inspect, and audit a new dataset", r"\texttt{read\_csv}, \texttt{describe}, \texttt{isna}"),
    ("Compare two groups honestly", r"\texttt{ttest\_ind}, plus an interval"),
    ("Fit and validate a model", r"\texttt{cross\_val\_score} inside a pipeline"),
    ("Attach an interval to any estimate", "bootstrap, or held-out residuals"),
    ("Turn a prediction into a decision", "expected cost over the predictive distribution"),
    ("Say what the analysis cannot support", "no library for this one"),
  ]),
}


def procedure_frame(title, steps):
    items = "\n".join(f"  \\item {s}" for s in steps)
    return (f"\\begin{{frame}}{{{title}}}\n"
            "\\small\n"
            "\\begin{enumerate}\n" + items + "\n"
            "\\end{enumerate}\n"
            "\\end{frame}\n\n")


def software_frame(rows):
    body = "\n".join(f"{task} & {tool} \\\\" for task, tool in rows)
    return (r"""\begin{frame}{What you should be able to do with software}
\small
Nobody is asking you to memorize syntax. You are expected to know \emph{which} procedure the
question calls for, what to hand it, and what the output means. With an AI assistant open, you
should be able to produce any of these and defend the result.
\begin{center}\footnotesize
\begin{tabular}{p{0.44\textwidth} p{0.46\textwidth}}
\toprule
\textbf{You should be able to} & \textbf{What you would reach for} \\
\midrule
""" + body + r"""
\bottomrule
\end{tabular}
\end{center}
\vspace{0.2em}
\centering\small
If you cannot say what the output means, the fact that you produced it is worth nothing.
\end{frame}

""")


for stem, spec in UNITS.items():
    path = SLIDES / f"{stem}.tex"
    s = path.read_text()
    if "What you should be able to do with software" in s:
        print(f"{stem:<46} already done, skipped")
        continue

    proc = procedure_frame(spec["proc_title"], spec["steps"])
    soft = software_frame(spec["software"])

    if stem == "Unit_12_Putting_It_Together":
        s = s.replace(r"\begin{frame}{The master trap list (1 of 2)}",
                      proc + r"\begin{frame}{The master trap list (1 of 2)}", 1)
        s = s.replace(r"\begin{frame}{The last slide}", soft + r"\begin{frame}{The last slide}", 1)
    else:
        s = s.replace(r"\begin{frame}{The traps, all in one place}",
                      proc + r"\begin{frame}{The traps, all in one place}", 1)
        s = s.replace(r"\begin{frame}{Where we go next}", soft + r"\begin{frame}{Where we go next}", 1)

    path.write_text(s)
    print(f"{stem:<46} procedure + software frames added")
