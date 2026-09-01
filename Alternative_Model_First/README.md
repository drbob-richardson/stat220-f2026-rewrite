# Stat 220 F2026: the model-first ordering

_A complete parallel build of the course in the alternative order. The original numbering lives in
`../Course_Rewrite/` and is untouched, so you can teach either one or compare them side by side.
The reasoning behind this order is in `../Course_Rewrite/ALTERNATIVE_ORDER_model_first.md`._

## The order

**Part I: Models, and what they can tell you**

| # | Unit | Frames | Was |
|---|------|--------|-----|
| 1 | Statistical Inference in the Wild | 54 | 1 |
| 2 | Regression as Reasoning | 44 | 5 |
| 3 | Building and Trusting a Model | 51 | 6 |
| 4 | Prediction and Its Uncertainty | 37 | 7 |
| 5 | Causal Thinking | 38 | 9 |
| 6 | Where the Data Comes From | 38 | 11 |

**Part II: The machinery, and two things that need it**

| # | Unit | Frames | Was |
|---|------|--------|-----|
| 7 | Probability: Randomness, Conditioning, and Bayes | 42 | 2, first half |
| 8 | Random Variables and Distributions | 26 | 2, second half |
| 9 | The Normal Distribution and the CLT | 42 | 3 |
| 10 | Estimation, Likelihood, and the Bootstrap | 39 | 4 |
| 11 | Categorical Outcomes | 55 | 8 |
| 12 | Bayesian Reasoning and Decisions | 36 | 10 |

Plus `Review_Capstone_Putting_It_Together` (39 frames), which is no longer a unit. It is material
for the two review/exam days and the flex days, along with the scenario cards.

## What actually changed

- **The old probability unit was split in two.** It was a merge of the original Modules 5 and 6, so
  the seam was still clean. Everything through Bayes and base rates became Unit 7; everything from
  the gamble auction onward became Unit 8. Each got its own closing material, traps list, question
  bank, mastery checklist, and software table.
- **Unit 1 gained a normal-distribution primer.** One frame giving the bell shape, 68-95-99.7, and
  the $z$-score, stating openly that Part I is borrowing the result on credit and that Unit 9 pays
  it back. This is the "touch only on the normal distribution" part of the plan.
- **Six decks got rewritten openers or closers**, because the transitions are the one thing
  renumbering cannot infer. Unit 6 now ends by handing off to Part II, and Unit 9 now opens as the
  payoff unit rather than as a prerequisite: "since Unit 1 we have written estimate plus or minus
  two standard errors and moved on, and this is where that gets earned."
- **Every cross-reference was remapped**, so "Unit 10 turns this into a whole way of doing
  inference" now points at the right place.

## Known gaps in this build

- **Unit 8 is thin at 26 frames**, because splitting the merged unit left the random-variables half
  smaller than the probability half. It needs roughly ten more frames to fill three days. The
  obvious candidates are worked expectation and variance examples, a second activity, and an
  LLM-check pair, all of which the other units have.
- **Units 7 and 8 share a code companion and homework.** The notebooks were copied under both
  numbers but not yet split along the same seam. The probability material is in the first half of
  each file and the random-variables material in the second, so the split is mechanical but has not
  been done.
- **The homework in Units 11 and 12 assumes the old ordering in a few prompts** where it says
  "as in Unit 8." Harmless, but worth a pass if you adopt this order.

## Everything else is unchanged

Same decks, same figures, same homework and code companions, same conventions, same voice rules.
`Exams/` is copied here as well, and because the question banks are named by topic rather than by
unit number they work with either ordering.

---

## Unit 13, optional: Choosing a Model

`Slides/Unit_13_Choosing_a_Model.tex` (37 pages) and
`Notebooks/Code_Unit13_Choosing_a_Model.ipynb`.

Not part of the 12-unit calendar. It sits most naturally after Unit 4, once regression,
model building, and prediction are all in hand and the four questions have each been
answered for linear regression exactly once.

The unit answers the question the other twelve leave open: when a more complicated model
earns its keep. Unit 3 teaches how to *detect* the right complexity with cross-validation,
but never says what *determines* it, and "bias-variance" appears once in the whole course.
This unit names the tradeoff, shows what moves the optimum, and turns model choice into
something a student can say out loud in order.

It deliberately forward-references logistic regression (Unit 11) and count models
(Units 7 and 8) rather than teaching them, so it works at slot 5 without needing
probability first.

Figures come from `tools/make_unit13_slide_figs.py` and are computed, not drawn. The
central one simulates a fixed true curve and varies only the sample size: the best
polynomial degree moves 3, 5, 8 as n goes 20, 50, 300.
