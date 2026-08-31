# Stat 220: Course Rewrite (F2026)

_Twelve three-day units. Each ships a deck, a code companion, and a homework._

> **New here?** Open a deck PDF in `Slides/` next to its notebook in `Notebooks/`, and read the
> calendar table below for what each unit covers. The `.tex` files are the source of truth for the
> slides, not the PDFs. Two things live on Drive rather than here: the exam question banks, because
> this repo is public, and the superseded 15-module version of the course. `Alternative_Model_First/`
> is a second complete ordering of the same material, not a work in progress.

## Guiding philosophy

Computation is cheap. Judgment is the differentiator. We teach the principles rigorously, but the
mastery target is **application under ambiguity**: given a messy situation and imperfect data, what
can you actually conclude, and what would have to be true for that conclusion to hold?

The framing is deliberately **kept in the background**. The decks do not announce every three
slides that this is how statisticians think or that this will be on an interview. The scenarios,
the traps, and the "what would change your mind" habit carry the message without the narration.
Concretely, each deck now has **one** short "what this unit gives you" frame instead of three
learning-contract frames, and the green example blocks are mostly labeled **In practice**, with the
explicit *You may be asked* framing reserved for one or two moments per deck.

Students are mostly CS majors, not statistics or math upperclassmen. We can be demanding, but
concepts get explained rather than assumed, and the code companions let them see a mechanism move
instead of taking it on faith.

---

## The calendar

42 class periods. Twelve units at roughly three days each comes to 36, plus 2 for review and
exams, leaving about **4 flex days**.

The decks no longer carry Day 1 / Day 2 / Day 3 separator slides. The material runs continuously
and you break where it makes sense on the day. The columns below are the natural seams in each
unit, not a timetable.

| # | Unit | Opens with | Then | Closes with |
|---|------|-------|-------|-------|
| 1 | Statistical Inference in the Wild | signal vs noise, SE, the $t$-statistic | $p$-values, tests, errors, power | CIs, practical significance, assumptions |
| 2 | Probability and Random Variables | rules, independence, correlated failure | conditioning, Bayes, base rates | random variables, expectation, variance |
| 3 | The Normal Distribution and the CLT | density, normal, $z$-scores | the CLT, SE, how big $n$ must be | skew, heavy tails, dependence |
| 4 | Estimation and the Bootstrap | estimators, bias/variance, shrinkage | likelihood and its curvature | the bootstrap and its failures |
| 5 | Regression as Reasoning | the line, least squares, reading a slope | inference on a slope, categorical predictors | multiple regression, confounding |
| 6 | Building and Trusting a Model | many predictors, interactions, collinearity | overfitting, cross-validation, leakage | trees, regularization, importance |
| 7 | Prediction and Its Uncertainty | the four layers of error | PI vs CI, intervals from real errors | extrapolation, regression to the mean, shift |
| 8 | Categorical Outcomes | proportions, rates, absolute vs relative | tables, chi-square, Simpson's, logistic | evaluation, thresholds, calibration |
| 9 | Causal Thinking | counterfactuals, randomization, the collider demo | confounder / collider / mediator | quasi-experiments, diff-in-diff |
| 10 | Bayesian Reasoning and Decisions | updating, prior/likelihood/posterior | priors, sensitivity, credible intervals | expected loss, value of information |
| 11 | Where the Data Comes From | population, frame, sampling designs | missing data and its mechanisms | measurement, proxies, provenance |
| 12 | Putting It Together (capstone) | the workflow and the red-flag checklist | eight worked scenarios | the interview bracket |

**What changed from the 15-module draft.** Units 2, 6, and 8 are merges. Old Modules 5+6
(probability, random variables) became Unit 2. Old Module 11 (flexible models) folded into Module 3
to become Unit 6, which removed a real overlap: both decks had been teaching overfitting and
train/test. Old Modules 9+10 (classification, categorical) became Unit 8, so proportions → tables →
logistic → evaluation is one arc instead of two separated ones.

