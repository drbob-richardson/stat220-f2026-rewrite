#!/usr/bin/env python3
"""Unit 6 deck: merge Module 03 (Building & Trusting a Model) with Module 11
(Flexible Models, Selection, Regularization) into one 3-day unit."""
import adapt

M3 = "Module_03_Building_and_Trusting_a_Model.tex"
M11 = "Module_11_Flexible_Models_and_Selection.tex"
f3, f11 = adapt.frames(M3), adapt.frames(M11)

out = []
add = out.append

add(adapt.preamble_of(M3, 6, "Building and Trusting a Model",
                      "From One Predictor to Many, and How Much Flexibility to Allow"))
add("\\begin{frame}\n  \\titlepage\n\\end{frame}\n\n")

# ============================ DAY 1 =======================================
add(adapt.section("Many predictors"))
add(r"""\begin{frame}{Day 1: where we left off}
\begin{itemize}
  \item Unit 5 fit a line and learned to read a slope, including what happens to it when another
        predictor joins the model.
  \item Now we build models with \emph{many} predictors and confront the question that decides
        whether any of it is real: \textbf{how well does this do on data it has never seen?}
  \item Three days: putting a model together, checking it honestly, and deciding how much
        flexibility the data can actually support.
\end{itemize}
\begin{principle}{the tension in one line}
A model that fits your data perfectly has told you nothing except what your data already said.
\end{principle}
\end{frame}

""")
add(f3["The tension at the heart of modeling"])
add(r"""\begin{frame}{What this unit gives you}
\begin{columns}[T]
\begin{column}{0.5\textwidth}
\textbf{Things to know}
\begin{itemize}\small
  \item multiple regression, and what ``holding the others fixed'' really means
  \item interactions and transformations
  \item multicollinearity, and what it does to coefficients
  \item overfitting, and why training error is not evidence
  \item cross-validation done correctly, including where leakage sneaks in
  \item regularization and trees: more flexibility, honestly measured
\end{itemize}
\end{column}
\begin{column}{0.5\textwidth}
\textbf{Mistakes to stop making}
\begin{itemize}\small
  \item judging a model by its fit to the training data
  \item chasing $R^2$
  \item preprocessing or selecting features outside the folds
  \item tuning on the test set and then reporting that score
  \item quoting $p$-values from a model built by variable search
  \item reading feature importance as a causal effect
\end{itemize}
\end{column}
\end{columns}
\end{frame}

""")
add(f3["Live experiment: trust, then verify"])
add(f3["First, let's ``verify'' on the same 10 people"])
add(f3["The honest test: people we held out"])
add(f3["From one predictor to many"])
add(f3["Interactions: when the effect of $x$ depends on something else"])
add(f3["Transformations: when straight lines don't fit"])
add(f3[r"Your turn \#1"])
add(f3[r"Your turn \#1: answer"])
add(f3["Multicollinearity: predictors that say the same thing"])
add(f3["How to recognize it, and what it means"])

# ============================ DAY 2 =======================================
add(adapt.section("Honest evaluation"))
add(adapt.day(2, "Judging a model honestly", [
    "overfitting: what it looks like and why $R^2$ cannot see it",
    "training error versus error on data the model has never seen",
    "cross-validation, and the three ways people accidentally cheat at it",
    "the one-standard-error rule: when to prefer the simpler model",
]))
add(f3["Overfitting: learning the noise"])
add(f3["Why $R^2$ alone will mislead you"])
add(f3["Training error vs new-data error"])
add(f11["The complexity curve, on real data"])
add(f11["K-fold cross-validation"])
add(f11["Doing cross-validation wrong"])
add(f11["The one-standard-error rule"])
add(f11[r"Your turn \#1"].replace(r"Your turn \#1", r"Your turn \#2"))
add(f11[r"Your turn \#1: answer"].replace(r"Your turn \#1", r"Your turn \#2"))
add(f3["Scenario: the R² jumped to 0.95"])

