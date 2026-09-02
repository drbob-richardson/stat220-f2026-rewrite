#!/usr/bin/env python3
"""Split the merged probability deck back into two units for the model-first order.

Unit 7 keeps randomness, the rules, conditioning, Bayes and base rates.
Unit 8 takes random variables, expectation, variance and the distribution stories.
Each gets its own closing material.
"""
import re
from pathlib import Path

OLD = Path("/Users/robertrichardson/Library/CloudStorage/GoogleDrive-richardson@stat.byu.edu/"
           "My Drive/BYU Classes/220/F2026/Course_Rewrite/Slides")
NEW = Path(__file__).resolve().parents[1] / "Slides"
src = (OLD / "Unit_02_Probability_and_Random_Variables.tex").read_text()

head = src[:src.index("\\begin{document}")] + "\\begin{document}\n\n"
title_frame = "\\begin{frame}\n  \\titlepage\n\\end{frame}\n\n"


def frames(text):
    out, pos = {}, 0
    while True:
        i = text.find("\\begin{frame}{", pos)
        if i < 0:
            break
        depth, k = 1, i + len("\\begin{frame}{")
        while depth:
            if text[k] == "{": depth += 1
            elif text[k] == "}": depth -= 1
            k += 1
        title = text[i + len("\\begin{frame}{"):k - 1]
        end = text.index("\\end{frame}", k) + len("\\end{frame}")
        out[title] = text[i:end] + "\n\n"
        pos = end
    return out


F = frames(src)
bar = "% " + "=" * 70 + "\n"
def section(n): return bar + "\\section{%s}\n" % n + bar


def retitle(head, title, subtitle):
    h = re.sub(r"\\title\{[^}]*\}", "\\\\title{%s}" % title, head)
    return re.sub(r"\\subtitle\{[^}]*\}", "\\\\subtitle{%s}" % subtitle, h)


# ---------------------------------------------------------------- UNIT 7
u7 = [retitle(head, "Probability: Randomness, Conditioning, and Bayes",
              "Unit 7: What Chance Produces, and How Evidence Moves You"), title_frame]
u7.append(section("Randomness"))
for t in ["The thing we assumed last unit", "Live experiment: can you fake a coin?",
          "Stay here while they write: what gives you away", "The reveal: look at the streaks",
          "Why that game matters at work", "What this unit gives you", "The vocabulary, quickly",
          "Three rules that generate everything else", "The complement rule is your best friend",
          "Conditional probability: shrinking the world", "Independence, stated carefully",
          "Why false independence is expensive", r"Your turn \#1", r"Your turn \#1: answer",
          "Two more things randomness does that surprise people",
          "Coincidences are more common than they feel"]:
    u7.append(F[t])
u7.append(section("Evidence"))
for t in ["The direction matters enormously", "A wrongful conviction built on a flipped conditional",
          r"Your turn \#2", r"Your turn \#2: answer", "Bayes' rule",
          "The four numbers a test comes with", "Do not use the formula. Use 10,000 people.",
          "The same fact, as a picture", "Why counting people beats the formula",
          "This is the churn model, the fraud flag, the spam filter",
          r"Your turn \#3", r"Your turn \#3: answer"]:
    u7.append(F[t])
