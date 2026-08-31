#!/usr/bin/env python3
"""Pre-flip the reference coins for the Unit 2 activity.

Flips 50 coins, 120 times, and saves the sequences so the in-class detector
compares a student's invented sequence against a fixed, real reference set
rather than a fresh simulation each time.
"""
import json
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parents[1] / "Slides" / "unit02_reference_flips.json"
N_FLIPS, N_SEQUENCES, SEED = 50, 120, 20260817


def longest_run(seq: str) -> int:
    best = run = 1
    for i in range(1, len(seq)):
        run = run + 1 if seq[i] == seq[i - 1] else 1
        best = max(best, run)
    return best


def switch_rate(seq: str) -> float:
    """Share of adjacent pairs that alternate. Fair coins sit near 0.50."""
    return sum(seq[i] != seq[i - 1] for i in range(1, len(seq))) / (len(seq) - 1)


rng = np.random.default_rng(SEED)
seqs = ["".join("HT"[b] for b in rng.integers(0, 2, N_FLIPS)) for _ in range(N_SEQUENCES)]
runs = np.array([longest_run(s) for s in seqs])
switches = np.array([switch_rate(s) for s in seqs])

OUT.write_text(json.dumps({
    "n_flips": N_FLIPS, "n_sequences": N_SEQUENCES, "seed": SEED,
    "sequences": seqs,
    "longest_runs": runs.tolist(),
    "switch_rates": [round(v, 4) for v in switches],
}, indent=1))

print(f"{N_SEQUENCES} real sequences of {N_FLIPS} flips -> {OUT.name}")
print(f"longest run : mean {runs.mean():.2f}, median {np.median(runs):.0f}, "
      f"range {runs.min()} to {runs.max()}")
print(f"  P(run <= 4) = {(runs <= 4).mean():.3f}   <-- where most invented sequences land")
print(f"  P(run >= 6) = {(runs >= 6).mean():.3f}")
print(f"switch rate : mean {switches.mean():.3f}, "
      f"middle 90% {np.percentile(switches, 5):.3f} to {np.percentile(switches, 95):.3f}")
