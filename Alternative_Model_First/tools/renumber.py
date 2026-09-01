#!/usr/bin/env python3
"""Copy the remaining decks into the model-first order and remap every unit reference."""
import re, shutil
from pathlib import Path

OLD = Path("/Users/robertrichardson/Library/CloudStorage/GoogleDrive-richardson@stat.byu.edu/"
           "My Drive/BYU Classes/220/F2026/Course_Rewrite")
NEW = Path(__file__).resolve().parents[1]

# old unit number -> new unit number  (7 and 8 come from the split, handled separately)
REMAP = {1: 1, 5: 2, 6: 3, 7: 4, 9: 5, 11: 6, 2: 7, 3: 9, 4: 10, 8: 11, 10: 12, 12: 99}

MOVES = [                       # (old stem, new stem)
 ("Unit_01_Inference",            "Unit_01_Inference"),
 ("Unit_05_Regression_as_Reasoning",          "Unit_02_Regression_as_Reasoning"),
 ("Unit_06_Building_and_Trusting_a_Model",    "Unit_03_Building_and_Trusting_a_Model"),
 ("Unit_07_Prediction_and_Its_Uncertainty",   "Unit_04_Prediction_and_Its_Uncertainty"),
 ("Unit_09_Causal_Thinking",                  "Unit_05_Causal_Thinking"),
 ("Unit_11_Where_the_Data_Comes_From",        "Unit_06_Where_the_Data_Comes_From"),
 ("Unit_03_Normal_and_the_CLT",               "Unit_09_Normal_and_the_CLT"),
 ("Unit_04_Estimation_and_the_Bootstrap",     "Unit_10_Estimation_and_the_Bootstrap"),
 ("Unit_08_Categorical_Outcomes",             "Unit_11_Categorical_Outcomes"),
 ("Unit_10_Bayesian_Reasoning_and_Decisions", "Unit_12_Bayesian_Reasoning_and_Decisions"),
 ("Unit_12_Putting_It_Together",              "Review_Capstone_Putting_It_Together"),
]

def remap_refs(text):
    def sub(m):
        old = int(m.group(1))
        new = REMAP.get(old)
        if new is None or new == 99:
            return "the capstone review" if new == 99 else m.group(0)
        return f"Unit {new}"
    return re.sub(r"Unit (\d{1,2})\b", sub, text)

for old_stem, new_stem in MOVES:
    src = OLD / "Slides" / f"{old_stem}.tex"
    s = src.read_text()
    s = remap_refs(s)
    # the header comment names its own file
    s = re.sub(r"bash tools/compile\.sh \S+", f"bash tools/compile.sh {new_stem}", s)
    if new_stem.startswith("Review"):
        s = re.sub(r"\\subtitle\{[^}]*\}",
                   r"\\subtitle{Review and capstone: Messy Questions, Answered Out Loud}", s)
    (NEW / "Slides" / f"{new_stem}.tex").write_text(s)
    print(f"  {old_stem:<44} ->  {new_stem}")

print("\nremaining stale references (should be none):")
import subprocess
for p in sorted((NEW / "Slides").glob("*.tex")):
    for m in re.finditer(r"Unit (\d{1,2})", p.read_text()):
        n = int(m.group(1))
        if n > 12:
            print(f"  {p.stem}: Unit {n}")