u7.append(section("LLM check"))
u7.append(F["LLM check: mistake or not? (1 of 2)"])
u7.append(F["LLM check: mistake or not? (2 of 2)"])
u7.append(section("Consolidate"))
u7.append(F["Turning a probability question into arithmetic"])
u7.append(F["How to attack any probability question, in order"])
u7.append(F["What you should be able to do with software"])
u7.append(r"""\begin{frame}{The traps, all in one place}
\begin{trap}{the ones that bite most often}
\begin{itemize}
  \item Flipping a conditional: reporting $\PR{B \mid A}$ when the question asked
        $\PR{A \mid B}$.
  \item Ignoring the base rate after a positive test or a model flag.
  \item Multiplying probabilities of events that share a common cause.
  \item Believing chance ``evens out'' in the short run.
  \item Ranking small groups by rates and believing the extremes.
  \item Being amazed by a coincidence without counting the opportunities.
\end{itemize}
\end{trap}
\end{frame}

\begin{frame}{Ten questions to be able to answer}
\begin{enumerate}\small
  \item A 99\%-accurate test for a 1-in-1000 disease comes back positive. Now what?
  \item Explain the difference between $\PR{A \mid B}$ and $\PR{B \mid A}$ with an example.
  \item What does independence require, and when have you seen it assumed wrongly?
  \item A coin lands heads six times in a row. What is the chance of heads next?
  \item Why is a 1\% daily failure risk a serious problem over a quarter?
  \item Define sensitivity, specificity, and predictive value, and say which one a patient wants.
  \item Our fraud model flags 2\% of transactions. How would you tell whether it is any good?
  \item Why are the healthiest and the sickest counties both mostly small ones?
  \item Three redundant servers each fail 1\% of the time. What is your real risk?
  \item Someone shows you a striking pattern in last month's data. What do you ask first?
\end{enumerate}
\end{frame}

\begin{frame}{Mastery checklist}
You have this unit when you can, from memory:
\begin{itemize}
  \item use complement, addition, and multiplication rules without confusing them
  \item say precisely what independence requires, and spot a shared cause
  \item translate any accuracy claim into a conditional probability, in the right direction
  \item solve a Bayes problem by counting 10,000 people
  \item name sensitivity, specificity, prevalence, and predictive value, and say which changes
        with the population
  \item explain why streaks, clusters, and coincidences are what randomness looks like
\end{itemize}
\end{frame}

\begin{frame}{Where we go next}
\begin{itemize}
  \item Probability describes whether something happens. \textbf{Unit 8} attaches a
        \emph{number} to the outcome, which is what lets us talk about an average, a total, and a
        risk.
  \item That is also the last piece we need before \textbf{Unit 9} explains why every standard
        error you have used since Unit 1 was legitimate.
\end{itemize}
\begin{principle}{the habit to keep}
Before you explain a pattern, work out what pure chance would have produced.
\end{principle}
\end{frame}

""")
u7.append("\\end{document}\n")
(NEW / "Unit_07_Probability.tex").write_text("".join(u7))

# ---------------------------------------------------------------- UNIT 8
u8 = [retitle(head, "Random Variables and Distributions",
              "Unit 8: Putting a Number on an Uncertain Thing"), title_frame]
u8.append(section("Random variables"))
u8.append(r"""\begin{frame}{Where this fits}
\begin{itemize}
  \item Unit 7 dealt in events: did the customer buy, is the test positive, did the server fail.
  \item Now we attach a \textbf{number} to the outcome. Revenue, wait time, defects, dollars lost.
  \item Once outcomes are numbers we can average them, add them up, and compare decisions, which
        is where this becomes useful to somebody with a budget.
\end{itemize}
\begin{principle}{a random variable is a rule, not a value}
It is not ``the number that came up.'' It is the whole recipe: which numbers are possible and how
often each one occurs.
\end{principle}
\end{frame}

""")
for t in ["Live experiment: what will you pay to play?",
          "Stay here while they bid: what each game is worth"]:
    u8.append(F[t])
u8.append(r"""\begin{frame}{What this unit gives you}
\begin{columns}[T]
\begin{column}{0.5\textwidth}
\textbf{Things to know}
\begin{itemize}\small
  \item expectation as a long-run average, and its linearity
  \item variance and standard deviation, in the right units
  \item what happens to the mean and spread when you add things up
  \item which standard distribution matches which real-world story
  \item why plugging an average into a curved calculation is wrong
\end{itemize}
\end{column}
\begin{column}{0.5\textwidth}
\textbf{Mistakes to stop making}
\begin{itemize}\small
  \item reporting a mean with no measure of spread
  \item treating the mean as typical when the data is skewed
  \item computing the answer at average inputs instead of averaging the answers
  \item adding variances of things that are not independent
  \item picking a distribution by eyeballing a histogram
\end{itemize}
\end{column}
\end{columns}
\end{frame}

""")
for t in ["Random variables and expectation", "Linearity: the most useful fact in this course",
          "Variance: how far things swing", "Why averaging works, and when it stops",
          r"Your turn \#4", r"Your turn \#4: answer", "Pick the distribution by the mechanism",
          "The four stories worth memorizing", "Choosing a model in practice",
          "Averages plugged into nonlinear things", "Why the gap appears",
          "The mean is not the typical case"]:
    u8.append(F[t].replace(r"Your turn \#4", r"Your turn \#1"))