# ============================ DAY 3 =======================================
add(adapt.section("Flexibility"))
add(adapt.day(3, "How much flexibility can the data support?", [
    "trees: models that carve the space instead of drawing a line",
    "why searching for variables is itself a form of overfitting",
    "ridge and lasso: shrinking coefficients instead of choosing them",
    "ensembles, and why feature importance is not an effect",
]))
add(f11["What a tree does"])
add(f11["Three fits to the same 392 cars"])
add(f11["Searching for variables is a form of overfitting"])
add(f11["What that means for stepwise selection"])
add(f11["Regularization: shrink instead of choose"])
add(f11["The lasso path, on the cars data"])
add(f11["Why one tree is rarely enough"])
add(f11["Feature importance is not an effect"])
add(f11[r"Your turn \#2"].replace(r"Your turn \#2", r"Your turn \#3"))
add(f11[r"Your turn \#2: answer"].replace(r"Your turn \#2", r"Your turn \#3"))
add(f3["Predict vs.\\ explain: pick one on purpose"])

# ============================ WRAP ========================================
add(adapt.section("LLM check"))
add(f11["LLM check: mistake or not? (1 of 2)"])
add(f3["LLM check: mistake or not? (2 of 2)"])

add(adapt.section("Consolidate"))
add(f11["The arc of a modeling project"])
add(r"""\begin{frame}{The traps, all in one place}
\begin{trap}{the list worth carrying}
\begin{itemize}
  \item Judging a model on training error, or on $R^2$ alone.
  \item Preprocessing, imputing, or selecting features outside the folds.
  \item Choosing among many models by test-set score and then reporting that score.
  \item Quoting $p$-values from a model whose variables were chosen by search.
  \item Reading feature importance as a causal effect.
  \item Preferring the complex model when the simple one is within noise of it.
  \item Interpreting individual coefficients of two nearly identical predictors.
\end{itemize}
\end{trap}
\end{frame}

""")
add(r"""\begin{frame}{Ten questions to be able to answer}
\begin{enumerate}\small
  \item How do you know you are not overfitting?
  \item Your $R^2$ jumped when you added 20 features. Better model?
  \item What does $k$-fold cross-validation estimate, and what does it not?
  \item Give three ways leakage sneaks into a cross-validation.
  \item Two predictors are correlated. What happens to their coefficients?
  \item What does the lasso do that dropping variables by $p$-value does not?
  \item Why are $p$-values invalid after stepwise selection?
  \item Your forest beats your regression by 0.02 AUC. Which do you ship?
  \item What does a random forest's feature importance actually measure?
  \item Predict or explain: how does the answer change what you build?
\end{enumerate}
\end{frame}

""")
add(r"""\begin{frame}{Mastery checklist}
You have this unit when you can, from memory:
\begin{itemize}
  \item interpret a coefficient in a multiple regression, with the right caveat attached;
  \item explain interactions and transformations, and when each is called for;
  \item recognize multicollinearity and say what it does and does not ruin;
  \item draw the training-versus-honest-error curve and explain the gap;
  \item run cross-validation correctly, with every preprocessing step inside the fold;
  \item apply the one-standard-error rule and defend the simpler model;
  \item explain ridge and lasso as shrinkage, and why selection breaks $p$-values;
  \item state the limits of feature importance.
\end{itemize}
\end{frame}

""")
add(r"""\begin{frame}{Where we go next}
\begin{itemize}
  \item We now have models we can trust, judged on data they have never seen.
  \item \textbf{Unit 7} zooms all the way in on a single \textbf{prediction}: when the model
        hands you one number for one case, how wrong is it likely to be, and where does that
        error come from?
\end{itemize}
\begin{principle}{the habit to keep}
Flexibility is not the goal. Honesty about performance is. A simple model you can check beats a
complex one you cannot.
\end{principle}
\end{frame}

""")
add("\\end{document}\n")

s = "".join(out)
s = adapt.soften_green(s, keep=1)
s = s.replace(r"\begin{frame}{Where this fits}", r"\begin{frame}{Day 1: where this fits}")
adapt.save(s, adapt.OUT / "Unit_06_Building_and_Trusting_a_Model.tex")
