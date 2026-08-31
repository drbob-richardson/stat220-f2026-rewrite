#!/usr/bin/env python3
"""Unit 8 deck: merge Module 10 (Counts, Proportions, Categorical Data) with
Module 09 (Classification and Evaluation) into one 3-day unit."""
import adapt

M9 = "Module_09_Classification_and_Evaluation.tex"
M10 = "Module_10_Counts_Proportions_and_Categorical_Data.tex"
f9, f10 = adapt.frames(M9), adapt.frames(M10)

out = []
add = out.append

add(adapt.preamble_of(M10, 8, "Categorical Outcomes",
                      "Rates, Tables, and Predicting a Yes or No"))
add("\\begin{frame}\n  \\titlepage\n\\end{frame}\n\n")

# ============================ DAY 1 =======================================
add(adapt.section("Proportions"))
add(r"""\begin{frame}{Day 1: where this fits}
\begin{itemize}
  \item Units 5 through 7 predicted a \emph{number}. An enormous share of real data is not a
        number: converted or not, churned or not, fraud or not, which region, which plan.
  \item The arithmetic here is simple enough that people skip straight to the conclusion, which is
        exactly why this is where the expensive mistakes happen.
  \item Three days: describing rates honestly, comparing them in tables, and building a model that
        predicts a yes or no and turns it into a decision.
\end{itemize}
\begin{principle}{a rate is a fraction with a story on both floors}
Every rate has a numerator and a denominator, and most arguments about rates are really arguments
about the denominator.
\end{principle}
\end{frame}

""")
add(f10["Live experiment: the rock-paper-scissors tournament"])
add(f10["Stay here while they play: what the research says"])
add(f10["Testing our own counts"])
add(r"""\begin{frame}{What this unit gives you}
\begin{columns}[T]
\begin{column}{0.5\textwidth}
\textbf{Things to know}
\begin{itemize}\small
  \item how to estimate a proportion and put an honest interval on it
  \item the three ways to express a comparison, and how differently they read
  \item contingency tables and chi-square, and what they do \emph{not} say
  \item why denominators and group mix can reverse a conclusion
  \item logistic regression, log-odds, and odds ratios
  \item precision, recall, ROC/AUC, thresholds, and calibration
\end{itemize}
\end{column}
\begin{column}{0.5\textwidth}
\textbf{Mistakes to stop making}
\begin{itemize}\small
  \item quoting a relative change with no base rate
  \item confusing percentage points with percent
  \item reading a significant chi-square as a large or causal effect
  \item pooling across a variable that drives the outcome
  \item reporting accuracy on imbalanced data
  \item leaving the threshold at 0.5 because it is the default
\end{itemize}
\end{column}
\end{columns}
\end{frame}

""")
add(f10["One proportion, with honest uncertainty"])
add(f10["When the count is small, patch the interval"])
add(f10["Comparing two proportions: three languages"])
add(f10["Relative risk without a base rate is a magic trick"])
add(f10[r"Your turn \#1"])
add(f10[r"Your turn \#1: answer"])

# ============================ DAY 2 =======================================
add(adapt.section("Tables and models"))
add(adapt.day(2, "From tables to a model", [
    "contingency tables, expected counts, and the chi-square test",
    "why the same data can rank groups two opposite ways",
    "logistic regression: fitting a probability instead of a number",
    "reading a coefficient as an odds ratio without overclaiming",
]))
add(f10["The contingency table"])
add(f10["A real table: loan purpose and default"])
add(f10["What a chi-square test does not tell you"])
add(f10["Assumptions and the small-cell problem"])
add(f10["Counts lie; rates need the right denominator"])
add(f10["Standardization: comparing apples to apples"])
add(f10["Simpson's paradox, with the famous real case"])
add(f10["Why the reversal happens, and what to do"])
add(f10[r"Your turn \#2"].replace(r"Your turn \#2", r"Your turn \#2"))
add(f10[r"Your turn \#2: answer"])
add(f9["Why not just fit a line?"])
add(f9["The curve, on real patient data"])
add(f9["Reading a logistic coefficient out loud"])

