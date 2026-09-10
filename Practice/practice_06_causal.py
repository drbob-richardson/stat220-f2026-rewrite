#!/usr/bin/env python3
"""Unit 6 practice, multiple choice with answers inline. STUDENT-FACING."""
from build_questions import build_mc

build_mc("Causal", "Causal Claims and Where the Data Came From",
"""Practice on what a causal claim requires, the three roles a third variable can play, and how
the way data was collected plants patterns nobody put there. No computer needed.""",
[
("What does randomization actually buy you?",
 ["A representative sample of the population.",
  "Groups that are comparable on everything, including the variables you never thought to "
  "measure.",
  "A larger effect size.",
  "Freedom from measurement error."],
 1,
 "Randomization balances the unmeasured just as well as the measured, which is the part no "
 "amount of statistical control can reproduce. Note that it does not make your sample "
 "representative. A randomized trial on volunteers gives a clean comparison within a group that "
 "may look nothing like the population you care about."),

("A variable affects both your predictor and your outcome. What is it, and what do you do?",
 ["A collider, and you should control for it.",
  "A confounder, and you should control for it.",
  "A mediator, and you should leave it out.",
  "A proxy, and you should replace it."],
 1,
 "This is the classic case and the one most people already have in mind. Income affects both "
 "whether someone buys organic food and how healthy they are, so a raw comparison of organic "
 "buyers to everyone else is partly a comparison of richer people to poorer ones. Controlling for "
 "it removes that distortion."),

("Why is controlling for a collider harmful?",
 ["It removes too much of the real effect.",
  "It creates an association between two variables that were not related to begin with.",
  "It inflates the standard errors.",
  "It has no effect, so it wastes a degree of freedom."],
 1,
 "A collider is a common consequence of two variables. Conditioning on it means comparing cases "
 "that reached the same outcome by different routes, so being low on one cause forces you to be "
 "high on the other. The association appears out of nothing, and it appears strongest when you "
 "have been most careful to control for everything available."),

("You want the effect of exercise on heart disease and you control for cholesterol, which "
 "exercise lowers. What have you done?",
 ["Removed a confounder correctly.",
  "Controlled for a mediator, so you removed part of the very effect you were measuring.",
  "Conditioned on a collider.",
  "Nothing, since cholesterol is a legitimate predictor."],
 1,
 "Cholesterol sits on the causal path between exercise and heart disease. Holding it fixed asks "
 "what exercise does other than by changing cholesterol, which is a real question but almost "
 "never the one being asked. The reported effect shrinks, and it looks like exercise matters less "
 "than it does."),

("Among admitted students, test scores and essay quality are negatively correlated, though they "
 "are unrelated in the applicant pool. Why?",
 ["Admissions officers trade one off against the other deliberately.",
  "Getting admitted requires being strong on at least one, so within the admitted group a weak "
  "score implies a strong essay.",
  "Test scores and essays measure the same underlying ability.",
  "The sample of admitted students is too small."],
 1,
 "Admission is a common consequence of both, so conditioning on it is conditioning on a collider. "
 "Restaurants you have heard of are good at food or location, and hospitalized patients have some "
 "serious condition, which is why unrelated diseases look connected among them. Same mechanism "
 "every time."),

("A study of successful companies finds they all took big risks, and concludes risk-taking causes "
 "success. What is missing?",
 ["A larger sample of successful companies.",
  "The companies that took big risks and failed, who are not in the data.",
  "A control for company size.",
  "Statistical significance testing."],
 1,
 "This is survivorship bias, which is the collider wearing different clothes. The sample was "
 "assembled by conditioning on the outcome, so any trait common among risk-takers who survived "
 "will look like a cause of survival. The question that catches it is always the same: who is "
 "missing from this table, and what did it take to get in?"),

("A survey gets 2 million responses with a 3\\% response rate. A different survey gets 1{,}200 "
 "responses from a proper random sample. Which do you trust?",
 ["The 2 million, since sampling error is far smaller.",
  "The 1{,}200, since a large biased sample estimates the wrong number very precisely.",
  "Both equally, since they measure the same thing.",
  "Neither, both are too small."],
 1,
 "Sample size shrinks the noise around whatever the sample is measuring. It does nothing about "
 "the sample measuring the wrong quantity. The 3\\% who chose to respond differ from the 97\\% "
 "who did not, and that gap does not close as more of the same kind of person responds. The huge "
 "sample gives you a tight interval centered in the wrong place."),

("A clinical dataset records blood pressure as 0 for 14\\% of patients. What is the likely "
 "problem?",
 ["Those patients had unusually low blood pressure.",
  "Zero is standing in for missing, and treating it as a real value will drag every summary "
  "downward.",
  "The data should be rescaled.",
  "Those rows should be deleted without further thought."],
 1,
 "A blood pressure of zero is not a measurement, it is a placeholder. Averaging them in pulls the "
 "mean toward zero and shrinks the apparent variance. Recode them as missing first. Whether to "
 "then drop or impute depends on why they are missing, which is a separate question worth asking "
 "before you decide."),

("When is dropping rows with missing values safe?",
 ["Always, since it is the simplest option.",
  "When the reason for missingness is unrelated to the outcome you are studying.",
  "Whenever fewer than 10\\% of rows are affected.",
  "Never."],
 1,
 "If a sensor failed at random, the rows you keep are still a fair sample and you have only lost "
 "power. If people with the worst outcomes are the ones who dropped out, the rows you keep are a "
 "biased sample and every result is shifted. The percentage missing does not tell you which "
 "situation you are in. Only knowing why does."),

("You cannot randomize, but a policy took effect in one state and not a neighboring one. What "
 "does difference in differences assume?",
 ["That the two states were identical before the policy.",
  "That without the policy, the two states' outcomes would have moved in parallel.",
  "That the policy was assigned at random.",
  "That the outcome was stable over time."],
 1,
 "The two states are allowed to differ in level, which is the whole point of using each as its "
 "own baseline. What has to hold is that their trends would have tracked each other absent the "
 "policy. That assumption is not testable directly, though checking whether the trends ran "
 "parallel for several years beforehand is the standard way to make it credible."),
])
