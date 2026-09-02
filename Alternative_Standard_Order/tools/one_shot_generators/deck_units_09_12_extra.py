#!/usr/bin/env python3
"""Extra frames for Units 9-12, bringing each to a full three days."""
import pathlib
import adapt

SL = adapt.OUT

# ---------------- UNIT 9 ----------------
p = SL / "Unit_09_Causal_Thinking.tex"; s = p.read_text()

# the added table was a hair too tall
s = s.replace(r"""Confounder & causes both $X$ and $Y$ & \textbf{Control for it.} Leaving it out biases the estimate
in a direction you can often sign. \\
Collider & is caused by both $X$ and $Y$ & \textbf{Never control for it}, and never select your
sample on it. Controlling creates an association from nothing. \\
Mediator & $X$ causes it, it causes $Y$ & \textbf{Leave it out} for the total effect. Include it
only if you deliberately want the effect through some \emph{other} channel. \\""",
r"""Confounder & causes both $X$ and $Y$ & \textbf{Control for it.} Omitting it biases the
estimate. \\
Collider & is caused by both $X$ and $Y$ & \textbf{Never control for it}, and never select the
sample on it. \\
Mediator & $X$ causes it, it causes $Y$ & \textbf{Leave it out} for the total effect. \\""")

s = s.replace(r"\begin{frame}{Natural experiments worth knowing}", r"""\begin{frame}{Difference in differences, with the actual arithmetic}
A chain raises pay in its \textbf{Ohio} stores in July and leaves \textbf{Indiana} alone.
\begin{center}\small
\begin{tabular}{lccc}
\toprule
 & \textbf{before} & \textbf{after} & \textbf{change} \\
\midrule
Ohio (treated)    & 42.0 & 55.0 & $+13.0$ \\
Indiana (control) & 30.0 & 36.0 & $+6.0$ \\
\midrule
\textbf{difference in differences} & & & $\mathbf{+7.0}$ \\
\bottomrule
\end{tabular}
\end{center}
\vspace{0.4em}
\begin{itemize}
  \item Ohio rose 13, but 6 of that would have happened anyway. The estimated effect is
        \textbf{7}.
  \item It all rests on the claim that Ohio \emph{would have} risen by 6 too, which is untestable
        after treatment.
\end{itemize}
\begin{principle}{how to check what you cannot test}
Plot both series for several periods \emph{before} the change. If they moved together then, the
assumption is credible.
\end{principle}
\end{frame}

\begin{frame}{Reverse causation, and how to rule it out}
\begin{itemize}
  \item Hospitals with more staff have higher mortality. Do nurses kill people, or do sicker
        patients get more nurses?
  \item Ad spend and sales move together, partly because budgets are \emph{set} as a percentage of
        expected sales.
  \item Police numbers and crime, tutoring and grades, maintenance and failures: in each case the
        outcome plausibly causes the treatment.
\end{itemize}
\begin{principle}{the fix is timing, not statistics}
Establish that the cause moved \emph{first}, and for a reason unrelated to the outcome. That is
what a rollout date, a policy change, or a budget freeze gives you, and no regression can
substitute for it.
\end{principle}
\end{frame}

\begin{frame}{Natural experiments worth knowing}""")

s = s.replace(r"\begin{frame}{LLM check: mistake or not? (1 of 2)}", r"""\begin{frame}{Your turn \#3}
\begin{yourturn}{sort the variables}
You want the effect of a \textbf{price increase} on \textbf{customer churn}. For each variable,
say confounder, collider, or mediator, and whether it belongs in the model:
\begin{enumerate}
  \item The customer's contract tier, which affects both the price they were offered and their
        likelihood of leaving.
  \item Whether the customer called support to complain about the price.
  \item How much the customer's monthly bill actually rose.
\end{enumerate}
\end{yourturn}
\end{frame}

\begin{frame}{Your turn \#3: answer}
\begin{itemize}
  \item \textbf{Contract tier: confounder.} It drives both the treatment and the outcome, so
        leaving it out biases the estimate. \textbf{Control for it.}
  \item \textbf{Complaint call: collider.} It is caused by the price increase \emph{and} by the
        customer's underlying unhappiness. Controlling for it, or studying only complainers,
        manufactures a relationship. \textbf{Leave it out.}
  \item \textbf{Size of the bill increase: mediator.} It is how the price increase acts. Include
        it only if you specifically want the effect of price that runs through something else.
\end{itemize}
\begin{principle}{the tell}
Ask ``did this happen before or after the treatment?'' Anything measured afterward is a candidate
mediator or collider, and both are dangerous controls.
\end{principle}
\end{frame}

\begin{frame}{LLM check: mistake or not? (1 of 2)}""")
adapt.save(s, p)

