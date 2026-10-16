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
\usepackage{graphicx}
\usepackage[colorlinks=true,linkcolor=black,urlcolor=black]{hyperref}
\setlist[enumerate]{itemsep=4pt, topsep=3pt}
\pagestyle{plain}
\begin{document}
"""


def _looks_patterned(seq):
    """True if a student could beat the paper by spotting the answer order."""
    if len(seq) < 8:
        return False
    for period in (1, 2, 3, 4, 5):
        if all(seq[i] == seq[i - period] for i in range(period, len(seq))):
            return True
    run = best = 1
    for i in range(1, len(seq)):
        run = run + 1 if seq[i] == seq[i - 1] else 1
        best = max(best, run)
    return best >= 4


def balance(questions, seed=0):
    """Move each correct option to a position drawn from a shuffled, even pool.

    The first version of this walked the positions in order, `i % 4`, which
    spread the answers perfectly evenly and produced A, B, C, D, A, B, C, D
    down the whole paper. Even is not the same as unpredictable, and the order
    is what a student sitting the exam can actually see.

    Positions now come from a near-even pool shuffled with a fixed seed, so a
    given paper always balances the same way, and the result is rejected and
    reshuffled if it falls into a cycle or a long run.
    """
    import random

    fixed = [i for i, q in enumerate(questions)
             if all(o.startswith("Panel ") for o in q[1])]
    movable = [i for i in range(len(questions)) if i not in fixed]

    pool = [i % 4 for i in range(len(movable))]
    rng = random.Random(seed)
    for _ in range(500):
        rng.shuffle(pool)
        targets = dict(zip(movable, pool))
        letters = ["ABCD"[targets.get(i, questions[i][2])] for i in range(len(questions))]
        if not _looks_patterned(letters):
            break
    else:
        raise RuntimeError("could not find an unpatterned answer order")

    out = []
    for i, (stem, options, ans, why) in enumerate(questions):
        if i in fixed:
            out.append((stem, list(options), ans, why))
            continue
        target = targets[i]
        opts = list(options)
        opts[target], opts[ans] = opts[ans], opts[target]
        out.append((stem, opts, target, why))
    return out


def check_questions(questions, label=""):
    """Every item needs exactly four options and an answer index inside them.

    A line-wrapped option that loses its implicit concatenation silently
    becomes two options, and the paper prints (A) through (E) without
    complaint. This catches it at build time instead.
    """
    for i, q in enumerate(questions, 1):
        opts, ans = q[1], q[2]
        if len(opts) != 4:
            raise ValueError(f"{label} question {i}: {len(opts)} options, expected 4")
        if not 0 <= ans < 4:
            raise ValueError(f"{label} question {i}: answer index {ans} is out of range")
        if len(set(opts)) != 4:
            raise ValueError(f"{label} question {i}: two options are identical")


def mc_block(questions, show_answers, figures=None):
    """questions: list of (stem, [options], answer_index, why)

    `figures` maps a question's 0-based index to (filename, width, span). The
    figure is printed above that question and the run of `span` questions it
    covers, with a line saying which numbers it belongs to. The enumerate is
    closed and resumed so the numbering carries on.
    """
    figures = figures or {}
    out = []
    for i, (stem, options, ans, why) in enumerate(questions):
        opts = "\n".join(r"  \item %s" % o for o in options)
        body = []
        if i in figures:
            fname, width, span = figures[i]
            first, last = i + 1, i + span
            which = (f"Question {first} refers" if span == 1
                     else f"Questions {first} to {last} refer")
            # a figure that several questions depend on starts its own page, so
            # the run cannot split and leave someone answering with the picture
            # on the sheet before
            body += [r"\end{enumerate}",
                     r"\clearpage" if span > 1 else "",
                     r"\begin{center}\includegraphics[width=%s\textwidth]{%s}\end{center}"
                     % (width, fname),
                     r"\noindent\textit{%s to the figure above.}" % which,
                     r"\vspace{4pt}",
                     r"\begin{enumerate}[resume]"]
        body += [r"\item %s" % stem,
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


def _may_rebuild(tag):
    """True only if the run was told to rebuild THIS exam's notebook.

    These notebooks get edited by hand, so a bare --force-notebooks used to
    overwrite every one of them, including exams already in student hands.
    The flag now has to name the exam: --force-notebooks=B
    """
    for a in sys.argv:
        if a.startswith("--force-notebooks="):
            return tag in a.split("=", 1)[1].split(",")
    return False


def build_exam(tag, title, blurb, dataset, columns, setup_code, mc, tasks, data_note):
    mc = balance(mc, seed=sum(ord(c) for c in tag) + 7)
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
    if path.exists() and not _may_rebuild(tag):
        # these get edited by hand, and a rebuild must not quietly undo that
        print(f"kept Exams/{path.name} as it is "
              f"(pass --force-notebooks={tag} to rebuild it)")
    else:
        nbf.write(nb, path)
        print(f"wrote Exams/{path.name} ({len(cells)} cells)")


AI_POLICY_TEX = r"""\vspace{6pt}
\textbf{Getting help.} You may use AI, and you may ask the TAs, the professor, and each other.
Two limits on the AI:

