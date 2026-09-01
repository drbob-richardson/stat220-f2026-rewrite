#!/usr/bin/env python3
"""Rewrite each deck's opening 'where this fits' and closing 'where we go next' for the
model-first order, and add the normal-distribution primer that Part I borrows on credit."""
import re
from pathlib import Path

S = Path(__file__).resolve().parents[1] / "Slides"

def replace_frame(text, title, new):
    i = text.index("\\begin{frame}{" + title + "}")
    j = text.index("\\end{frame}", i) + len("\\end{frame}\n")
    return text[:i] + new + text[j:]

def patch(stem, pairs, insert_before=None, insert_text=None):
    p = S / f"{stem}.tex"; s = p.read_text()
    for title, new in pairs:
        s = replace_frame(s, title, new)
    if insert_before:
        s = s.replace("\\begin{frame}{" + insert_before + "}",
                      insert_text + "\\begin{frame}{" + insert_before + "}", 1)
    p.write_text(s)
    print(f"  patched {stem}")

# ---- Unit 1: new closer, plus the normal primer Part I leans on -------------
NORMAL_PRIMER = r"""\begin{frame}{The normal distribution, the version you need for now}
We will keep meeting the bell curve before we have earned it. Here is the working version.
\begin{itemize}
  \item It is described by two numbers: where it sits (the mean) and how wide it is (the SD).
  \item About \textbf{68\%} of the curve lies within one SD of the mean, \textbf{95\%} within two,
        and \textbf{99.7\%} within three.
  \item A \textbf{$z$-score}, $z = (x - \text{mean})/\text{SD}$, says how many SDs from the middle
        a value sits. It has no units, so it compares things measured on different scales.
\end{itemize}
\begin{principle}{what we are borrowing on credit}
Nearly every estimate we compute this semester, a mean, a difference, a slope, has a sampling
distribution that is close to normal. That is a real theorem, and \textbf{Unit 9} proves it. Until
then we use it, and we flag the places it would let us down.
\end{principle}
\end{frame}

"""

patch("Unit_01_Inference",
 [("Where we go next", r"""\begin{frame}{Where we go next}
\begin{itemize}
  \item You now have the template: an estimate, its standard error, and the discipline to ask what
        chance alone would have produced.
  \item \textbf{Unit 2} points that template at a relationship instead of a difference. The
        estimate becomes a \emph{slope}, and almost everything from this unit transfers unchanged.
  \item The rest of Part I builds and stress-tests models. Part II, starting at Unit 7, goes back
        and earns the machinery we are about to use on credit.
\end{itemize}
\begin{principle}{the habit to keep}
Before you explain a result, work out what pure chance would have produced. Most of this course is
that one habit, applied to harder situations.
\end{principle}
\end{frame}
""")],
 insert_before="What a $t$-statistic actually is", insert_text=NORMAL_PRIMER)

# ---- Unit 2 (regression) ---------------------------------------------------
patch("Unit_02_Regression_as_Reasoning",
 [("Where we left off", r"""\begin{frame}{Where we left off}
\begin{itemize}
  \item Unit 1 compared two groups and asked whether the gap was bigger than the wobble.
  \item Now the question changes shape. Instead of two buckets we have a \emph{relationship}: as
        one number moves, what happens to another?
  \item The machinery does not change. We will still produce an estimate, a standard error, and an
        interval, and we will still ask what chance alone would produce.
\end{itemize}
\begin{principle}{same template, new estimate}
A slope is an estimate like any other. Everything you learned about reading a difference applies
to reading a slope.
\end{principle}
\end{frame}
""")])

# ---- Unit 5 (causal), now following prediction ------------------------------
patch("Unit_05_Causal_Thinking",
 [("Where this fits", r"""\begin{frame}{Where this fits}
\begin{itemize}
  \item Units 2 through 4 built models, checked them honestly, and predicted with them. Every one
        of those answers an \emph{association} question: given what I see, what do I expect?
  \item Every decision anyone actually needs is a \emph{causal} question: if we change the price,
        send the email, launch the program, what happens?
  \item These are different questions, and no amount of model accuracy converts one into the
        other.
\end{itemize}
\begin{principle}{prediction and intervention are not the same job}
A model can predict rain beautifully from barometer readings. Smashing the barometer does not stop
the rain.
\end{principle}
\end{frame}
""")])