u8.append(section("Consolidate"))
u8.append(r"""\begin{frame}{Modeling an uncertain quantity, in order}
\small
\begin{enumerate}
  \item \textbf{Define the variable in words and units.} ``Tickets per hour,'' not ``tickets.''
  \item \textbf{Tell the generating story.} Fixed tries? Arrivals over time? A waiting time? A sum
        of many small pieces?
  \item \textbf{Pick the distribution the story implies}, and write down what it assumes.
  \item \textbf{Get the mean and the SD}, and sanity-check both against reality.
  \item \textbf{Check the assumption that breaks first}, usually independence or a constant rate.
  \item \textbf{Compute the decision quantity by simulation}, never by plugging in averages.
\end{enumerate}
\end{frame}

\begin{frame}{What you should be able to do with software}
\small
Nobody is asking you to memorize syntax. You are expected to know \emph{which} procedure the
question calls for and what the output means.
\begin{center}\footnotesize
\begin{tabular}{p{0.44\textwidth} p{0.46\textwidth}}
\toprule
\textbf{You should be able to} & \textbf{What you would reach for} \\
\midrule
Mean and SD of a simulated quantity & \texttt{.mean()}, \texttt{.std(ddof=1)} \\
Exact binomial probabilities and tails & \texttt{stats.binom.pmf}, \texttt{.sf} \\
Counts over a window & \texttt{stats.poisson.pmf}, \texttt{.sf} \\
Waiting times & \texttt{stats.expon} \\
Check whether counts are over-dispersed & compare the sample variance to the mean \\
Expected profit or cost under uncertainty & simulate the scenarios, then average \\
Find the best decision, not the average one & sweep the choice and take the maximum \\
\bottomrule
\end{tabular}
\end{center}
\vspace{0.2em}
\centering\small
If you cannot say what the output means, producing it is worth nothing.
\end{frame}

\begin{frame}{The traps, all in one place}
\begin{trap}{the ones that bite most often}
\begin{itemize}
  \item Reporting a mean with no standard deviation or range.
  \item Calling the mean ``typical'' when the data is skewed.
  \item Computing the answer at average inputs instead of averaging the answers.
  \item Adding variances for things that share a driver.
  \item Choosing a distribution from a histogram instead of a mechanism.
  \item Maximizing expected value on a one-shot bet you cannot survive losing.
\end{itemize}
\end{trap}
\end{frame}

\begin{frame}{Ten questions to be able to answer}
\begin{enumerate}\small
  \item Define expected value and give a case where it is the wrong thing to maximize.
  \item Two projects have equal expected return. What else do you want to know?
  \item Why does the SD of an average shrink like $1/\sqrt{n}$, and when does it not?
  \item Our average customer spends \$80. What is wrong with planning around that?
  \item Why is profit at average demand not the same as average profit?
  \item Which distribution would you use for tickets per hour, and what does it assume?
  \item Your count data has variance three times its mean. What does that tell you?
  \item How would you staff when understaffing and overstaffing cost different amounts?
  \item Explain to a manager why the median and mean of our revenue differ.
  \item When would you simulate instead of using a formula?
\end{enumerate}
\end{frame}

\begin{frame}{Mastery checklist}
You have this unit when you can, from memory:
\begin{itemize}
  \item define a random variable, its expectation, and its standard deviation
  \item use linearity to break a total into pieces
  \item say what happens to the mean and SD when independent things are summed or averaged
  \item match binomial, Poisson, exponential, and normal to their generating stories
  \item explain the flaw of averages with a concrete example
  \item argue when expected value is and is not the right objective
\end{itemize}
\end{frame}

\begin{frame}{Where we go next}
\begin{itemize}
  \item We just saw that averages of many independent pieces get predictably tighter, like
        $1/\sqrt{n}$.
  \item \textbf{Unit 9} explains why, and shows they also take on a specific \emph{shape}. That
        result is what finally justifies every standard error you have used since Unit 1.
\end{itemize}
\begin{principle}{the habit to keep}
A number without a spread is a guess. The mean says where, the SD says how much to hedge.
\end{principle}
\end{frame}

""")
u8.append("\\end{document}\n")
(NEW / "Unit_08_Random_Variables.tex").write_text("".join(u8))

for f in ["Unit_07_Probability.tex", "Unit_08_Random_Variables.tex"]:
    n = (NEW / f).read_text().count("\\begin{frame}")
    print(f"wrote {f}  ({n} frames)")
