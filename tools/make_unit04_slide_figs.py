#!/usr/bin/env python3
"""Figures for Unit 4 (prediction, over/underfitting, choosing predictors).

All of them use data/moving_jobs.csv, the made-up moving-company jobs.

Run:  python tools/make_unit04_slide_figs.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

ROOT = Path(__file__).resolve().parent.parent
SLIDES = ROOT / "Slides"
BLUE, RED, GREY, GREEN = "#4878a8", "#c0392b", "#7f8c8d", "#2e7d5b"
jobs = pd.read_csv(ROOT / "data" / "moving_jobs.csv")


def save(fig, name):
    fig.tight_layout()
    fig.savefig(SLIDES / name, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote Slides/{name}")


def fig_intervals():
    """One band for the line, a wider band for a single new job."""
    d = jobs.sample(150, random_state=1).sort_values("volume_cuft")
    x, y = d.volume_cuft.values, d.hours.values
    X = np.column_stack([x])
    fit = LinearRegression().fit(X, y)
    grid = np.linspace(x.min(), x.max(), 100)
    pred = fit.predict(grid.reshape(-1, 1))

    resid_sd = (y - fit.predict(X)).std(ddof=2)
    n = len(x)
    se_mean = resid_sd * np.sqrt(1/n + (grid - x.mean())**2 / ((x - x.mean())**2).sum())
    se_new = np.sqrt(resid_sd**2 + se_mean**2)

    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.scatter(x, y, s=12, color=GREY, alpha=0.55, label="completed jobs")
    ax.fill_between(grid, pred - 2*se_new, pred + 2*se_new, color=BLUE, alpha=0.16,
                    label="where one new job lands")
    ax.fill_between(grid, pred - 2*se_mean, pred + 2*se_mean, color=RED, alpha=0.40,
                    label="where the line itself sits")
    ax.plot(grid, pred, color=RED, lw=2)
    ax.set_xlabel("volume (cubic feet)"); ax.set_ylabel("hours on site")
    ax.legend(fontsize=8, loc="upper left")
    save(fig, "fig_u4_intervals.pdf")


def fig_flex():
    """Too simple, about right, too flexible, on the same 40 jobs."""
    d = jobs.sample(40, random_state=7).sort_values("volume_cuft")
    x, y = d.volume_cuft.values, d.hours.values
    grid = np.linspace(x.min(), x.max(), 300)

    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.1), sharey=True)
    for ax, deg, label in zip(axes, [1, 2, 14],
                              ["too simple", "about right", "too flexible"]):
        model = make_pipeline(PolynomialFeatures(deg), LinearRegression())
        model.fit(x.reshape(-1, 1), y)
        ax.scatter(x, y, s=16, color=GREY, alpha=0.7)
        ax.plot(grid, model.predict(grid.reshape(-1, 1)), color=RED, lw=2)
        ax.set_title(f"{label}\n(polynomial degree {deg})", fontsize=9)
        ax.set_xlabel("volume (cubic feet)")
        ax.set_ylim(y.min() - 2, y.max() + 2)
    axes[0].set_ylabel("hours")
    save(fig, "fig_u4_flex.pdf")


def fig_curve():
    """Training error keeps falling, held-out error turns back up."""
    d = jobs.sample(60, random_state=3)
    x, y = d.volume_cuft.values.reshape(-1, 1), d.hours.values
    x = (x - x.mean()) / x.std()      # so a high-degree polynomial stays numerically sane

    degs = range(1, 11)
    tr, te = [], []
    for deg in degs:
        a_tr, a_te = [], []
        for split in range(40):       # average over splits, so the shape is not one lucky draw
            xtr, xte, ytr, yte = train_test_split(x, y, test_size=0.4, random_state=split)
            m = make_pipeline(PolynomialFeatures(deg), LinearRegression()).fit(xtr, ytr)
            a_tr.append(np.sqrt(((ytr - m.predict(xtr))**2).mean()))
            a_te.append(np.sqrt(((yte - m.predict(xte))**2).mean()))
        tr.append(np.mean(a_tr)); te.append(np.mean(a_te))

    fig, ax = plt.subplots(figsize=(7.2, 3.5))
    ax.plot(list(degs), tr, "o-", color=BLUE, lw=2, label="error on the rows it was fitted on")
    ax.plot(list(degs), te, "s-", color=RED, lw=2, label="error on rows held back")
    ax.axvline(int(np.argmin(te)) + 1, color=GREEN, ls="--", lw=1.5,
               label="best held-out error")
    ax.set_xlabel("model complexity (polynomial degree)")
    ax.set_ylabel("typical error (hours)")
    ax.set_ylim(0, 3.2 * min(te))     # the red curve runs off the top, which is the point
    ax.legend(fontsize=8)
    save(fig, "fig_u4_curve.pdf")


def fig_cv():
    """Five folds, each one taking a turn as the held-out piece."""
    fig, ax = plt.subplots(figsize=(7.6, 2.8))
    k = 5
    for row in range(k):
        for col in range(k):
            held = row == col
            ax.add_patch(plt.Rectangle((col, k - row - 1), 0.94, 0.86,
                                       color=RED if held else BLUE,
                                       alpha=0.85 if held else 0.30))
        ax.text(k + 0.15, k - row - 0.6, f"round {row + 1}", fontsize=9, va="center")
    ax.set_xlim(0, k + 1.5); ax.set_ylim(0, k)
    ax.set_xticks([c + 0.47 for c in range(k)])
    ax.set_xticklabels([f"fifth {c+1}" for c in range(k)], fontsize=8)
    ax.set_yticks([]); ax.set_frame_on(False)
    ax.set_title("each fifth is held out once (red), and used for fitting the other four times",
                 fontsize=9)
    save(fig, "fig_u4_cv.pdf")


def fig_sets():
    """Candidate predictor sets, scored by cross-validated error."""
    sets = [
        ("volume", ["volume_cuft"]),
        ("volume + crew", ["volume_cuft", "crew_size"]),
        ("+ stairs, miles, packing", ["volume_cuft", "crew_size", "stairs_flights",
                                      "miles", "packing_service"]),
        ("+ boxes, rating, weekend", ["volume_cuft", "crew_size", "stairs_flights",
                                      "miles", "packing_service", "est_boxes",
                                      "dispatcher_rating", "weekend"]),
    ]
    folds = KFold(5, shuffle=True, random_state=0)
    rmse = []
    for _, cols in sets:
        mse = -cross_val_score(LinearRegression(), jobs[cols], jobs.hours, cv=folds,
                               scoring="neg_mean_squared_error").mean()
        rmse.append(np.sqrt(mse))

    fig, ax = plt.subplots(figsize=(7.4, 3.2))
    ypos = np.arange(len(sets))[::-1]
    ax.barh(ypos, rmse, color=BLUE, alpha=0.8, height=0.6)
    for yy, r in zip(ypos, rmse):
        ax.text(r + 0.01, yy, f"{r:.3f}", va="center", fontsize=9)
    ax.set_yticks(ypos); ax.set_yticklabels([s[0] for s in sets], fontsize=9)
    ax.set_xlabel("cross-validated error (hours)")
    ax.set_xlim(0, max(rmse) * 1.18)
    save(fig, "fig_u4_sets.pdf")


def fig_extrap():
    """A line fitted on ordinary jobs, pushed out to a job twice the size."""
    d = jobs[jobs.volume_cuft.between(300, 900)]
    fit = LinearRegression().fit(d[["volume_cuft"]], d.hours)
    grid = np.linspace(300, 1700, 200)

    fig, ax = plt.subplots(figsize=(7.2, 3.5))
    ax.scatter(d.volume_cuft, d.hours, s=10, color=GREY, alpha=0.5,
               label="jobs the model was fitted on")
    far = jobs[jobs.volume_cuft > 1100]
    ax.scatter(far.volume_cuft, far.hours, s=18, color=GREEN, alpha=0.8,
               label="jobs that big, later")
    ax.plot(grid, fit.predict(grid.reshape(-1, 1)), color=RED, lw=2, label="the fitted line")
    ax.axvspan(900, 1700, color=RED, alpha=0.06)
    ax.text(1290, d.hours.min() + 0.5, "outside the data", fontsize=9, color=RED, ha="center")
    ax.set_xlabel("volume (cubic feet)"); ax.set_ylabel("hours")
    ax.legend(fontsize=8, loc="upper left")
    save(fig, "fig_u4_extrap.pdf")


if __name__ == "__main__":
    fig_intervals()
    fig_flex()
    fig_curve()
    fig_cv()
    fig_sets()
    fig_extrap()
