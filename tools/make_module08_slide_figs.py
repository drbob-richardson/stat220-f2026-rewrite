#!/usr/bin/env python3
"""Figures for Module 08: Estimation, Likelihood, and the Bootstrap."""
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

# --- 1. three estimators for the tank problem ------------------------------
N_TRUE, n, reps = 400, 5, 20000
samples = np.array([rng.choice(np.arange(1, N_TRUE + 1), size=n, replace=False)
                    for _ in range(reps)])
est_max = samples.max(axis=1)
est_twice = 2 * samples.mean(axis=1) - 1
est_mvu = samples.max(axis=1) * (n + 1) / n - 1

fig, axes = plt.subplots(1, 3, figsize=(9.6, 2.9), sharex=True)
for ax, est, name in zip(axes, [est_max, est_twice, est_mvu],
                         ["largest seen", r"$2\bar{x}-1$", r"max$\cdot\frac{n+1}{n}-1$"]):
    ax.hist(est, bins=45, color=BLUE, edgecolor="white")
    ax.axvline(N_TRUE, color=RED, lw=2)
    bias, sd = est.mean() - N_TRUE, est.std()
    ax.set_title(f"{name}\nbias {bias:+.0f}, SD {sd:.0f}", fontsize=10)
    ax.set_yticks([])
    ax.set_xlim(100, 700)
fig.suptitle("Three estimates of the same unknown (true value in red)", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "fig_m08_tanks.pdf")
plt.close(fig)

# --- 2. bias-variance: MSE decomposition ----------------------------------
lam = np.linspace(0, 1, 200)          # shrinkage toward a prior guess
true, prior = 1.0, 0.3
var0 = 0.30
bias2 = (lam * (prior - true)) ** 2
var = (1 - lam) ** 2 * var0
fig, ax = plt.subplots(figsize=(6.0, 3.2))
ax.plot(lam, bias2, color=RED, lw=2.2, label="bias$^2$ (grows as you shrink)")
ax.plot(lam, var, color=BLUE, lw=2.2, label="variance (falls as you shrink)")
ax.plot(lam, bias2 + var, color="black", lw=2.6, label="MSE = bias$^2$ + variance")
i = int(np.argmin(bias2 + var))
ax.plot(lam[i], (bias2 + var)[i], "o", color=GREEN, ms=9)
ax.annotate("the best estimator here\nis a biased one", xy=(lam[i], (bias2 + var)[i]),
            xytext=(lam[i] + 0.12, 0.22), fontsize=9, color=GREEN,
            arrowprops=dict(arrowstyle="->", color=GREEN))
ax.set_xlabel("how much you shrink toward a prior guess")
ax.set_ylabel("error")
ax.legend(frameon=False, fontsize=9)
ax.set_title("Unbiased is not the same as accurate")
fig.tight_layout()
fig.savefig(OUT / "fig_m08_biasvar.pdf")
plt.close(fig)

# --- 3. likelihood curves: curvature is precision --------------------------
p_grid = np.linspace(0.01, 0.99, 400)
fig, ax = plt.subplots(figsize=(6.2, 3.2))
for k, nn, c, ls in [(3, 10, GREY, "--"), (30, 100, BLUE, "-"), (300, 1000, RED, "-")]:
    ll = k * np.log(p_grid) + (nn - k) * np.log(1 - p_grid)
    ll = ll - ll.max()
    ax.plot(p_grid, np.exp(ll), color=c, ls=ls, lw=2.2, label=f"{k} of {nn} converted")
ax.axvline(0.3, color="black", lw=1, ls=":")
ax.set_xlabel("conversion rate $p$")
ax.set_ylabel("likelihood (scaled)")
ax.set_xlim(0, 0.8)
ax.legend(frameon=False, fontsize=9)
ax.set_title("Same estimate, very different confidence")
fig.tight_layout()
fig.savefig(OUT / "fig_m08_likelihood.pdf")
plt.close(fig)

# --- 4. bootstrap on real data --------------------------------------------
ins = pd.read_csv(DATA / "insurance_all.csv")
ch = ins["charges"].values
B = 20000
idx = rng.integers(0, len(ch), size=(B, len(ch)))
boot_mean = ch[idx].mean(axis=1)
boot_med = np.median(ch[idx], axis=1)

fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.1))
for ax, b, name in zip(axes, [boot_mean, boot_med], ["mean charge", "median charge"]):
    ax.hist(b, bins=60, color=BLUE, edgecolor="white")
    lo, hi = np.percentile(b, [2.5, 97.5])
    ax.axvline(lo, color=RED, lw=2)
    ax.axvline(hi, color=RED, lw=2)
    ax.set_title(f"bootstrap {name}\n95% interval: {lo:,.0f} to {hi:,.0f}", fontsize=10)
    ax.set_yticks([])
fig.suptitle("Resampling the data gives an interval with no formula at all", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "fig_m08_bootstrap.pdf")
plt.close(fig)

# --- 5. where the bootstrap fails: the maximum -----------------------------
x = rng.uniform(0, 100, 60)
boot_max = x[rng.integers(0, len(x), size=(20000, len(x)))].max(axis=1)
fig, ax = plt.subplots(figsize=(6.0, 3.0))
ax.hist(boot_max, bins=40, color=BLUE, edgecolor="white")
ax.axvline(x.max(), color=RED, lw=2)
ax.text(x.max() - 0.3, ax.get_ylim()[1] * 0.55, "the sample maximum,\nand a ceiling the\nbootstrap can never pass",
        ha="right", fontsize=9, color=RED)
ax.set_xlabel("bootstrap estimates of the maximum")
ax.set_yticks([])
ax.set_title("The bootstrap is not magic: it cannot invent unseen values")
fig.tight_layout()
fig.savefig(OUT / "fig_m08_bootfail.pdf")
plt.close(fig)

print("wrote module 08 figures to", OUT)