\begin{itemize}\itemsep1pt
  \item Do not paste the whole notebook into it.
  \item Do not give it an entire task prompt and ask for the answer. If a prompt is unclear,
        you can paste a whole task prompt in to help clarify.
\end{itemize}

\noindent Everything else is open. Use the generate function in Colab or your editor to help write
the code, ask about a specific piece of output, or have a piece of your work checked.

\noindent Use the methods from this course. A technique we have not covered is a sign
that the AI has been asked for the answer rather than for help."""

AI_POLICY_MD = """**Getting help.** You may use AI, and you may ask the TAs, the professor, and \
each other. Two limits on the AI:

- Do not paste the whole notebook into it.
- Do not give it an entire task prompt and ask for the answer. If a prompt is unclear, you can \
paste a whole task prompt in to help clarify.

Everything else is open. Use the generate function in Colab or your editor to help write the code, \
ask about a specific piece of output, or have a piece of your work checked.\n\nUse the methods from this course. A technique we have not covered is a sign that the AI has been asked for the answer rather than for help."""


def build_takehome(tag, title, blurb, dataset, columns, setup_code, tasks, data_note):
    """Midterm B: the analysis, on its own. The multiple choice is a separate paper."""
    cols = "\n".join(r"\texttt{%s} & %s \\" % (c, d) for c, d in columns)
    total = sum(t[2] for t in tasks)
    head = r"""
\begin{center}
{\Large\textbf{Stat 220 Midterm %s: the take-home analysis}}\\[4pt]
{\large %s}\\[8pt]
\end{center}

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

\vspace{4pt}
\textbf{%d points in all.} Work the tasks in order; several of them build on an earlier one.
Show the output you are reading from, and answer in sentences, not in numbers alone.

%s

\vspace{6pt}\hrule\vspace{8pt}

\begin{enumerate}
%s
\end{enumerate}
"""
    exam = PREAMBLE + head % (tag, title, blurb, cols, data_note, total, AI_POLICY_TEX,
                              applied_block(tasks, False)) + "\n\\end{document}\n"
    build_pdf(f"Midterm_{tag}_TakeHome", exam)

    key = PREAMBLE + r"""
\begin{center}
{\Large\textbf{Stat 220 Midterm %s take-home: answer key}}\\[4pt]
{\large %s}\\[6pt]
\end{center}

\textit{Instructor copy. For each task, what a full-credit answer contains, with the
numbers this data actually produces, so a grader can check a student's output
without rerunning anything.}

\vspace{6pt}\hrule\vspace{8pt}

