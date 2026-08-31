"""Shared surgery for turning a Module_NN deck into a 3-day Unit_NN deck.

The repeated edits: soften the interview framing, collapse the three "learning
contract" frames into one, merge the two question-bank frames, retitle the
consolidation frames, and insert Day dividers.
"""
import re
from pathlib import Path

REF = Path(__file__).resolve().parents[1].parent / "ref"
OUT = Path(__file__).resolve().parents[1] / "Slides"


def load(module_name, unit_file):
    s = (REF / module_name).read_text()
    return s, OUT / unit_file


def preamble(s):
    """Add the softer green block and keep `interview` for rare, deliberate use."""
    old = (r"\newenvironment{interview}[1]{\begin{exampleblock}"
           r"{\textbf{Interview question:} #1}}{\end{exampleblock}}")
    new = (r"\newenvironment{practice}[1]{\begin{exampleblock}"
           r"{\textbf{In practice:} #1}}{\end{exampleblock}}" + "\n" +
           r"\newenvironment{interview}[1]{\begin{exampleblock}"
           r"{\textbf{You may be asked:} #1}}{\end{exampleblock}}")
    if old in s:
        s = s.replace(old, new)
    return s


def subtitle(s, unit_no, new_subtitle=None):
    m = re.search(r"\\subtitle\{([^}]*)\}", s)
    if not m:
        return s
    text = new_subtitle if new_subtitle else re.sub(r"^Part \d+: ", "", m.group(1))
    return s[:m.start()] + f"\\subtitle{{Unit {unit_no}: {text}}}" + s[m.end():]


def soften_green(s, keep=0):
    """Demote every `interview` block to `practice`, optionally keeping the last `keep`."""
    s = s.replace(r"\begin{interview}{", r"\begin{practice}{")
    s = s.replace(r"\end{interview}", r"\end{practice}")
    if keep:
        # promote the last `keep` occurrences back
        parts = s.rsplit(r"\begin{practice}{", keep)
        s = parts[0] + "".join(r"\begin{interview}{" + p for p in parts[1:])
        parts = s.rsplit(r"\end{practice}", keep)
        s = parts[0] + "".join(r"\end{interview}" + p for p in parts[1:])
    return s


def contract(s, know, avoid):
    """Replace the three learning-contract frames with one two-column frame."""
    start = s.index(r"\begin{frame}{The learning contract: (a)")
    # the contract frames are always followed by a section comment banner
    end = s.index("% " + "=" * 70, start)
    know_items = "\n".join(f"  \\item {k}" for k in know)
    avoid_items = "\n".join(f"  \\item {a}" for a in avoid)
    new = (r"\begin{frame}{What this unit gives you}" "\n"
           r"\begin{columns}[T]" "\n"
           r"\begin{column}{0.5\textwidth}" "\n"
           r"\textbf{Things to know}" "\n"
           r"\begin{itemize}\small" "\n" + know_items + "\n"
           r"\end{itemize}" "\n"
           r"\end{column}" "\n"
           r"\begin{column}{0.5\textwidth}" "\n"
           r"\textbf{Mistakes to stop making}" "\n"
           r"\begin{itemize}\small" "\n" + avoid_items + "\n"
           r"\end{itemize}" "\n"
           r"\end{column}" "\n"
           r"\end{columns}" "\n"
           r"\end{frame}" "\n\n")
    return s[:start] + new + s[end:]


def question_bank(s, questions, title="Ten questions to be able to answer"):
    """Merge the two interview-question-bank frames into a single frame."""
    start = s.index(r"\begin{frame}{(b) The interview-question bank (1 of 2)}")
    end = s.index(r"\begin{frame}{(a) The principles: mastery checklist}")
    items = "\n".join(f"  \\item {q}" for q in questions)
    new = (f"\\begin{{frame}}{{{title}}}\n"
           r"\begin{enumerate}\small" "\n" + items + "\n"
           r"\end{enumerate}" "\n"
           r"\end{frame}" "\n\n")
    return s[:start] + new + s[end:]