# ---------------- UNIT 10 ----------------
p = SL / "Unit_10_Bayesian_Reasoning_and_Decisions.tex"; s = p.read_text()
s = s.replace(r"\begin{frame}{Belief sharpening, batch by batch}", r"""\begin{frame}{Updating a rate, with the actual numbers}
Conjugate shortcut: with a Beta$(a, b)$ prior, $s$ successes and $f$ failures give a
Beta$(a+s,\; b+f)$ posterior. The prior acts like $a$ imaginary successes and $b$ imaginary
failures you saw before the study.
\begin{center}\small
\begin{tabular}{lcccc}
\toprule
\textbf{after} & \textbf{data so far} & \textbf{posterior} & \textbf{mean} & \textbf{95\% interval} \\
\midrule
nothing        & ---            & Beta(2, 8)     & 0.200 & 0.03 to 0.48 \\
10 visitors    & 2 of 10        & Beta(4, 16)    & 0.200 & 0.07 to 0.40 \\
50 visitors    & 12 of 50       & Beta(14, 46)   & 0.233 & 0.14 to 0.35 \\
200 visitors   & 48 of 200      & Beta(50, 160)  & 0.238 & 0.18 to 0.30 \\
\bottomrule
\end{tabular}
\end{center}
\vspace{0.3em}
\begin{itemize}
  \item The prior contributes 10 imaginary observations. After 200 real ones it is outvoted 20 to
        1, and the interval has shrunk by two thirds.
\end{itemize}
\end{frame}

\begin{frame}{Belief sharpening, batch by batch}""")

s = s.replace(r"\begin{frame}{When to stop a test}", r"""\begin{frame}{Your turn \#3}
\begin{yourturn}{how much would this move you?}
Your company's landing pages historically convert between 6\% and 14\%. A new page is tested and
converts \textbf{4 of 10} visitors, which is 40\%.
\vspace{0.3em}

With a neighbor: pick a prior that encodes the company history, work out roughly where the
posterior lands, and decide what you would tell the person who wants to ship it today.
\end{yourturn}
\end{frame}

\begin{frame}{Your turn \#3: answer}
\begin{itemize}
  \item A prior centered near 10\% with real weight, say Beta(10, 90), encodes ``about 10\%, worth
        roughly 100 past observations.''
  \item Posterior: Beta$(10+4,\; 90+6) =$ Beta(14, 96), a mean near \textbf{12.7\%}. The
        spectacular 40\% barely moves the needle, because 10 visitors is almost no evidence.
  \item What to say: ``This is encouraging but it is 10 people. Our best estimate is still about
        13\%. Run it to a few thousand visitors before we decide.''
\end{itemize}
\begin{principle}{the winner's curse, in Bayesian clothing}
A sensible prior automatically discounts extreme results from tiny samples. That is not
conservatism; it is what the arithmetic says once you admit you knew something beforehand.
\end{principle}
\end{frame}

\begin{frame}{When to stop a test}""")
adapt.save(s, p)

# ---------------- UNIT 11 ----------------
p = SL / "Unit_11_Where_the_Data_Comes_From.tex"; s = p.read_text()
s = s.replace(r"\begin{frame}{You measure a proxy, not the concept}", r"""\begin{frame}{Weighting: the partial repair}
When your sample's composition is wrong but you \emph{know} the true composition, you can reweight.
\begin{center}\small
\begin{tabular}{lccc}
\toprule
\textbf{Age group} & \textbf{\% of population} & \textbf{\% of respondents} & \textbf{weight} \\
\midrule
18--34 & 30\% & 12\% & 2.50 \\
35--54 & 35\% & 33\% & 1.06 \\
55+    & 35\% & 55\% & 0.64 \\
\bottomrule
\end{tabular}
\end{center}
\vspace{0.4em}
\begin{itemize}
  \item Each young respondent now counts for 2.5 people, so the estimate reflects the population
        mix rather than who answered.
  \item It only fixes imbalance on variables you \emph{measured}, and heavy weights inflate the
        variance.
\end{itemize}
\begin{trap}{weighting as a blank check}
``We weighted the survey'' does not mean the bias is gone. It means the bias on the weighting
variables is gone.
\end{trap}
\end{frame}

\begin{frame}{Your turn \#3}
\begin{yourturn}{interrogate a dataset}
You are handed a dataset of loan applications that were \textbf{approved}, with a default
indicator, and asked to build a model deciding whom to approve next.
\vspace{0.3em}

With a neighbor: name the population this data actually represents, the group that is missing, and
the specific way a model trained on it would mislead the credit team.
\end{yourturn}
\end{frame}

\begin{frame}{Your turn \#3: answer}
\begin{itemize}
  \item The population is \textbf{applicants the old policy already approved}, not applicants in
        general. Everyone the previous rule rejected is invisible.
  \item The model therefore learns to reproduce the old policy's judgments, including its
        mistakes, and it has no information at all about the region of applicant space that was
        never approved.
  \item Consequence: it will look accurate in backtesting and will be unable to tell you whether
        the applicants you currently reject would in fact have repaid.
  \item Partial fixes: approve a small random sample of marginal applicants (deliberate
        exploration), or use the rejected applicants' outcomes elsewhere if they can be observed.
\end{itemize}
\end{frame}

\begin{frame}{You measure a proxy, not the concept}""")
adapt.save(s, p)

