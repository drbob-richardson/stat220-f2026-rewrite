#!/usr/bin/env python3
"""Unit 5 deck: adapt Module 02 (Regression as Reasoning) into 3 days."""
import adapt

s, out = adapt.load("Module_02_Regression_as_Reasoning.tex",
                    "Unit_05_Regression_as_Reasoning.tex")

s = adapt.preamble(s)
s = adapt.subtitle(s, 5, "Reasoning With a Slope")
s = adapt.soften_green(s, keep=1)

s = s.replace(r"\begin{frame}{Where we left off}", r"\begin{frame}{Day 1: where we left off}")

s = adapt.contract(s, know=[
    r"what a regression line is, and what least squares actually minimizes",
    r"how to read a slope and an intercept \emph{with their units}",
    r"that a slope is an estimate, so it carries a standard error",
    r"how binary and categorical predictors enter a model",
    r"what an interaction means, in words",
    r"what happens to a coefficient when you add or remove another predictor",
], avoid=[
    r"reading a slope without checking its units or its range",
    r"treating a slope as the effect of intervening",
    r"confusing a significant slope with a useful model",
    r"chasing $R^2$ as if it measured correctness",
    r"comparing coefficients on variables measured in different units",
    r"controlling for a variable without asking what it does in the causal story",
])

# ---- Day 2 divider: inference on the slope ----
s = adapt.insert_before(s, r"\begin{frame}{The slope is an estimate, so it has a standard error}",
    adapt.day(2, "The slope is an estimate", [
        "standard errors and tests for a slope: the Unit 1 template returns",
        "why a tiny p-value and a tiny $R^2$ can happily coexist",
        "binary predictors, categorical predictors, and what a baseline is",
        "interactions: when the slope itself depends on the group",
    ]))

# ---- Day 3 divider: confounding ----
s = adapt.insert_before(s, r"\begin{frame}{Multiple regression, in one breath}",
    adapt.day(3, "More than one predictor", [
        "multiple regression, and what \\emph{holding the others fixed} really means",
        "confounding: how a lurking variable rewrites a conclusion",
        "the Simpson's-paradox vote, and the reveal",
        "what adding or removing a predictor does, and when each is right",
    ]))

# ---- A worked coefficient-reading frame for students new to regression ----
s = s.replace(r"\begin{frame}{Residuals and least squares}", r"""\begin{frame}{Reading a fitted line out loud}
Suppose a fit on housing data gives
\[
\widehat{\text{price}} = 41{,}000 + 118 \times \text{square feet}.
\]
\begin{itemize}
  \item \textbf{Slope:} each extra square foot is associated with \$118 more in price,
        \emph{among houses like these}. Units: dollars per square foot.
  \item \textbf{Intercept:} the fitted price of a zero-square-foot house. Not a house. Intercepts
        are often meaningless alone; they position the line.
  \item \textbf{Range matters:} if the data runs 800 to 3{,}000 square feet, the line says nothing
        about a 12{,}000-square-foot mansion.
\end{itemize}
\begin{trap}{the units trap}
``The coefficient is 118, so it is a big effect.'' Big compared to what? Switch to square
\emph{meters} and the same relationship reports 1{,}270.
\end{trap}
\end{frame}

\begin{frame}{Residuals and least squares}""")

s = adapt.question_bank(s, [
    "What does the slope mean, in the units of this problem?",
    "Our slope is significant but $R^2$ is 0.04. Is the model useful?",
    "How do you put a categorical predictor with five levels into a regression?",
    "What does an interaction term mean, in plain language?",
    "The coefficient flipped sign when we added a variable. What happened?",
    "When is controlling for a variable the right move, and when is it a mistake?",
    "Can you say the slope is the effect of changing $x$? Under what conditions?",
    "Two predictors are highly correlated. What happens to their coefficients?",
    "How would you explain a regression output to a non-technical manager?",
    "What would make you distrust a regression you did not run yourself?",
])
s = adapt.consolidate_headings(s)

adapt.save(s, out)
