#!/usr/bin/env python3
"""Voice pass over the built Unit decks.

Three jobs, in order:
  1. strip terminal semicolons from bulleted lists (the giveaway pattern)
  2. rewrite mid-sentence semicolons into real sentences
  3. replace writerly phrasing with plain wording

Idempotent: safe to run twice. Reports what it changed.
"""
import re
import sys
from pathlib import Path

SLIDES = Path(__file__).resolve().parents[1] / "Slides"

# ---------------------------------------------------------------------------
# 2. Mid-sentence semicolons, rewritten one at a time.
# ---------------------------------------------------------------------------
REWRITES = [
 # --- Unit 1 ---
 ("(He used 8 cups of tea; we used 10 cups of Coke.)",
  "(He used 8 cups of tea, we used 10 cups of Coke.)"),
 ("its average is all over the place; a couple",
  "its average is all over the place. A couple"),
 ("Show me the effect size and the CI; significance alone tells us little",
  "Show me the effect size and the CI. Significance alone tells us little"),
 ("probability that the drug does nothing; that would be circular.",
  "probability that the drug does nothing. That would be circular."),
 ("Use \\textbf{Welch's $t$}; it's free and it fixes the problem.",
  "Use \\textbf{Welch's $t$}. It is free and it fixes the problem."),
 ("(could be low power; check the CI)", "(could be low power, so check the CI)"),
 ("slope; in classification it becomes a log-odds.",
  "slope. In classification it becomes a log-odds."),
 # --- Unit 2 ---
 ("more likely than not; with 50 it is nearly certain.",
  "more likely than not. With 50 it is nearly certain."),
 ("\\item 50 are users; 98\\% of them", "\\item 50 are users, and 98\\% of them"),
 ("\\item 9,950 are not; 2\\% of them", "\\item 9,950 are not, and 2\\% of them"),
 # --- Unit 3 ---
 ("\\item $|z| > 2$ is noteworthy; $|z| > 3$ is rare",
  "\\item $|z| > 2$ is noteworthy, and $|z| > 3$ is rare"),
 # --- Unit 4 ---
 ("barely moves from the site average; one with",
  "barely moves from the site average. A seller with"),
 ("distribution over $p$; it is a ranking of parameter values",
  "distribution over $p$. It ranks parameter values"),
 ("sound worse than it is; reporting", "sound worse than it is. Reporting"),
 ("likelihood; this is what software reports", "likelihood, which is what software reports"),
 ("\\item 100{,}000 page views from 6{,}000 visitors; you want mean session length.",
  "\\item Mean session length, from 100{,}000 page views by 6{,}000 visitors."),
 ("\\item 365 consecutive days of sales at one store; you want mean daily sales.",
  "\\item Mean daily sales, from 365 consecutive days at one store."),
 ("\\item Test scores for 900 students in 30 classrooms; you want the district average.",
  "\\item The district average, from 900 students in 30 classrooms."),
 ("day is not an independent draw; resample contiguous stretches",
  "day is not an independent draw, so resample contiguous stretches"),
 # --- Unit 5 ---
 ("size 0 is nonsense, and that's fine; the intercept is just where the line starts.",
  "size 0 is nonsense, and that is fine. The intercept only positions the line."),
 ("are often meaningless alone; they position the line.",
  "are often meaningless alone. They position the line."),
 ("part; knowing which slope answers your question is the skill.",
  "part. Knowing which slope answers your question is the skill."),
 ("\\item \\textbf{Check:} residuals look fine; no single building is driving the result.",
  "\\item \\textbf{Check:} residuals look fine, and no single building drives the result."),
 # --- Unit 6 ---
 ("The model gets simpler; the sentence gets more careful.",
  "The model gets simpler and the sentence gets more careful."),
 ("A teammate adds 40 features; training $R^2$ rises",
  "A teammate adds 40 features, and training $R^2$ rises"),
 ("highly correlated; both have huge standard", "highly correlated, and both have huge standard"),
 # --- Unit 7 ---
 ("the world is random; even a perfect model misses an",
  "the world is random, so even a perfect model misses an"),
 ("neither; they simply record what went wrong last time.",
  "neither. They record what went wrong last time."),
 ("averaged \\textbf{2.55}; next time they averaged",
  "averaged \\textbf{2.55}. Next time they averaged"),
 # --- Unit 8 ---
 ("get colorectal cancer; among daily processed-meat",
  "get colorectal cancer, and among daily processed-meat"),
 ("default far less than expected; debt consolidation and medical loans far",
  "default far less than expected. Debt consolidation and medical loans default far"),
 ("{Counts lie; rates need the right denominator}",
  "{Counts mislead. Rates need the right denominator}"),
 ("sweeps every threshold at once; AUC is the area under it",
  "sweeps every threshold at once, and AUC is the area under it"),
 ("Missing a case costs \\$500; an unnecessary follow-up costs \\$60.",
  "Missing a case costs \\$500 and an unnecessary follow-up costs \\$60."),
 ("\\item Imbalance is not a modeling bug; it is a fact about the world. Fraud really is rare.",
  "\\item Imbalance is a fact about the world, not a modeling bug. Fraud really is rare."),
 ("It supplies probabilities; you supply the costs.",
  "It supplies probabilities, and you supply the costs."),
 # --- Unit 9 ---
 ("spend \\$340 a year; non-members spend \\$180.",
  "spend \\$340 a year. Non-members spend \\$180."),
 # --- Unit 10 ---
 ("\\textbf{Bag A} is 70\\% red chips; \\textbf{Bag B} is 30\\% red.",
  "\\textbf{Bag A} is 70\\% red chips. \\textbf{Bag B} is 30\\% red."),
 ("by $0.7/0.3 = 2.33$; each white", "by $0.7/0.3 = 2.33$. Each white"),
 ("``Ship B; the chance we are wrong is 6\\%",
  "``Ship B. The chance we are wrong is 6\\%"),
 ("across repeated samples; the parameter is not being treated as",
  "across repeated samples. The parameter is not treated as"),
 ("Evidence updates belief; belief plus costs makes a decision.",
  "Evidence updates belief. Belief plus costs makes a decision."),
 # --- Unit 11 ---
 ("People with strong feelings answer surveys; the indifferent middle does not.",
  "People with strong feelings answer surveys. The indifferent middle does not."),
 ("Dropping is biased; modeling with age is not.",
  "Dropping is biased. Modeling with age is not."),
 ("report income; the sickest patients miss follow-up.",
  "report income, and the sickest patients miss follow-up."),
 ("exercise, and reading; they", "exercise, and reading. They"),
 # --- Unit 12 ---
 ("a tool you already have; the work is choosing which",
  "a tool you already have. The work is choosing which"),
 ("without the base rate; if 85\\% of hires", "without the base rate. If 85\\% of hires"),
 ("Winners pair off; the two losers score.",
  "Winners pair off, and the two losers score."),
]