def consolidate_headings(s):
    s = s.replace(r"\begin{frame}{(c) The traps, all in one place}",
                  r"\begin{frame}{The traps, all in one place}")
    s = s.replace(r"\begin{trap}{carry this list into every interview}",
                  r"\begin{trap}{the list worth carrying}")
    s = s.replace(r"\begin{frame}{(a) The principles: mastery checklist}",
                  r"\begin{frame}{Mastery checklist}")
    s = s.replace("You've mastered this module when you can, from memory:",
                  "You have this unit when you can, from memory:")
    s = s.replace("By the end of this module you should", "By the end of this unit you should")
    return s


def day(number, title, bullets):
    """A full-bleed day-divider frame."""
    items = "\n".join(f"  \\item {b}" for b in bullets)
    return (r"\begin{frame}[plain]" "\n"
            r"\vfill" "\n"
            r"\centering" "\n"
            f"{{\\Large\\textbf{{Day {number}}}}}\\\\[6pt]\n"
            f"{{\\large {title}}}\\\\[14pt]\n"
            r"\begin{minipage}{0.74\textwidth}\small" "\n"
            r"\begin{itemize}" "\n" + items + "\n"
            r"\end{itemize}" "\n"
            r"\end{minipage}" "\n"
            r"\vfill" "\n"
            r"\end{frame}" "\n\n")


def insert_before(s, anchor, text):
    i = s.index(anchor)
    return s[:i] + text + s[i:]


def replace_frame(s, frame_title, new_text):
    """Swap out a whole frame identified by its title."""
    start = s.index("\\begin{frame}{" + frame_title + "}")
    end = s.index(r"\end{frame}", start) + len(r"\end{frame}") + 1
    return s[:start] + new_text + s[end:]


def save(s, path):
    Path(path).write_text(s)
    n_frames = s.count(r"\begin{frame}")
    print(f"wrote {Path(path).name}  ({n_frames} frames)")


# --------------------------------------------------------------------------
# Frame-level surgery, for building a merged unit out of two source decks.
# --------------------------------------------------------------------------
def frames(module_name):
    """Return {frame title: full frame source} for a deck in ref/."""
    s = (REF / module_name).read_text()
    out, pos = {}, 0
    while True:
        i = s.find(r"\begin{frame}{", pos)
        if i < 0:
            break
        j = s.index("}", i + len(r"\begin{frame}{"))
        # handle titles containing braces, e.g. {Your turn \#1}
        depth, k = 1, i + len(r"\begin{frame}{")
        while depth:
            if s[k] == "{":
                depth += 1
            elif s[k] == "}":
                depth -= 1
            k += 1
        title = s[i + len(r"\begin{frame}{"):k - 1]
        end = s.index(r"\end{frame}", k) + len(r"\end{frame}")
        out[title] = s[i:end] + "\n"
        pos = end
    return out


def preamble_of(module_name, unit_no, title, subtitle_text):
    """Reuse a source deck's preamble, with the softened green block."""
    s = (REF / module_name).read_text()
    head = s[:s.index(r"\begin{document}")]
    head = preamble(head)
    import re as _re
    head = _re.sub(r"\\title\{[^}]*\}", r"\\title{%s}" % title, head)
    head = _re.sub(r"\\subtitle\{[^}]*\}",
                   r"\\subtitle{Unit %d: %s}" % (unit_no, subtitle_text), head)
    if r"\newenvironment{llmcheck}" not in head:
        head = head.replace(r"\title{", (
            r"\newenvironment{llmcheck}[1]{%" "\n"
            r"  \setbeamercolor{block title}{fg=white,bg=violet!75!black}%" "\n"
            r"  \setbeamercolor{block body}{bg=violet!10}%" "\n"
            r"  \begin{block}{\textbf{LLM check:} #1}}{\end{block}}" "\n\n"
            r"\title{"), 1)
    return head + "\\begin{document}\n\n"


def section(name):
    bar = "% " + "=" * 70 + "\n"
    return bar + "\\section{%s}\n" % name + bar
