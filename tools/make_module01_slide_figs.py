#!/usr/bin/env python3
"""
Make the two 'stay-on during the activity' figures for the Module 1 slides, and print the
exact tail probabilities to embed on the slides.

  fig_binom10.pdf      -- P(get n right out of 10) if a taster is just guessing
  fig_binom_diff.pdf   -- P(two guessers' scores differ by d), the two-sample version
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

OUT = Path(__file__).resolve().parents[1] / "Slides"
OUT.mkdir(parents=True, exist_ok=True)

# ---------- one-sample: Binomial(10, 0.5) ----------
n = 10
k = np.arange(n + 1)
pmf = stats.binom.pmf(k, n, 0.5)

plt.figure(figsize=(7.5, 4.3))
bars = plt.bar(k, pmf, color=["#c0392b" if (kk <= 1 or kk >= 9) else "#34607d" for kk in k])
plt.xticks(k, fontsize=12); plt.yticks(fontsize=11)
plt.xlabel("number correct out of 10 (if just guessing)", fontsize=13)
plt.ylabel("probability", fontsize=13)
for kk, p in zip(k, pmf):
    plt.text(kk, p + 0.004, f"{p:.3f}", ha="center", va="bottom", fontsize=8)
plt.ylim(0, pmf.max() * 1.18)
plt.title("If they cannot tell Coke from Coke Zero", fontsize=14)
plt.tight_layout(); plt.savefig(OUT / "fig_binom10.pdf"); plt.close()

print("ONE-SAMPLE  P(exactly n right):")
for kk, p in zip(k, pmf):
    print(f"  n={kk:2d}: {p:.4f}")
print("ONE-SAMPLE  P(n or more right):")
for kk in [7, 8, 9, 10]:
    print(f"  >= {kk}: {stats.binom.sf(kk-1, n, 0.5):.4f}")

# ---------- two-sample: difference of two independent Binomial(10, 0.5) ----------
d = np.arange(-n, n + 1)
# P(D=d) = sum_a P(A=a) P(B=a-d)
pmf_diff = np.array([np.sum(pmf * stats.binom.pmf(np.arange(n + 1) - dd, n, 0.5))
                     for dd in d])

plt.figure(figsize=(7.5, 4.3))
plt.bar(d, pmf_diff,
        color=["#c0392b" if abs(dd) >= 5 else "#34607d" for dd in d])
plt.xticks(np.arange(-10, 11, 2), fontsize=12); plt.yticks(fontsize=11)
plt.xlabel("(taster A correct) - (taster B correct), if both guessing", fontsize=13)
plt.ylabel("probability", fontsize=13)
plt.title("How far apart two guessers land", fontsize=14)
plt.tight_layout(); plt.savefig(OUT / "fig_binom_diff.pdf"); plt.close()

print("\nTWO-SAMPLE  P(|difference| >= k):")
for kk in range(0, 9):
    p = np.sum(pmf_diff[np.abs(d) >= kk])
    print(f"  |diff| >= {kk}: {p:.4f}")

print(f"\nwrote {OUT/'fig_binom10.pdf'} and {OUT/'fig_binom_diff.pdf'}")
