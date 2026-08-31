#!/usr/bin/env python3
"""Drop the full-page Day 1/2/3 separators. Teaching days are fluid, so the decks
should flow continuously and the instructor decides where a day ends.
"""
import re
from pathlib import Path

SLIDES = Path(__file__).resolve().parents[1] / "Slides"

# Wording that only made sense with hard day boundaries.
REWORD = [
    ("\\begin{frame}{Day 1: what this course is actually about}",
     "\\begin{frame}{What this course is actually about}"),
    ("\\begin{frame}{Day 1: the thing we assumed last unit}",
     "\\begin{frame}{The thing we assumed last unit}"),
    ("\\begin{frame}{Day 1: where this fits}", "\\begin{frame}{Where this fits}"),
    ("\\begin{frame}{Day 1: where we left off}", "\\begin{frame}{Where we left off}"),
    ("\\begin{frame}{Yesterday in one slide}", "\\begin{frame}{The idea so far, in one slide}"),
    ("\\begin{principle}{today's question}", "\\begin{principle}{the question now}"),
    ("Now we turn that ratio into a probability, and then spend most of the day on what that\nprobability does not mean.",
     "Now we turn that ratio into a probability, and then spend most of this unit on what that\nprobability does not mean."),
    ("and of the cross-validation we set up yesterday.",
     "and of the cross-validation we set up earlier."),
    ("\\item Everything after that reuses today's template.",
     "\\item Everything after that reuses this template."),
]

DIVIDER = re.compile(
    r"\\begin\{frame\}\[plain\]\s*\n\\vfill\s*\n\\centering\s*\n"
    r"\{\\Large\\textbf\{Day \d+\}\}.*?\\end\{frame\}\s*\n+",
    re.DOTALL,
)

total = 0
for path in sorted(SLIDES.glob("Unit_*.tex")):
    s = original = path.read_text()
    s, n = DIVIDER.subn("", s)
    for old, new in REWORD:
        s = s.replace(old, new)
    if s != original:
        path.write_text(s)
    total += n
    print(f"{path.stem:<46} removed {n}")
print(f"\ntotal separators removed: {total}")