# ============================ DAY 3 =======================================
add(adapt.section("Decisions"))
add(adapt.day(3, "Turning a probability into a decision", [
    "the confusion matrix, and the two very different ways to be wrong",
    "precision, recall, ROC and AUC, and when each one misleads",
    "why the threshold comes from costs, not from the software default",
    "class imbalance and calibration: is a predicted 30\\% really 30\\%?",
]))
add(f9["Live experiment: the inbox game"])
add(f9["The inbox: 20 emails and the model's spam score"])
add(f9["Stay here while they choose: what will happen"])
add(f9["Scoring the inbox game"])
add(f9["The confusion matrix, and the two ways to be wrong"])
add(f9["Two thresholds on the same model"])
add(f9["Which one do you care about?"])
add(f9["Why accuracy lies"])
add(f9["ROC and precision-recall curves"])
add(f9["What AUC does and does not tell you"])
add(f9["The threshold follows from the costs"])
add(f9["Where 0.5 comes from, and why it is usually wrong"])
add(f9["Class imbalance, handled honestly"])
add(f9[r"Calibration: does 30\% mean 30\%?"])
add(f9[r"Your turn \#2"].replace(r"Your turn \#2", r"Your turn \#3"))
add(f9[r"Your turn \#2: answer"].replace(r"Your turn \#2", r"Your turn \#3"))
add(f9["Scenario: the model that was too good"])

# ============================ WRAP ========================================
add(adapt.section("LLM check"))
add(f10["LLM check: mistake or not? (1 of 2)"])
add(f9["LLM check: mistake or not? (2 of 2)"])

add(adapt.section("Consolidate"))
add(f9["The arc of a classification project"])
add(r"""\begin{frame}{The traps, all in one place}
\begin{trap}{the list worth carrying}
\begin{itemize}
  \item Reporting a relative change with no base rate, or points confused with percent.
  \item Comparing counts across groups of different size.
  \item Treating a significant chi-square as a large or causal effect.
  \item Pooling across a variable that drives both the group and the outcome.
  \item Reporting accuracy when the classes are imbalanced.
  \item Leaving the threshold at 0.5, or treating the two errors as equally costly.
  \item Multiplying an uncalibrated ``probability'' by dollars.
  \item Believing a near-perfect classifier before checking for leakage.
\end{itemize}
\end{trap}
\end{frame}

""")
add(r"""\begin{frame}{Ten questions to be able to answer}
\begin{enumerate}\small
  \item ``This doubles your risk.'' What do you ask next?
  \item Conversion moved from 2.0\% to 2.4\%. How would you decide whether it is real?
  \item We saw zero failures in 50 tests. What is the failure rate?
  \item What does a chi-square test tell you, and what does it not?
  \item How can a treatment look better in every subgroup and worse overall?
  \item A model is 99\% accurate on a 1-in-1000 event. What do you ask next?
  \item Define precision and recall, and give a case where each is the priority.
  \item Where do you set the threshold, and what do you need to know first?
  \item How do you interpret a logistic coefficient of 0.8?
  \item What is calibration, how would you check it, and when does it matter?
\end{enumerate}
\end{frame}

""")
add(r"""\begin{frame}{Mastery checklist}
You have this unit when you can, from memory:
\begin{itemize}
  \item estimate a proportion with an honest interval, even with very few events;
  \item express a comparison as an absolute difference, a relative change, and an odds ratio;
  \item build a contingency table, compute expected counts, and read the residuals;
  \item choose and defend a denominator, and standardize when the group mix differs;
  \item recognize and resolve Simpson's paradox in a real table;
  \item write the logistic model and interpret a coefficient as an odds ratio;
  \item compute precision and recall, and explain why accuracy fails under imbalance;
  \item derive a threshold from the two error costs and state the operating point in plain
        business language.
\end{itemize}
\end{frame}

""")
add(r"""\begin{frame}{Where we go next}
\begin{itemize}
  \item Every model in Units 5 through 8 answers ``what tends to go with what.'' None of them
        answers ``what happens if we change something.''
  \item \textbf{Unit 9} takes that second question seriously, and shows exactly which assumptions
        you have to buy in order to earn a causal claim.
\end{itemize}
\begin{principle}{the habit to keep}
A classifier does not make decisions. It supplies probabilities; you supply the costs. Keeping
those two jobs separate is most of the skill.
\end{principle}
\end{frame}

""")
add("\\end{document}\n")

s = "".join(out)
s = adapt.soften_green(s, keep=2)
adapt.save(s, adapt.OUT / "Unit_08_Categorical_Outcomes.tex")
