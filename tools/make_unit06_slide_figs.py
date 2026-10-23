#!/usr/bin/env python3
"""Figures for Unit 6 (inference without a formula).

Runs on data/rent.csv, the Indian rental listings the Unit 5 homework used, so
students meet familiar data asking an unfamiliar question. One column is added
here and nowhere else: id_number, pure noise with many distinct values, which
is what exposes the bias in impurity importance.

Run:  python tools/make_unit06_slide_figs.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent.parent
SLIDES = ROOT / "Slides"
BLUE, RED, GREY, GREEN = "#4878a8", "#c0392b", "#7f8c8d", "#2e7d5b"
COLS = ["Size", "BHK", "Bathroom", "City", "FurnishingStatus", "id_number"]
NICE = {"City_Mumbai": "city is Mumbai", "FurnishingStatus_Unfurnished": "unfurnished",
        "FurnishingStatus_Semi-Furnished": "semi-furnished", "City_Delhi": "city is Delhi",
        "City_Kolkata": "city is Kolkata", "City_Chennai": "city is Chennai",
        "City_Hyderabad": "city is Hyderabad", "id_number": "id_number (random)",
        "Size": "size", "BHK": "bedrooms", "Bathroom": "bathrooms"}


def load():
    rng = np.random.default_rng(6)
    d = pd.read_csv(ROOT / "data" / "rent.csv")
    d = d[(d.Rent > 0) & (d.Size > 0)].copy()
    d["id_number"] = rng.integers(100000, 999999, len(d))
    return d


def save(fig, name):
    fig.tight_layout()
    fig.savefig(SLIDES / name, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote Slides/{name}")


def fig_two_importances():
    """The same forest, two importance methods, two different answers."""
    d = load()
    X = pd.get_dummies(d[COLS], drop_first=True)
    y = np.log(d.Rent)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
    f = RandomForestRegressor(n_estimators=300, random_state=0, n_jobs=-1).fit(Xtr, ytr)
    imp = pd.Series(f.feature_importances_, index=X.columns)
    perm = pd.Series(permutation_importance(f, Xte, yte, n_repeats=10, random_state=0,
                                            n_jobs=-1).importances_mean, index=X.columns)

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 3.9))
    for ax, s, title in [(axes[0], imp, "impurity importance, the default"),
                         (axes[1], perm, "permutation importance")]:
        s = s.sort_values().tail(7)
        colors = [RED if i == "id_number" else BLUE for i in s.index]
        ax.barh([NICE.get(i, i) for i in s.index], s.values, color=colors)
        ax.set_title(title, fontsize=11)
        ax.tick_params(labelsize=9)
    axes[0].set_xlabel("share of the splitting it accounts for", fontsize=9)
    axes[1].set_xlabel("how much worse the forest predicts when the column is shuffled",
                       fontsize=9)
    save(fig, "fig_u6_two_importances.pdf")
    print(f"   id_number: impurity rank {list(imp.sort_values(ascending=False).index).index('id_number')+1}"
          f" of {len(imp)}, permutation rank "
          f"{list(perm.sort_values(ascending=False).index).index('id_number')+1}")


def fig_bootstrap():
    """600 resamples of an elasticity, against the interval the formula gives."""
    d = load()
    RHS = "BHK + Bathroom + C(City) + C(FurnishingStatus)"
    m = smf.ols(f"np.log(Rent) ~ np.log(Size) + {RHS}", data=d).fit()
    lo_f, hi_f = m.conf_int().loc["np.log(Size)"]
    rng = np.random.default_rng(1)
    boot = []
    for _ in range(600):
        s = d.iloc[rng.integers(0, len(d), len(d))]
        boot.append(smf.ols(f"np.log(Rent) ~ np.log(Size) + {RHS}", data=s)
                    .fit().params["np.log(Size)"])
    lo_b, hi_b = np.percentile(boot, [2.5, 97.5])

    fig, ax = plt.subplots(figsize=(7.6, 3.5))
    ax.hist(boot, bins=38, color=BLUE, alpha=0.8)
    top = ax.get_ylim()[1]
    ax.axvline(lo_b, color=RED, lw=2); ax.axvline(hi_b, color=RED, lw=2)
    ax.hlines(top * 0.88, lo_f, hi_f, color=GREEN, lw=3.5)
    ax.annotate("the interval the formula gives", (lo_f, top * 0.93), color=GREEN, fontsize=9.5)
    ax.annotate("middle 95% of the resamples", (lo_b, top * 0.60), color=RED, fontsize=9.5)
    ax.set_xlabel("elasticity of rent with respect to size, one value per resample", fontsize=10)
    ax.set_ylabel("resamples", fontsize=10)
    save(fig, "fig_u6_bootstrap.pdf")
    print(f"   formula [{lo_f:.4f}, {hi_f:.4f}]   bootstrap [{lo_b:.4f}, {hi_b:.4f}]")


def fig_importance_ci():
    """Importance with a bootstrap interval, so a score can be compared with zero."""
    d = load()
    X = pd.get_dummies(d[COLS], drop_first=True)
    y = np.log(d.Rent)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)

    def imp(Xf, yf, seed):
        f = RandomForestRegressor(n_estimators=60, random_state=0, n_jobs=-1).fit(Xf, yf)
        return pd.Series(permutation_importance(f, Xte, yte, n_repeats=5, random_state=seed,
                                                n_jobs=-1).importances_mean, index=X.columns)

    base = imp(Xtr, ytr, 0)
    rng = np.random.default_rng(6)
    # only the training rows are resampled. Resampling before the split would put
    # the same row on both sides, and the forest would score every column, noise
    # included, as important.
    reps = pd.DataFrame([imp(Xtr.iloc[i], ytr.iloc[i], k)
                         for k, i in enumerate(rng.integers(0, len(Xtr), (40, len(Xtr))))])

    show = ["City_Mumbai", "Size", "Bathroom", "BHK", "id_number"]
    fig, ax = plt.subplots(figsize=(7.6, 3.2))
    ys = np.arange(len(show))[::-1]
    for yy, c in zip(ys, show):
        lo, hi = np.percentile(reps[c], [2.5, 97.5])
        col = RED if lo <= 0 <= hi else BLUE
        ax.hlines(yy, lo, hi, color=col, lw=3)
        ax.plot(base[c], yy, "o", color=col, ms=7)
    ax.axvline(0, color=GREY, ls="--", lw=1.3)
    ax.set_yticks(ys); ax.set_yticklabels([NICE.get(c, c) for c in show], fontsize=10)
    ax.set_xlabel("permutation importance, with a 95% bootstrap interval", fontsize=10)
    ax.tick_params(axis="x", labelsize=9)
    save(fig, "fig_u6_importance_ci.pdf")
    for c in show:
        lo, hi = np.percentile(reps[c], [2.5, 97.5])
        print(f"   {c:<14} {base[c]:+.4f}  [{lo:+.4f}, {hi:+.4f}]")


if __name__ == "__main__":
    fig_two_importances()
    fig_bootstrap()
    fig_importance_ci()
