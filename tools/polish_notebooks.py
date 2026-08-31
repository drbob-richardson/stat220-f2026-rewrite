#!/usr/bin/env python3
"""Voice pass over the notebook builders, so the rebuilt notebooks inherit it.

Only touches strings students actually read. Python comments and module
docstrings are left alone.
"""
import re
from pathlib import Path

TOOLS = Path(__file__).resolve().parent

# (old, new) applied to every builder file
EDITS = [
 # --- nblib.py headers ---
 ('f"# Unit {unit} code companion --- {title}\\n\\n{blurb}\\n\\n"',
  'f"# Unit {unit} code companion: {title}\\n\\n{blurb}\\n\\n"'),
 ('f"# Stat 220 --- Unit {unit} Homework: {title}\\n\\n{intro}"',
  'f"# Stat 220, Unit {unit} Homework: {title}\\n\\n{intro}"'),
 ("Run the cells in order. Each section matches a moment in the slides; the point "
  "is to see the mechanism move when you change the inputs, so change them.",
  "Run the cells in order. Each section matches a moment in the slides. The point is to see the "
  "mechanism move when you change the inputs, so change them."),
 # --- shared homework boilerplate ---
 ("Show your work ---\npartial credit is given for clear reasoning.",
  "Show your work, since partial credit is given for clear reasoning."),
 # --- prose semicolons in homework prompts ---
 ("*What can and cannot be said.* No new computation unless you want it; this is the\npart that separates an analyst from a calculator.",
  "*What can and cannot be said.* No new computation is required here. This is the part that\nseparates an analyst from a calculator."),
 ("Q2 averages; do the same for the top 10%.", "Q2 averages, then do the same for the top 10%."),
 ("A missed case costs \\\\$500 in later complications; an unnecessary\nfollow-up costs \\\\$60.",
  "A missed case costs \\\\$500 in later complications and an unnecessary\nfollow-up costs \\\\$60."),
 ("visitors; variant B converts 104 of 1,000.", "visitors. Variant B converts 104 of 1,000."),
 ("three versions: values missing completely at random; missing at random given age (older people\nskip the question, and you recorded age); and missing not at random (high earners skip it).",
  "three versions. First, values missing completely at random. Second, missing at random given age,\nwhere older people skip the question and you recorded age. Third, missing not at random, where\nhigh earners skip it."),
 ("A default costs \\\\$4,000 on average; rejecting an applicant who would have repaid\ncosts \\\\$900 in forgone profit.",
  "A default costs \\\\$4,000 on average. Rejecting an applicant who would have repaid costs\n\\\\$900 in forgone profit."),
 ("Each bike costs \\\\$3 for the day; each rental earns \\\\$9.",
  "Each bike costs \\\\$3 for the day and each rental earns \\\\$9."),
 # --- prose semicolons in code-companion narration ---
 ("The spread of those estimates *is* the standard error; the formula sigma/sqrt(n) just predicts it.",
  "The spread of those estimates *is* the standard error. The formula sigma/sqrt(n) only predicts it."),
 ("Every marginal probability is identical; only the dependence changed.",
  "Every marginal probability is identical. Only the dependence changed."),
 ("The first column collapses toward zero; the second never moves.",
  "The first column collapses toward zero. The second never moves."),
 ("The effect never changed; only the sample size did.",
  "The effect never changed. Only the sample size did."),
 ("The model is the easy part; the threshold is the decision.",
  "The model is the easy part. The threshold is the decision."),
 ("Each red chip multiplies the odds for A by 0.7/0.3; each white chip divides by the same.",
  "Each red chip multiplies the odds for A by 0.7/0.3, and each white chip divides by the same."),
 ("Both numbers are correct; they answer different questions.",
  "Both numbers are correct. They answer different questions."),
 ("watch which designs are merely noisy and which are wrong; measure why a huge biased sample "
  "loses to a small clean one",
  "watch which designs are merely noisy and which are wrong, measure why a huge biased sample "
  "loses to a small clean one"),
 ("Simple and stratified are unbiased; stratified is tighter for the same cost.",
  "Simple and stratified are both unbiased, and stratified is tighter for the same cost."),
 ("Each bike costs $3 for the day; each rental earns $9. The point forecast is not the "
  "answer to 'how many bikes'.",
  "Each bike costs $3 for the day and each rental earns $9. The point forecast is not the "
  "answer to 'how many bikes'."),
 # --- em dashes inside student text ---
 ('*"Confirmed --- holidays make\nno difference, staff them normally."*',
  '*"Confirmed, holidays make no difference. Staff them normally."*'),
 ("state which of the two problems --- skew or dependence --- you\nwould worry about more",
  "state which of the two problems, skew or dependence, you would worry about more"),
 ("compute the mean rent two ways --- treating all listings as independent, and treating each of the six\ncities as one observation --- and report the standard error each way.",
  "compute the mean rent two ways, first treating all listings as independent and then treating\neach of the six cities as one observation. Report the standard error each way."),
 # --- writerly phrasing in narration ---
 ("Most of the raw relationship was weight wearing a disguise.",
  "Most of the raw relationship was weight, relabeled."),
 ("Track the skewness number, not just the picture.", "Track the skewness number, not the picture."),
 ("This is the 2008 mortgage story in eight lines.",
  "This is the 2008 mortgage problem in eight lines."),
]


def main():
    files = ["nblib.py"] + sorted(p.name for p in TOOLS.glob("build_unit*.py"))
    total = 0
    for name in files:
        p = TOOLS / name
        s = original = p.read_text()
        hits = 0
        for old, new in EDITS:
            if old in s:
                s = s.replace(old, new)
                hits += 1
        # "2--3 sentences" reads as LaTeX in a notebook; spell the range out.
        s2 = re.sub(r"(\d)--(\d)", r"\1 to \2", s)
        rng = len(re.findall(r"\d--\d", s))
        s = s2
        # data-source bullets: `url` --- description
        s2 = re.sub(r"(`\S+?\.csv`) --- ", r"\1: ", s)
        bullets = len(re.findall(r"`\S+?\.csv` --- ", s))
        s = s2
        if s != original:
            p.write_text(s)
        if hits or rng or bullets:
            print(f"{name:<26} edits {hits:>2}   ranges {rng:>2}   data bullets {bullets:>2}")
            total += hits + rng + bullets
    print(f"\ntotal changes: {total}")


if __name__ == "__main__":
    main()
