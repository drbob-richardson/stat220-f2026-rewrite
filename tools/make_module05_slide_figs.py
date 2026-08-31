#!/usr/bin/env python3
"""Figures for Module 05: Randomness and How to Reason About It."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "Slides"
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(220)
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})


def longest_run(seq):
    best = run = 1
    for i in range(1, len(seq)):
        run = run + 1 if seq[i] == seq[i - 1] else 1
        best = max(best, run)
    return best


# --- 1. longest streak: real coins vs human-invented sequences -------------
runs = np.array([longest_run(rng.integers(0, 2, 100)) for _ in range(20000)])
fig, ax = plt.subplots(figsize=(6.2, 3.4))
vals, counts = np.unique(runs, return_counts=True)
ax.bar(vals, counts / counts.sum(), color="#4878a8", edgecolor="white")
ax.axvline(4.2, color="#c0392b", lw=2.5)
ax.text(4.35, ax.get_ylim()[1] * 0.86, "where most\nfaked sequences\ntop out", color="#c0392b", fontsize=9.5)
ax.set_xlabel("longest streak of the same side in 100 real flips")
ax.set_ylabel("probability")
ax.set_title("Real randomness streaks more than people expect")
fig.tight_layout()
fig.savefig(OUT / "fig_m05_streaks.pdf")
plt.close(fig)

# --- 2. natural frequencies for a screening test --------------------------
# 1% prevalence, 99% sensitivity, 95% specificity, 10,000 people
N, prev, sens, spec = 10000, 0.01, 0.99, 0.95
sick = int(N * prev)
well = N - sick
tp, fn = int(sick * sens), sick - int(sick * sens)
fp = int(well * (1 - spec))
tn = well - fp

fig, ax = plt.subplots(figsize=(6.6, 3.6))
grid = np.zeros((100, 100))
# 0 = well/negative, 1 = false positive, 2 = true positive, 3 = false negative
flat = np.zeros(N)
flat[:tp] = 2
flat[tp:tp + fn] = 3
flat[tp + fn:tp + fn + fp] = 1
grid = flat.reshape(100, 100)
cmap = matplotlib.colors.ListedColormap(["#dfe6ec", "#e8b04b", "#c0392b", "#7f8c8d"])
ax.imshow(grid, cmap=cmap, interpolation="nearest")
ax.set_xticks([]); ax.set_yticks([])
ax.set_title("10,000 people: who tests positive?")
handles = [
    matplotlib.patches.Patch(color="#c0392b", label=f"sick and positive  ({tp})"),
    matplotlib.patches.Patch(color="#e8b04b", label=f"healthy but positive  ({fp})"),
    matplotlib.patches.Patch(color="#7f8c8d", label=f"sick but negative  ({fn})"),
    matplotlib.patches.Patch(color="#dfe6ec", label=f"healthy and negative  ({tn})"),
]
ax.legend(handles=handles, loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "fig_m05_screening.pdf")
plt.close(fig)

# --- 3. birthday problem ---------------------------------------------------
n = np.arange(1, 71)
p = 1 - np.array([np.prod(1 - np.arange(k) / 365) for k in n])
fig, ax = plt.subplots(figsize=(5.8, 3.3))
ax.plot(n, p, color="#4878a8", lw=2.5)
ax.axhline(0.5, color="#c0392b", ls="--", lw=1.2)
ax.axvline(23, color="#c0392b", ls="--", lw=1.2)
ax.plot([23], [0.507], "o", color="#c0392b")
ax.annotate("23 people:\nbetter than a coin flip", xy=(23, 0.507), xytext=(30, 0.30),
            fontsize=9.5, color="#c0392b",
            arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax.set_xlabel("people in the room")
ax.set_ylabel("P(some shared birthday)")
ax.set_ylim(0, 1.02)
ax.set_title("Coincidences are much likelier than they feel")
fig.tight_layout()
fig.savefig(OUT / "fig_m05_birthday.pdf")
plt.close(fig)

# --- 4. law of large numbers is not a correction ---------------------------
flips = rng.integers(0, 2, 3000)
flips[:20] = 1  # a hot streak up front
prop = np.cumsum(flips) / np.arange(1, len(flips) + 1)
excess = np.cumsum(flips * 2 - 1)
fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.2))
axes[0].plot(prop, color="#4878a8", lw=1.4)
axes[0].axhline(0.5, color="#c0392b", ls="--", lw=1.2)
axes[0].set_xlabel("flips"); axes[0].set_ylabel("proportion heads")
axes[0].set_title("The proportion settles down")
axes[1].plot(excess, color="#4878a8", lw=1.4)
axes[1].axhline(0, color="#c0392b", ls="--", lw=1.2)
axes[1].set_xlabel("flips"); axes[1].set_ylabel("heads minus tails")
axes[1].set_title("The surplus is never repaid")
fig.tight_layout()
fig.savefig(OUT / "fig_m05_lln.pdf")
plt.close(fig)

print("wrote module 05 figures to", OUT)
