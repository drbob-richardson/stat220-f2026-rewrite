#!/usr/bin/env python3
"""Make delivery_routes.csv: a made-up dataset of completed delivery routes.

One row per route driven. The outcome is `minutes`, how long the route took.
The truth behind it uses stops, packages, miles, and whether the route is
downtown, with a mild bend in stops. Stops and packages travel together, which
is what makes a combination like "few stops, many packages" absent from the
data although each value on its own is ordinary. Several columns are recorded
and have nothing to do with the time a route takes.

Used by the Unit 4 homework. The slides and code companion use the moving
company data instead, so the homework is not a copy of the worked example.

Run:  python tools/make_delivery_data.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "data" / "delivery_routes.csv"


def main(n: int = 500, seed: int = 12) -> None:
    rng = np.random.default_rng(seed)

    stops = rng.integers(8, 75, n)
    # packages ride along with stops, about two and a half per stop
    packages = (stops * rng.normal(2.5, 0.45, n) + rng.normal(0, 3, n)).clip(5, None).round(0)
    miles = (stops * rng.normal(0.9, 0.25, n) + rng.normal(12, 6, n)).clip(3, None).round(1)
    downtown = rng.binomial(1, 0.35, n)
    rain = rng.binomial(1, 0.22, n)

    # recorded, and unrelated to how long a route takes
    van_age_years = rng.integers(1, 9, n)
    dispatcher_rating = rng.integers(1, 6, n)
    month = rng.integers(1, 13, n)

    minutes = (22
               + 3.1 * stops
               + 0.0075 * (stops - 40) ** 2      # a gentle bend
               + 0.55 * packages
               + 1.15 * miles
               + 11.0 * downtown
               + 7.5 * rain
               + rng.normal(0, 22, n))
    minutes = minutes.clip(15, None).round(1)

    df = pd.DataFrame({
        "minutes": minutes,
        "stops": stops,
        "packages": packages.astype(int),
        "miles": miles,
        "downtown": downtown,
        "rain": rain,
        "van_age_years": van_age_years,
        "dispatcher_rating": dispatcher_rating,
        "month": month,
    })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"wrote {OUT}  ({len(df)} routes, {df.shape[1]} columns)")
    print(df.head().to_string(index=False))
    print(f"\ncorr(stops, packages) = {df.stops.corr(df.packages):.2f}")


if __name__ == "__main__":
    main()
