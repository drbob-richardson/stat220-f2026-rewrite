#!/usr/bin/env python3
"""Make moving_jobs.csv: a made-up dataset of completed moving-company jobs.

One row per job. The outcome is `hours`, the crew's time on site. The truth
behind it uses volume, crew size, stairs, and distance, plus a mild bend in
volume so a straight line is not quite right. Several columns are recorded by
the company but have nothing to do with the time a job takes, which is what
makes this useful for a unit on choosing predictors.

Run:  python tools/make_moving_data.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "data" / "moving_jobs.csv"


def main(n: int = 600, seed: int = 4) -> None:
    rng = np.random.default_rng(seed)

    volume = rng.normal(700, 220, n).clip(120, 1600).round(0)      # cubic feet
    crew = rng.choice([2, 3, 4], n, p=[0.45, 0.4, 0.15])           # movers on the job
    miles = rng.gamma(2.0, 6.0, n).clip(1, 90).round(1)            # one-way distance
    stairs = rng.poisson(1.1, n).clip(0, 6)                        # flights of stairs
    packing = rng.binomial(1, 0.3, n)                              # packing service bought
    weekend = rng.binomial(1, 0.28, n)

    # Recorded, but unrelated to how long a job takes.
    quote_source = rng.choice(["phone", "web", "referral"], n)
    truck = rng.choice([f"T-{i}" for i in range(1, 8)], n)
    dispatcher_rating = rng.integers(1, 6, n)
    est_boxes = (volume / 12 + rng.normal(0, 8, n)).clip(4, None).round(0)

    hours = (1.1
             + 0.0125 * volume                 # the main driver
             + 0.0000045 * (volume - 700) ** 2  # a gentle bend
             - 0.55 * (crew - 2)                # a bigger crew finishes sooner
             + 0.30 * stairs
             + 0.012 * miles
             + 0.9 * packing
             + rng.normal(0, 0.8, n))
    hours = hours.clip(1.0, None).round(2)

    df = pd.DataFrame({
        "hours": hours,
        "volume_cuft": volume.astype(int),
        "crew_size": crew,
        "miles": miles,
        "stairs_flights": stairs,
        "packing_service": packing,
        "weekend": weekend,
        "est_boxes": est_boxes.astype(int),
        "dispatcher_rating": dispatcher_rating,
        "quote_source": quote_source,
        "truck_id": truck,
    })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"wrote {OUT}  ({len(df)} jobs, {df.shape[1]} columns)")
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    main()
