#!/usr/bin/env python3
"""
Figures for Module 4 (prediction and its uncertainty).

  fig_irreducible.pdf    even the true line misses each point (natural noise)
  fig_ensemble.pdf       many bootstrap-fit lines: the line itself is uncertain
  fig_bands.pdf          confidence band (narrow) vs prediction band (wide)
  fig_extrapolation.pdf  two models agree in-range, diverge wildly outside it
  fig_regression_mean.pdf the top group drifts back toward the mean next time
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

OUT = Path(__file__).resolve().parents[1] / "Slides"
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(404)

B0, B1, SIGMA = 2.0, 1.3, 3.0

# ---------- 1. irreducible noise ----------
x = rng.uniform(0, 10, 40)
y = B0 + B1 * x + rng.normal(0, SIGMA, 40)
xs = np.array([0, 10])
plt.figure(figsize=(6.4, 4.2))
plt.scatter(x, y, color="#34607d", zorder=3, label="data")
plt.plot(xs, B0 + B1 * xs, color="#2e7d32", lw=2.6, label="the TRUE line")
for xi, yi in zip(x, y):
    plt.plot([xi, xi], [yi, B0 + B1 * xi], color="gray", lw=0.8, zorder=1)
plt.title("Even the true line misses each point (natural noise)")
plt.xlabel("x"); plt.ylabel("y"); plt.legend(fontsize=9)
plt.tight_layout(); plt.savefig(OUT / "fig_irreducible.pdf"); plt.close()

# ---------- 2. estimation uncertainty: bootstrap lines ----------
xd = rng.uniform(0, 10, 25)
yd = B0 + B1 * xd + rng.normal(0, SIGMA, 25)
xg = np.linspace(0, 10, 50)
plt.figure(figsize=(6.4, 4.2))
for _ in range(60):
    idx = rng.integers(0, len(xd), len(xd))
    b1b, b0b = np.polyfit(xd[idx], yd[idx], 1)
    plt.plot(xg, b0b + b1b * xg, color="#c0392b", alpha=0.12, lw=1.2)
plt.scatter(xd, yd, color="#34607d", zorder=3)
b1h, b0h = np.polyfit(xd, yd, 1)
plt.plot(xg, b0h + b1h * xg, color="black", lw=2.2, label="fit on our data")
plt.title("We don't know the true line: each resample gives another")
plt.xlabel("x"); plt.ylabel("y"); plt.legend(fontsize=9)
plt.tight_layout(); plt.savefig(OUT / "fig_ensemble.pdf"); plt.close()

# ---------- 3. CI band vs PI band ----------
n = 40
xb = rng.uniform(0, 10, n)
yb = B0 + B1 * xb + rng.normal(0, SIGMA, n)
b1h, b0h = np.polyfit(xb, yb, 1)
xbar = xb.mean(); Sxx = np.sum((xb - xbar) ** 2)
resid = yb - (b0h + b1h * xb); s = np.sqrt(np.sum(resid ** 2) / (n - 2))
tcrit = stats.t.ppf(0.975, n - 2)
yhat = b0h + b1h * xg
se_mean = s * np.sqrt(1 / n + (xg - xbar) ** 2 / Sxx)
se_pred = s * np.sqrt(1 + 1 / n + (xg - xbar) ** 2 / Sxx)
plt.figure(figsize=(6.6, 4.3))
plt.fill_between(xg, yhat - tcrit * se_pred, yhat + tcrit * se_pred,
                 color="#e67e22", alpha=0.25, label="95% prediction band (a new case)")
plt.fill_between(xg, yhat - tcrit * se_mean, yhat + tcrit * se_mean,
                 color="#34607d", alpha=0.45, label="95% confidence band (the line)")
plt.scatter(xb, yb, color="#34607d", s=22, zorder=3)
plt.plot(xg, yhat, color="black", lw=2.0)
plt.title("Confidence band (narrow) vs prediction band (wide)")
plt.xlabel("x"); plt.ylabel("y"); plt.legend(fontsize=8.5, loc="upper left")
plt.tight_layout(); plt.savefig(OUT / "fig_bands.pdf"); plt.close()

# ---------- 4. extrapolation ----------
xin = rng.uniform(3, 8, 40)
yin = 2 + 1.0 * xin + rng.normal(0, 1.2, 40)
xfull = np.linspace(0, 12, 200)
lin = np.polyfit(xin, yin, 1)
quad = np.polyfit(xin, yin, 2)
plt.figure(figsize=(6.6, 4.3))
plt.axvspan(0, 3, color="gray", alpha=0.12)
plt.axvspan(8, 12, color="gray", alpha=0.12, label="outside the data")
plt.scatter(xin, yin, color="#34607d", zorder=3)
plt.plot(xfull, np.polyval(lin, xfull), color="#2e7d32", lw=2.3, label="linear fit")
plt.plot(xfull, np.polyval(quad, xfull), color="#c0392b", lw=2.3, label="quadratic fit")
plt.title("Two fits agree on the data, disagree wildly outside it")
plt.xlabel("x"); plt.ylabel("y"); plt.legend(fontsize=8.5, loc="upper left")
plt.tight_layout(); plt.savefig(OUT / "fig_extrapolation.pdf"); plt.close()

# ---------- 5. regression to the mean ----------
N = 400
ability = rng.normal(0, 1, N)
occ1 = ability + rng.normal(0, 1, N)
occ2 = ability + rng.normal(0, 1, N)
b1h, b0h = np.polyfit(occ1, occ2, 1)
top = occ1 >= np.quantile(occ1, 0.90)
gx = np.array([occ1.min(), occ1.max()])
plt.figure(figsize=(6.6, 4.3))
plt.scatter(occ1[~top], occ2[~top], color="#7f8c8d", alpha=0.5, s=18)
plt.scatter(occ1[top], occ2[top], color="#c0392b", s=26, label="top 10% on occasion 1")
plt.plot(gx, gx, "k--", lw=1.5, label="y = x (no change)")
plt.plot(gx, b0h + b1h * gx, color="#34607d", lw=2.4, label=f"regression line (slope {b1h:.2f})")
plt.title("The top group drifts back toward the mean")
plt.xlabel("score, occasion 1"); plt.ylabel("score, occasion 2")
plt.legend(fontsize=8.5, loc="upper left")
plt.tight_layout(); plt.savefig(OUT / "fig_regression_mean.pdf"); plt.close()
print(f"REGRESSION TO MEAN: top-10% mean occ1 = {occ1[top].mean():.2f}, "
      f"their mean occ2 = {occ2[top].mean():.2f} (drifts toward 0)")
print(f"PI vs CI width at center: PI={2*tcrit*se_pred[len(xg)//2]:.1f}, CI={2*tcrit*se_mean[len(xg)//2]:.1f}")
print("wrote 5 Module 4 figures to", OUT)
