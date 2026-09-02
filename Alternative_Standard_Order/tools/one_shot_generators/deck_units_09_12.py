#!/usr/bin/env python3
"""Decks for Units 9-12: adapt Modules 12-15 into 3-day units."""
import adapt

# =====================================================================
# UNIT 9 --- Causal Thinking (from Module 12)
# =====================================================================
s, out = adapt.load("Module_12_Causal_Thinking.tex", "Unit_09_Causal_Thinking.tex")
s = adapt.preamble(s)
s = adapt.subtitle(s, 9, "From ``What Goes With What'' to ``What Happens If We Change It''")
s = adapt.soften_green(s, keep=1)
s = s.replace(r"\begin{frame}{Where this fits}", r"\begin{frame}{Day 1: where this fits}")
s = adapt.contract(s, know=[
    r"what a causal effect is, in terms of what would have happened otherwise",
    r"why randomization works, and precisely what it buys",
    r"what a confounder is, and why you must control for it",
    r"what a collider is, and why controlling for it is a disaster",
    r"what a mediator is, and when controlling for it answers the wrong question",
    r"the main quasi-experimental designs and the assumption each one leans on",
], avoid=[
    r"reading a regression coefficient as the effect of intervening",
    r"controlling for a collider or for a variable on the causal path",
    r"comparing volunteers to non-volunteers and calling it an effect",
    r"ignoring who selected into the dataset",
    r"treating a before-and-after change as an effect with no control group",
    r"forgetting that the treatment might be caused by the outcome",
])
s = adapt.insert_before(s, r"\begin{frame}{The three roles a third variable can play}",
    adapt.day(2, "Which variables to control, and which to leave alone", [
        "confounder, collider, mediator: three roles, three different rules",
        "why ``control for everything you have'' is bad advice",
        "confounding you can watch happen in real data",
        "classifying a variable before you write the model",
    ]))
s = adapt.insert_before(s, r"\begin{frame}{The realistic situation}",
    adapt.day(3, "When you cannot randomize", [
        "matching, difference-in-differences, regression discontinuity, instruments",
        "the assumption each design is buying, and how to check it",
        "natural experiments: finding the accident that assigned treatment for you",
        "designing a rollout that produces a causal estimate for free",
    ]))
# A concrete "which control?" table, for students who need the rules explicit.
s = s.replace(r"\begin{frame}{Your turn \#1}", r"""\begin{frame}{The rules, in one table}
\begin{center}\small
\begin{tabular}{p{0.20\textwidth} p{0.30\textwidth} p{0.38\textwidth}}
\toprule
\textbf{Role} & \textbf{Structure} & \textbf{What to do} \\
\midrule
Confounder & causes both $X$ and $Y$ & \textbf{Control for it.} Leaving it out biases the estimate
in a direction you can often sign. \\
Collider & is caused by both $X$ and $Y$ & \textbf{Never control for it}, and never select your
sample on it. Controlling creates an association from nothing. \\
Mediator & $X$ causes it, it causes $Y$ & \textbf{Leave it out} for the total effect. Include it
only if you deliberately want the effect through some \emph{other} channel. \\
\bottomrule
\end{tabular}
\end{center}
\vspace{0.4em}
\begin{principle}{the order of operations}
Decide the role from what you believe about the world, \emph{then} write the model. You cannot
read the role off a correlation matrix, and the fit will not tell you either.
\end{principle}
\end{frame}

\begin{frame}{Your turn \#1}""")
s = adapt.question_bank(s, [
    "Users of feature X retain better. Should we push everyone onto it?",
    "Why does randomization work, and what does it fail to fix?",
    "Should you control for every variable you have? Explain with an example.",
    "What is a collider, and give a case where selecting on one misled someone?",
    "When would controlling for a variable be actively harmful?",
    "We cannot run an experiment. What are the options, and what does each assume?",
    "How would you check the parallel-trends assumption?",
    "Ad spend and sales correlate at 0.8. What do you conclude?",
    "Our program's participants improved 18\\%. What do you ask first?",
    "How would you design a rollout so it produces a causal estimate for free?",
])
s = adapt.consolidate_headings(s)
s = s.replace(r"""  \item We have been treating the data as the only source of information. Next part:
        \textbf{Bayesian reasoning}, where prior knowledge enters the estimate explicitly, and
        decisions are made by weighing outcomes rather than by rejecting a null.""",
r"""  \item We have been treating the data as the only source of information. \textbf{Unit 10} lets
        prior knowledge enter the estimate explicitly, and makes decisions by weighing outcomes
        rather than by rejecting a null.""")
