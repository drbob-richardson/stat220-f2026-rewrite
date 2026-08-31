#!/usr/bin/env python3
"""Printable handout for the Unit 3 sampling-distribution activity.

200 house prices from a right-skewed population, laid out in a grid students can
point at. One page, cut nothing, hand one to each student.
"""
import subprocess
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parents[1] / "Slides"
rng = np.random.default_rng(220)

# Right-skewed by construction: most homes modest, a few mansions.
prices = np.round(rng.lognormal(mean=12.5, sigma=0.55, size=200) / 1000) * 1000
prices = np.clip(prices, 60_000, None).astype(int)

mean, median = prices.mean(), np.median(prices)
se10 = prices.std(ddof=1) / np.sqrt(10)

rows = []
for r in range(25):
    cells = " & ".join(f"{prices[r + 25*c]:,}" for c in range(8))
    rows.append(cells + r" \\")
table = "\n".join(rows)

tex = r"""\documentclass[10pt]{article}
\usepackage[margin=0.6in,letterpaper]{geometry}
\usepackage{booktabs}
\pagestyle{empty}
\renewcommand{\arraystretch}{1.15}
\begin{document}
\begin{center}
{\large\textbf{Stat 220, Unit 3: 200 house prices}}\\[2pt]
{\footnotesize Round 1: close your eyes and point at \textbf{one} price. Write it down.\\
Round 2: pick \textbf{ten} at random and write down their \emph{average}.\\
Then put a sticky note in the right bin on the board.}
\end{center}
\vspace{4pt}
\centering\footnotesize
\begin{tabular}{rrrrrrrr}
\toprule
""" + table + r"""
\bottomrule
\end{tabular}
\end{document}
"""

src = OUT / "Unit_03_Price_Handout.tex"
src.write_text(tex)
subprocess.run(["pdflatex", "-interaction=nonstopmode", src.name],
               cwd=OUT, capture_output=True)
for ext in (".aux", ".log"):
    (OUT / ("Unit_03_Price_Handout" + ext)).unlink(missing_ok=True)

print(f"population mean   {mean:,.0f}")
print(f"population median {median:,.0f}   (mean sits above it, as it should)")
print(f"SD                {prices.std(ddof=1):,.0f}")
print(f"predicted SD of an average of 10 = {se10:,.0f}, "
      f"about {prices.std(ddof=1)/se10:.1f}x narrower than one draw")
print(f"wrote {OUT/'Unit_03_Price_Handout.pdf'}")