# ---------------------------------------------------------------------------
# 3. Writerly phrasing, replaced with plain wording.
# ---------------------------------------------------------------------------
PHRASING = [
 # the trap-block title, repeated in all twelve decks
 ("\\begin{trap}{the list worth carrying}", "\\begin{trap}{the ones that bite most often}"),
 # Unit 1
 ("statistic, and interpret each part", "statistic, and interpret each part"),
 ("Robust, complete", "Complete"),
 # Unit 2
 ("A number without a spread is a guess wearing a suit. Expectation says where; variance says how\nmuch to hedge.",
  "Report a spread with every number. The mean says where things sit, the SD says how far they\nmove."),
 ("{Coincidences are mass-produced}", "{Coincidences are more common than they feel}"),
 ("That is the entire economics of sample size, and it is why 'just collect more data' gets\nexpensive fast.",
  "That is why collecting more data gets expensive fast."),
 ("Real randomness \\textbf{clumps}. Our intuition spreads things out evenly, which is itself\n        a recognizable pattern.",
  "Real randomness \\textbf{clumps}. Invented sequences spread out too evenly, and that is what\n        gives them away."),
 ("\\begin{practice}{the skill underneath the parlor trick}",
  "\\begin{practice}{the judgment this is really about}"),
 # Unit 3
 ("That is the brutal economics behind every ``can we just collect more data?'' conversation.",
  "That is the arithmetic behind every ``can we just collect more data?'' conversation."),
 ("\\begin{principle}{the normal earns its place}", "\\begin{principle}{why the normal shows up}"),
 # Unit 4
 ("choosing the resampling unit, which is the whole ballgame",
  "choosing the resampling unit, which decides everything else"),
 ("\\begin{principle}{an estimate is a recipe, not a result}",
  "\\begin{principle}{judge the recipe, not one result}"),
 # Unit 5
 ("{Multiple regression, in one breath}", "{Multiple regression, quickly}"),
 # Unit 6
 ("{The tension at the heart of modeling}", "{The tension in every model you build}"),
 # Unit 7
 ("\\begin{principle}{the dangerous, quiet layer}", "\\begin{principle}{the layer that hides}"),
 ("Noise and estimation error announce themselves in the standard errors. Model error hides,\nbecause the software happily reports tight intervals around a biased prediction.",
  "Noise and estimation error show up in the standard errors. Model error does not, because the\nsoftware reports tight intervals around a biased prediction without complaint."),
 ("look at how wrong the model was on fresh data, not at\nthe tidy interval the formula prints from the training set.",
  "look at how wrong the model was on fresh data, rather than\nat the interval the formula prints from the training set."),
 # Unit 8
 ("{Relative risk without a base rate is a magic trick}",
  "{Relative risk without a base rate is not usable}"),
 ("\\begin{principle}{the threshold is a business decision wearing a math costume}",
  "\\begin{principle}{the threshold is a business decision, not a modeling one}"),
 # Unit 9
 ("{Why that demo is not a party trick}", "{Where this shows up in real data}"),
 ("{Difference in differences, in one picture}", "{Difference in differences, drawn}"),
 ("Weight drives both acceleration and fuel economy", "Weight drives both acceleration and fuel economy"),
 # Unit 11
 ("\\begin{trap}{the discontinuity in your time series}",
  "\\begin{trap}{check the instrument before the world}"),
 # Unit 12
 ("Lifetime value is savagely right-skewed.", "Lifetime value is heavily right-skewed."),
 # generic: "the tell" as a standalone label
 ("\\begin{principle}{the tell}", "\\begin{principle}{how to spot it}"),
 ("\\begin{trap}{the tell}", "\\begin{trap}{how to spot it}"),
]



