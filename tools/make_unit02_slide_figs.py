#!/usr/bin/env python3
"""Figures for Unit 2: A Map of Models. One picture per model, plus the framing ones.

Run from the Course_Rewrite folder:  python tools/make_unit02_slide_figs.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import lasso_path
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from sklearn.preprocessing import StandardScaler

OUT = Path(__file__).resolve().parents[1] / "Slides"
DATA = Path(__file__).resolve().parents[2] / "data"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
BLUE, RED, GREEN, GREY, PURPLE = "#4878a8", "#c0392b", "#2e8b57", "#7f8c8d", "#8e44ad"

cars = pd.read_csv(DATA / "cars.csv").dropna()
rent = pd.read_csv(DATA / "rent.csv").dropna()
bikes = pd.read_csv(DATA / "bikes.csv").dropna()
x, y = cars[["weight"]].values, cars["mpg"].values
grid = np.linspace(x.min(), x.max(), 400).reshape(-1, 1)

def scatter(ax):
    ax.scatter(x, y, s=7, color=GREY, alpha=0.35)
    ax.set_xlabel("weight"); ax.set_ylabel("mpg")

def save(fig, name):
    fig.tight_layout(); fig.savefig(OUT / name); plt.close(fig)
    print("  ", name)

# ---- framing: four shapes of f -------------------------------------------
fits = [("a straight line", np.poly1d(np.polyfit(x.ravel(), y, 1))(grid.ravel()), BLUE),
        ("a curve", np.poly1d(np.polyfit(x.ravel(), y, 2))(grid.ravel()), GREEN),
        ("a tree (steps)", DecisionTreeRegressor(max_depth=3, random_state=0).fit(x, y).predict(grid), RED),
        ("a forest", RandomForestRegressor(n_estimators=300, random_state=0).fit(x, y).predict(grid), PURPLE)]
fig, axes = plt.subplots(1, 4, figsize=(10.2, 2.5), sharey=True)
for ax, (lab, pred, col) in zip(axes, fits):
    ax.scatter(x, y, s=6, color=GREY, alpha=0.35); ax.plot(grid, pred, color=col, lw=2)
    ax.set_title(lab, fontsize=9); ax.set_xlabel("weight")
axes[0].set_ylabel("mpg"); save(fig, "fig_u2_shapes.pdf")

# ---- framing: the four outcome types -------------------------------------
fig, axes = plt.subplots(1, 4, figsize=(10.2, 2.4))
axes[0].hist(cars["mpg"], bins=20, color=BLUE); axes[0].set_title("a number\n(mpg)", fontsize=9)
b = (cars["mpg"] > 30).astype(int)
axes[1].bar(["no","yes"], b.value_counts().sort_index().values, color=RED, width=.55)
axes[1].set_title("yes or no\n(over 30 mpg?)", fontsize=9)
c = rent["BHK"].value_counts().sort_index()
axes[2].bar(c.index.astype(str), c.values, color=GREEN, width=.6); axes[2].set_title("a count\n(bedrooms)", fontsize=9)
k = cars["origin"].value_counts()
axes[3].bar(k.index.astype(str), k.values, color=PURPLE, width=.55); axes[3].set_title("a category\n(origin)", fontsize=9)
for ax in axes: ax.tick_params(labelsize=8)
save(fig, "fig_u2_ytypes.pdf")

# ---- one per model -------------------------------------------------------
fig, ax = plt.subplots(figsize=(5.4, 3.0)); scatter(ax)
ax.plot(grid, np.poly1d(np.polyfit(x.ravel(), y, 1))(grid.ravel()), color=BLUE, lw=2.2)
save(fig, "fig_u2_m_linear.pdf")

fig, ax = plt.subplots(figsize=(5.4, 3.0))
yb = (cars["mpg"] > 30).astype(int)
lg = sm.Logit(yb, sm.add_constant(cars[["weight"]])).fit(disp=0)
ax.scatter(cars.weight, yb + np.random.default_rng(0).normal(0, .02, len(yb)), s=7, color=GREY, alpha=.4)
ax.plot(grid, lg.predict(sm.add_constant(pd.DataFrame(grid, columns=["weight"]))), color=RED, lw=2.2)
ax.set_xlabel("weight"); ax.set_ylabel("P(over 30 mpg)")
save(fig, "fig_u2_m_logistic.pdf")

fig, ax = plt.subplots(figsize=(5.4, 3.0))
po = smf.glm("Count ~ Temperature", data=bikes, family=sm.families.Poisson()).fit()
tg = pd.DataFrame({"Temperature": np.linspace(bikes.Temperature.min(), bikes.Temperature.max(), 200)})
ax.scatter(bikes.Temperature, bikes.Count, s=5, color=GREY, alpha=.25)
ax.plot(tg.Temperature, po.predict(tg), color=GREEN, lw=2.2)
ax.set_xlabel("temperature"); ax.set_ylabel("bikes rented that hour")
save(fig, "fig_u2_m_poisson.pdf")

fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.0))
t3 = DecisionTreeRegressor(max_depth=2, random_state=0).fit(x, y)
axes[0].scatter(x, y, s=7, color=GREY, alpha=.35)
axes[0].plot(grid, t3.predict(grid), color=RED, lw=2.2)
axes[0].set_xlabel("weight"); axes[0].set_ylabel("mpg"); axes[0].set_title("what it predicts", fontsize=9)
plot_tree(t3, feature_names=["weight"], filled=False, ax=axes[1], fontsize=7, precision=0, impurity=False)
axes[1].set_title("the rules it learned", fontsize=9)
save(fig, "fig_u2_m_tree.pdf")

fig, ax = plt.subplots(figsize=(5.4, 3.0)); scatter(ax)
for s in range(4):
    ax.plot(grid, DecisionTreeRegressor(max_depth=3, random_state=s).fit(
        *(lambda i: (x[i], y[i]))(np.random.default_rng(s).integers(0, len(y), len(y)))).predict(grid),
        color=GREY, lw=.8, alpha=.7)
ax.plot(grid, RandomForestRegressor(n_estimators=300, random_state=0).fit(x, y).predict(grid), color=PURPLE, lw=2.2)
ax.set_title("four single trees (thin) and their average (thick)", fontsize=9)
save(fig, "fig_u2_m_forest.pdf")

fig, ax = plt.subplots(figsize=(5.4, 3.0)); scatter(ax)
for n, col, a in [(1, "#dab6e8", 1), (10, "#b47fd0", 1), (200, PURPLE, 1)]:
    ax.plot(grid, GradientBoostingRegressor(n_estimators=n, max_depth=2, random_state=0).fit(x, y).predict(grid),
            color=col, lw=1.8, label=f"{n} tree" + ("s" if n > 1 else ""))
ax.legend(frameon=False, fontsize=8)
save(fig, "fig_u2_m_boost.pdf")

fig, ax = plt.subplots(figsize=(5.4, 3.0)); scatter(ax)
for kk, col in [(3, RED), (40, BLUE)]:
    ax.plot(grid, KNeighborsRegressor(n_neighbors=kk).fit(x, y).predict(grid), color=col, lw=2, label=f"k = {kk}")
ax.legend(frameon=False, fontsize=8)
save(fig, "fig_u2_m_knn.pdf")

fig, ax = plt.subplots(figsize=(5.8, 3.0))
preds = ["weight","displacement","horsepower","acceleration","model_year","cylinder"]
Xs = StandardScaler().fit_transform(cars[preds])
alphas, coefs, _ = lasso_path(Xs, cars["mpg"].values)
for i, name in enumerate(preds):
    ax.plot(alphas, coefs[i], lw=1.6, label=name)
ax.set_xscale("log"); ax.invert_xaxis()
ax.set_xlabel("penalty (large on the left)"); ax.set_ylabel("coefficient")
ax.axhline(0, color="black", lw=.7)
ax.legend(frameon=False, fontsize=7, ncol=2)
save(fig, "fig_u2_m_lasso.pdf")

# ---- training error against honest error ---------------------------------
from sklearn.model_selection import cross_val_score, KFold
depths = range(1, 11); tr, cv = [], []
folds = KFold(5, shuffle=True, random_state=0)
Xall = cars[preds].values
for d in depths:
    m = DecisionTreeRegressor(max_depth=d, random_state=0).fit(Xall, y)
    tr.append(np.mean((m.predict(Xall) - y) ** 2))
    cv.append(-cross_val_score(DecisionTreeRegressor(max_depth=d, random_state=0),
                               Xall, y, cv=folds, scoring="neg_mean_squared_error").mean())
fig, ax = plt.subplots(figsize=(6.0, 3.2))
ax.plot(list(depths), tr, "o-", color=BLUE, label="training MSE")
ax.plot(list(depths), cv, "s-", color=RED, label="cross-validated MSE")
best = list(depths)[int(np.argmin(cv))]
ax.axvline(best, color=GREY, ls=":", lw=1)
ax.annotate(f"lowest honest error\nat depth {best}", xy=(best, min(cv)),
            xytext=(best + 1.2, min(cv) + 6), fontsize=8,
            arrowprops=dict(arrowstyle="->", lw=1))
ax.set_xlabel("tree depth"); ax.set_ylabel("mean squared error"); ax.set_xticks(list(depths))
ax.legend(frameon=False, fontsize=8)
save(fig, "fig_u2_mse.pdf")

def little_tree(ax, cx, cy, w=0.62, h=0.5, color=GREY):
    """A small stylised decision tree centred at (cx, cy)."""
    top = (cx, cy + h/2)
    mid = [(cx - w/3, cy), (cx + w/3, cy)]
    bot = [(cx - w/2, cy - h/2), (cx - w/6, cy - h/2), (cx + w/6, cy - h/2), (cx + w/2, cy - h/2)]
    for m in mid:
        ax.plot([top[0], m[0]], [top[1], m[1]], color=color, lw=1.1, zorder=1)
    for i, m in enumerate(mid):
        for b in bot[2*i:2*i+2]:
            ax.plot([m[0], b[0]], [m[1], b[1]], color=color, lw=1.1, zorder=1)
    for pt in [top] + mid:
        ax.plot(*pt, "o", ms=4.5, color=color, zorder=2)
    for b in bot:
        ax.plot(*b, "s", ms=4.5, color=color, zorder=2)

def arrow(ax, a, b, color="black", lw=1.2, style="-|>"):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=11,
                                 color=color, lw=lw, shrinkA=3, shrinkB=3))

# ---------------- random forest: many trees, one average -------------------
fig, ax = plt.subplots(figsize=(7.4, 3.2))
xs = [0.9, 2.4, 3.9, 6.3]
for i, cx in enumerate(xs):
    if i == 3:
        continue
    little_tree(ax, cx, 2.05, color=GREY)
    ax.text(cx, 1.45, f"tree {i+1}", ha="center", fontsize=8, color=GREY)
    ax.text(cx, 1.18, f"says {[31.2, 28.6, 30.1][i]}", ha="center", fontsize=8, color="black")
ax.text(5.2, 2.0, r"$\cdots$", ha="center", va="center", fontsize=16, color=GREY)
ax.text(6.3, 1.45, "tree 500", ha="center", fontsize=8, color=GREY)
ax.text(6.3, 1.18, "says 29.4", ha="center", fontsize=8, color="black")
little_tree(ax, 6.3, 2.05, color=GREY)
box = FancyBboxPatch((2.35, 0.12), 2.6, 0.52, boxstyle="round,pad=0.06",
                     fc="#efe7f6", ec=PURPLE, lw=1.4)
ax.add_patch(box)
ax.text(3.65, 0.38, "average them:  29.8 mpg", ha="center", va="center",
        fontsize=10, color=PURPLE, weight="bold")
for cx in [0.9, 2.4, 3.9, 6.3]:
    arrow(ax, (cx, 1.05), (3.65, 0.70), color=GREY, lw=1.0)
ax.set_xlim(0.2, 7.2); ax.set_ylim(0, 2.7); ax.axis("off")
ax.set_title("every tree votes, and the forest reports the average", fontsize=9)
fig.tight_layout(); fig.savefig(OUT / "fig_u2_m_forest.pdf"); plt.close(fig)
print("  fig_u2_m_forest.pdf")

# ---------------- boosting: each tree fixes the last ----------------------
fig, ax = plt.subplots(figsize=(8.4, 2.9))
xs = [0.8, 2.9, 5.0, 7.6]
labels = ["tree 1", "tree 2", "tree 3", "tree 200"]
running = ["23.0", "26.4", "28.1", "29.8"]
for i, cx in enumerate(xs):
    little_tree(ax, cx, 1.75, w=0.55, h=0.45, color=GREY)
    ax.text(cx, 1.20, labels[i], ha="center", fontsize=8, color=GREY)
    box = FancyBboxPatch((cx - 0.52, 0.55), 1.04, 0.42, boxstyle="round,pad=0.05",
                         fc="#efe7f6" if i == 3 else "white", ec=PURPLE, lw=1.3)
    ax.add_patch(box)
    ax.text(cx, 0.76, running[i], ha="center", va="center", fontsize=9,
            color=PURPLE, weight="bold" if i == 3 else "normal")
    arrow(ax, (cx, 1.10), (cx, 1.00), color=GREY, lw=1.0)
for a, b, lab in [(0.8, 2.9, "what it\nstill missed"), (2.9, 5.0, "what it\nstill missed")]:
    arrow(ax, (a + 0.55, 0.76), (b - 0.55, 0.76), color=RED, lw=1.2)
    ax.text((a + b) / 2, 1.02, lab, ha="center", fontsize=7, color=RED)
ax.text(6.3, 0.76, r"$\cdots$", ha="center", va="center", fontsize=15, color=GREY)
arrow(ax, (5.55, 0.76), (6.0, 0.76), color=RED, lw=1.2)
arrow(ax, (6.6, 0.76), (7.05, 0.76), color=RED, lw=1.2)
ax.text(7.6, 0.30, "final prediction", ha="center", fontsize=8, color=PURPLE)
ax.set_xlim(0.1, 8.3); ax.set_ylim(0.1, 2.35); ax.axis("off")
ax.set_title("each tree is fitted to what the ones before it got wrong", fontsize=9)
fig.tight_layout(); fig.savefig(OUT / "fig_u2_m_boost.pdf"); plt.close(fig)
print("  fig_u2_m_boost.pdf")

# ---------------- lasso path: penalty increasing to the right -------------
cars = pd.read_csv(DATA / "cars.csv").dropna()
preds = ["displacement", "horsepower", "model_year", "cylinder", "acceleration"]
Xs = StandardScaler().fit_transform(cars[preds])
alphas, coefs, _ = lasso_path(Xs, cars["mpg"].values, eps=5e-4, n_alphas=200)
order = np.argsort(alphas)                    # ascending penalty, so it reads left to right
alphas, coefs = alphas[order], coefs[:, order]
fig, ax = plt.subplots(figsize=(6.4, 3.3))
cols = [BLUE, RED, GREEN, "#e08214", PURPLE]
for i, name in enumerate(preds):
    ax.plot(alphas, coefs[i], lw=2.0, color=cols[i], label=name)
ax.set_xscale("log")
ax.set_xlim(alphas[0] * 0.9, alphas[-1] * 3.4)
ax.legend(frameon=False, fontsize=7.5, loc="upper right", ncol=2)
ax.axhline(0, color="black", lw=.8)
ax.set_xlabel("penalty, increasing to the right")
ax.set_ylabel("coefficient")
ax.set_title("raise the penalty and coefficients are driven to zero, one at a time", fontsize=9)
fig.tight_layout(); fig.savefig(OUT / "fig_u2_m_lasso.pdf"); plt.close(fig)
print("  fig_u2_m_lasso.pdf")

print("done")