\begin{enumerate}
%s
\end{enumerate}
""" % (tag, title, applied_block(tasks, True)) + "\n\\end{document}\n"
    build_pdf(f"Midterm_{tag}_TakeHome_Key", key)

    nb = nbf.v4.new_notebook()
    cells = [nbf.v4.new_markdown_cell(
        f"# Stat 220 Midterm {tag}: the take-home analysis\n## {title}\n\n{blurb}\n\n"
        f"**{total} points in all.** Run the setup cell first. Put your work in the cell under "
        "each task and your written answer in the markdown cell that follows it. Several tasks "
        f"build on an earlier one, so work them in order.\n\n---\n\n{AI_POLICY_MD}"),
        nbf.v4.new_code_cell(setup_code)]
    for n, (t, prompt, points, _) in enumerate(tasks, 1):
        # the student notebook carries no task titles. Several of them named the
        # answer ("A column that adds nothing"), and the rest set an expectation
        # before the student had read the prompt. The titles stay in the key,
        # where they are a grader's index.
        cells.append(nbf.v4.new_markdown_cell(
            f"### Task {n}.  ({points} points)\n\n{_to_markdown(prompt)}"))
        cells.append(nbf.v4.new_code_cell(""))
        cells.append(nbf.v4.new_markdown_cell("_Your answer:_\n\n"))
    nb["cells"] = cells
    nb["metadata"] = {"kernelspec": {"display_name": "Python 3", "language": "python",
                                     "name": "python3"},
                      "language_info": {"name": "python"}}
    path = OUT / f"Midterm_{tag}_TakeHome.ipynb"
    if path.exists() and not _may_rebuild(tag):
        print(f"kept Exams/{path.name} as it is "
              f"(pass --force-notebooks={tag} to rebuild it)")
    else:
        nbf.write(nb, path)
        print(f"wrote Exams/{path.name} ({len(cells)} cells)")


def build_mc_exam(questions, name="Midterm_MC", title="Units 1 through 5", per=2):
    """The question paper, and an instructor key.

    `title` labels the key only. It stays off the student paper, which says
    nothing about which units it covers or how it is invigilated: this is sat
    in a testing centre, and the rules there are theirs, not the paper's.
    """
    from collections import Counter
    check_questions(questions, name)
    meta = [(q[4], q[5]) for q in questions]
    figures = {i: q[6] for i, q in enumerate(questions) if len(q) > 6 and q[6]}
    quad = balance([(q[0], q[1], q[2], q[3]) for q in questions],
                   seed=sum(ord(c) for c in name))
    total = len(quad) * per

    head = r"""
\thispagestyle{empty}
\vspace*{2.6in}
\begin{center}
{\Huge\textbf{Stat 220 Midterm}}\\[26pt]
{\Large %d questions}
\end{center}
\newpage
\setcounter{page}{1}

Mark your answers on the bubble sheet.

\vspace{6pt}\hrule\vspace{10pt}

\begin{enumerate}
%s
\end{enumerate}
"""
    exam = PREAMBLE + head % (len(quad), mc_block(quad, False, figures)) + "\n\\end{document}\n"
    build_pdf(f"{name}_Exam", exam)

    units = Counter(u for u, _ in meta)
    kinds = Counter(k for _, k in meta)
    tally = ", ".join(f"Unit {u}: {n}" for u, n in sorted(units.items()))
    letters = Counter("ABCD"[a] for _, _, a, _ in quad)
    spread = ", ".join(f"{L}: {letters.get(L, 0)}" for L in "ABCD")

    key = PREAMBLE + r"""
\begin{center}
{\Large\textbf{Stat 220 Midterm: answer key}}\\[4pt]
{\large %s}\\[6pt]
\end{center}

\textit{Instructor copy. %s. Answers spread across the four positions: %s.
%d of the %d questions are the same idea as a practice-guide question in new clothes;
the other %d ask the student to put two ideas together or read a result they have not
been handed before.}

\vspace{6pt}\hrule\vspace{8pt}

\begin{enumerate}
%s
\end{enumerate}
""" % (title, tally, spread, kinds["echo"], len(quad), kinds["new"],
       mc_block(quad, True, figures)) + "\n\\end{document}\n"
    build_pdf(f"{name}_Key", key)
    print(f"   {tally};  answer positions {spread};  "
          f"{kinds['echo']} echo / {kinds['new']} new")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    import exam_content_a, exam_content_b, exam_content_mc, exam_content_mc2
    build_exam(**exam_content_a.EXAM)          # A stays a complete two-part exam
    build_takehome(**exam_content_b.EXAM)      # B is the take-home analysis
    build_mc_exam(exam_content_mc.QUESTIONS, name="Midterm_MC",
                  title="paper 1, released to students as practice")
    build_mc_exam(exam_content_mc2.QUESTIONS, name="Midterm_MC2",
                  title="paper 2, the live exam")