# ---------------------------------------------------------------------------
# Second pass: wrapped lines and leftovers found on re-scan.
# ---------------------------------------------------------------------------
REWRITES += [
 ("\\item $\\PR{\\text{rich} \\mid \\text{owns a private jet}}$ is near 1;\n        $\\PR{\\text{owns a private jet} \\mid \\text{rich}}$ is not.",
  "\\item $\\PR{\\text{rich} \\mid \\text{owns a private jet}}$ is near 1. The reverse,\n        $\\PR{\\text{owns a private jet} \\mid \\text{rich}}$, is not."),
 ("The top region converts at 22\\%;\nthe company average is 9\\%.",
  "The top region converts at 22\\% against a\ncompany average of 9\\%."),
 ("Adjustment can only handle confounders you measured;\n        randomization handles the ones you did not.",
  "Adjustment can only handle confounders you\n        measured. Randomization handles the ones you did not."),
 ("That is not stubbornness; it\nis arithmetic.", "That is arithmetic, not stubbornness."),
 ("That is not\nconservatism; it is what the arithmetic says once you admit you knew something beforehand.",
  "That is not conservatism. It is what the\narithmetic says once you admit you knew something beforehand."),
]

PHRASING += [
 ("{The reveal: streaks are the tell}", "{The reveal: look at the streaks}"),
 ("\\item Notice what we never needed: the distribution of daily revenue. Linearity got the mean\n        without it.",
  "\\item We never needed the distribution of daily revenue. Linearity gave us the mean without\n        it."),
 ("\\begin{trap}{a flat likelihood dressed up as an estimate}",
  "\\begin{trap}{a flat likelihood still prints a number}"),
 ("\\item Notice what is \\emph{not} in there: any distributional assumption, any formula, any\n        derivation.",
  "\\item Nothing in there assumes a distribution, requires a formula, or needs a derivation."),
 ("It is the two-sample comparison from Part 1, wearing a regression costume.",
  "It is the two-sample comparison from Unit 1, written as a regression."),
 ("\\item Each coefficient then reads as ``this level versus the baseline, holding everything",
  "\\item Each coefficient then means ``this level versus the baseline, holding everything"),
 ("\\begin{principle}{the tension in one line}", "\\begin{principle}{the tension, stated plainly}"),
 ("That is the whole idea of a holdout.", "That is what a holdout is for."),
 ("\\item The tell was the AUC itself. Real clinical prediction lives around 0.7 to 0.85.",
  "\\item The AUC itself was the warning. Real clinical prediction lands around 0.7 to 0.85."),
 ("\\item That last clause is the magic.", "\\item That last clause is the important one."),
 ("of the raw relationship was weight wearing a disguise.",
  "of the raw relationship was weight, relabeled."),
 ("That is the whole module.", "That is this unit in three sentences."),
 ("which reads as ``not significant.''", "which most people read as ``not significant.''"),
 ("impossible: those are missing values wearing a disguise.",
  "impossible: those are missing values recorded as zero."),
 ("\\item This is a \\textbf{multiple comparisons} problem wearing a business suit. With a dozen",
  "\\item This is a \\textbf{multiple comparisons} problem. With a dozen"),
 ("looks magical in testing and useless in real life.",
  "looks perfect in testing and useless in real life."),
]


