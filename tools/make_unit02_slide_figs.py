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

print("done")
