#!/usr/bin/env python3
"""Build closed-book question banks, one PDF per topic.

Every question is scenario-based and answerable with a pencil: no software, no
arithmetic beyond what fits in the margin. Each carries a short answer sketch for
whoever grades it. Files are named by topic, not unit number, so they survive any
reordering of the course.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[margin=0.9in,letterpaper]{geometry}
\usepackage{enumitem}
\usepackage{amsmath}
\usepackage{parskip}
\usepackage[colorlinks=true,linkcolor=black]{hyperref}
\setlist[enumerate]{itemsep=7pt, topsep=5pt}
\pagestyle{plain}
\begin{document}
"""

def build(slug, title, blurb, questions):
    """questions: list of (question_text, answer_sketch)"""
    q = "\n".join(r"\item %s" % text for text, _ in questions)
    a = "\n".join(r"\item %s" % ans for _, ans in questions)
    tex = PREAMBLE + r"""
\begin{center}
{\Large\textbf{Stat 220: %s}}\\[3pt]
{\large Closed-book question bank}\\[6pt]
\end{center}

%s

\vspace{8pt}
\hrule
\vspace{10pt}

\begin{enumerate}
%s
\end{enumerate}

\newpage
\begin{center}{\large\textbf{Answer sketches (instructor copy)}}\end{center}

\small
These are what a full-credit answer contains, not model prose. Most of these are
graded on whether the student names the right consideration, not on wording.

\begin{enumerate}
%s
\end{enumerate}

\end{document}
""" % (title, blurb, q, a)
    src = HERE / f"Practice_{slug}.tex"
    src.write_text(tex)
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", src.name],
                       cwd=HERE, capture_output=True, text=True)
    pdf = HERE / f"Questions_{slug}.pdf"
    ok = pdf.exists()
    for ext in (".aux", ".log", ".out"):
        (HERE / f"Questions_{slug}{ext}").unlink(missing_ok=True)
    print(f"  {slug:<20} {len(questions):>2} questions   {'PDF ok' if ok else 'COMPILE FAILED'}")
    if not ok:
        print(r.stdout[-800:])
    return ok


def build_mc(slug, title, blurb, questions):
    """Multiple-choice study guide. Each question is followed by its answer.

    questions: list of (stem, [options], answer_index, explanation)
    Because the answers sit inline, this is a STUDENT-FACING practice document.
    Do not reuse these items as live exam questions.
    """
    body = []
    for stem, opts, ans, expl in questions:
        letters = "ABCDEFGH"
        choices = "\n".join(r"  \item %s" % o for o in opts)
        body.append(
            r"""\item %s

\begin{enumerate}[label=\Alph*., itemsep=1pt, topsep=3pt]
%s
\end{enumerate}

\vspace{2pt}
\textbf{Answer: %s.} %s
\vspace{4pt}
""" % (stem, choices, letters[ans], expl))
    tex = PREAMBLE + r"""
\begin{center}
{\Large\textbf{Stat 220: %s}}\\[3pt]
{\large Midterm practice questions, with answers}\\[6pt]
\end{center}

%s

\vspace{8pt}
\hrule
\vspace{10pt}

\begin{enumerate}[itemsep=14pt]
%s
\end{enumerate}

\end{document}
""" % (title, blurb, "\n".join(body))
    src = HERE / f"Practice_{slug}.tex"
    src.write_text(tex)
    subprocess.run(["pdflatex", "-interaction=nonstopmode", src.name],
                   cwd=HERE, capture_output=True)
    subprocess.run(["pdflatex", "-interaction=nonstopmode", src.name],
                   cwd=HERE, capture_output=True)
    print(f"wrote Practice_{slug}.pdf  ({len(questions)} questions)")
