#!/usr/bin/env python3
"""Figures for Unit 13: Choosing a Model.

Three figures, all computed rather than drawn:

  fig_u13_bias_variance.pdf   the U-shape, decomposed into real bias and real variance
  fig_u13_afford_truth.pdf    simulated: the best degree moves right as n grows
  fig_u13_overshoot.pdf       cars data: the PENALTY for overshooting collapses as n grows

Run from the Alternative_Model_First folder:
    python tools/make_unit13_slide_figs.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score

OUT = Path(__file__).resolve().parents[1] / "Slides"
DATA = Path(__file__).resolve().parents[2] / "data"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
BLUE, RED, GREEN, GREY = "#4878a8", "#c0392b", "#2e8b57", "#7f8c8d"

DEGS = np.arange(1, 11)
SD = 0.6
# A smooth S-curve plus drift. Genuinely curved, but not periodic, so
# polynomial approximation improves steadily instead of alternating by parity.
truth = lambda x: 3.0 / (1 + np.exp(-3.2 * (x - 0.4))) + 0.45 * x
XT = np.linspace(-3, 3, 1500)
YT = truth(XT)


def fit_predict(x, y, d):
    m = make_pipeline(PolynomialFeatures(d), StandardScaler(), LinearRegression())
    m.fit(x.reshape(-1, 1), y)
    return m.predict(XT.reshape(-1, 1))


def replicate(n, reps, seed, degs=DEGS):
    """reps fitted curves per degree, evaluated on the noise-free grid."""
    rng = np.random.default_rng(seed)
    preds = np.zeros((len(degs), reps, len(XT)))
    for r in range(reps):
        x = rng.uniform(-3, 3, n)
        y = truth(x) + rng.normal(0, SD, n)
        for j, d in enumerate(degs):
            preds[j, r] = fit_predict(x, y, d)
    return preds


# --- 1. the U-shape, decomposed -------------------------------------------
# Degrees 1-8 at n=60: past that the fits explode and the measured "bias"
# becomes dominated by a few wild replicates, which teaches nothing.
DEGS_BV = np.arange(1, 9)
preds = replicate(n=60, reps=600, seed=7, degs=DEGS_BV)
bias2 = ((preds.mean(axis=1) - YT) ** 2).mean(axis=1)
var = preds.var(axis=1).mean(axis=1)
total = bias2 + var

fig, ax = plt.subplots(figsize=(6.4, 3.4))
ax.plot(DEGS_BV, bias2, "o-", color=BLUE, label="bias$^2$: wrong on average")
ax.plot(DEGS_BV, var, "s-", color=RED, label="variance: jumpy from refit to refit")
ax.plot(DEGS_BV, total, "^-", color="black", lw=2.2, label="total error")
best = DEGS_BV[int(np.argmin(total))]
ax.plot([best], [total.min()], marker="*", ms=18, color="black", zorder=5)
ax.annotate("lowest total error", xy=(best, total.min()),
            xytext=(best + 0.7, total.min() * 2.6), fontsize=9,
            arrowprops=dict(arrowstyle="->", lw=1))
ax.set_yscale("log")
ax.set_xlabel("model complexity (polynomial degree)")
ax.set_ylabel("squared error (log scale)")
ax.set_xticks(DEGS_BV)
ax.legend(frameon=False, fontsize=9, loc="lower left")
fig.tight_layout()
fig.savefig(OUT / "fig_u13_bias_variance.pdf")
plt.close(fig)

# --- 2. can you afford the truth? -----------------------------------------
fig, ax = plt.subplots(figsize=(6.4, 3.4))
for n, color, mk in ((20, RED, "o"), (50, GREY, "s"), (300, GREEN, "^")):
    p = replicate(n=n, reps=400, seed=3)
    err = ((p - YT) ** 2).mean(axis=2)
    med = np.median(err, axis=1)
    b = DEGS[int(np.argmin(med))]
    ax.plot(DEGS, med, mk + "-", color=color, label=f"n = {n}   (best: degree {b})")
    ax.plot([b], [med.min()], marker="*", ms=16, color=color, zorder=5)
ax.set_yscale("log")
ax.set_xlabel("model complexity (polynomial degree)")
ax.set_ylabel("error on new data (log scale)")
ax.set_xticks(DEGS)
ax.legend(frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "fig_u13_afford_truth.pdf")
plt.close(fig)

# --- 3. the cost of overshooting, on real cars ----------------------------
cars = pd.read_csv(DATA / "cars.csv").dropna()
X, y = cars[["weight"]].values, cars["mpg"].values
rng = np.random.default_rng(5)

fig, ax = plt.subplots(figsize=(6.4, 3.4))
for n, color, mk in ((25, RED, "o"), (392, GREEN, "^")):
    curves = []
    for r in range(60):
        idx = rng.choice(len(y), n, replace=False) if n < len(y) else np.arange(len(y))
        row = []
        for d in DEGS:
            m = make_pipeline(PolynomialFeatures(d), StandardScaler(), LinearRegression())
            s = cross_val_score(m, X[idx], y[idx], scoring="neg_mean_squared_error",
                                cv=KFold(5, shuffle=True, random_state=r))
            row.append(-s.mean())
        curves.append(row)
        if n == len(y):
            break
    med = np.median(np.array(curves), axis=0)
    ax.plot(DEGS, med, mk + "-", color=color, label=f"n = {n}")
ax.set_yscale("log")
ax.set_xlabel("model complexity (polynomial degree), mpg on weight")
ax.set_ylabel("cross-validated error (log scale)")
ax.set_xticks(DEGS)
ax.legend(frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "fig_u13_overshoot.pdf")
plt.close(fig)

print("wrote:")
for f in ("fig_u13_bias_variance.pdf", "fig_u13_afford_truth.pdf", "fig_u13_overshoot.pdf"):
    print(f"  {OUT / f}")
