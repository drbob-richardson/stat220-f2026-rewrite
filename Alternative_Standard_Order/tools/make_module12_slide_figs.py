#!/usr/bin/env python3
"""Figures for Module 12: Causal Thinking."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "Slides"
DATA = Path(__file__).resolve().parents[2] / "data"
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(220)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
BLUE, RED, GREEN, GREY = "#4878a8", "#c0392b", "#2e8b57", "#7f8c8d"

# --- 1. the dice collider demo --------------------------------------------
n = 600
d1 = rng.integers(1, 7, n)
d2 = rng.integers(1, 7, n)
keep = (d1 + d2) >= 9
fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.2))
jit = lambda a: a + rng.normal(0, 0.11, len(a))
axes[0].plot(jit(d1), jit(d2), "o", color=GREY, ms=3.5, alpha=0.55)
axes[0].set_title(f"every roll: r = {np.corrcoef(d1, d2)[0,1]:+.2f}", fontsize=10.5)
axes[1].plot(jit(d1[keep]), jit(d2[keep]), "o", color=RED, ms=4, alpha=0.7)
axes[1].set_title(f"only rolls summing to 9 or more: r = {np.corrcoef(d1[keep], d2[keep])[0,1]:+.2f}",
                  fontsize=10.5)
for ax in axes:
    ax.set_xlabel("first die"); ax.set_ylabel("second die")
    ax.set_xlim(0.3, 6.7); ax.set_ylim(0.3, 6.7)
fig.suptitle("Two independent things, made dependent by selection", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "fig_m12_collider.pdf")
plt.close(fig)

# --- 2. three diagrams: confounder, collider, mediator --------------------
def node(ax, xy, text, color="white"):
    ax.annotate(text, xy, ha="center", va="center", fontsize=10.5,
                bbox=dict(boxstyle="round,pad=0.35", fc=color, ec="black", lw=1.2))

def arrow(ax, a, b):
    ax.annotate("", xy=b, xytext=a,
                arrowprops=dict(arrowstyle="-|>", lw=1.8, color="black",
                                shrinkA=20, shrinkB=20))

fig, axes = plt.subplots(1, 3, figsize=(9.6, 2.9))
titles = ["CONFOUNDER: control for it",
          "COLLIDER: never control for it",
          "MEDIATOR: control only if you\nwant the direct effect"]
for ax, t in zip(axes, titles):
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    ax.set_title(t, fontsize=9.5)

node(axes[0], (2, 1.5), "X"); node(axes[0], (8, 1.5), "Y"); node(axes[0], (5, 4.5), "Z", "#f6d6d6")
arrow(axes[0], (5, 4.5), (2, 1.5)); arrow(axes[0], (5, 4.5), (8, 1.5))
arrow(axes[0], (2, 1.5), (8, 1.5))

node(axes[1], (2, 4.5), "X"); node(axes[1], (8, 4.5), "Y"); node(axes[1], (5, 1.3), "Z", "#f6d6d6")
arrow(axes[1], (2, 4.5), (5, 1.3)); arrow(axes[1], (8, 4.5), (5, 1.3))

node(axes[2], (1.6, 3), "X"); node(axes[2], (5, 3), "Z", "#f6d6d6"); node(axes[2], (8.4, 3), "Y")
arrow(axes[2], (1.6, 3), (5, 3)); arrow(axes[2], (5, 3), (8.4, 3))
fig.tight_layout()
fig.savefig(OUT / "fig_m12_dags.pdf")
plt.close(fig)

# --- 3. confounding in real data: cars, weight and model year -------------
cars = pd.read_csv(DATA / "cars.csv").dropna()
fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.2))
axes[0].plot(cars["acceleration"], cars["mpg"], "o", color=GREY, ms=3.5, alpha=0.6)
b = np.polyfit(cars["acceleration"], cars["mpg"], 1)
xs = np.linspace(cars["acceleration"].min(), cars["acceleration"].max(), 50)
axes[0].plot(xs, np.polyval(b, xs), color=RED, lw=2.4)
axes[0].set_xlabel("0-60 acceleration time (s)"); axes[0].set_ylabel("mpg")
axes[0].set_title(f"raw: slower cars get better mpg\nslope {b[0]:+.2f} mpg per second", fontsize=10)

# within weight bands the relationship largely disappears
bands = pd.qcut(cars["weight"], 4)
for (name, g), c in zip(cars.groupby(bands, observed=True), ["#dbe6f0", "#9fc0dd", BLUE, "#1f3b57"]):
    axes[1].plot(g["acceleration"], g["mpg"], "o", color=c, ms=3.5, alpha=0.8)
    if len(g) > 10:
        bb = np.polyfit(g["acceleration"], g["mpg"], 1)
        xx = np.linspace(g["acceleration"].min(), g["acceleration"].max(), 20)
        axes[1].plot(xx, np.polyval(bb, xx), color=c, lw=2.2)
axes[1].set_xlabel("0-60 acceleration time (s)"); axes[1].set_ylabel("mpg")
axes[1].set_title("within weight groups, the effect shrinks", fontsize=10)
fig.suptitle("Weight drives both acceleration and fuel economy", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "fig_m12_confounder.pdf")
plt.close(fig)

# --- 4. difference in differences ------------------------------------------
periods = np.array([0, 1])
treat = np.array([42, 55])
control = np.array([30, 36])
counterfactual = np.array([42, 42 + (control[1] - control[0])])
fig, ax = plt.subplots(figsize=(6.2, 3.3))
ax.plot(periods, treat, "o-", color=RED, lw=2.6, ms=8, label="treated region")
ax.plot(periods, control, "o-", color=BLUE, lw=2.6, ms=8, label="control region")
ax.plot(periods, counterfactual, "o--", color=GREY, lw=2.2, ms=7,
        label="treated, had nothing happened")
ax.annotate("", xy=(1.02, treat[1]), xytext=(1.02, counterfactual[1]),
            arrowprops=dict(arrowstyle="<->", color=GREEN, lw=2))
ax.text(1.05, (treat[1] + counterfactual[1]) / 2, "the estimated\neffect: +7",
        color=GREEN, fontsize=9.5, va="center")
ax.set_xticks([0, 1]); ax.set_xticklabels(["before", "after"])
ax.set_ylabel("sales per store")
ax.set_xlim(-0.15, 1.45)
ax.legend(frameon=False, fontsize=8.5, loc="upper left")
ax.set_title("Difference in differences: borrow a trend from the control")
fig.tight_layout()
fig.savefig(OUT / "fig_m12_did.pdf")
plt.close(fig)

print("collider r before/after:", round(np.corrcoef(d1, d2)[0, 1], 2),
      round(np.corrcoef(d1[keep], d2[keep])[0, 1], 2))
print("raw acceleration slope", round(b[0], 3))
print("wrote module 12 figures to", OUT)