# ---------------- UNIT 12 ----------------
p = SL / "Unit_12_Putting_It_Together.tex"; s = p.read_text()
s = s.replace(r"\begin{frame}{Translating for a non-technical audience}", r"""\begin{frame}{Scenario 7: the model that decides about people}
\textbf{They say:} ``Our hiring model is 88\% accurate at predicting who will be a top performer.
Let's use it to screen applications.''
\vspace{0.4em}

\begin{yourturn}{two minutes, out loud}
What do you ask, what could go wrong, and what would you need before this touches a real
applicant?
\end{yourturn}
\end{frame}

\begin{frame}{Scenario 7: a strong answer}
\begin{itemize}
  \item \textbf{The label:} ``top performer'' is a manager's rating, a proxy carrying whatever
        biases that manager had. The model predicts the rating, not the performance.
  \item \textbf{The sample:} it only observes people who were \emph{hired}. Strong candidates the
        old process rejected are invisible, so the model learns the old process.
  \item \textbf{The metric:} 88\% accuracy means nothing without the base rate; if 85\% of hires
        are rated acceptable, the model is barely beating ``say yes.''
  \item \textbf{Before deployment:} the base rate, precision and recall at the operating
        threshold, error rates broken out across groups, and a human in the loop.
\end{itemize}
\end{frame}

\begin{frame}{Scenario 8: the number with no error bar}
\textbf{They say:} ``Customer lifetime value is \$1,840. I've put it in the pricing model.''
\vspace{0.4em}

\begin{yourturn}{two minutes, out loud}
Where did that number come from, and what are the three things you check before pricing depends on
it?
\end{yourturn}
\end{frame}

\begin{frame}{Scenario 8: a strong answer}
\begin{itemize}
  \item \textbf{Mean or median?} Lifetime value is savagely right-skewed. If \$1,840 is a mean, a
        handful of whales are setting your prices for everyone.
  \item \textbf{Which customers?} Almost certainly the ones who have already churned, since only
        they have a complete lifetime. That is survivorship in reverse: your best customers are
        excluded precisely because they are still here.
  \item \textbf{How wide is the interval?} A bootstrap on a skewed quantity like this is often
        embarrassingly wide, and pricing built on a point estimate inherits all of that.
  \item \textbf{What I would report:} median and mean, an interval on each, and a segment
        breakdown, because one number for all customers is the actual error here.
\end{itemize}
\end{frame}

\begin{frame}{Translating for a non-technical audience}""")

s = s.replace(r"\begin{frame}{The last slide}", r"""\begin{frame}{Running the bracket (logistics)}
\begin{itemize}
  \item \textbf{Round 1 (pairs, 10 min).} Everyone answers one card, partner scores the five
        beats. Swap. Higher score advances.
  \item \textbf{Round 2 (fours, 10 min).} Winners pair off; the two losers score.
  \item \textbf{Semifinals and final (front of room).} Two minutes each, class votes with the
        rubric, not on charisma.
  \item \textbf{The rule that matters:} nobody may say ``run a $t$-test'' without saying what
        would make the test inappropriate.
\end{itemize}
\begin{principle}{what wins}
Not the most confident answer. The one that names its own assumptions and says what would change
its mind.
\end{principle}
\end{frame}

\begin{frame}{The last slide}""")
adapt.save(s, p)
