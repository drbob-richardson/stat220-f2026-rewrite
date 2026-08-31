#!/usr/bin/env python3
"""Make the in-class activities runnable.

Adds a one-line materials/time note under every live demo, restores the
tree-building activity that the Unit 6 merge dropped, and points the Unit 3
demo at its printable handout.
"""
from pathlib import Path

SLIDES = Path(__file__).resolve().parents[1] / "Slides"

# Keyed by the livedemo's title so each note lands under the right demo.
NOTES = {
 "the taste test":
   "Materials: one bottle each of Coke and Coke Zero, 10 opaque cups, a screen to pour behind. "
   "Time: 10 minutes.",
 "the two-sample taste test":
   "Materials: the same setup, one more volunteer. Time: 5 minutes.",
 "half of you will lie to me":
   "Materials: paper. Time: 8 minutes to write, 5 to sort and reveal.",
 "a sealed-bid auction for three gambles":
   "Materials: slips of paper. Time: 8 minutes. Do not reveal the expected values until the bids "
   "are collected.",
 "the class becomes the simulation":
   "Materials: the printed price handout (\\texttt{Unit\\_03\\_Price\\_Handout.pdf}), sticky notes, "
   "a board with two labeled axes. Time: 15 minutes.",
 "estimate what you cannot see":
   "Materials: a bag of numbered tickets, or just draw them on screen. Time: 15 minutes, including "
   "scoring each team's rule on fresh draws.",
 "a quick contest":
   "Materials: none. Time: 6 minutes.",
 "predict shoe size from height":
   "Materials: 10 volunteers, a tape measure if handy. Time: 12 minutes.",
 "you build the tree, one split at a time":
   "Materials: the board. Time: 15 minutes.",
 "how good is your sense of uncertainty?":
   "Materials: paper. Time: 10 minutes. Collect the intervals before showing any answers.",
 "can you be random?":
   "Materials: none. Time: 8 minutes including tallying the throws.",
 "you are the spam filter":
   "Materials: the email table on the next slide. Time: 10 minutes.",
 "everyone roll two dice":
   "Materials: dice, or a phone. Time: 10 minutes.",
 "stand on the probability line":
   "Materials: two opaque bags, about 30 red and 30 white chips, a marked wall or floor line. "
   "Time: 12 minutes.",
 "estimate the same number three ways":
   "Materials: none, but have the roster handy for the random draw. Time: 12 minutes.",
 "two minutes, out loud, no notes":
   "Materials: printed scenario cards (\\texttt{Unit\\_12\\_Scenario\\_Cards.pdf}). Time: 30 minutes "
   "for the full bracket.",
}

TREE_ACTIVITY = r"""\begin{frame}{Live experiment: the class builds a tree}
\begin{livedemo}{you build the tree, one split at a time}
On the board: 30 cars with weight, horsepower, model year, and mpg. The goal is to predict mpg.
\begin{enumerate}
  \item By vote, pick \textbf{one variable and one cutoff} to split the 30 cars into two groups.
  \item I compute the error after your split on those 30 cars, and also on \textbf{10 cars you
        have not seen}.
  \item Keep going. Each round, vote on which group to split next.
\end{enumerate}
\end{livedemo}
\centering\small We stop when somebody in the room says stop. Then we look at the two error curves.
\end{frame}

\begin{frame}{What happens every time we run it}
\begin{itemize}
  \item The error on the 30 cars falls after \emph{every single split}. It has to: more groups
        means a closer fit to the points being fitted.
  \item The error on the 10 held-out cars falls for the first few splits, flattens, and then
        climbs.
  \item Nobody in the room can feel where that turn happens, and the training error gives no
        warning at all.
\end{itemize}
\begin{principle}{why the stopping rule cannot come from the training data}
You cannot detect overfitting from the data you fit. That is the entire job of the held-out set,
and of the cross-validation we set up yesterday.
\end{principle}
\end{frame}

"""


def add_notes(text):
    """Put a materials/time line just after each \\end{livedemo}."""
    added = 0
    for title, note in NOTES.items():
        opener = "\\begin{livedemo}{" + title + "}"
        if opener not in text:
            continue
        start = text.index(opener)
        end = text.index("\\end{livedemo}", start) + len("\\end{livedemo}")
        marker = "\n\\vspace{0.2em}\n{\\tiny\\textit{"
        if text[end:end + len(marker)] == marker:
            continue                      # already annotated
        text = text[:end] + marker + note + "}}" + text[end:]
        added += 1
    return text, added


def main():
    total_notes = 0
    for path in sorted(SLIDES.glob("Unit_*.tex")):
        s = original = path.read_text()

        # Unit 6 lost its Day 3 activity in the merge. Put it back at the top of Day 3.
        if path.stem.startswith("Unit_06") and "the class builds a tree" not in s:
            anchor = "\\begin{frame}{What a tree does}"
            s = s.replace(anchor, TREE_ACTIVITY + anchor, 1)

        # Unit 3's demo needs the handout named on the slide.
        if path.stem.startswith("Unit_03"):
            s = s.replace(
                "Each of you gets the same list of 200 house prices (badly right-skewed: lots of "
                "modest homes, a\nfew mansions).",
                "Everyone gets the same printed list of 200 house prices. It is badly right-skewed: "
                "mostly\nmodest homes, a few mansions.")

        s, n = add_notes(s)
        total_notes += n
        if s != original:
            path.write_text(s)
        print(f"{path.stem:<46} activity notes added: {n}")
    print(f"\ntotal notes: {total_notes}")


if __name__ == "__main__":
    main()
