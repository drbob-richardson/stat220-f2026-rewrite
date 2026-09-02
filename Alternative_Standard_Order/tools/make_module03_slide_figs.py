#!/usr/bin/env python3
"""
Figures for the Module 3 (building & trusting a model) slides.

  fig_m3_activity.pdf   height -> shoe size: 10 training points + line + 2 held-out people
  fig_overfit.pdf       noisy data: a simple line vs a wiggly overfit curve
  fig_traintest.pdf     model complexity vs train error (down) and test error (U-shape)
  fig_transform.pdf     a curved relationship, and the same data made straight by a log
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "Slides"
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(303)

# ---------- 1. activity: height -> shoe ----------
height = np.array([63, 65, 66, 68, 69, 70, 71, 72, 74, 76.0])
shoe = -25 + 0.52 * height + rng.normal(0, 0.6, len(height))
b1, b0 = np.polyfit(height, shoe, 1)
hx = np.array([height.min() - 1, height.max() + 1])
hold_h = np.array([64.0, 73.0])
hold_s = -25 + 0.52 * hold_h + rng.normal(0, 0.6, 2)
plt.figure(figsize=(6.6, 4.3))
plt.scatter(height, shoe, color="#34607d", s=55, zorder=3, label="our 10 volunteers (training)")
plt.plot(hx, b0 + b1 * hx, color="#c0392b", lw=2.5, label="line fit on those 10")
plt.scatter(hold_h, hold_s, color="#e67e22", s=80, marker="D", zorder=4,
            label="2 new people (held out)")
plt.xlabel("height (inches)"); plt.ylabel("shoe size")
plt.title("Predict shoe size from height")
plt.legend(loc="upper left", fontsize=8.5)
plt.tight_layout(); plt.savefig(OUT / "fig_m3_activity.pdf"); plt.close()

# ---------- 2. overfit: line vs wiggly polynomial ----------
xo = np.sort(rng.uniform(0, 1, 12))
yo = np.sin(2 * np.pi * xo * 0.8) + rng.normal(0, 0.25, len(xo))
xg = np.linspace(0, 1, 300)
p1 = np.polyfit(xo, yo, 1)
p9 = np.polyfit(xo, yo, 9)
plt.figure(figsize=(6.6, 4.3))
plt.scatter(xo, yo, color="#34607d", s=55, zorder=3, label="data")
plt.plot(xg, np.polyval(p1, xg), color="#2e7d32", lw=2.5, label="simple line (underfits a bit)")
plt.plot(xg, np.polyval(p9, xg), color="#c0392b", lw=2.0, label="degree-9 fit (overfits)")
plt.ylim(yo.min() - 1.2, yo.max() + 1.2)
plt.xlabel("x"); plt.ylabel("y")
plt.title("The wiggly curve nails the dots and learns the noise")
plt.legend(fontsize=8.5)
plt.tight_layout(); plt.savefig(OUT / "fig_overfit.pdf"); plt.close()

# ---------- 3. train vs test error across complexity ----------
def make(n):
    x = rng.uniform(0, 1, n)
    y = np.sin(2 * np.pi * x * 0.8) + rng.normal(0, 0.25, n)
    return x, y
xtr, ytr = make(30)
xte, yte = make(300)
degs = range(1, 13)
tr_err, te_err = [], []
for d in degs:
    c = np.polyfit(xtr, ytr, d)
    tr_err.append(np.mean((np.polyval(c, xtr) - ytr) ** 2))
    te_err.append(np.mean((np.polyval(c, xte) - yte) ** 2))
plt.figure(figsize=(6.6, 4.3))
plt.plot(list(degs), tr_err, "o-", color="#2e7d32", label="error on training data")
plt.plot(list(degs), te_err, "s-", color="#c0392b", label="error on new data")
plt.yscale("log")
plt.xlabel("model complexity (polynomial degree)"); plt.ylabel("mean squared error")
plt.title("Training error keeps dropping; new-data error turns back up")
plt.legend(fontsize=9)
plt.tight_layout(); plt.savefig(OUT / "fig_traintest.pdf"); plt.close()
print("train err:", [round(e, 3) for e in tr_err])
print("test  err:", [round(e, 3) for e in te_err], " -> min at degree", list(degs)[int(np.argmin(te_err))])

# ---------- 4. transform: curved -> straight by log ----------
xt = rng.uniform(1, 10, 60)
yt = np.exp(0.45 * xt) * rng.lognormal(0, 0.18, 60)
fig, ax = plt.subplots(1, 2, figsize=(10.5, 4.2))
ax[0].scatter(xt, yt, color="#34607d", alpha=0.8)
bl = np.polyfit(xt, yt, 1)
sx = np.array([xt.min(), xt.max()])
ax[0].plot(sx, np.polyval(bl, sx), color="#c0392b", lw=2.3)
ax[0].set_title("Raw: curved, a straight line misses"); ax[0].set_xlabel("x"); ax[0].set_ylabel("y")
ax[1].scatter(xt, np.log(yt), color="#34607d", alpha=0.8)
bl2 = np.polyfit(xt, np.log(yt), 1)
ax[1].plot(sx, np.polyval(bl2, sx), color="#c0392b", lw=2.3)
ax[1].set_title("After log(y): straight, a line fits"); ax[1].set_xlabel("x"); ax[1].set_ylabel("log(y)")
plt.tight_layout(); plt.savefig(OUT / "fig_transform.pdf"); plt.close()

print("wrote 4 Module 3 figures to", OUT)
