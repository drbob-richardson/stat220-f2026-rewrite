#!/usr/bin/env python3
"""Figures for Module 14: Where the Data Comes From."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle

OUT = Path(__file__).resolve().parents[1] / "Slides"
DATA = Path(__file__).resolve().parents[2] / "data"
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(220)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
BLUE, RED, GREEN, GREY = "#4878a8", "#c0392b", "#2e8b57", "#7f8c8d"


def plane(ax):
    ax.add_patch(Ellipse((0, 0), 1.1, 6.2, fc="#e8edf2", ec="black", lw=1.4))      # fuselage
    ax.add_patch(Ellipse((0, 0.3), 7.4, 1.5, fc="#e8edf2", ec="black", lw=1.4))    # wings
    ax.add_patch(Ellipse((0, -2.5), 3.0, 0.9, fc="#e8edf2", ec="black", lw=1.4))   # tail
    ax.add_patch(Rectangle((-0.28, -0.9), 0.56, 1.9, fc="#d5dde5", ec="black", lw=1.1))
    ax.set_xlim(-4.2, 4.2); ax.set_ylim(-3.6, 3.6)
    ax.set_aspect("equal"); ax.axis("off")


# --- 1. survivorship bias --------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.4))
plane(axes[0]); plane(axes[1])
wing = np.column_stack([rng.uniform(-3.4, 3.4, 90), rng.normal(0.3, 0.45, 90)])
tail = np.column_stack([rng.uniform(-1.3, 1.3, 25), rng.normal(-2.5, 0.3, 25)])
body = np.column_stack([rng.normal(0, 0.28, 20), rng.uniform(-1.6, 2.4, 20)])
hits = np.vstack([wing, tail, body])
axes[0].plot(hits[:, 0], hits[:, 1], "o", color=RED, ms=3.2, alpha=0.8)
axes[0].set_title("Damage on planes that came back", fontsize=10)
engine = np.column_stack([rng.normal(0, 0.22, 30), rng.uniform(-0.8, 0.9, 30)])
cockpit = np.column_stack([rng.normal(0, 0.2, 22), rng.normal(2.3, 0.25, 22)])
axes[1].plot(np.vstack([engine, cockpit])[:, 0], np.vstack([engine, cockpit])[:, 1],
             "o", color=GREEN, ms=3.6, alpha=0.9)
axes[1].set_title("Where armor was actually added", fontsize=10)
fig.suptitle("The holes you never see are the ones that matter", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "fig_m14_survivorship.pdf")
plt.close(fig)

# --- 2. a big biased sample loses to a small random one -------------------
truth = 0.50
bias = 0.04                                   # 4-point systematic tilt
ns = np.logspace(1, 6, 60)
rmse_biased = np.sqrt(bias ** 2 + truth * (1 - truth) / ns)
rmse_random = np.sqrt(truth * (1 - truth) / ns)
fig, ax = plt.subplots(figsize=(6.2, 3.3))
ax.loglog(ns, rmse_biased * 100, color=RED, lw=2.6, label="biased sample (4-point tilt)")
ax.loglog(ns, rmse_random * 100, color=BLUE, lw=2.6, label="true random sample")
ax.axhline(bias * 100, color=RED, ls=":", lw=1.4)
n_eq = truth * (1 - truth) / bias ** 2
ax.plot([n_eq], [np.sqrt(2) * bias * 100], "o", color="black", ms=7)
ax.annotate(f"a random sample of {n_eq:.0f}\nbeats a biased sample of any size",
            xy=(n_eq, np.sqrt(2) * bias * 100), xytext=(2e3, 12),
            fontsize=9, arrowprops=dict(arrowstyle="->", color="black"))
ax.set_xlabel("sample size")
ax.set_ylabel("typical error (percentage points)")
ax.legend(frameon=False, fontsize=9)
ax.set_title("More data does not fix bias")
fig.tight_layout()
fig.savefig(OUT / "fig_m14_bias_vs_n.pdf")
plt.close(fig)

# --- 3. missing data disguised as zeros, in real data ---------------------
dia = pd.read_csv(DATA / "diabetes.csv")
cols = ["Insulin", "SkinThickness", "BloodPressure", "BMI", "Glucose"]
frac0 = [(dia[c] == 0).mean() for c in cols]
fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.2))
axes[0].barh(cols, [f * 100 for f in frac0], color=BLUE)
axes[0].set_xlabel("percent of rows recorded as zero")
axes[0].set_title("Impossible values, silently stored", fontsize=10.5)
for i, f in enumerate(frac0):
    axes[0].text(f * 100 + 0.7, i, f"{f*100:.0f}%", va="center", fontsize=8.5)

ins_all = dia["Insulin"]
ins_real = ins_all[ins_all > 0]
means = {
    "keep zeros\n(wrong)": ins_all.mean(),
    "drop zeros": ins_real.mean(),
    "impute the\nmean of the rest": pd.concat([ins_real,
                                               pd.Series([ins_real.mean()] * (ins_all == 0).sum())]).mean(),
}
imputed = pd.concat([ins_real, pd.Series([ins_real.mean()] * (ins_all == 0).sum())])
sds = [ins_all.std(), ins_real.std(), imputed.std()]
axes[1].bar(list(means), list(means.values()), color=[RED, BLUE, GREEN])
for i, (m, sd) in enumerate(zip(means.values(), sds)):
    axes[1].text(i, m + 4, f"mean {m:.0f}\nSD {sd:.0f}", ha="center", fontsize=8.5)
axes[1].set_ylim(0, 210)
axes[1].set_ylabel("estimated mean insulin")
axes[1].set_title("Three answers from one column", fontsize=10.5)
plt.setp(axes[1].get_xticklabels(), fontsize=8.5)
fig.tight_layout()
fig.savefig(OUT / "fig_m14_missing.pdf")
plt.close(fig)

# --- 4. nonresponse bends an estimate --------------------------------------
groups = ["very satisfied", "satisfied", "neutral", "dissatisfied", "very dissatisfied"]
true_share = np.array([0.15, 0.30, 0.30, 0.17, 0.08])
resp_rate = np.array([0.45, 0.20, 0.08, 0.15, 0.40])       # the extremes answer surveys
observed = true_share * resp_rate
observed = observed / observed.sum()
x = np.arange(len(groups))
fig, ax = plt.subplots(figsize=(6.6, 3.2))
ax.bar(x - 0.2, true_share, 0.4, color=BLUE, label="true population")
ax.bar(x + 0.2, observed, 0.4, color=RED, label="who answered the survey")
ax.set_xticks(x); ax.set_xticklabels(groups, fontsize=8.5)
ax.set_ylabel("share")
ax.legend(frameon=False, fontsize=9)
ax.set_title("Nonresponse is not random: the people with opinions reply")
fig.tight_layout()
fig.savefig(OUT / "fig_m14_nonresponse.pdf")
plt.close(fig)

print("equivalent-n:", round(n_eq), "means:", {k.split(chr(10))[0]: round(v,1) for k,v in means.items()}, "sds:", [round(v,1) for v in sds])
print("wrote module 14 figures to", OUT)
