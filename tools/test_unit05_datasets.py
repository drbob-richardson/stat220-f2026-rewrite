#!/usr/bin/env python3
"""Audition real datasets for Unit 5.

The unit needs one dataset to carry four demonstrations:

  1. residuals that fan out, so the log has something to fix
  2. a relationship that bends, so a transform or a squared term earns its place
  3. a threshold or a category effect a shallow tree can find and state plainly
  4. an interaction the tree finds that then improves the regression

This scores each candidate on all four and prints a scorecard, so the choice is
made on evidence rather than on which dataset is famous.

Run:  python tools/test_unit05_datasets.py
"""
import warnings

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score
from sklearn.tree import DecisionTreeRegressor, export_text

warnings.filterwarnings("ignore")
FOLDS = KFold(5, shuffle=True, random_state=0)


def load_candidates():
    out = {}
    d = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv")
    out["diamonds"] = (d.sample(5000, random_state=0), "price",
                       ["carat", "depth", "table"], ["cut", "color", "clarity"])

    a = pd.read_csv("https://richardson.byu.edu/220/airfoil.csv")
    num = [c for c in a.columns if c != a.columns[-1]]
    out["airfoil"] = (a, a.columns[-1], num[:5], [])

    r = pd.read_csv("https://richardson.byu.edu/220/rent.csv").dropna()
    out["rent"] = (r, "Rent", ["Size", "BHK", "Bathroom"], ["City", "FurnishingStatus"])

    from sklearn.datasets import fetch_california_housing
    ch = fetch_california_housing(as_frame=True).frame.sample(5000, random_state=0)
    out["california housing"] = (ch, "MedHouseVal",
                                 ["MedInc", "HouseAge", "AveRooms", "Population"], [])

    ab = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data",
                     header=None, names=["sex", "length", "diameter", "height", "whole_wt",
                                         "shucked_wt", "viscera_wt", "shell_wt", "rings"])
    out["abalone"] = (ab, "rings", ["length", "diameter", "height", "whole_wt"], ["sex"])
    return out


def fan_ratio(fit):
    """Residual spread at high fitted values, over the spread at low ones."""
    g = pd.DataFrame({"f": fit.fittedvalues, "r": fit.resid})
    lo = g[g.f < g.f.median()].r.std()
    hi = g[g.f >= g.f.median()].r.std()
    return hi / lo


def score(name, df, y, nums, cats):
    df = df.dropna(subset=[y] + nums + cats).copy()
    df = df[df[y] > 0]
    rhs = " + ".join(nums + [f"C({c})" for c in cats])
    plain = smf.ols(f"{y} ~ {rhs}", data=df).fit()
    logged = smf.ols(f"np.log({y}) ~ {rhs}", data=df).fit()

    main = nums[0]
    loglog = smf.ols(f"np.log({y}) ~ np.log({main}) + " +
                     " + ".join(nums[1:] + [f"C({c})" for c in cats]), data=df).fit()
    quad = smf.ols(f"{y} ~ {rhs} + I({main}**2)", data=df).fit()

    X = pd.get_dummies(df[nums + cats], drop_first=True)
    tree = DecisionTreeRegressor(max_depth=3, random_state=0).fit(X, df[y])
    rules = export_text(tree, feature_names=list(X.columns))
    used = {ln.split("<=")[0].split(">")[0].strip(" |-") for ln in rules.splitlines()
            if "<=" in ln or ">" in ln}
    used = {u for u in used if u in X.columns}

    # does a tree-suggested interaction help the logged model?
    best = None
    if len(used) >= 2:
        for a in list(used)[:4]:
            for b in list(used)[:4]:
                if a >= b:
                    continue
                try:
                    f = smf.ols(f"np.log({y}) ~ {rhs} + Q('{a}'):Q('{b}')",
                                data=df.join(X[[a, b]], rsuffix="_d")).fit()
                    gain = logged.aic - f.aic
                    if best is None or gain > best[1]:
                        best = (f"{a} x {b}", gain)
                except Exception:
                    continue

    print(f"\n=== {name}  ({len(df)} rows, outcome {y})")
    print(f"  fan in residuals            {fan_ratio(plain):.2f}  (1 = none, >1.3 is visible)")
    print(f"  fan after logging y         {fan_ratio(logged):.2f}")
    print(f"  R2: plain {plain.rsquared:.3f} -> log {logged.rsquared:.3f} -> log-log {loglog.rsquared:.3f}")
    print(f"  squared term on {main}: p = {quad.pvalues.get(f'I({main} ** 2)', float('nan')):.2g}")
    print(f"  tree splits on: {sorted(used)}")
    if best:
        print(f"  best tree-suggested interaction: {best[0]}, AIC gain {best[1]:.0f}")
    else:
        print("  no interaction candidate from the tree")


if __name__ == "__main__":
    for name, (df, y, nums, cats) in load_candidates().items():
        try:
            score(name, df, y, nums, cats)
        except Exception as e:
            print(f"\n=== {name}: could not score ({type(e).__name__}: {e})")
