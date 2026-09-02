#!/usr/bin/env python3
"""Figures for Module 09: Classification and Evaluation (real diabetes data)."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc, precision_recall_curve, confusion_matrix

OUT = Path(__file__).resolve().parents[1] / "Slides"
DATA = Path(__file__).resolve().parents[2] / "data"
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
BLUE, RED, GREEN, GREY = "#4878a8", "#c0392b", "#2e8b57", "#7f8c8d"

dia = pd.read_csv(DATA / "diabetes.csv")
feats = ["Glucose", "BMI", "Age", "Pregnancies", "BloodPressure"]
X, y = dia[feats].values, dia["Outcome"].values
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.35, random_state=220, stratify=y)
model = LogisticRegression(max_iter=5000).fit(Xtr, ytr)
p = model.predict_proba(Xte)[:, 1]

# --- 1. the logistic curve on one predictor -------------------------------
g = dia[["Glucose"]].values
m1 = LogisticRegression(max_iter=5000).fit(g, y)
grid = np.linspace(g.min(), g.max(), 300).reshape(-1, 1)
fig, ax = plt.subplots(figsize=(6.2, 3.3))
jitter = np.random.default_rng(1).normal(0, 0.02, len(y))
ax.plot(g.ravel(), y + jitter, "o", color=GREY, ms=3, alpha=0.35)
ax.plot(grid.ravel(), m1.predict_proba(grid)[:, 1], color=BLUE, lw=2.8)
ax.axhline(0.5, color=RED, ls="--", lw=1.2)
thr_x = (-m1.intercept_[0] / m1.coef_[0][0])
ax.axvline(thr_x, color=RED, ls="--", lw=1.2)
ax.text(thr_x + 3, 0.06, f"predicted 50/50\nat glucose {thr_x:.0f}", fontsize=9, color=RED)
ax.set_xlabel("plasma glucose")
ax.set_ylabel("probability of diabetes")
ax.set_title("Logistic regression bends a line into a probability")
fig.tight_layout()
fig.savefig(OUT / "fig_m09_logistic.pdf")
plt.close(fig)

# --- 2. two thresholds, two confusion matrices ----------------------------
fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.2))
for ax, t in zip(axes, [0.5, 0.25]):
    cm = confusion_matrix(yte, (p >= t).astype(int))
    ax.imshow(cm, cmap="Blues", vmin=0, vmax=cm.max())
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha="center", va="center", fontsize=14,
                    color="white" if cm[i, j] > cm.max() * 0.6 else "black")
    tp, fn, fp = cm[1, 1], cm[1, 0], cm[0, 1]
    prec, rec = tp / (tp + fp), tp / (tp + fn)
    ax.set_title(f"threshold {t}\nprecision {prec:.2f}, recall {rec:.2f}", fontsize=10)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["say no", "say yes"])
    ax.set_yticks([0, 1]); ax.set_yticklabels(["really no", "really yes"])
    ax.grid(False)
fig.suptitle("Moving the threshold trades one error for the other", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "fig_m09_confusion.pdf")
plt.close(fig)

# --- 3. ROC and precision-recall ------------------------------------------
fpr, tpr, _ = roc_curve(yte, p)
pr, rc, _ = precision_recall_curve(yte, p)
fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.2))
axes[0].plot(fpr, tpr, color=BLUE, lw=2.4)
axes[0].plot([0, 1], [0, 1], color=GREY, ls="--", lw=1.2)
axes[0].set_xlabel("false positive rate")
axes[0].set_ylabel("true positive rate (recall)")
axes[0].set_title(f"ROC curve, AUC = {auc(fpr, tpr):.2f}", fontsize=10.5)
axes[1].plot(rc, pr, color=BLUE, lw=2.4)
axes[1].axhline(yte.mean(), color=RED, ls="--", lw=1.2)
axes[1].text(0.45, yte.mean() + 0.03, "guessing at the base rate", fontsize=9, color=RED)
axes[1].set_xlabel("recall")
axes[1].set_ylabel("precision")
axes[1].set_ylim(0, 1)
axes[1].set_title("Precision-recall curve", fontsize=10.5)
fig.tight_layout()
fig.savefig(OUT / "fig_m09_roc.pdf")
plt.close(fig)

# --- 4. cost of the threshold ---------------------------------------------
thresholds = np.linspace(0.02, 0.98, 200)
COST_FN, COST_FP = 500, 60      # missing a case vs an unnecessary follow-up
costs = []
for t in thresholds:
    pred = (p >= t).astype(int)
    fn = ((pred == 0) & (yte == 1)).sum()
    fp = ((pred == 1) & (yte == 0)).sum()
    costs.append((fn * COST_FN + fp * COST_FP) / len(yte))
costs = np.array(costs)
best = thresholds[int(np.argmin(costs))]
fig, ax = plt.subplots(figsize=(6.2, 3.2))
ax.plot(thresholds, costs, color=BLUE, lw=2.4)
ax.axvline(0.5, color=GREY, ls="--", lw=1.4)
ax.axvline(best, color=GREEN, lw=2)
ax.text(0.5 + 0.01, costs.max() * 0.92, "the default 0.5", fontsize=9, color=GREY)
ax.text(best - 0.02, costs.min() * 1.25, f"cost-minimizing\nthreshold {best:.2f}",
        fontsize=9, color=GREEN, ha="right")
ax.set_xlabel("threshold for calling it positive")
ax.set_ylabel("expected cost per patient ($)")
ax.set_title("When a miss costs $500 and a false alarm costs $60")
fig.tight_layout()
fig.savefig(OUT / "fig_m09_threshold.pdf")
plt.close(fig)

# --- 5. calibration --------------------------------------------------------
bins = np.linspace(0, 1, 11)
idx = np.digitize(p, bins) - 1
xs, ys = [], []
for b in range(10):
    m = idx == b
    if m.sum() > 5:
        xs.append(p[m].mean()); ys.append(yte[m].mean())
fig, ax = plt.subplots(figsize=(5.6, 3.2))
ax.plot([0, 1], [0, 1], color=GREY, ls="--", lw=1.4, label="perfect calibration")
ax.plot(xs, ys, "o-", color=BLUE, lw=2.2, ms=6, label="this model")
ax.set_xlabel("predicted probability")
ax.set_ylabel("actual frequency")
ax.legend(frameon=False, fontsize=9)
ax.set_title("Does 30% mean 30%?")
fig.tight_layout()
fig.savefig(OUT / "fig_m09_calibration.pdf")
plt.close(fig)

print("base rate", round(yte.mean(), 3), "AUC", round(auc(fpr, tpr), 3),
      "best threshold", round(best, 3),
      "accuracy of always-no", round(1 - yte.mean(), 3))
print("wrote module 09 figures to", OUT)
