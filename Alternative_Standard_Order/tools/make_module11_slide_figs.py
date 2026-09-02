#!/usr/bin/env python3
"""Figures for Module 11: Flexible Models (trees, selection, regularization)."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression, lasso_path
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

OUT = Path(__file__).resolve().parents[1] / "Slides"
DATA = Path(__file__).resolve().parents[2] / "data"
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(3)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
BLUE, RED, GREEN, GREY = "#4878a8", "#c0392b", "#2e8b57", "#7f8c8d"

cars = pd.read_csv(DATA / "cars.csv").dropna()
X1 = cars[["weight"]].values
y = cars["mpg"].values

# --- 1. a line, a shallow tree, and a deep tree ---------------------------
grid = np.linspace(X1.min(), X1.max(), 400).reshape(-1, 1)
fig, axes = plt.subplots(1, 3, figsize=(9.6, 2.9), sharey=True)
models = [("straight line", LinearRegression()),
          ("tree, depth 2", DecisionTreeRegressor(max_depth=2, random_state=0)),
          ("tree, depth 12", DecisionTreeRegressor(max_depth=12, random_state=0))]
for ax, (name, m) in zip(axes, models):
    m.fit(X1, y)
    ax.plot(X1.ravel(), y, "o", color=GREY, ms=3, alpha=0.5)
    ax.plot(grid.ravel(), m.predict(grid), color=BLUE, lw=2.4)
    ax.set_title(name, fontsize=10.5)
    ax.set_xlabel("vehicle weight (lbs)")
axes[0].set_ylabel("miles per gallon")
fig.suptitle("Trees make step functions; depth decides how many steps", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "fig_m11_treefit.pdf")
plt.close(fig)

# --- 2. the complexity curve: train vs test -------------------------------
feats = ["weight", "horsepower", "displacement", "acceleration", "model_year", "cylinder"]
X = cars[feats].values
# 120 training cars, the 6 real predictors plus 20 pure-noise columns: the standard
# situation of a wide dataset where most columns carry nothing.
Xnoisy = np.hstack([X, rng.normal(size=(len(cars), 20))])
Xtr, Xte, ytr, yte = train_test_split(Xnoisy, y, train_size=120, random_state=7)
depths = range(1, 16)
tr_err, te_err, cv_err = [], [], []
for d in depths:
    m = DecisionTreeRegressor(max_depth=d, random_state=0).fit(Xtr, ytr)
    tr_err.append(np.sqrt(np.mean((ytr - m.predict(Xtr)) ** 2)))
    te_err.append(np.sqrt(np.mean((yte - m.predict(Xte)) ** 2)))
    s = cross_val_score(DecisionTreeRegressor(max_depth=d, random_state=0), Xtr, ytr,
                        cv=KFold(5, shuffle=True, random_state=1),
                        scoring="neg_root_mean_squared_error")
    cv_err.append(-s.mean())
fig, ax = plt.subplots(figsize=(6.4, 3.3))
ax.plot(depths, tr_err, "o-", color=BLUE, lw=2, label="training error")
ax.plot(depths, cv_err, "o-", color=GREEN, lw=2, label="cross-validated error")
ax.plot(depths, te_err, "o-", color=RED, lw=2, ls="--", label="test error")
best = list(depths)[int(np.argmin(cv_err))]
ax.axvline(best, color=GREY, ls=":", lw=1.6)
ax.text(best + 0.2, max(te_err) * 0.9, f"CV picks depth {best}", fontsize=9, color=GREY)
ax.set_xlabel("tree depth (flexibility)")
ax.set_ylabel("RMSE (mpg)")
ax.legend(frameon=False, fontsize=9)
ax.set_title("Training error always falls. Only honest error has a minimum.", fontsize=10.5)
fig.tight_layout()
fig.savefig(OUT / "fig_m11_complexity.pdf")
plt.close(fig)

# --- 3. lasso path: coefficients shrink and switch off --------------------
Xs = StandardScaler().fit_transform(X)
alphas, coefs, _ = lasso_path(Xs, y, n_alphas=60)
fig, ax = plt.subplots(figsize=(6.4, 3.3))
for i, f in enumerate(feats):
    ax.plot(np.log10(alphas), coefs[i], lw=2, label=f)
ax.axhline(0, color="black", lw=0.8)
ax.set_xlabel(r"$\log_{10}$ penalty strength (more shrinkage to the right)")
ax.set_ylabel("coefficient")
ax.legend(frameon=False, fontsize=8, ncol=2)
ax.set_title("The lasso shrinks coefficients, then switches them off")
ax.invert_xaxis()
fig.tight_layout()
fig.savefig(OUT / "fig_m11_lasso.pdf")
plt.close(fig)

# --- 4. feature importance is unstable with correlated predictors ---------
runs = []
for seed in range(30):
    Xa, _, ya, _ = train_test_split(X, y, test_size=0.4, random_state=seed)
    rf = RandomForestRegressor(n_estimators=120, random_state=seed).fit(Xa, ya)
    runs.append(rf.feature_importances_)
runs = np.array(runs)
order = np.argsort(-runs.mean(axis=0))
fig, ax = plt.subplots(figsize=(6.4, 3.2))
ax.boxplot([runs[:, i] for i in order], labels=[feats[i] for i in order], widths=0.6)
ax.set_ylabel("random-forest importance")
ax.set_title("Same data, different splits: importances move a lot")
plt.setp(ax.get_xticklabels(), rotation=18, fontsize=8.5)
fig.tight_layout()
fig.savefig(OUT / "fig_m11_importance.pdf")
plt.close(fig)

# --- 5. selection on noise: the winner's curse of feature search ----------
n, p = 60, 200
Xn = rng.normal(size=(n, p))
yn = rng.normal(size=n)                      # pure noise, no signal at all
r = np.array([np.corrcoef(Xn[:, j], yn)[0, 1] for j in range(p)])
best_j = int(np.argmax(np.abs(r)))
fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.0))
axes[0].hist(r, bins=30, color=BLUE, edgecolor="white")
axes[0].axvline(r[best_j], color=RED, lw=2)
axes[0].set_xlabel("correlation with a pure-noise outcome")
axes[0].set_yticks([])
axes[0].set_title("200 useless predictors", fontsize=10.5)
axes[1].plot(Xn[:, best_j], yn, "o", color=GREY, ms=4)
b = np.polyfit(Xn[:, best_j], yn, 1)
xs = np.linspace(Xn[:, best_j].min(), Xn[:, best_j].max(), 50)
axes[1].plot(xs, np.polyval(b, xs), color=RED, lw=2.2)
axes[1].set_title(f"the 'best' one: r = {r[best_j]:.2f}", fontsize=10.5)
axes[1].set_xlabel("selected predictor")
axes[1].set_ylabel("outcome")
fig.suptitle("Search hard enough and noise looks like signal", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "fig_m11_selection.pdf")
plt.close(fig)

print("best CV depth", best, "test RMSE at best", round(te_err[best - 1], 2),
      "deepest test RMSE", round(te_err[-1], 2), "max |r| on noise", round(abs(r).max(), 2))
print("wrote module 11 figures to", OUT)