adapt.save(s, out)


# =====================================================================
# UNIT 10 --- Bayesian Reasoning and Decisions (from Module 13)
# =====================================================================
s, out = adapt.load("Module_13_Bayesian_Reasoning_and_Decisions.tex",
                    "Unit_10_Bayesian_Reasoning_and_Decisions.tex")
s = adapt.preamble(s)
s = adapt.subtitle(s, 10, "Updating Beliefs, and Acting on Them")
s = adapt.soften_green(s, keep=1)
s = s.replace(r"\begin{frame}{Where this fits}", r"\begin{frame}{Day 1: where this fits}")
s = adapt.contract(s, know=[
    r"probability as a degree of belief, and when that reading is the useful one",
    r"prior, likelihood, and posterior, and how they combine",
    r"why the prior matters with little data and washes out with plenty",
    r"what a credible interval says, and how it differs from a confidence interval",
    r"why Bayesian estimates shrink small groups automatically",
    r"how to turn a posterior into a decision using costs",
], avoid=[
    r"pretending you have no prior when you obviously do",
    r"letting a strong prior drive a conclusion the data cannot support",
    r"reading a 95\% confidence interval as a 95\% probability statement",
    r"treating a high posterior probability as proof rather than as a bet",
    r"forgetting that Bayes assumes your \emph{model} is right",
    r"reporting a posterior without saying which prior produced it",
])
s = adapt.insert_before(s, r"\begin{frame}{``Isn't the prior just making things up?''}",
    adapt.day(2, "Priors, and how much they matter", [
        "where priors come from, and how to defend one",
        "sensitivity analysis: reporting the answer under a skeptic's prior too",
        "credible intervals versus confidence intervals, stated precisely",
        "shrinkage as a free consequence of using a prior",
    ]))
s = adapt.insert_before(s, r"\begin{frame}{A Bayesian A/B test}",
    adapt.day(3, "From belief to decision", [
        "a Bayesian A/B test, and the question it answers that a p-value does not",
        "expected loss: what it costs to be wrong, and why it beats a threshold",
        "the value of information, and when a study is worth nothing",
        "when to stop a test, and the trap that Bayesian methods do \\emph{not} remove",
    ]))
s = adapt.question_bank(s, [
    "Explain prior, likelihood, and posterior with an example from your own work.",
    "What is the probability variant B is better, and how is that different from a $p$-value?",
    "Is choosing a prior unscientific? Defend your practice.",
    "Credible interval versus confidence interval: state both precisely.",
    "We have 12 observations from a new market. How do you estimate the rate?",
    "How do you turn a posterior into a ship-or-not decision?",
    "What is expected loss, and why report it alongside a probability?",
    "Can you peek at a Bayesian test whenever you like? Explain carefully.",
    "How much is a market study worth, and when is it worth nothing?",
    "A colleague reports a 240\\% lift from 60 users. What is your posterior?",
])
s = adapt.consolidate_headings(s)
adapt.save(s, out)


# =====================================================================
# UNIT 11 --- Where the Data Comes From (from Module 14)
# =====================================================================
s, out = adapt.load("Module_14_Where_the_Data_Comes_From.tex",
                    "Unit_11_Where_the_Data_Comes_From.tex")
s = adapt.preamble(s)
s = adapt.subtitle(s, 11, "Sampling, Selection, and Missingness")
s = adapt.soften_green(s, keep=1)
s = s.replace(r"\begin{frame}{Where this fits}", r"\begin{frame}{Day 1: where this fits}")
s = adapt.contract(s, know=[
    r"the difference between a population, a sampling frame, and a sample",
    r"the main sampling designs and what each one buys you",
    r"how selection bias arises, including survivorship and nonresponse",
    r"why a large biased sample can be worse than a small random one",
    r"what missing data does, and the three ways it can be missing",
    r"why measurement choices are modeling choices",
], avoid=[
    r"treating sample size as evidence of representativeness",
    r"studying only the survivors, winners, or responders",
    r"dropping rows with missing values without asking why they are missing",
    r"imputing the mean and then reporting the resulting tighter interval",
    r"accepting a proxy variable as if it were the concept you meant",
    r"quoting a margin of error that only accounts for sampling error",
])
s = adapt.insert_before(s, r"\begin{frame}{Missing values in real data}",
    adapt.day(2, "Missing data, and what it hides", [
        "the three missingness mechanisms, and what dropping rows does under each",
        "values missing in disguise: zeros, $-1$, 999, and empty strings",
        "why mean imputation manufactures precision that does not exist",
        "when the fact that a value is missing is itself the best predictor",
    ]))