# ---- Unit 6 (data provenance), the hinge into Part II ----------------------
patch("Unit_06_Where_the_Data_Comes_From",
 [("Where we go next", r"""\begin{frame}{Where we go next}
\begin{itemize}
  \item That closes Part I. Five units of building models and one on whether the data underneath
        them deserved the trust.
  \item Sampling raised a question we have been dodging since Unit 1: what does \emph{random}
        actually mean, and how do we compute with it?
  \item \textbf{Part II} answers it. Unit 7 does probability, Unit 8 puts numbers on uncertain
        outcomes, and \textbf{Unit 9} finally proves the result every standard error in Part I was
        quietly assuming.
\end{itemize}
\begin{principle}{the habit to keep}
The most important question in any analysis comes before the first line of code: where did this
data come from, and who is not in it?
\end{principle}
\end{frame}
""")])

# ---- Unit 9 (normal/CLT): now the payoff unit ------------------------------
patch("Unit_09_Normal_and_the_CLT",
 [("Where this fits", r"""\begin{frame}{Where this fits}
\begin{itemize}
  \item Since Unit 1 we have written $\text{estimate} \pm 2 \times \text{SE}$ and moved on. This
        unit is where that gets earned.
  \item The claim we have been leaning on is that an \emph{estimate}, a mean or a difference or a
        slope, has a distribution that is close to normal, almost regardless of what the data
        looks like.
  \item That claim is the central limit theorem, and it is the reason a single formula covered
        every test and interval in Part I.
\end{itemize}
\begin{principle}{the debt comes due}
The bell curve is not common because nature loves it. It is common because \emph{adding things up}
produces it, and an average is a sum.
\end{principle}
\end{frame}
""")])

# ---- Unit 11 (categorical) -------------------------------------------------
patch("Unit_11_Categorical_Outcomes",
 [("Where this fits", r"""\begin{frame}{Where this fits}
\begin{itemize}
  \item Part I predicted \emph{numbers}. An enormous share of real data is not a number: converted
        or not, churned or not, fraud or not, which region, which plan.
  \item This unit needed Part II first. Odds, base rates, and predictive values are conditional
        probability wearing different hats, and we only built that in Unit 7.
  \item Three arcs: describing rates honestly, comparing them in tables, and modeling a yes or no
        and turning it into a decision.
\end{itemize}
\begin{principle}{a rate is a fraction with a story on both floors}
Every rate has a numerator and a denominator, and most arguments about rates are really arguments
about the denominator.
\end{principle}
\end{frame}
""")])

# ---- Unit 12 (bayesian), the finale ----------------------------------------
patch("Unit_12_Bayesian_Reasoning_and_Decisions",
 [("Where this fits", r"""\begin{frame}{Where this fits}
\begin{itemize}
  \item Everything so far asked: if the null were true, how surprising is this data?
  \item The question people actually ask is the reverse: given this data, what should I now
        believe, and what should I do?
  \item That reversal is Bayes' rule, which you built in Unit 7 for medical tests. Here we point
        it at the unknown quantity itself, and then at the decision.
\end{itemize}
\begin{principle}{the question you were always trying to answer}
A $p$-value is $\PR{\text{data} \mid \text{hypothesis}}$. A posterior is
$\PR{\text{hypothesis} \mid \text{data}}$. People misread the first as the second constantly,
because the second is what they wanted.
\end{principle}
\end{frame}
"""),
  ("Where we go next", r"""\begin{frame}{Where the course ends}
\begin{itemize}
  \item Part I gave you models and the discipline to distrust them. Part II gave you the machinery
        underneath and two applications that needed it.
  \item What ties them together is one move, repeated: produce a number, say how much it could
        have been otherwise, and say what would have to be true for it to mean what you claim.
\end{itemize}
\begin{principle}{the whole course, in one sentence}
Anyone can produce a number. You have been trained to ask what would have to be true for that
number to mean anything.
\end{principle}
\end{frame}
""")])
