#!/usr/bin/env python3
"""Figures for the multiple-choice midterm. They land in Exams/, which is
gitignored, next to the .tex the builder compiles there.

Panels are numbered, never lettered, so a question can say "panel 3" without
colliding with the answer options (A)-(D).

Run:  python tools/make_mc_exam_figs.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

OUT = Path(__file__).resolve().parent.parent / "Exams"
GREY, RED, BLUE, GREEN = "#7f8c8d", "#c0392b", "#4878a8", "#2e7d5b"


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote Exams/{name}")


def fig_resid_four():
    """The four diagnoses, numbered, in a scrambled order so it is not Unit 5's."""
    rng = np.random.default_rng(11)
    x = rng.uniform(0, 10, 240)
    panels = [
        ("1", 0.42 * (x - 5) ** 2 - 3.4 + rng.normal(0, 1, 240)),     # curve
        ("2", rng.normal(0, 1, 240)),                                  # nothing wrong
        ("3", rng.normal(0, 0.25 + 0.40 * x)),                         # fan
        ("4", rng.normal(0, 1, 240)),                                  # one point
    ]
    panels[3][1][19] = 12.0
    fig, axes = plt.subplots(1, 4, figsize=(11.4, 3.7), sharex=True)
    for i, (ax, (lab, r)) in enumerate(zip(axes, panels)):
        ax.scatter(x, r, s=13, color=GREY, alpha=0.75)
        ax.axhline(0, color=RED, lw=1.5)
        ax.set_title(f"panel {lab}", fontsize=13)
        ax.set_xlabel("fitted value", fontsize=10)
        ax.tick_params(labelsize=9)
        ax.set_yticks([])
        if i == 3:
            # the lone far-out point has to survive being printed small
            j = int(np.argmax(r))
            ax.scatter([x[j]], [r[j]], s=46, color=RED, zorder=5)
    axes[0].set_ylabel("residual", fontsize=10)
    save(fig, "fig_mc_resid_four.pdf")


def fig_fan_fix():
    """The same model before and after logging the outcome."""
    rng = np.random.default_rng(4)
    x = rng.uniform(1, 10, 320)
    y = np.exp(0.9 + 0.22 * x + rng.normal(0, 0.33, 320))
    d = pd.DataFrame({"x": x, "y": y})
    a = smf.ols("y ~ x", data=d).fit()
    b = smf.ols("np.log(y) ~ x", data=d).fit()
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.2))
    for ax, f, t, yl in [(axes[0], a, "left: y on x", "residual"),
                         (axes[1], b, "right: log(y) on x", "residual (log scale)")]:
        ax.scatter(f.fittedvalues, f.resid, s=11, color=GREY, alpha=0.65)
        ax.axhline(0, color=RED, lw=1.4)
        ax.set_title(t, fontsize=10); ax.set_xlabel("fitted value"); ax.set_ylabel(yl)
    save(fig, "fig_mc_fan_fix.pdf")


def fig_depth():
    """Train error falls forever, held-out error turns."""
    rng = np.random.default_rng(7)
    n = 500
    X = pd.DataFrame({"a": rng.uniform(0, 10, n), "b": rng.uniform(0, 5, n),
                      "c": rng.normal(0, 1, n)})
    y = 3 * X.a + 2 * np.sin(X.b) + rng.normal(0, 3.2, n)
    depths, tr, te = range(1, 15), [], []
    for d in depths:
        A, B = [], []
        for s in range(20):
            Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=s)
            t = DecisionTreeRegressor(max_depth=d, random_state=0).fit(Xtr, ytr)
            A.append(np.sqrt(((ytr - t.predict(Xtr)) ** 2).mean()))
            B.append(np.sqrt(((yte - t.predict(Xte)) ** 2).mean()))
        tr.append(np.mean(A)); te.append(np.mean(B))
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    ax.plot(list(depths), tr, "o-", color=BLUE, lw=2, label="error on the rows it was fitted on")
    ax.plot(list(depths), te, "s-", color=RED, lw=2, label="error on rows held back")
    ax.set_xlabel("depth the tree is allowed to reach"); ax.set_ylabel("typical error")
    ax.legend(fontsize=8)
    save(fig, "fig_mc_depth.pdf")
    print(f"   best held-out depth {int(np.argmin(te)) + 1}")


def fig_intervals():
    """A fitted line with both bands drawn and labelled."""
    rng = np.random.default_rng(2)
    x = rng.uniform(0, 10, 90)
    y = 4 + 1.8 * x + rng.normal(0, 3.4, 90)
    d = pd.DataFrame({"x": x, "y": y})
    f = smf.ols("y ~ x", data=d).fit()
    grid = pd.DataFrame({"x": np.linspace(0, 10, 120)})
    p = f.get_prediction(grid).summary_frame(alpha=0.05)
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    ax.scatter(x, y, s=14, color=GREY, alpha=0.7)
    ax.plot(grid.x, p["mean"], color=RED, lw=2)
    ax.fill_between(grid.x, p.obs_ci_lower, p.obs_ci_upper, color=BLUE, alpha=0.14,
                    label="band 1")
    ax.fill_between(grid.x, p.mean_ci_lower, p.mean_ci_upper, color=GREEN, alpha=0.45,
                    label="band 2")
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.legend(fontsize=9, loc="upper left")
    save(fig, "fig_mc_intervals.pdf")


def fig_tree_steps():
    """What a fitted tree's prediction looks like, and what it does past the edge."""
    rng = np.random.default_rng(5)
    x = rng.uniform(1, 8, 160)
    y = 5 + 2.2 * x + rng.normal(0, 2.2, 160)
    t = DecisionTreeRegressor(max_depth=3, random_state=0).fit(x.reshape(-1, 1), y)
    grid = np.linspace(1, 13, 500).reshape(-1, 1)
    fig, ax = plt.subplots(figsize=(6.8, 3.3))
    ax.scatter(x, y, s=16, color=GREY, alpha=0.7)
    ax.plot(grid, t.predict(grid), color=RED, lw=2)
    ax.axvline(8, color=GREEN, ls="--", lw=1.4)
    ax.annotate("edge of the data", (8.15, y.min() + 1), color=GREEN, fontsize=9)
    ax.set_xlabel("x"); ax.set_ylabel("y")
    save(fig, "fig_mc_tree_steps.pdf")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    fig_resid_four(); fig_fan_fix(); fig_depth(); fig_intervals(); fig_tree_steps()
