#!/usr/bin/env python3
"""Make lawn_jobs.csv, the dataset Unit 5 runs on.

It is built to break a straight line in the specific ways the unit teaches:

  * time scales multiplicatively with lot size, so residuals from a plain
    linear fit fan out and the log scale fixes them,
  * slope matters far more on big lots than small ones, which is an
    interaction a tree finds on its own,
  * there is a threshold at the gate: gated properties cost a fixed extra
    stretch of time regardless of size, which a line smooths over and a tree
    catches in one split.

Run:  python tools/make_lawn_data.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "data" / "lawn_jobs.csv"


def main(n: int = 700, seed: int = 55) -> None:
    rng = np.random.default_rng(seed)

    lot_sqft = np.exp(rng.normal(np.log(7000), 0.55, n)).clip(1200, 60000).round(0)
    slope = rng.choice(["flat", "moderate", "steep"], n, p=[0.5, 0.33, 0.17])
    steep = (slope == "steep").astype(int)
    moderate = (slope == "moderate").astype(int)
    obstacles = rng.poisson(3.0, n).clip(0, 14)          # trees, beds, play sets
    gated = rng.binomial(1, 0.22, n)
    crew_size = rng.choice([1, 2, 3], n, p=[0.35, 0.45, 0.20])

    # recorded, and unrelated to how long a job takes
    invoice_id = rng.integers(10000, 99999, n)
    customer_rating = rng.integers(1, 6, n)

    big = (lot_sqft > 12000).astype(int)

    log_minutes = (np.log(14)
                   + 0.52 * np.log(lot_sqft / 7000)       # multiplicative in size
                   + 0.10 * moderate
                   + 0.12 * steep
                   + 0.34 * steep * big                   # slope bites on big lots
                   + 0.022 * obstacles
                   + 0.26 * gated                          # a fixed toll at the gate
                   - 0.18 * (crew_size - 1)
                   + rng.normal(0, 0.21, n))
    minutes = np.exp(log_minutes)

    df = pd.DataFrame({
        "minutes": minutes.clip(4, None).round(1),
        "lot_sqft": lot_sqft.astype(int),
        "slope": slope,
        "obstacles": obstacles,
        "gated": gated,
        "crew_size": crew_size,
        "invoice_id": invoice_id,
        "customer_rating": customer_rating,
    })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"wrote data/{OUT.name}  ({len(df)} jobs, {df.shape[1]} columns)")
    print(df.head().to_string(index=False))
    print(f"\nminutes: median {df.minutes.median():.0f}, max {df.minutes.max():.0f}, "
          f"skew {df.minutes.skew():.2f}")


if __name__ == "__main__":
    main()
