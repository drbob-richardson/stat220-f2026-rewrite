#!/usr/bin/env python3
"""Unit 4 deck: adapt Module 08 (Estimation, Likelihood, the Bootstrap) into 3 days."""
import adapt

s, out = adapt.load("Module_08_Estimation_Likelihood_and_the_Bootstrap.tex",
                    "Unit_04_Estimation_and_the_Bootstrap.tex")

s = adapt.preamble(s)
s = adapt.subtitle(s, 4, "Turning a Sample Into a Number You Can Defend")
s = adapt.soften_green(s, keep=1)

s = s.replace(r"\begin{frame}{Where this fits}", r"\begin{frame}{Day 1: where this fits}")

s = adapt.contract(s, know=[
    r"what an estimator is, and how to judge one by \textbf{bias}, \textbf{variance}, and MSE",
    r"why the best estimator is often a slightly biased one",
    r"shrinkage, and why every leaderboard needs it",
    r"what a likelihood is, and what maximum likelihood actually maximizes",
    r"why the curvature of the likelihood is the precision of the estimate",
    r"how the bootstrap manufactures a sampling distribution from one sample",
], avoid=[
    r"chasing unbiasedness at the cost of enormous variance",
    r"reporting an estimate with no standard error",
    r"confusing the SD of the data with the SE of the estimate",
    r"bootstrapping rows when the independent unit is a user, store, or week",
    r"bootstrapping maxima or extreme quantiles",
    r"ranking groups of very different sizes without shrinkage",
])

# ---- Day 1: add method of moments, right after "Where do estimators come from?" ----
s = s.replace(r"\begin{frame}{Likelihood, concretely}", r"""\begin{frame}{Method of moments, in one slide}
The simplest recipe there is: \emph{make the model's average match the data's average}, then solve.
\begin{itemize}
  \item Data: 40 support calls per day on average. Model: Poisson($\lambda$). Poisson's mean is
        $\lambda$, so set $\hat\lambda = 40$. Done.
  \item Data: mean 0.30 conversion. Model: Bernoulli($p$), whose mean is $p$, so $\hat p = 0.30$.
  \item It is quick, it is intuitive, and it often lands on the same answer as maximum likelihood.
\end{itemize}
\begin{trap}{where it falls apart}
Method of moments uses only the mean (and maybe the variance). It throws away the rest of the
data's shape, which is exactly the information you need when the model has several parameters or
the data is censored.
\end{trap}
\end{frame}

\begin{frame}{Likelihood, concretely}""")

# ---- Day 2 divider before the likelihood section ----
s = adapt.insert_before(s, r"\begin{frame}{Where do estimators come from?}",
    adapt.day(2, "Where estimates come from", [
        "method of moments and maximum likelihood, the two general recipes",
        "the likelihood function, and why its peak is the estimate",
        "why the curvature at that peak is the standard error",
        "what a flat likelihood is telling you about your data",
    ]))

# ---- Day 3 divider before the bootstrap section ----
s = adapt.insert_before(s, r"\begin{frame}{The problem the bootstrap solves}",
    adapt.day(3, "Uncertainty without a formula", [
        "the bootstrap: resample the sample, and watch the estimate move",
        "confidence intervals for medians, percentiles, and ratios",
        "choosing the resampling unit, which is the whole ballgame",
        "three situations where the bootstrap quietly fails",
    ]))

# ---- Day 3 addition: the three ways to get a standard error ----
s = s.replace(r"\begin{frame}{Where the bootstrap fails}", r"""\begin{frame}{Three ways to get a standard error}
\begin{center}\small
\begin{tabular}{p{0.24\textwidth} p{0.34\textwidth} p{0.32\textwidth}}
\toprule
\textbf{Method} & \textbf{How} & \textbf{Use it when} \\
\midrule
Formula & $s/\sqrt{n}$ and its relatives & the statistic is a mean or a slope and the assumptions
hold \\
Likelihood curvature & how sharply the log-likelihood peaks & you fit a model by maximum
likelihood; this is what software reports \\
Bootstrap & resample and look at the spread & anything else, or when you do not trust the
formula's assumptions \\
\bottomrule
\end{tabular}
\end{center}
\vspace{0.4em}
\begin{principle}{they should agree, and it is worth checking}
On a well-behaved mean, all three land in the same place. When the bootstrap disagrees with the
formula, believe the bootstrap and go find out which assumption broke.
\end{principle}
\end{frame}

\begin{frame}{Where the bootstrap fails}""")

s = adapt.question_bank(s, [
    "What makes one estimator better than another? Define bias, variance, and MSE.",
    "Give an example where a biased estimator is the better choice.",
    "Explain maximum likelihood in plain English.",
    "Why does the shape of the likelihood tell you the standard error?",
    "How would you get a confidence interval for a 90th percentile?",
    "Explain the bootstrap to a product manager in thirty seconds.",
    "When does the bootstrap fail, and what would you do instead?",
    "We have 80{,}000 rows from 5{,}000 customers. What do you resample?",
    "A new rep is 3-for-3. What is your estimate of her close rate?",
    "How would you build a leaderboard that new sellers cannot game with two reviews?",
])
s = adapt.consolidate_headings(s)

s = s.replace(r"""\begin{itemize}
  \item We can now produce an estimate and an honest interval for almost anything. That is exactly
        the machinery inference needs.
  \item Next comes the question of whether an observed difference is real: hypothesis tests,
        $p$-values, and the discipline of separating signal from noise.
\end{itemize}""",
r"""\begin{itemize}
  \item You can now produce an estimate and an honest interval for almost any quantity, with or
        without a formula. That closes out the foundations.
  \item \textbf{Unit 5} puts the machinery to work on a relationship rather than a single number:
        regression, where the estimate is a slope and every idea from Units 1 through 4 comes back
        wearing new clothes.
\end{itemize}""")

adapt.save(s, out)
