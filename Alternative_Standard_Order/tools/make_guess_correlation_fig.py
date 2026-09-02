#!/usr/bin/env python3
"""Four scatterplots (A-D) for the Module 2 'guess the correlation' contest."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "Slides"
rng = np.random.default_rng(7)
targets = {"A": 0.30, "B": 0.95, "C": -0.60, "D": 0.05}

fig, axes = plt.subplots(2, 2, figsize=(8, 6.2))
for ax, (label, r) in zip(axes.ravel(), targets.items()):
    x = rng.normal(0, 1, 90)
    y = r * x + np.sqrt(max(1e-6, 1 - r**2)) * rng.normal(0, 1, 90)
    actual = np.corrcoef(x, y)[0, 1]
    ax.scatter(x, y, color="#34607d", alpha=0.8, s=22)
    ax.set_title(label, fontsize=15, fontweight="bold")
    ax.set_xticks([]); ax.set_yticks([])
    print(f"{label}: target r={r:+.2f}, actual r={actual:+.2f}")
plt.tight_layout()
plt.savefig(OUT / "fig_guess_correlation.pdf"); plt.close()
print("wrote", OUT / "fig_guess_correlation.pdf")