**Ordering note.** Unit 1 stays first as the motivating hook (the Coke taste test on day one), with
Units 2 to 4 then building the machinery underneath it. If you would rather teach foundations first,
move Unit 1 to slot 4. Nothing else has to change, because each unit's opener refers back only
loosely.

---

## What ships with every unit

**1. The deck** (`Slides/Unit_NN_*.tex` + PDF), 34 to 54 frames, running continuously with no day
separators. Every deck compiles with **zero overfull boxes and zero em dashes**, and every one ends
with two frames added for this revision:

- **a step-by-step procedure frame**, the actual recipe for carrying the method out, with the
  function names attached
- **"What you should be able to do with software"**, a table pairing each task with what you would
  reach for, stating plainly that syntax is not the thing being examined but knowing which
  procedure to run and what the output means is

**2. A code companion** (`Notebooks/Code_UnitNN_*.ipynb`), executed end to end with outputs stored,
so you can present from it or assign it as reading. These exist to make a mechanism visible, not to
cover every concept: roughly 7 to 10 substantive cells each. Highlights:

- Unit 1: p-values are uniform under the null, and peeking inflates the false-positive rate from 5% to
  **26%**, and a session-level test reports $t = -7.8$ where the user-level test reports $t = -1.6$.
- Unit 2: three data centers with identical 1% failure rates but a shared shock have a joint
  failure probability **1,000× higher** than independence implies.
- Unit 3: a coverage table showing "95%" intervals that actually cover 61% (badly skewed, $n=5$)
  and 5% (rare events, $n=5$). This is the honest answer to "is $n>30$ enough?"
- Unit 6: feature selection done before cross-validation yields $R^2 = +0.34$ on data that is
  **pure noise**. Done correctly inside the folds it yields $-0.42$.
- Unit 12: one dataset worked end to end, from provenance to a costed recommendation, as the
  template for the capstone.

**3. A homework** (`Homework/Stat_220_HW_UnitNN_*.ipynb`), five problems in the autograder's
`**Problem N**` / `Part a.` structure, all verified to parse.

---

## Homework design

Every assignment follows the same shape, by request:

