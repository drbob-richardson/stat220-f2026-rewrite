# Alternative ordering: models first, machinery second

_A worked-out version of "go straight into modeling and do probability after." Written as a
proposal you can accept, reject, or cherry-pick. Nothing in the current numbering has been
overwritten._

## The idea

The current order builds the machinery first (probability, distributions, CLT, estimation) and
then spends it on models. This alternative flips that: Unit 1 sets the habits, Units 2 through 6
do the modeling with the machinery borrowed on credit, and Units 7 through 12 go back and pay for
what was borrowed, then spend it again on the two topics that genuinely need it.

The argument for it is that the first half of the semester is the half students are most awake
for, and regression on real data is more gripping than the axioms of probability. The argument
against is that a few things get used before they are earned. Both are addressed below.

## The order

### Part I: Models, and what they can tell you

| # | Unit | Was | Why here |
|---|------|-----|----------|
| 1 | Statistical Inference in the Wild | 1 | Unchanged. Sets the habits and hands you the template (estimate minus null, over its standard error) that everything else reuses. |
| 2 | Regression as Reasoning | 5 | The template again, with a slope in place of a difference. Needs nothing from probability. |
| 3 | Building and Trusting a Model | 6 | Many predictors, overfitting, cross-validation, regularization. Purely empirical, no distribution theory required. |
| 4 | Prediction and Its Uncertainty | 7 | Intervals built from held-out residuals rather than from formulas, which is why this works before the CLT. |
| 5 | Causal Thinking | 9 | Pairs directly with regression. "What does controlling for this variable do?" lands hardest right after students have been controlling for things. |
| 6 | Where the Data Comes From | 11 | The hinge. Five units of trusting the model, then one on trusting the data, ending in sampling, which is the natural door into probability. |

### Part II: The machinery, and two things that need it

| # | Unit | Was | Why here |
|---|------|-----|----------|
| 7 | Probability: Randomness, Conditioning, and Bayes | 2 (first half) | Sampling in Unit 6 raises "what does random mean," and this answers it. |
| 8 | Random Variables and Distributions | 2 (second half) | Expectation, variance, the distribution stories, the flaw of averages. |
| 9 | The Normal Distribution and the CLT | 3 | The payoff unit. This is where the standard errors used since Unit 1 finally get justified. |
| 10 | Estimation, Likelihood, and the Bootstrap | 4 | Needs the sampling distribution from Unit 9. |
| 11 | Categorical Outcomes | 8 | Logistic regression, and evaluation built on base rates. Needs conditional probability, so it cannot come earlier. |
| 12 | Bayesian Reasoning and Decisions | 10 | Needs Bayes and distributions. A good finale: probability turned back into decisions. |

The capstone deck (currently Unit 12, "Putting It Together") stops being a unit and becomes
**review-day material**. You have 2 exam/review days and about 4 flex days, and the interview
bracket plus the scenario cards are exactly what those days want.

## What this costs, honestly

Three things get used before they are formally taught. Two are fine and one needs a patch.

**1. Standard errors and the $t$-distribution, from Unit 1 onward.** Unit 1 already introduces the
sampling distribution and the standard error informally, without deriving them, and that is enough
to carry Units 2 through 5. Unit 9 then closes the loop, and it lands better as a payoff
("this is why everything you have been doing was legitimate") than as a prerequisite.

**2. The normal distribution, mentioned in passing.** Regression diagnostics and prediction
intervals refer to it. **Patch:** a single compact frame in Unit 1, "the normal, the version you
need for now," giving the bell shape, 68-95-99.7, and the $z$-score, with an explicit promise that
Unit 9 earns it properly. This is the "touching only on the normal distribution" you asked for.

**3. Probability language inside the modeling units.** Causal thinking talks about confounders
without conditional probability notation. This turns out to be fine, because the causal unit is
built on diagrams and comparisons rather than on $P(Y \mid X, Z)$.

**What does not work:** moving Categorical Outcomes into Part I. That unit runs on odds, base
rates, and predictive values, which are conditional probability wearing different hats. Putting it
before Unit 7 would recreate exactly the ordering bug we just fixed inside the old Unit 2, where
independence was defined using conditional probability three slides before conditional probability
existed. If you want logistic regression earlier, the honest move is to pull the *modeling* half of
it (the logistic curve, log-odds, reading a coefficient) into Unit 3 and leave the *evaluation*
half (thresholds, precision and recall, calibration) at Unit 11. I can split it that way if you
want.

## What changes mechanically

- **The old Unit 2 splits back into two units** (7 and 8). It was itself a merge of the original
  Modules 5 and 6, and the seam is still clean: everything through Bayes and base rates becomes
  Unit 7, everything from the gamble auction onward becomes Unit 8. This is what gets the count
  back to 12 after the capstone leaves.
- **Renumbering**, which touches each deck's subtitle, its opening "where this fits," its closing
  "where we go next," and about a dozen forward references such as "Unit 10 turns this into a whole
  way of doing inference."
- **Homework and code companions renumber with their units.** Their content is per-topic and does
  not care about order, with one exception noted below.
- **One homework dependency breaks and is already fixed.** Unit 1's homework used to ask for a
  bootstrap, which now sits in Unit 10 rather than Unit 4. It was rewritten last week to use only
  Unit 1 tools, so it is safe in either ordering.

## Risks worth watching

- **Unit 2 lands hard.** Regression in week two, with no distribution theory behind it, asks
  students to accept a standard error on faith. Some will want to know where it comes from. The
  answer is a promissory note, and it should be made out loud in Unit 2 rather than dodged.
- **Part II can feel like a step backward** if it is framed as new material. It should be framed as
  the explanation for what they have already been doing. Every unit in Part II should open by
  naming the thing from Part I that it is finally justifying.
- **The exam split changes.** A midterm after Unit 6 covers modeling with almost no probability,
  which is unusual for a stats course and worth deciding on deliberately rather than by accident.

## If you want to try it

The reordered decks are built in `Alternative_Model_First/`, which is a complete parallel
copy. The current numbering in this folder is untouched, so you can teach either one, or diff them.
