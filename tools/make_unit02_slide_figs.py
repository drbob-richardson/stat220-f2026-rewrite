#!/usr/bin/env python3
"""Figures for Unit 2: A Map of Models.

  fig_u2_shapes.pdf    what f looks like for four different families, same data
  fig_u2_ytypes.pdf    the four outcome types you will actually meet
  fig_u2_ci_pi.pdf     a confidence band and a prediction band on one plot

Run from the Course_Rewrite folder:  python tools/make_unit02_slide_figs.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

OUT = Path(__file__).resolve().parents[1] / "Slides"
DATA = Path(__file__).resolve().parents[2] / "data"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
BLUE, RED, GREEN, GREY = "#4878a8", "#c0392b", "#2e8b57", "#7f8c8d"

cars = pd.read_csv(DATA / "cars.csv").dropna()
rent = pd.read_csv(DATA / "rent.csv").dropna()
x, y = cars[["weight"]].values, cars["mpg"].values
grid = np.linspace(x.min(), x.max(), 400).reshape(-1, 1)

# --- 1. four shapes of f, same data ---------------------------------------
fits = [
    ("a straight line", np.poly1d(np.polyfit(x.ravel(), y, 1))(grid.ravel()), BLUE),
    ("a curve", np.poly1d(np.polyfit(x.ravel(), y, 2))(grid.ravel()), GREEN),
    ("a tree (steps)", DecisionTreeRegressor(max_depth=3, random_state=0).fit(x, y).predict(grid), RED),
    ("a forest", RandomForestRegressor(n_estimators=300, random_state=0).fit(x, y).predict(grid), "#8e44ad"),
]
fig, axes = plt.subplots(1, 4, figsize=(10.2, 2.5), sharey=True)
for ax, (label, pred, col) in zip(axes, fits):
    ax.scatter(x, y, s=6, color=GREY, alpha=0.35)
    ax.plot(grid, pred, color=col, lw=2)
    ax.set_title(label, fontsize=9)
    ax.set_xlabel("weight")
axes[0].set_ylabel("mpg")
fig.tight_layout()
fig.savefig(OUT / "fig_u2_shapes.pdf")
plt.close(fig)

# --- 2. the four outcome types --------------------------------------------
fig, axes = plt.subplots(1, 4, figsize=(10.2, 2.4))
axes[0].hist(cars["mpg"], bins=20, color=BLUE)
axes[0].set_title("a number\n(mpg)", fontsize=9)

binary = (cars["mpg"] > 30).astype(int)   # a real threshold, not a forced 50/50
axes[1].bar(["no", "yes"], binary.value_counts().sort_index().values, color=RED, width=0.55)
axes[1].set_title("yes or no\n(over 30 mpg?)", fontsize=9)

counts = rent["BHK"].value_counts().sort_index()
axes[2].bar(counts.index.astype(str), counts.values, color=GREEN, width=0.6)
axes[2].set_title("a count\n(bedrooms)", fontsize=9)

cat = cars["origin"].value_counts()
axes[3].bar(cat.index.astype(str), cat.values, color="#8e44ad", width=0.55)
axes[3].set_title("a category\n(origin)", fontsize=9)
for ax in axes:
    ax.set_ylabel("")
    ax.tick_params(labelsize=8)
fig.tight_layout()
fig.savefig(OUT / "fig_u2_ytypes.pdf")
plt.close(fig)

# --- 3. confidence band vs prediction band --------------------------------
fit = smf.ols("mpg ~ weight", data=cars).fit()
gx = pd.DataFrame({"weight": np.linspace(cars.weight.min(), cars.weight.max(), 200)})
pred = fit.get_prediction(gx).summary_frame(alpha=0.05)

fig, ax = plt.subplots(figsize=(6.2, 3.4))
ax.scatter(cars.weight, cars.mpg, s=8, color=GREY, alpha=0.4, label="the data")
ax.fill_between(gx.weight, pred["obs_ci_lower"], pred["obs_ci_upper"],
                color=RED, alpha=0.15, label="95% prediction band (one new car)")
ax.fill_between(gx.weight, pred["mean_ci_lower"], pred["mean_ci_upper"],
                color=BLUE, alpha=0.45, label="95% confidence band (the mean)")
ax.plot(gx.weight, pred["mean"], color="black", lw=1.6)
ax.set_xlabel("weight"); ax.set_ylabel("mpg")
ax.legend(frameon=False, fontsize=8, loc="upper right")
fig.tight_layout()
fig.savefig(OUT / "fig_u2_ci_pi.pdf")
plt.close(fig)

print("wrote fig_u2_shapes.pdf, fig_u2_ytypes.pdf, fig_u2_ci_pi.pdf")
