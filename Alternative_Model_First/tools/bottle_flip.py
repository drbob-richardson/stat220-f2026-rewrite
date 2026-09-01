#!/usr/bin/env python3
"""Score the bottle-flip demo live, in class.

Ten volunteers flip ten times. You write round 1 on the board, coach the
bottom three, then everyone flips ten more times. This takes the two rounds
and produces the comparison, the tests, and the plot.

    python tools/bottle_flip.py --r1 3 1 0 5 2 4 1 2 6 3 \
                                --r2 2 3 1 4 2 2 3 1 4 4

Optional:
    --k 3                how many at each end were selected (default 3)
    --names Ann Bob ...  labels for the board
    --no-plot            numbers only

It deliberately does not tell you whether the pep talk "worked". It reports
what the coached group did, what the untouched top group did, and lets the
room argue.
"""
from __future__ import annotations

import argparse

import numpy as np


def paired(before, after):
    """Paired t-test on the change scores. Returns (mean change, t, p)."""
    from scipy import stats
    d = np.asarray(after, float) - np.asarray(before, float)
    if len(d) < 2 or d.std(ddof=1) == 0:
        return d.mean(), float("nan"), float("nan")
    res = stats.ttest_rel(np.asarray(after, float), np.asarray(before, float))
    return d.mean(), res.statistic, res.pvalue


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--r1", type=int, nargs="+", required=True, help="round 1 counts")
    ap.add_argument("--r2", type=int, nargs="+", required=True, help="round 2 counts")
    ap.add_argument("--k", type=int, default=3, help="group size at each end (default 3)")
    ap.add_argument("--names", nargs="*", default=None)
    ap.add_argument("--no-plot", action="store_true")
    a = ap.parse_args()

    r1, r2 = np.array(a.r1), np.array(a.r2)
    if len(r1) != len(r2):
        raise SystemExit(f"round 1 has {len(r1)} scores, round 2 has {len(r2)}")
    n, k = len(r1), a.k
    if 2 * k > n:
        raise SystemExit(f"{n} flippers cannot give two disjoint groups of {k}")
    names = a.names if a.names and len(a.names) == n else [f"#{i+1}" for i in range(n)]

    order = np.argsort(r1, kind="stable")
    bot, top = order[:k], order[-k:]
    mid = order[k:n - k]
    label = {}
    for i in bot: label[i] = "coached"
    for i in top: label[i] = "top"
    for i in mid: label[i] = "middle"

    print(f"\n{'':<8}{'round 1':>9}{'round 2':>9}{'change':>9}   group")
    print("  " + "-" * 46)
    for i in order[::-1]:
        print(f"  {names[i]:<6}{r1[i]:>9}{r2[i]:>9}{r2[i]-r1[i]:>+9}   {label[i]}")

    print("\n  group means")
    print("  " + "-" * 46)
    for tag, idx in (("coached (bottom %d)" % k, bot), ("middle", mid), ("top %d, untouched" % k, top)):
        if len(idx) == 0:
            continue
        m, t, p = paired(r1[idx], r2[idx])
        pstr = "n/a" if np.isnan(p) else f"{p:.3f}"
        print(f"  {tag:<22}{r1[idx].mean():>6.2f} -> {r2[idx].mean():<6.2f}"
              f"  change {m:>+5.2f}   paired p = {pstr}")

    print(f"\n  whole group: {r1.mean():.2f} -> {r2.mean():.2f}")
    print("\n  Two questions for the room:")
    print("    1. Whatever the coached group did, what did the untouched top group do?")
    print("    2. If you had only been shown the coached group, what would you have concluded?")

    if a.no_plot:
        return
    import matplotlib.pyplot as plt
    colors = {"coached": "#c0392b", "top": "#2e8b57", "middle": "#7f8c8d"}
    fig, ax = plt.subplots(figsize=(6.5, 4))
    for i in range(n):
        ax.plot([1, 2], [r1[i], r2[i]], "o-", color=colors[label[i]], alpha=0.55, lw=1.2)
    for tag, idx in (("coached", bot), ("middle", mid), ("top", top)):
        if len(idx):
            ax.plot([1, 2], [r1[idx].mean(), r2[idx].mean()], "o-",
                    color=colors[tag], lw=3.5, label=f"{tag} mean")
    ax.set_xticks([1, 2]); ax.set_xticklabels(["round 1", "round 2"])
    ax.set_ylabel("upright landings out of 10")
    ax.set_xlim(0.85, 2.15); ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout(); plt.show()


if __name__ == "__main__":
    main()
