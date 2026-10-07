#!/usr/bin/env python3
"""Figures for Unit 5 (when a line is not enough, and decision trees).

Most of them use data/diamonds.csv, a 5,000-stone sample of the standard
diamonds dataset. The interaction figure uses data/lawn_jobs.csv, which is made
up, because the diamonds do not show a clean interaction and that principle
still needs a picture.

Run:  python tools/make_unit05_slide_figs.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, plot_tree

ROOT = Path(__file__).resolve().parent.parent
SLIDES = ROOT / "Slides"
BLUE, RED, GREY, GREEN = "#4878a8", "#c0392b", "#7f8c8d", "#2e7d5b"
gems = pd.read_csv(ROOT / "data" / "diamonds.csv")
jobs = pd.read_csv(ROOT / "data" / "lawn_jobs.csv")
RHS = "C(cut) + C(color) + C(clarity)"


def save(fig, name):
    fig.tight_layout()
    fig.savefig(SLIDES / name, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote Slides/{name}")


def fig_diagnostics():
    """The four things a residual plot shows you."""
    rng = np.random.default_rng(3)
    x = rng.uniform(0, 10, 220)
    panels = [
        ("nothing wrong", rng.normal(0, 1, 220)),
        ("curvature", 0.45 * (x - 5) ** 2 - 3.5 + rng.normal(0, 1, 220)),
        ("spread that grows", rng.normal(0, 0.25 + 0.38 * x)),
        ("one point doing the work", rng.normal(0, 1, 220)),
    ]
    panels[3][1][7] = 11.5
    fig, axes = plt.subplots(1, 4, figsize=(11.6, 2.7), sharex=True)
    for ax, (title, resid) in zip(axes, panels):
        ax.scatter(x, resid, s=9, color=GREY, alpha=0.65)
        ax.axhline(0, color=RED, lw=1.4)
        ax.set_title(title, fontsize=9)
        ax.set_xlabel("fitted value", fontsize=8)
        ax.set_yticks([])
    axes[0].set_ylabel("residual", fontsize=8)
    save(fig, "fig_u5_diagnostics.pdf")


def fig_fan():
    """The same stones, before and after taking logs."""
    plain = smf.ols(f"price ~ carat + {RHS}", data=gems).fit()
    logm = smf.ols(f"np.log(price) ~ np.log(carat) + {RHS}", data=gems).fit()
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.4))
    for ax, f, title, ylab in [
            (axes[0], plain, "price, straight from the data", "residual (dollars)"),
            (axes[1], logm, "log(price) on log(carat)", "residual (log scale)")]:
        ax.scatter(f.fittedvalues, f.resid, s=10, color=GREY, alpha=0.6)
        ax.axhline(0, color=RED, lw=1.5)
        ax.set_title(title, fontsize=9.5)
        ax.set_xlabel("fitted value"); ax.set_ylabel(ylab)
    save(fig, "fig_u5_fan.pdf")


def fig_poly():
    """A line, a quadratic, and what the log does to the same cloud."""
    d = gems.sort_values("carat")
    x, y = d.carat.values, d.price.values
    grid = np.linspace(x.min(), x.max(), 300)
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.2))

    axes[0].scatter(x, y, s=8, color=GREY, alpha=0.5)
    b = np.polyfit(x, y, 1)
    axes[0].plot(grid, np.polyval(b, grid), color=RED, lw=2)
    axes[0].set_title("a straight line", fontsize=9.5)

    axes[1].scatter(x, y, s=8, color=GREY, alpha=0.5)
    b2 = np.polyfit(x, y, 2)
    axes[1].plot(grid, np.polyval(b2, grid), color=RED, lw=2)
    axes[1].set_title("add a squared term", fontsize=9.5)

    axes[2].scatter(np.log(x), np.log(y), s=8, color=GREY, alpha=0.5)
    bl = np.polyfit(np.log(x), np.log(y), 1)
    axes[2].plot(np.log(grid), np.polyval(bl, np.log(grid)), color=RED, lw=2)
    axes[2].set_title("or take logs of both", fontsize=9.5)
    for ax in axes[:2]:
        ax.set_xlabel("carat")
    axes[2].set_xlabel("log carat")
    axes[0].set_ylabel("price ($)"); axes[2].set_ylabel("log price")
    save(fig, "fig_u5_poly.pdf")


def fig_one_split():
    """What a single split is, and the step function it makes."""
    d = gems.sample(400, random_state=2)
    x, y = d.carat.values, d.price.values
    cut = 1.0
    left, right = y[x <= cut].mean(), y[x > cut].mean()

    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    ax.scatter(x, y, s=14, color=GREY, alpha=0.6)
    ax.axvline(cut, color=GREEN, ls="--", lw=1.6)
    ax.hlines(left, x.min(), cut, color=RED, lw=2.5)
    ax.hlines(right, cut, x.max(), color=RED, lw=2.5)
    ax.annotate(f"predict ${left:,.0f}", (cut * 0.35, left + 1800), color=RED, fontsize=9)
    ax.annotate(f"predict ${right:,.0f}", (cut * 1.15, right + 2200), color=RED, fontsize=9)
    ax.annotate(f"carat = {cut}", (cut, y.max() * 0.97), color=GREEN, fontsize=8.5, ha="center")
    ax.set_xlabel("carat"); ax.set_ylabel("price ($)")
    save(fig, "fig_u5_one_split.pdf")


def fig_tree_steps():
    """More splits, more steps: depth 1, 3, and 10 on the same jobs."""
    d = gems.sample(400, random_state=2).sort_values("carat")
    x = d[["carat"]].values
    y = d.price.values
    grid = np.linspace(x.min(), x.max(), 600).reshape(-1, 1)
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.1), sharey=True)
    for ax, depth in zip(axes, (1, 3, 10)):
        t = DecisionTreeRegressor(max_depth=depth, random_state=0).fit(x, y)
        ax.scatter(x, y, s=12, color=GREY, alpha=0.55)
        ax.plot(grid, t.predict(grid), color=RED, lw=2)
        ax.set_title(f"depth {depth}: {t.get_n_leaves()} groups", fontsize=9.5)
        ax.set_xlabel("carat")
    axes[0].set_ylabel("price ($)")
    save(fig, "fig_u5_tree_steps.pdf")


def fig_tree_depth():
    """Deeper always fits better, and stops predicting better."""
    # the mowing data, not the diamonds: carat is such a clean predictor that a
    # deeper tree barely hurts, so the diamonds show no honest overfitting turn
    X = pd.get_dummies(jobs[["lot_sqft", "slope", "obstacles", "gated", "crew_size"]],
                       drop_first=True)
    y = jobs.minutes
    depths = range(1, 15)
    tr, te = [], []
    for depth in depths:
        a, b = [], []
        for split in range(25):
            Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=split)
            t = DecisionTreeRegressor(max_depth=depth, random_state=0).fit(Xtr, ytr)
            a.append(np.sqrt(((ytr - t.predict(Xtr)) ** 2).mean()))
            b.append(np.sqrt(((yte - t.predict(Xte)) ** 2).mean()))
        tr.append(np.mean(a)); te.append(np.mean(b))
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.plot(list(depths), tr, "o-", color=BLUE, lw=2, label="error on the rows it was fitted on")
    ax.plot(list(depths), te, "s-", color=RED, lw=2, label="error on rows held back")
    best = int(np.argmin(te)) + 1
    ax.axvline(best, color=GREEN, ls="--", lw=1.5, label=f"best held-out depth: {best}")
    ax.set_xlabel("how deep the tree is allowed to go"); ax.set_ylabel("typical error (minutes)")
    ax.legend(fontsize=8)
    save(fig, "fig_u5_tree_depth.pdf")
    print(f"   best depth {best}, held-out error {min(te):.2f}")


def fig_tree_diagram():
    """The tree itself, drawn, so the splits can be read out loud."""
    X = pd.get_dummies(gems[["carat", "cut", "color", "clarity"]], drop_first=True)
    t = DecisionTreeRegressor(max_depth=3, random_state=0).fit(X, gems.price)
    fig, ax = plt.subplots(figsize=(12, 5.2))
    plot_tree(t, feature_names=[c.replace("_", " ") for c in X.columns], filled=True,
              impurity=False, precision=0, fontsize=8, ax=ax,
              label="root", proportion=False)
    save(fig, "fig_u5_tree_diagram.pdf")


def fig_carat_spike():
    """Cutters lose weight to reach 1.00, so the data has a hole just below it."""
    fig, ax = plt.subplots(figsize=(7.6, 3.2))
    d = gems[(gems.carat > 0.7) & (gems.carat < 1.4)]
    ax.hist(d.carat, bins=70, color=BLUE, alpha=0.75)
    ax.axvline(1.0, color=RED, lw=1.8)
    just_under = ((gems.carat >= 0.95) & (gems.carat < 0.995)).sum()
    at_one = ((gems.carat >= 1.0) & (gems.carat <= 1.01)).sum()
    ax.annotate(f"{at_one} stones at 1.00", (1.02, ax.get_ylim()[1] * 0.85), color=RED, fontsize=9)
    ax.annotate(f"only {just_under} just below", (0.80, ax.get_ylim()[1] * 0.6), color=GREY,
                fontsize=9)
    ax.set_xlabel("carat"); ax.set_ylabel("stones in the sample")
    save(fig, "fig_u5_carat_spike.pdf")


def fig_interaction_found():
    """What the tree noticed: slope only matters once the lot is big."""
    d = jobs.copy()
    d["size_band"] = pd.cut(d.lot_sqft, [0, 6000, 12000, 25000, 1e9],
                            labels=["small", "medium", "large", "very large"])
    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    for slope, color, mark in [("flat", BLUE, "o"), ("moderate", GREY, "s"),
                               ("steep", RED, "^")]:
        g = d[d.slope == slope].groupby("size_band", observed=True).minutes.mean()
        ax.plot(range(len(g)), g.values, mark + "-", color=color, lw=2, label=slope)
    ax.set_xticks(range(4))
    ax.set_xticklabels(["small", "medium", "large", "very large"])
    ax.set_xlabel("lot size"); ax.set_ylabel("average minutes")
    ax.legend(title="slope", fontsize=8.5, title_fontsize=8.5)
    save(fig, "fig_u5_interaction.pdf")


if __name__ == "__main__":
    fig_diagnostics()
    fig_carat_spike()
    fig_fan()
    fig_poly()
    fig_one_split()
    fig_tree_steps()
    fig_tree_depth()
    fig_tree_diagram()
    fig_interaction_found()
