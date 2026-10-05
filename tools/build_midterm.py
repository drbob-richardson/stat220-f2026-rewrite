#!/usr/bin/env python3
"""Build the two midterm exams.

Each exam has two parts:

  Part 1  multiple choice, in the style of the practice guides (40 points)
  Part 2  a guided applied problem on a dataset the student has not seen,
          with a fixed place for each piece of work (60 points)

For each exam this writes, into Exams/:

  Midterm_<X>_Exam.pdf      what the student sees, both parts
  Midterm_<X>_Key.pdf       answers, the numbers, and what earns credit
  Midterm_<X>_Applied.ipynb the notebook the student fills in

Exams/ is gitignored, so the keys never reach a public repository.

Run:  python tools/build_midterm.py
"""
import json
import subprocess
import sys
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Exams"
DATA_URL = "https://drbob-richardson.github.io/stat220/F2026/data"

PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[margin=0.85in,letterpaper]{geometry}
\usepackage{enumitem}
\usepackage{amsmath}
\usepackage{parskip}
\usepackage{booktabs}
\usepackage[colorlinks=true,linkcolor=black,urlcolor=black]{hyperref}
\setlist[enumerate]{itemsep=4pt, topsep=3pt}
\pagestyle{plain}
\begin{document}
"""


def balance(questions):
    """Spread the correct answers evenly across A, B, C, D.

    Each question's correct option is swapped into a target slot, cycling
    through the four positions. Swapping two independent options changes
    nothing about the question, and it keeps a reader from noticing that the
    right answer is usually B.
    """
    out = []
    for i, (stem, options, ans, why) in enumerate(questions):
        target = i % 4
        opts = list(options)
        opts[target], opts[ans] = opts[ans], opts[target]
        out.append((stem, opts, target, why))
    return out


def mc_block(questions, show_answers):
    """questions: list of (stem, [options], answer_index, why)"""
    out = []
    for stem, options, ans, why in questions:
        opts = "\n".join(r"  \item %s" % o for o in options)
        body = [r"\item %s" % stem,
                r"\begin{enumerate}[label=(\Alph*)]", opts, r"\end{enumerate}"]
        if show_answers:
            body.append(r"\textbf{Answer: (%s)} %s" % ("ABCD"[ans], why))
        out.append("\n".join(body))
    return "\n\n".join(out)


def applied_block(tasks, show_answers):
    out = []
    for n, (title, prompt, points, sketch) in enumerate(tasks, 1):
        body = [r"\item \textbf{%s} \hfill (%d points)" % (title, points), "", prompt]
        if show_answers:
            body += ["", r"\textbf{Full credit:} %s" % sketch]
        out.append("\n".join(body))
    return "\n\n".join(out)


def _to_markdown(text):
    """The LaTeX used in a prompt, rendered for a notebook cell."""
    import re
    text = re.sub(r"\\texttt\{([^}]*)\}", r"`\1`", text)
    text = re.sub(r"\\textbf\{([^}]*)\}", r"**\1**", text)
    text = re.sub(r"\\emph\{([^}]*)\}", r"*\1*", text)
    return text.replace(r"\%", "%").replace(r"\$", "$").replace("\\_", "_")


def build_pdf(name, tex):
    src = OUT / f"{name}.tex"
    src.write_text(tex)
    for _ in range(2):
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", src.name],
                       cwd=OUT, capture_output=True)
    pdf = OUT / f"{name}.pdf"
    if not pdf.exists():
        log = (OUT / f"{name}.log").read_text()[-1500:]
        print(f"FAILED: {name}\n{log}")
        sys.exit(1)
    pages = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    pages = [l.split()[-1] for l in pages.splitlines() if l.startswith("Pages")][0]
    print(f"wrote Exams/{name}.pdf ({pages} pages)")
    for ext in (".aux", ".log", ".out"):
        (OUT / f"{name}{ext}").unlink(missing_ok=True)


def build_exam(tag, title, blurb, dataset, columns, setup_code, mc, tasks, data_note):
    mc = balance(mc)
    cols = "\n".join(r"\texttt{%s} & %s \\" % (c, d) for c, d in columns)
    head = r"""
\begin{center}
{\Large\textbf{Stat 220 Midterm, %s}}\\[4pt]
{\large %s}\\[8pt]
\end{center}

%s

\vspace{6pt}\hrule\vspace{10pt}

{\large\textbf{Part 1. Multiple choice}} \hfill (40 points, 2 each)

Circle one answer for each question.

\begin{enumerate}
%s
\end{enumerate}

\newpage
{\large\textbf{Part 2. The analysis}} \hfill (60 points)

%s

\vspace{4pt}
\begin{center}\small
\begin{tabular}{ll}
\toprule
\textbf{Column} & \textbf{What it is} \\
\midrule
%s
\bottomrule
\end{tabular}
\end{center}

%s

\begin{enumerate}
%s
\end{enumerate}
"""
    exam = PREAMBLE + head % (tag, title, blurb, mc_block(mc, False), dataset, cols,
                              data_note, applied_block(tasks, False)) + "\n\\end{document}\n"
    build_pdf(f"Midterm_{tag}_Exam", exam)

    key = PREAMBLE + r"""
\begin{center}
{\Large\textbf{Stat 220 Midterm %s: answer key}}\\[4pt]
{\large %s}\\[6pt]
\end{center}

\textit{Instructor copy. Part 1 answers are below; Part 2 lists what a full-credit
answer contains, with the numbers this data actually produces.}

\vspace{6pt}\hrule\vspace{8pt}

{\large\textbf{Part 1}}

\begin{enumerate}
%s
\end{enumerate}

\newpage
{\large\textbf{Part 2}}

\begin{enumerate}
%s
\end{enumerate}
""" % (tag, title, mc_block(mc, True), applied_block(tasks, True)) + "\n\\end{document}\n"
    build_pdf(f"Midterm_{tag}_Key", key)

    # the notebook the student fills in
    nb = nbf.v4.new_notebook()
    cells = [nbf.v4.new_markdown_cell(
        f"# Stat 220 Midterm, {tag}\n## Part 2: {title}\n\n{blurb}\n\n"
        "Run the setup cell first. Put your work in the cell under each task, and your written "
        "answers in the markdown cell that follows it."),
        nbf.v4.new_code_cell(setup_code)]
    for n, (t, prompt, points, _) in enumerate(tasks, 1):
        clean = _to_markdown(prompt)
        cells.append(nbf.v4.new_markdown_cell(f"### Task {n}. {t}  ({points} points)\n\n{clean}"))
        cells.append(nbf.v4.new_code_cell(""))
        cells.append(nbf.v4.new_markdown_cell("_Your answer:_\n\n"))
    nb["cells"] = cells
    nb["metadata"] = {"kernelspec": {"display_name": "Python 3", "language": "python",
                                     "name": "python3"},
                      "language_info": {"name": "python"}}
    path = OUT / f"Midterm_{tag}_Applied.ipynb"
    if path.exists() and "--force-notebooks" not in sys.argv:
        # these get edited by hand, and a rebuild must not quietly undo that
        print(f"kept Exams/{path.name} as it is (pass --force-notebooks to rebuild it)")
    else:
        nbf.write(nb, path)
        print(f"wrote Exams/{path.name} ({len(cells)} cells)")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    import exam_content_a, exam_content_b
    build_exam(**exam_content_a.EXAM)
    build_exam(**exam_content_b.EXAM)
