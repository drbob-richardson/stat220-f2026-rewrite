#!/usr/bin/env python3
"""Figures for Module 13: Bayesian Reasoning and Decisions."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

OUT = Path(__file__).resolve().parents[1] / "Slides"
DATA = Path(__file__).resolve().parents[2] / "data"
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(220)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
BLUE, RED, GREEN, GREY = "#4878a8", "#c0392b", "#2e8b57", "#7f8c8d"
p = np.linspace(0, 1, 600)

# --- 1. sequential updating -----------------------------------------------
fig, ax = plt.subplots(figsize=(6.4, 3.3))
prior_a, prior_b = 2, 8              # prior belief: conversion around 20%
stages = [(0, 0, "prior belief"), (2, 8, "after 10 visitors"),
          (12, 38, "after 50 visitors"), (48, 152, "after 200 visitors")]
shades = ["#cbd8e4", "#8fb0cc", "#5182ac", "#22456b"]
for (s, f, lab), c in zip(stages, shades):
    ax.plot(p, stats.beta.pdf(p, prior_a + s, prior_b + f), color=c, lw=2.4, label=lab)
ax.set_xlim(0, 0.6)
ax.set_xlabel("conversion rate")
ax.set_ylabel("belief density")
ax.legend(frameon=False, fontsize=9)
ax.set_title("Evidence sharpens belief, one batch at a time")
fig.tight_layout()
fig.savefig(OUT / "fig_m13_update.pdf")
plt.close(fig)

# --- 2. how much does the prior matter? -----------------------------------
fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.1))
priors = [(1, 1, "flat prior"), (2, 8, "skeptical: about 20%"), (20, 5, "bullish: about 80%")]
for ax, (s, f, title) in zip(axes, [(3, 7, "small data: 3 of 10"),
                                    (150, 350, "large data: 150 of 500")]):
    for (a, b, lab), c in zip(priors, [GREY, BLUE, RED]):
        ax.plot(p, stats.beta.pdf(p, a + s, b + f), color=c, lw=2.4, label=lab)
    ax.set_title(title, fontsize=10.5)
    ax.set_xlabel("conversion rate")
    ax.set_yticks([])
    ax.set_xlim(0, 0.9)
axes[0].legend(frameon=False, fontsize=8.5)
fig.suptitle("With enough data the prior stops mattering; with little data it is doing the work",
             fontsize=10.5)
fig.tight_layout()
fig.savefig(OUT / "fig_m13_priors.pdf")
plt.close(fig)

# --- 3. Bayesian A/B test --------------------------------------------------
a_s, a_f = 84, 916          # 8.4% of 1000
b_s, b_f = 104, 896         # 10.4% of 1000
post_a = stats.beta(1 + a_s, 1 + a_f)
post_b = stats.beta(1 + b_s, 1 + b_f)
draws_a, draws_b = post_a.rvs(200000, random_state=1), post_b.rvs(200000, random_state=2)
p_better = (draws_b > draws_a).mean()
lift = draws_b - draws_a
exp_loss_choose_b = np.maximum(draws_a - draws_b, 0).mean()

fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.1))
axes[0].plot(p, post_a.pdf(p), color=BLUE, lw=2.4, label="variant A (84/1000)")
axes[0].plot(p, post_b.pdf(p), color=RED, lw=2.4, label="variant B (104/1000)")
axes[0].set_xlim(0.05, 0.15)
axes[0].set_xlabel("conversion rate"); axes[0].set_yticks([])
axes[0].legend(frameon=False, fontsize=8.5)
axes[0].set_title("Two posteriors", fontsize=10.5)

axes[1].hist(lift, bins=80, color=GREEN, edgecolor="white", density=True)
axes[1].axvline(0, color="black", lw=1.4)
axes[1].set_xlabel("B minus A (percentage points)")
axes[1].set_yticks([])
axes[1].set_title(f"P(B better) = {p_better:.1%}", fontsize=10.5)
fig.tight_layout()
fig.savefig(OUT / "fig_m13_ab.pdf")
plt.close(fig)

# --- 4. shrinkage on real group rates --------------------------------------
credit = pd.read_csv(DATA / "credit_risk.csv")
sub = credit.sample(400, random_state=5)
g = sub.groupby("loan_intent")["loan_status"].agg(["sum", "count"])
overall = sub["loan_status"].mean()
k = 40.0
g["raw"] = g["sum"] / g["count"]
g["shrunk"] = (g["sum"] + k * overall) / (g["count"] + k)
g = g.sort_values("raw")

fig, ax = plt.subplots(figsize=(6.6, 3.3))
ypos = np.arange(len(g))
ax.hlines(ypos, g["raw"], g["shrunk"], color=GREY, lw=1.6)
ax.plot(g["raw"], ypos, "o", color=RED, ms=8, label="raw rate")
ax.plot(g["shrunk"], ypos, "o", color=BLUE, ms=8, label="after shrinkage")
ax.axvline(overall, color="black", ls="--", lw=1.4)
ax.text(overall + 0.005, len(g) - 0.6, "overall rate", fontsize=8.5)
ax.set_yticks(ypos)
ax.set_yticklabels([f"{i}  (n={n})" for i, n in zip(g.index, g["count"])], fontsize=8)
ax.set_xlabel("default rate")
ax.legend(frameon=False, fontsize=9)
ax.set_title("Small groups get pulled toward the overall rate")
fig.tight_layout()
fig.savefig(OUT / "fig_m13_shrinkage.pdf")
plt.close(fig)

print("P(B better) =", round(p_better, 4), " expected loss if you pick B =",
      round(exp_loss_choose_b * 100, 4), "points")
print("wrote module 13 figures to", OUT)
