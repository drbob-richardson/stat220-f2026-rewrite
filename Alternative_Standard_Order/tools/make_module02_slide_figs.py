#!/usr/bin/env python3
"""
Figures for the Module 2 (regression) slides, plus the real numbers to quote on the slides.

  fig_reg_scatter.pdf    a cloud of points with the least-squares line
  fig_reg_residuals.pdf  the same, with residual segments drawn in
  fig_activity_shoe.pdf  illustrative shoe-size vs height scatter + line + a "?" to predict
  fig_dummy.pdf          a binary predictor: two groups, two parallel lines
  fig_interaction.pdf    an interaction: two groups, two different slopes
  fig_confounding.pdf    Simpson's paradox: positive overall, negative within each group
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

OUT = Path(__file__).resolve().parents[1] / "Slides"
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(220)

def ols(x, y):
    x = np.asarray(x); y = np.asarray(y)
    n = len(x)
    b1, b0 = np.polyfit(x, y, 1)
    yhat = b0 + b1 * x
    resid = y - yhat
    s2 = np.sum(resid**2) / (n - 2)
    se_b1 = np.sqrt(s2 / np.sum((x - x.mean())**2))
    t = b1 / se_b1
    p = 2 * stats.t.sf(abs(t), n - 2)
    r2 = 1 - np.sum(resid**2) / np.sum((y - y.mean())**2)
    return dict(b0=b0, b1=b1, se_b1=se_b1, t=t, p=p, r2=r2)

# ---------- 1. basic scatter + line ----------
x = rng.uniform(0, 10, 60)
y = 2 + 1.4 * x + rng.normal(0, 3, 60)
fit = ols(x, y)
xs = np.array([x.min(), x.max()])
plt.figure(figsize=(6.4, 4.2))
plt.scatter(x, y, color="#34607d", alpha=0.8)
plt.plot(xs, fit["b0"] + fit["b1"] * xs, color="#c0392b", lw=2.5)
plt.xlabel("x"); plt.ylabel("y")
plt.title(f"$\\hat{{y}} = {fit['b0']:.1f} + {fit['b1']:.1f}\\,x$")
plt.tight_layout(); plt.savefig(OUT / "fig_reg_scatter.pdf"); plt.close()
print("BASIC FIT:", {k: round(v, 3) for k, v in fit.items()})

# ---------- 2. residuals ----------
xr = rng.uniform(0, 10, 14)
yr = 2 + 1.4 * xr + rng.normal(0, 3, 14)
fr = ols(xr, yr)
plt.figure(figsize=(6.4, 4.2))
plt.scatter(xr, yr, color="#34607d", zorder=3)
plt.plot(xs, fr["b0"] + fr["b1"] * xs, color="#c0392b", lw=2.5, zorder=2)
for xi, yi in zip(xr, yr):
    plt.plot([xi, xi], [yi, fr["b0"] + fr["b1"] * xi], color="gray", lw=1.2, zorder=1)
plt.xlabel("x"); plt.ylabel("y")
plt.title("Least squares minimizes the squared residuals")
plt.tight_layout(); plt.savefig(OUT / "fig_reg_residuals.pdf"); plt.close()

# ---------- 3. activity: shoe size vs height ----------
shoe = np.array([6, 7, 7.5, 8, 8.5, 9, 9.5, 10, 11, 12.0])
height = 50 + 1.85 * shoe + rng.normal(0, 1.6, len(shoe))
fa = ols(shoe, height)
plt.figure(figsize=(6.6, 4.3))
plt.scatter(shoe, height, color="#34607d", s=55, zorder=3, label="our 10 volunteers")
sx = np.array([shoe.min() - 0.5, shoe.max() + 1.0])
plt.plot(sx, fa["b0"] + fa["b1"] * sx, color="#c0392b", lw=2.5, label="best-fit line")
plt.axvline(11.5, color="#2e7d32", ls="--", lw=1.8)
plt.text(11.55, height.min(), "new person:\nshoe 11.5,\nheight = ?",
         color="#2e7d32", fontsize=10, va="bottom")
plt.xlabel("shoe size"); plt.ylabel("height (inches)")
plt.title("Predict the 11th person from the line")
plt.legend(loc="upper left", fontsize=9)
plt.tight_layout(); plt.savefig(OUT / "fig_activity_shoe.pdf"); plt.close()
print("SHOE FIT:", {k: round(v, 3) for k, v in fa.items()})

# ---------- 4. dummy: parallel lines ----------
xd = rng.uniform(0, 10, 80)
grp = rng.integers(0, 2, 80)            # 0 or 1
yd = 3 + 1.2 * xd + 6.0 * grp + rng.normal(0, 2, 80)
plt.figure(figsize=(6.4, 4.2))
for g, c, lab in [(0, "#34607d", "group 0"), (1, "#e67e22", "group 1")]:
    m = grp == g
    f = ols(xd[m], yd[m])
    plt.scatter(xd[m], yd[m], color=c, alpha=0.8, label=lab)
    plt.plot(xs, f["b0"] + f["b1"] * xs, color=c, lw=2.5)
plt.xlabel("x"); plt.ylabel("y")
plt.title("A 0/1 predictor shifts the line up (same slope)")
plt.legend(fontsize=9); plt.tight_layout(); plt.savefig(OUT / "fig_dummy.pdf"); plt.close()

# ---------- 5. interaction: different slopes ----------
xi_ = rng.uniform(0, 10, 80)
gi = rng.integers(0, 2, 80)
yi_ = 4 + 1.0 * xi_ + 0.0 * gi + 1.6 * gi * xi_ + rng.normal(0, 2.5, 80)
plt.figure(figsize=(6.4, 4.2))
for g, c, lab in [(0, "#34607d", "group 0"), (1, "#e67e22", "group 1")]:
    m = gi == g
    f = ols(xi_[m], yi_[m])
    plt.scatter(xi_[m], yi_[m], color=c, alpha=0.8, label=lab)
    plt.plot(xs, f["b0"] + f["b1"] * xs, color=c, lw=2.5)
plt.xlabel("x"); plt.ylabel("y")
plt.title("Interaction: the slope itself differs by group")
plt.legend(fontsize=9); plt.tight_layout(); plt.savefig(OUT / "fig_interaction.pdf"); plt.close()

# ---------- 6. confounding / Simpson's paradox ----------
xs_all, ys_all, gs_all = [], [], []
for g in range(4):
    xg = 2.5 * g + rng.uniform(-0.9, 0.9, 25)
    yg = 5 + 6.0 * g - 1.2 * (xg - 2.5 * g) + rng.normal(0, 0.7, 25)
    xs_all.append(xg); ys_all.append(yg); gs_all.append(np.full(25, g))
xa = np.concatenate(xs_all); ya = np.concatenate(ys_all); ga = np.concatenate(gs_all)
overall = ols(xa, ya)

fig, ax = plt.subplots(1, 2, figsize=(10.5, 4.2), sharex=True, sharey=True)
ax[0].scatter(xa, ya, color="#7f8c8d", alpha=0.8)
axx = np.array([xa.min(), xa.max()])
ax[0].plot(axx, overall["b0"] + overall["b1"] * axx, color="#c0392b", lw=2.6)
ax[0].set_title(f"Ignore the group: slope = {overall['b1']:+.1f}")
ax[0].set_xlabel("x"); ax[0].set_ylabel("y")
colors = ["#34607d", "#e67e22", "#2e7d32", "#8e44ad"]
within = []
for g in range(4):
    m = ga == g
    f = ols(xa[m], ya[m]); within.append(f["b1"])
    ax[1].scatter(xa[m], ya[m], color=colors[g], alpha=0.85, label=f"group {g}")
    gx = np.array([xa[m].min(), xa[m].max()])
    ax[1].plot(gx, f["b0"] + f["b1"] * gx, color=colors[g], lw=2.4)
ax[1].set_title(f"Within each group: slope $\\approx$ {np.mean(within):+.1f}")
ax[1].set_xlabel("x"); ax[1].legend(fontsize=8, ncol=2)
plt.tight_layout(); plt.savefig(OUT / "fig_confounding.pdf"); plt.close()
print(f"CONFOUNDING: overall slope = {overall['b1']:+.2f}, mean within-group slope = {np.mean(within):+.2f}")

print("\nwrote 6 figures to", OUT)