def strip_list_semicolons(text):
    """In any itemize/enumerate where two or more items end in ';', drop the
    terminal punctuation from every item in that block."""
    out, changed = [], 0
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r"\s*\\begin\{(itemize|enumerate)\}", line):
            depth, j = 1, i + 1
            while j < len(lines) and depth:
                if re.match(r"\s*\\begin\{(itemize|enumerate)\}", lines[j]): depth += 1
                if re.match(r"\s*\\end\{(itemize|enumerate)\}", lines[j]): depth -= 1
                j += 1
            block = lines[i:j]
            semi = sum(1 for b in block if re.search(r";\s*$", b))
            if semi >= 2:
                for k, b in enumerate(block):
                    nb = re.sub(r";\s*$", "", b)
                    if nb == b:
                        nb = re.sub(r"(?<=[a-z\}\)])\.\s*$", "", b) if re.search(r"\.\s*$", b) else b
                    if nb != b: changed += 1
                    block[k] = nb
            out.extend(block)
            i = j
        else:
            out.append(line)
            i += 1
    return "\n".join(out) + ("\n" if text.endswith("\n") else ""), changed


def main():
    totals = {"lists": 0, "semicolons": 0, "phrasing": 0}
    for path in sorted(SLIDES.glob("Unit_*.tex")):
        s = original = path.read_text()

        s, n_lists = strip_list_semicolons(s)
        totals["lists"] += n_lists

        n_semi = 0
        for old, new in REWRITES:
            if old in s:
                s = s.replace(old, new)
                n_semi += 1
        totals["semicolons"] += n_semi

        n_phrase = 0
        for old, new in PHRASING:
            if old in s and old != new:
                s = s.replace(old, new)
                n_phrase += 1
        totals["phrasing"] += n_phrase

        if s != original:
            path.write_text(s)
        print(f"{path.stem:<46} lists {n_lists:>3}   semicolons {n_semi:>2}   phrasing {n_phrase:>2}")
    print(f"\ntotals: {totals}")


if __name__ == "__main__":
    main()
