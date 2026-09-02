#!/usr/bin/env python3
"""Unit 7 deck: adapt Module 04 (Prediction and Its Uncertainty) into 3 days."""
import adapt

s, out = adapt.load("Module_04_Prediction_and_Its_Uncertainty.tex",
                    "Unit_07_Prediction_and_Its_Uncertainty.tex")

s = adapt.preamble(s)
s = adapt.subtitle(s, 7, "Why Predictions Are Wrong, and How Wrong")
s = adapt.soften_green(s, keep=1)

s = s.replace(r"\begin{frame}{Where we left off}", r"\begin{frame}{Day 1: where we left off}")
s = s.replace("Part 3 built models and judged them on data they hadn't seen.",
              "Unit 6 built models and judged them on data they had not seen.")
s = s.replace("The questions for this part:", "The questions for this unit:")

s = adapt.contract(s, know=[
    r"that a prediction is a point \emph{plus} an honest interval",
    r"the four layers of error: noise, estimation, model structure, and shift",
    r"why a prediction interval is much wider than a confidence interval",
    r"how to size an interval from real out-of-sample errors",
    r"what extrapolation and regression to the mean do to predictions",
    r"what it means for predictions to be \textbf{calibrated}",
], avoid=[
    r"reporting a point prediction with no interval at all",
    r"giving intervals that are far too narrow",
    r"quoting a confidence interval when the question needed a prediction interval",
    r"extrapolating past the range of the data",
    r"assuming next year looks like the training data",
    r"mistaking regression to the mean for a real effect",
])

# ---- Day 2 divider before the estimating section ----
s = adapt.insert_before(s, r"\begin{frame}{How to get honest error bars}",
    adapt.day(2, "Putting an honest number on the error", [
        "prediction intervals versus confidence intervals, concretely",
        "sizing an interval from held-out residuals instead of a formula",
        "the bootstrap and ensembles as a way to see estimation wobble",
        "calibration: checking that a 90\\% interval really catches 90\\%",
    ]))

# ---- Day 3 divider before the follies ----
s = adapt.insert_before(s, r"\begin{frame}{Folly 1: extrapolation}",
    adapt.day(3, "The four ways predictions go wrong in the wild", [
        "extrapolation: confident answers about places you have no data",
        "regression to the mean, and the interventions it fakes",
        "distribution shift, leakage, and Goodhart's law",
        "how to report a prediction so nobody is misled",
    ]))

# ---- Day 2 content: make the PI concrete ----
s = s.replace(r"\begin{frame}{Calibration: do your intervals mean what they say?}",
r"""\begin{frame}{Building a prediction interval from your own errors}
The most reliable interval needs no distributional theory at all:
\begin{enumerate}
  \item Fit the model on training data.
  \item Predict on a \textbf{held-out} set and collect the residuals
        $e_i = y_i - \hat y_i$.
  \item For a new case, report $\hat y \pm$ the 5th and 95th \emph{percentiles} of those held-out
        residuals.
\end{enumerate}
\begin{itemize}
  \item Worked: a model predicts 640 rentals. Held-out residuals run from $-210$ to $+260$ at the
        5th and 95th percentiles. Report \textbf{640, with a 90\% range of 430 to 900}.
  \item The interval is automatically the right width, because it is made of mistakes the model
        actually made.
\end{itemize}
\begin{principle}{why this beats the textbook formula}
The formula assumes the model is correct and the noise is constant. Held-out residuals assume
neither; they simply record what went wrong last time.
\end{principle}
\end{frame}

\begin{frame}{Your turn \#2}
\begin{yourturn}{which interval does the question need?}
Your model predicts revenue for a single store next month.
\begin{enumerate}
  \item The CFO asks: ``what will \emph{this store} bring in?''
  \item The board asks: ``what is average monthly revenue \emph{per store} across our 400
        stores?''
\end{enumerate}
With a neighbor: which question needs the wider interval, roughly how much wider, and why?
\end{yourturn}
\end{frame}

\begin{frame}{Your turn \#2: answer}
\begin{itemize}
  \item (1) needs a \textbf{prediction interval}: it carries the store's own irreducible
        variability plus our uncertainty about the model.
  \item (2) needs a \textbf{confidence interval} for the mean, which shrinks like $1/\sqrt{400}$
        and can be dramatically narrower.
  \item The prediction interval can easily be ten times wider. Handing the CFO the board's
        interval is the single most common way analysts get blamed for a ``wrong'' forecast.
\end{itemize}
\begin{principle}{one question to ask first}
Am I predicting \emph{one case} or locating \emph{an average}? Everything about the width follows
from that.
\end{principle}
\end{frame}

\begin{frame}{Calibration: do your intervals mean what they say?}""")

s = adapt.question_bank(s, [
    "A prediction is wrong. Walk me through the possible sources of the error.",
    "What is the difference between irreducible noise and estimation uncertainty?",
    "Which sources of error shrink with more data, and which do not?",
    "Confidence interval or prediction interval: which do you give a customer, and why?",
    "How would you actually put honest error bars on a forecast?",
    "Your model was great in testing and failed in production. What happened?",
    "Your best performer slumped the next quarter. Did your intervention fail?",
    "A model predicts almost perfectly. Are you excited or suspicious?",
    "Why is extrapolating beyond the data so dangerous?",
    "What does it mean for intervals to be calibrated, and how would you check?",
])
s = adapt.consolidate_headings(s)

s = s.replace(r"""\begin{itemize}
  \item So far the prediction has been a number. \textbf{Part 5} turns to \textbf{classification}:
        predicting a yes or no, where the model outputs a probability and you choose a threshold.""",
r"""\begin{itemize}
  \item So far the prediction has been a number. \textbf{Unit 8} turns to categorical outcomes:
        rates, tables, and predicting a yes or no, where the model outputs a probability and
        somebody has to choose a threshold.""")

adapt.save(s, out)
