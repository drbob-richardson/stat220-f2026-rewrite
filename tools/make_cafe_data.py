#!/usr/bin/env python3
"""Build campus_cafe.csv, a made-up dataset for the Unit 2 homework.

One story that carries all three outcome types, so students can practise picking
a model by the type of y without meeting three unrelated datasets:

    revenue      a number    -> linear regression
    drinks_sold  a count     -> Poisson regression
    sold_out     yes or no   -> logistic regression

Deliberately not one of the datasets used in the code companion.
"""
from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(2026)
n = 700

day_of_week = rng.integers(0, 5, n)                       # 0=Mon .. 4=Fri
temp_f = np.clip(rng.normal(58, 16, n), 10, 100).round(1)
exam_week = rng.binomial(1, 0.18, n)
promo = rng.binomial(1, 0.25, n)
foot_traffic = np.clip(rng.normal(900, 220, n)
                       + 120 * exam_week
                       - 25 * (day_of_week == 4), 200, None).round(0)

# counts: cold days, exam weeks and promotions all push drinks up
log_rate = (3.05
            - 0.011 * (temp_f - 58)
            + 0.22 * exam_week
            + 0.15 * promo
            + 0.00042 * (foot_traffic - 900))
drinks_sold = rng.poisson(np.exp(log_rate))

# a number: revenue follows the drinks, with a bigger basket during exams
price = 4.15 + 0.35 * exam_week
revenue = (drinks_sold * price + rng.normal(0, 12, n)).round(2)

# yes or no: running out is driven by how many they sold
p_out = 1 / (1 + np.exp(-(-4.40 + 0.145 * drinks_sold + 0.45 * promo)))
sold_out = rng.binomial(1, p_out)

cafe = pd.DataFrame({
    "day_of_week": pd.Categorical.from_codes(day_of_week, ["Mon","Tue","Wed","Thu","Fri"]),
    "temp_f": temp_f,
    "exam_week": exam_week,
    "promo": promo,
    "foot_traffic": foot_traffic.astype(int),
    "drinks_sold": drinks_sold,
    "revenue": revenue,
    "sold_out": sold_out,
})
out = Path(__file__).resolve().parents[2] / "data" / "campus_cafe.csv"
out.parent.mkdir(parents=True, exist_ok=True)
cafe.to_csv(out, index=False)
print(f"wrote {out}  ({len(cafe)} rows)")
print(cafe.describe().round(2).to_string())
print("\nsold_out rate:", round(cafe.sold_out.mean(), 3))
