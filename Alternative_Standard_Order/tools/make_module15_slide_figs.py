#!/usr/bin/env python3
"""Figures for Module 15: Putting It Together."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parents[1] / "Slides"
OUT.mkdir(parents=True, exist_ok=True)
BLUE, RED, GREEN, PURPLE, ORANGE = "#4878a8", "#c0392b", "#2e8b57", "#7a5c99", "#d98c2b"


def box(ax, x, y, w, h, text, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12",
                                fc=color, ec="none", alpha=0.18))
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12",
                                fc="none", ec=color, lw=1.6))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8.6, color="black")


def arrow(ax, xy1, xy2, color="#555555"):
    ax.annotate("", xy=xy2, xytext=xy1,
                arrowprops=dict(arrowstyle="-|>", lw=1.5, color=color))


fig, ax = plt.subplots(figsize=(9.4, 4.6))
ax.set_xlim(0, 100); ax.set_ylim(0, 52); ax.axis("off")

box(ax, 2, 38, 20, 9, "Randomness\nand probability\n(what chance alone does)", BLUE)
box(ax, 2, 25, 20, 9, "Random variables\nand expectation\n(mean, spread, decisions)", BLUE)
box(ax, 2, 12, 20, 9, "The normal and the CLT\n(why estimates behave)", BLUE)

box(ax, 28, 31, 20, 9, "Estimation, likelihood,\nthe bootstrap\n(a number and its error)", GREEN)
box(ax, 28, 18, 20, 9, "Inference\n(is it signal or noise?)", GREEN)

box(ax, 54, 38, 20, 9, "Regression\n(reasoning with a slope)", PURPLE)
box(ax, 54, 26, 20, 9, "Model building,\nflexibility, selection", PURPLE)
box(ax, 54, 14, 20, 9, "Prediction, uncertainty,\nclassification", PURPLE)

box(ax, 79, 31, 19, 9, "Causal thinking\n(what if we change it?)", RED)
box(ax, 79, 18, 19, 9, "Bayesian reasoning\nand decisions", RED)

box(ax, 28, 3, 46, 7, "Where the data comes from: sampling, selection, missingness", ORANGE)

arrow(ax, (22, 42), (28, 37))
arrow(ax, (22, 29), (28, 35))
arrow(ax, (22, 16), (28, 33))
arrow(ax, (38, 31), (38, 27))
arrow(ax, (48, 24), (54, 30))
arrow(ax, (48, 22), (54, 18))
arrow(ax, (64, 38), (64, 35))
arrow(ax, (64, 26), (64, 23))
arrow(ax, (74, 33), (79, 34))
arrow(ax, (74, 20), (79, 23))
arrow(ax, (51, 10), (51, 17), color=ORANGE)

ax.text(50, 49, "Every arrow is a question that the next box answers",
        ha="center", fontsize=10.5)
ax.text(51, 0.6, "this one sits underneath everything", ha="center", fontsize=8.5,
        color=ORANGE, style="italic")
fig.tight_layout()
fig.savefig(OUT / "fig_m15_map.pdf")
plt.close(fig)
print("wrote module 15 figure to", OUT)
