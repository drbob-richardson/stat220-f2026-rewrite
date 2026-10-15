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
    for ax, f, t, yl in [(axes[0], a, "left: cost on job size", "residual (dollars)"),
                         (axes[1], b, "right: log(cost) on job size",
                          "residual (log scale)")]:
        ax.scatter(f.fittedvalues, f.resid, s=11, color=GREY, alpha=0.65)
        ax.axhline(0, color=RED, lw=1.4)
        ax.set_title(t, fontsize=11); ax.set_xlabel("fitted repair cost"); ax.set_ylabel(yl)
        ax.tick_params(labelsize=9)
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


def fig_yield_curve():
    """A scenario with a real bend: fertilizer and crop yield, 280 plots.

    Deliberately not the four-panel diagnostic grid from the Unit 5 slides.
    Left is the data with the straight line someone actually fitted; right is
    what that fit left behind.
    """
    rng = np.random.default_rng(21)
    kg = rng.uniform(20, 260, 280)
    yld = 1.9 + 0.055 * kg - 0.000145 * kg ** 2 + rng.normal(0, 0.42, 280)
    d = pd.DataFrame({"kg": kg, "yld": yld})
    f = smf.ols("yld ~ kg", data=d).fit()
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.8))
    g = np.linspace(20, 260, 200)
    axes[0].scatter(kg, yld, s=15, color=GREY, alpha=0.7)
    axes[0].plot(g, f.params["Intercept"] + f.params["kg"] * g, color=RED, lw=2.2)
    axes[0].set_xlabel("fertilizer applied (kg per hectare)", fontsize=10)
    axes[0].set_ylabel("yield (tonnes per hectare)", fontsize=10)
    axes[0].set_title("the data, with the line that was fitted", fontsize=11)
    axes[1].scatter(f.fittedvalues, f.resid, s=15, color=GREY, alpha=0.7)
    axes[1].axhline(0, color=RED, lw=1.6)
    axes[1].set_xlabel("fitted yield", fontsize=10)
    axes[1].set_ylabel("residual", fontsize=10)
    axes[1].set_title("what the line left behind", fontsize=11)
    for ax in axes:
        ax.tick_params(labelsize=9)
    save(fig, "fig_mc_yield_curve.pdf")
    print(f"   slope {f.params['kg']:.4f}, R2 {f.rsquared:.3f}; "
          f"turning point near {-0.055 / (2 * -0.000145):.0f} kg")


def fig_coefplot():
    """Five coefficients with 95% intervals, two of them straddling zero.

    A picture the course has not shown, so it tests reading intervals rather
    than recognising a slide.
    """
    names = ["floor area (per 100 sq ft)", "staff on duty", "parking spaces",
             "competitor within 1 mile", "loyalty members (per 100)"]
    est = np.array([2.80, 1.95, 0.12, -3.40, 0.46])
    se = np.array([0.42, 0.55, 0.38, 1.05, 0.51])
    lo, hi = est - 1.96 * se, est + 1.96 * se
    y = np.arange(len(names))[::-1]
    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    ax.axvline(0, color=GREY, ls="--", lw=1.3)
    ax.hlines(y, lo, hi, color=BLUE, lw=2.4)
    ax.plot(est, y, "o", color=RED, ms=7)
    ax.set_yticks(y); ax.set_yticklabels(names, fontsize=10)
    ax.set_xlabel(r"estimated change in monthly revenue (\$000) per unit, with 95% interval",
                  fontsize=10)
    ax.tick_params(axis="x", labelsize=9)
    save(fig, "fig_mc_coefplot.pdf")
    for n, e, l, h in zip(names, est, lo, hi):
        print(f"   {n:<30} {e:+.2f}  [{l:+.2f}, {h:+.2f}]")


def fig_threshold():
    """A pile of recorded times just under a 30 minute service promise.

    Same idea as the carat spike in Unit 5, in a setting the course has not
    used, so it tests the idea rather than recall of the picture.
    """
    rng = np.random.default_rng(31)
    base = rng.gamma(9.0, 3.1, 2600)
    # drivers round down anything close to the promise
    # most drivers close to the promise round down, but not all of them
    near = np.where((base > 30) & (base < 35))[0]
    moved = rng.choice(near, int(0.72 * len(near)), replace=False)
    base[moved] = rng.uniform(27.0, 29.9, len(moved))
    fig, ax = plt.subplots(figsize=(7.4, 3.3))
    ax.hist(base[base < 60], bins=80, color=BLUE, alpha=0.8)
    ax.axvline(30, color=RED, lw=2)
    ax.annotate("the 30 minute promise", (30.8, ax.get_ylim()[1] * 0.82), color=RED, fontsize=10)
    ax.set_xlabel("delivery time as recorded by the driver (minutes)", fontsize=10)
    ax.set_ylabel("deliveries", fontsize=10)
    ax.tick_params(labelsize=9)
    save(fig, "fig_mc_threshold.pdf")
    print(f"   recorded in 27.5-30: {((base >= 27.5) & (base < 30)).sum()}, "
          f"in 30-32.5: {((base >= 30) & (base < 32.5)).sum()}")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    fig_fan_fix(); fig_intervals(); fig_tree_steps()
    fig_yield_curve(); fig_coefplot(); fig_threshold()