1. **Problem 1 is a simulation lab.** Students build a world where they set the truth, so the
   principle is demonstrated rather than asserted. They construct the bias on purpose (a collider,
   a confounder, leakage, the winner's curse) and measure exactly how wrong the naive analysis is.
2. **Problems 2 to 4 are real data with a real decision attached.** Not "compute the coefficient" but
   "the engineering team wants a number for design tradeoffs" or "the clinic wants to know whether
   to adopt this screening rule."
3. **Problem 5 asks what can and cannot be said.** What population does this apply to? Is this
   causal? What would have to be true? What would you tell the manager who wants one number?

Written parts are graded on reasoning, and the instructions say so: *a correct number with a wrong
interpretation earns very little.*

### Real data used

All from `https://richardson.byu.edu/220/`. Several datasets are used deliberately because their
flaws are teachable:

| Dataset | Used in | Why it earns its place |
|---------|---------|------------------------|
| `bikes.csv` | 1, 2, 7, 12 | 365 **consecutive** days, lag-1 autocorrelation 0.50, and only 18 holidays, so the holiday comparison is genuinely underpowered |
| `rent.csv` | 1, 3, 4, 11 | heavily skewed (mean 35k, median 16k), a normal fit implies **33% of listings have negative rent**, and listings cluster within six cities |
| `cars.csv` | 5, 6, 9 | the acceleration slope drops from $+1.20$ to $+0.26$ once you adjust for weight, and weight and displacement correlate at 0.93 |
| `diabetes.csv` | 2, 8, 11 | 46% of `Insulin` values are zeros standing in for missing data |
| `credit_risk.csv` | 2, 8, 9, 10, 11, 12 | rebalanced to a ~48% default rate and contains **only approved loans**: a selection lesson in itself |
| `insurance_all.csv` | 2, 4, 7, 9, 12 | heavy right tail, and the smoker effect is large, real, and thoroughly confounded |
| `housing_data.csv` | 5, 7 | clean categorical predictors and a natural interaction |
| `airfoil.csv` | 6 | 1,503 rows, good for honest model comparison |
| `fish.csv` | 4, 10 | seven species with 6 to 56 observations each: shrinkage and the winner's curse |
| `product_sales_complaint_data.csv` | 2 | counts that are binomial, not Poisson (variance *below* the mean) |

---

## Conventions

- 🟦 `principle`: a principle to retain
- 🟩 `practice` (**In practice**): a judgment call, worked
- 🟩 `interview` (**You may be asked**): used sparingly, once or twice per deck
- 🟥 `trap`: a mistake to avoid
- 🟧 `yourturn`: a pause where students reason out loud, always followed by an answer frame
- 🟦 `livedemo`: the participation activity
- 🟪 `llmcheck`: two in a row, one right and one wrong, so they cannot assume the verdict

Every unit has at least one activity requiring participation, and no two are alike: the Coke taste
test, fake-a-coin, a sealed-bid gamble auction, sticky-note sampling distributions, the
serial-number estimator contest, guess-the-correlation, train-then-verify, the calibration game,
rock-paper-scissors, the inbox game, the dice collider, the two-bag probability line, sampling this
room three ways, and the interview bracket.

---

## Two other things in this folder

**`ALTERNATIVE_ORDER_model_first.md`** works out a different sequence: Unit 1 as-is, then straight
into regression, models, prediction, and causal thinking, with probability and distributions in the
second half. It is built as a complete parallel copy in `Alternative_Model_First/`, so nothing
here was renumbered. Read the plan first; it is honest about what the order costs.

**`Exams/` is deliberately not in this repository.** It holds the closed-book question banks, one
PDF per topic, 199 scenario questions with answer sketches for whoever grades them. This repo is
public, so the banks stay on Drive. Ask Dr. Richardson for access. Every question is answerable
with a pencil: no software, and no arithmetic that will not fit in a margin. Files are named by
topic rather than by unit number so they survive any reordering. `build_questions.py` plus the
`qb_*.py` scripts regenerate them.

## Editing this material

**Slides.** Do not edit the PDFs. Each `Slides/Unit_NN_*.tex` is the source, it is
self-contained (its own preamble, no shared style file), and it sits next to its PDF. Change the
`.tex`, then from this folder run:

```bash
bash tools/compile.sh Unit_09_Causal_Thinking
```

That compiles twice and prints the page count plus any overfull boxes or em dashes, so you find
out immediately if an edit pushed a frame off the slide. Every deck carries a comment header
repeating this.

Figures are the `fig_*.pdf` files in `Slides/`, produced by `tools/make_module*_slide_figs.py`. To
change a figure, edit its script and re-run it. To swap in your own image, just point the
`\includegraphics` at a different file.

**Homework and code companions.** These are generated. Edit `tools/build_unitNN.py` and re-run it,
which rewrites the notebook and re-executes the code companion so the stored outputs always match
the code. If you would rather hand-edit a `.ipynb` directly, that is fine, but stop running that
unit's builder afterwards or your edits will be overwritten.

**The one trap.** The scripts that originally generated the decks from the 15-module draft live in
`tools/one_shot_generators/`. Re-running them would overwrite `Slides/Unit_*.tex`. They are parked
out of the way for that reason and are not needed again.

## Tooling

- `tools/adapt.py`: deck surgery, covering the preamble, day dividers, contract collapse, question-bank merge,
  frame extraction for the merged units.
- `tools/nblib.py`: notebook builders. `HW.write()` validates against **the autograder's own
  splitter** and raises if the problems do not come out as expected. It also refuses an intro that
  starts a line with "Problem N", which silently created a phantom section the first time.
- `tools/build_unitNN.py`: one script per unit, regenerating that unit's code companion and
  homework, executing the companion so stored outputs always match the code.
- `tools/deck_unitNN.py`, `tools/deck_units_09_12*.py`: regenerate the decks from the archived
  modules.
- `tools/compile.sh <deck>`: compiles twice and reports pages, overfull boxes, and em dashes.

The superseded 15-module drafts are in `Archive_Modules/` in case you want to pull a frame back.

### A grader change worth knowing about

The autograder used to hand the model the whole problem section, and that section includes *your*
prompt text. With these assignments that meant an untouched notebook looked like a 1,500-character
answer per problem, and the model was reading questions that often state the very thing the rubric
asks for.

It now takes the blank assignment as a reference. Put a copy at
`Autograder/grading/<HW>/assignment.ipynb`, or pass `--template`. Cells that match the blank are
labelled as prompt text, anything the student added is labelled as student work, unanswered
problems score 0 without an API call, and the system prompt tells the model that prompt text earns
no credit. Verified on a blank submission and a partially-completed one.

`Autograder/tools/scaffold_rubric.py` reads an assignment and writes a pre-filled rubric, one row
per part, with the problem number, part letter, and a draft criterion pulled from the prompt. You
set the points and fix the wording. Scaffolds for all twelve units are already in
`Autograder/rubrics/scaffolds/`.

## Voice

The prose was passed over again to remove the tells of machine writing: no em dashes, no
semicolons joining two clauses, no bullet lists whose items all end in a semicolon, and no
phrases like "wearing a suit," "the whole ballgame," or "a magic trick." Punctuation inside
mathematics is untouched. If you add material later, the two scripts that enforce this are
`tools/polish_decks.py` and `tools/polish_notebooks.py`, and both are safe to re-run.

Counts after the pass: 0 em dashes and 0 prose semicolons across the twelve decks, and the same
across all twenty-four notebooks.

## Activities

Every unit has at least one participation activity, and each one now carries a small note on the
slide giving the materials and the time it takes, so someone else could run it. Units 1, 2, 6,
and 8 have two, placed on different days. Unit 6 had lost its Day 3 activity in the merge, so the
tree-building exercise is back.

Unit 1 also opens with two single-page reviews, the one-sample and two-sample $t$-test laid out in
full with the left-tailed, right-tailed, and two-sided cases side by side, placed just before the
Coke tests so the activity lands on top of a refresher rather than in a vacuum. Unit 2 defines
conditional probability before it is used to define independence, and names sensitivity,
specificity, and prevalence before the screening arithmetic uses them.

Two supporting handouts live in `Slides/`:

- `Unit_03_Price_Handout.pdf`, the 200 house prices students sample from in the
  sampling-distribution demo (population mean 331,525, median 294,000, so the skew is visible).
- `Unit_12_Scenario_Cards.pdf`, 18 cards for the interview bracket.

The Unit 2 coin activity now runs the other way round: **everyone** is on the fool-me team, and
`tools/coin_detector.py` scores a typed sequence against 120 real 50-flip sequences pre-flipped
into `Slides/unit02_reference_flips.json`. It flags a longest run of 4 or shorter and an
alternation rate above 60%, which between them catch nearly every hand-written attempt. The same
detector is built into the Unit 2 code companion so students can keep trying on their own.

## Status

- [x] Twelve 3-day decks, all compiling clean
- [x] Twelve code companions, all executing with zero errors
- [x] Twelve homeworks, all parsing with the autograder
- [x] Printable handouts for the Unit 3 and Unit 12 activities
- [x] Voice pass: em dashes, prose semicolons, and writerly phrasing removed throughout
- [x] Activity pass: materials and timing on every demo, Unit 6's Day 3 activity restored
- [x] Grader pass: the autograder now separates prompt text from student work (see below)
- [x] All 20 numbers quoted on slides re-verified against the data
- [ ] Your pass on ordering and on which units need the 4 flex days
- [ ] Units 7, 9, 10, 11 are the shortest at 32 to 35 frames, so they have the most room if a day feels thin
- [ ] Push `ab_experiment.csv` to the public repo if you still want Module 1's original data links
