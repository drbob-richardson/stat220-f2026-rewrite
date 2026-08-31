#!/usr/bin/env python3
"""Figures for Module 10: Counts, Proportions, and Categorical Data."""
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
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
BLUE, RED, GREEN, GREY = "#4878a8", "#c0392b", "#2e8b57", "#7f8c8d"

# --- 1. rock-paper-scissors is not uniform --------------------------------
labels = ["rock", "paper", "scissors"]
observed = np.array([0.359, 0.353, 0.288])      # published first-throw frequencies
fig, ax = plt.subplots(figsize=(5.8, 3.0))
ax.bar(labels, observed, color=[RED, BLUE, GREEN], edgecolor="white")
ax.axhline(1 / 3, color="black", ls="--", lw=1.6)
ax.text(2.35, 1 / 3 + 0.006, "uniform", fontsize=9)
ax.set_ylabel("share of first throws")
ax.set_ylim(0, 0.42)
ax.set_title("Humans are bad random generators")
fig.tight_layout()
fig.savefig(OUT / "fig_m10_rps.pdf")
plt.close(fig)

# --- 2. relative vs absolute risk -----------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.0))
for ax, (rate, title) in zip(axes, [(0.0002, "without the drug: 2 in 10,000"),
                                    (0.0003, "with the drug: 3 in 10,000")]):
    grid = np.zeros(10000)
    grid[:int(rate * 10000)] = 1
    ax.imshow(grid.reshape(100, 100), cmap=matplotlib.colors.ListedColormap(["#e4eaf0", RED]),
              interpolation="nearest")
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    ax.set_title(title, fontsize=10)
fig.suptitle('"A 50% increase in risk" looks like this', fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "fig_m10_relrisk.pdf")
plt.close(fig)

# --- 3. Simpson's paradox: Berkeley 1973 admissions ------------------------
dept = ["A", "B", "C", "D", "E", "F"]
men_app = np.array([825, 560, 325, 417, 191, 373])
men_adm = np.array([512, 353, 120, 138, 53, 22])
wom_app = np.array([108, 25, 593, 375, 393, 341])
wom_adm = np.array([89, 17, 202, 131, 94, 24])
fig, ax = plt.subplots(figsize=(6.6, 3.3))
w = 0.38
x = np.arange(len(dept))
ax.bar(x - w / 2, men_adm / men_app, w, color=BLUE, label="men")
ax.bar(x + w / 2, wom_adm / wom_app, w, color=RED, label="women")
ax.set_xticks(x); ax.set_xticklabels([f"Dept {d}\n({m}m / {f}w)" for d, m, f in
                                      zip(dept, men_app, wom_app)], fontsize=7.5)
ax.set_ylabel("admission rate")
ax.legend(frameon=False, fontsize=9)
overall_m = men_adm.sum() / men_app.sum()
overall_w = wom_adm.sum() / wom_app.sum()
ax.set_title(f"Overall: men {overall_m:.0%} admitted, women {overall_w:.0%}. "
             f"Within departments, mostly the reverse.", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "fig_m10_simpson.pdf")
plt.close(fig)

# --- 4. observed vs expected on real loan data ----------------------------
credit = pd.read_csv(DATA / "credit_risk.csv")
tab = pd.crosstab(credit["loan_intent"], credit["loan_status"])
chi2, p, dof, expected = stats.chi2_contingency(tab)
diff = (tab.values - expected) / np.sqrt(expected)     # standardized residuals
fig, ax = plt.subplots(figsize=(6.4, 3.4))
im = ax.imshow(diff, cmap="RdBu_r", vmin=-4, vmax=4)
ax.set_xticks([0, 1]); ax.set_xticklabels(["repaid", "defaulted"])
ax.set_yticks(range(len(tab.index))); ax.set_yticklabels(tab.index, fontsize=8.5)
for i in range(diff.shape[0]):
    for j in range(diff.shape[1]):
        ax.text(j, i, f"{tab.values[i, j]}\n({expected[i, j]:.0f})", ha="center", va="center",
                fontsize=8)
ax.grid(False)
ax.set_title(f"Observed (expected) counts, shaded by residual\n"
             f"chi-square = {chi2:.0f}, df = {dof}, p = {p:.1e}", fontsize=10)
fig.colorbar(im, ax=ax, shrink=0.8, label="standardized residual")
fig.tight_layout()
fig.savefig(OUT / "fig_m10_chisq.pdf")
plt.close(fig)

print("Berkeley overall:", round(overall_m, 3), round(overall_w, 3))
print("loan chi2", round(chi2, 1), "df", dof, "p", p)
print("wrote module 10 figures to", OUT)