s = adapt.insert_before(s, r"\begin{frame}{You measure a proxy, not the concept}",
    adapt.day(3, "Measurement, and the questions to ask first", [
        "every column is a proxy for something you actually care about",
        "instrument drift, question wording, and definition changes",
        "Goodhart's law: what happens once a proxy becomes a target",
        "the provenance checklist to run before you model anything",
    ]))
s = adapt.question_bank(s, [
    "We have 40 million records. Is that representative?",
    "Our response rate was 8\\%. What can we conclude?",
    "Explain survivorship bias with an example from business.",
    "What do you do about missing values, and what do you check first?",
    "What is the difference between undercoverage and nonresponse?",
    "When would a sample of 1{,}000 beat a sample of 10 million?",
    "How would you design a sample to estimate this on a fixed budget?",
    "Our metric jumped on March 3. What do you check before explaining it?",
    "What is the risk of using clicks as a proxy for engagement?",
    "Why can a model trained on past hiring decisions be unfair with no protected attributes?",
])
s = adapt.consolidate_headings(s)
s = s.replace(r"""  \item That is the full toolkit: probability, estimation, inference, models, prediction,
        classification, causality, and the data behind all of it.
  \item The last part puts it together the way it will actually be tested: \textbf{messy scenarios,
        out loud, under time pressure}, which is to say, an interview.""",
r"""  \item That is the full toolkit: probability, estimation, inference, models, prediction,
        classification, causality, and now the data underneath all of it.
  \item \textbf{Unit 12} puts it together the way it actually shows up: messy scenarios, out
        loud, under time pressure, with somebody waiting on a decision.""")
adapt.save(s, out)


# =====================================================================
# UNIT 12 --- Putting It Together (from Module 15)
# =====================================================================
s, out = adapt.load("Module_15_Putting_It_Together.tex", "Unit_12_Putting_It_Together.tex")
s = adapt.preamble(s)
s = adapt.subtitle(s, 12, "Messy Questions, Answered Out Loud")
s = adapt.soften_green(s, keep=0)
s = s.replace(r"\begin{frame}{Where this fits}", r"\begin{frame}{Day 1: where this fits}")

# This deck has a one-frame contract already; rewrite it without the (a)/(b)/(c) scaffolding.
s = adapt.replace_frame(s, "The learning contract for this part", r"""\begin{frame}{What this unit is}
\begin{itemize}
  \item No new mathematics. Everything here is a tool you already have; the work is choosing which
        one, fast, on a problem stated badly by someone who is not a statistician.
  \item Day 1 builds the reusable answer structure and the checklist. Day 2 runs six full
        scenarios. Day 3 is the bracket, where you do it out loud.
  \item The scenarios come from every unit at once, and none of them announce which unit they came
        from. That is the point.
\end{itemize}
\end{frame}
""")
s = adapt.insert_before(s, r"\begin{frame}{Scenario 1: the metric that jumped}",
    adapt.day(2, "Six scenarios, worked", [
        "a metric that jumped, a model that looks too good, a subgroup that shines",
        "a comparison that is really selection, a survey nobody answered, a forecast with no range",
        "for each: what you ask, what you compute, and what would change your mind",
    ]))
s = adapt.insert_before(s, r"\begin{frame}{Translating for a non-technical audience}",
    adapt.day(3, "Saying it out loud", [
        "translating for a non-technical audience without hiding the uncertainty",
        "what to say when you genuinely do not know",
        "the interview bracket: two minutes per scenario, scored on the five beats",
        "the master trap list and the final question bank",
    ]))
adapt.save(s, out)
