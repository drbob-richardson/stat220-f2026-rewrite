#!/usr/bin/env python3
"""Made-up data for the two midterm applied parts.

Both sets are built so the exam's intended answers are actually true of them:

  * a two-group comparison that shrinks a lot once the obvious predictor is
    controlled for, so the naive gap is misleading,
  * one predictor that is nearly a copy of another, so a search drops it,
  * two or three columns with no relationship to the outcome at all,
  * a gentle bend in the main predictor, so residuals show a pattern,
  * enough spread that a prediction interval is much wider than a confidence
    interval.

Run:  python tools/make_exam_data.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "Exams" / "data"


def clinic(n: int = 900, seed: int = 21) -> pd.DataFrame:
    """Exam A: minutes a patient spends in an urgent care clinic."""
    rng = np.random.default_rng(seed)

    # The kiosk was rolled out part way through, and the clinic also got busier
    # after the rollout, so the raw kiosk-vs-not gap is tangled with volume.
    kiosk = (np.arange(n) > n * 0.45).astype(int)
    rng.shuffle(kiosk)
    patients_ahead = (rng.poisson(6 + 3 * kiosk, n)).clip(0, 25)
    waiting_room = (patients_ahead + rng.normal(0, 0.8, n)).round().clip(0, None)  # near-copy
    staff_on_shift = rng.choice([2, 3, 4], n, p=[0.3, 0.45, 0.25])
    severity = rng.choice(["minor", "moderate", "urgent"], n, p=[0.5, 0.35, 0.15])
    sev_add = pd.Series(severity).map({"minor": 0.0, "moderate": 9.0, "urgent": 22.0}).values

    # recorded, unrelated to how long a visit takes
    room_number = rng.integers(1, 13, n)
    front_desk_rating = rng.integers(1, 6, n)
    month = rng.integers(1, 13, n)

    minutes = (18
               + 4.2 * patients_ahead
               + 0.09 * (patients_ahead - 6) ** 2       # a gentle bend
               - 6.5 * (staff_on_shift - 2)
               + sev_add
               - 5.0 * kiosk                            # the real effect, modest
               + rng.normal(0, 11, n))
    return pd.DataFrame({
        "minutes": minutes.clip(5, None).round(1),
        "patients_ahead": patients_ahead,
        "waiting_room_count": waiting_room.astype(int),
        "staff_on_shift": staff_on_shift,
        "severity": severity,
        "kiosk": kiosk,
        "room_number": room_number,
        "front_desk_rating": front_desk_rating,
        "month": month,
    })


def repairs(n: int = 800, seed: int = 34) -> pd.DataFrame:
    """Exam B: days to finish a bicycle repair."""
    rng = np.random.default_rng(seed)

    new_supplier = (np.arange(n) > n * 0.5).astype(int)
    rng.shuffle(new_supplier)
    # the new supplier was brought in for the harder jobs, so the raw gap misleads
    parts_needed = rng.poisson(2.2 + 1.3 * new_supplier, n).clip(0, 12)
    parts_cost = (18 * parts_needed + rng.normal(0, 6, n)).clip(0, None)   # near-copy
    tech_years = rng.choice([1, 2, 5, 9], n, p=[0.3, 0.3, 0.25, 0.15])
    bike_type = rng.choice(["commuter", "road", "mountain", "electric"], n,
                           p=[0.4, 0.25, 0.2, 0.15])
    type_add = pd.Series(bike_type).map({"commuter": 0.0, "road": 0.6,
                                         "mountain": 0.9, "electric": 2.4}).values

    ticket_number = rng.integers(1000, 9999, n)
    shop_rating = rng.integers(1, 6, n)
    quarter = rng.integers(1, 5, n)

    days = (1.4
            + 0.75 * parts_needed
            + 0.035 * (parts_needed - 3) ** 2          # a gentle bend
            - 0.16 * tech_years
            + type_add
            - 0.9 * new_supplier                       # the real effect, modest
            + rng.normal(0, 1.5, n))
    return pd.DataFrame({
        "days": days.clip(0.3, None).round(2),
        "parts_needed": parts_needed,
        "parts_cost": parts_cost.round(2),
        "tech_years": tech_years,
        "bike_type": bike_type,
        "new_supplier": new_supplier,
        "ticket_number": ticket_number,
        "shop_rating": shop_rating,
        "quarter": quarter,
    })


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, df in [("clinic_visits.csv", clinic()), ("repair_jobs.csv", repairs())]:
        df.to_csv(OUT / name, index=False)
        print(f"wrote {OUT.name}/{name}  ({len(df)} rows, {df.shape[1]} columns)")


if __name__ == "__main__":
    main()
