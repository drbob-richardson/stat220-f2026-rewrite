#!/usr/bin/env python3
"""Can you fake a coin? The in-class detector for Unit 2.

Everyone invents 50 H/T by hand and types it in. The program scores it against
120 sequences of 50 real flips (pre-flipped in unit02_reference_flips.json) and
calls it human or coin.

    python tools/coin_detector.py                 # type sequences one at a time
    python tools/coin_detector.py HTHTTHHT...     # score one from the command line
    python tools/coin_detector.py --demo          # show what the reference set looks like
"""
import json
import sys
from pathlib import Path

REF = Path(__file__).resolve().parents[1] / "Slides" / "unit02_reference_flips.json"


def longest_run(seq):
    best = run = 1
    for i in range(1, len(seq)):
        run = run + 1 if seq[i] == seq[i - 1] else 1
        best = max(best, run)
    return best


def switch_rate(seq):
    return sum(seq[i] != seq[i - 1] for i in range(1, len(seq))) / (len(seq) - 1)


def clean(raw):
    s = "".join(c for c in raw.upper() if c in "HT01")
    return s.replace("0", "T").replace("1", "H")


def verdict(seq, ref):
    """Two tells, combined. Long runs are the strong one; over-alternating is the backup."""
    runs, switches = ref["longest_runs"], ref["switch_rates"]
    n = len(runs)
    run, sw = longest_run(seq), switch_rate(seq)

    p_run = sum(r <= run for r in runs) / n          # how ordinary is a run this short?
    p_sw = sum(s >= sw for s in switches) / n        # how ordinary is alternating this much?

    flags = []
    if run <= 4:
        flags.append(f"longest run of {run} (only {100*p_run:.0f}% of real sequences are that short)")
    if sw >= 0.60:
        flags.append(f"alternates {100*sw:.0f}% of the time (real coins sit near 50%)")

    called_human = bool(flags)
    return run, sw, p_run, p_sw, called_human, flags


def report(seq, ref):
    if len(seq) < 20:
        print(f"  need at least 20 flips, got {len(seq)}")
        return
    run, sw, p_run, p_sw, human, flags = verdict(seq, ref)
    print(f"  length {len(seq)}   heads {seq.count('H')}   longest run {run}   "
          f"alternates {100*sw:.0f}%")
    print(f"  reference: real sequences average a longest run of "
          f"{sum(ref['longest_runs'])/len(ref['longest_runs']):.1f}")
    if human:
        print("  VERDICT: a person wrote this.")
        for f in flags:
            print(f"     - {f}")
    else:
        print("  VERDICT: this could be a real coin. Well done.")
        print(f"     - a run of {run} is unremarkable, and the alternation rate looks right")


def main():
    ref = json.loads(REF.read_text())
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if "--demo" in sys.argv:
        runs = ref["longest_runs"]
        print(f"{ref['n_sequences']} sequences of {ref['n_flips']} real flips")
        print(f"longest run: mean {sum(runs)/len(runs):.2f}, "
              f"min {min(runs)}, max {max(runs)}")
        for k in range(3, 10):
            bar = "#" * sum(r == k for r in runs)
            print(f"  run of {k:>2}: {bar} ({sum(r == k for r in runs)})")
        print("\nAnything with a longest run of 4 or less is suspicious.")
        return

    if args:
        seq = clean(args[0])
        print(f"\nsequence: {seq[:60]}{'...' if len(seq) > 60 else ''}")
        report(seq, ref)
        return

    print("Type 50 H/T characters (or 1/0) and press enter. Blank line quits.\n")
    while True:
        try:
            raw = input("your sequence > ")
        except (EOFError, KeyboardInterrupt):
            break
        if not raw.strip():
            break
        report(clean(raw), ref)
        print()


if __name__ == "__main__":
    main()
