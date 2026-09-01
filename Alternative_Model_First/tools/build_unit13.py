#!/usr/bin/env python3
"""Code companion for Unit 13 (optional): Choosing a Model.

Run from the Alternative_Model_First folder:
    python tools/build_unit13.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nblib import CodeNB

nb = CodeNB(
    unit=13,
    title="Choosing a Model",
    blurb="Optional unit. How much flexibility your data can pay for, and how to "
          "choose a model family out loud, before you see the answer.",
)

nb.section("Setup")
nb.code("""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression, LassoCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_score, learning_curve, train_test_split

rng = np.random.default_rng(0)
cars = pd.read_csv("https://richardson.byu.edu/220/cars.csv").dropna()
print(cars.shape)
cars.head(3)
""")

nb.section(
    "1. The live demo: commit before you see the test set",
    "In class you picked a polynomial degree without seeing the held-out points. "
    "This is that demo. Change `class_picks` to whatever the room actually chose.",
)
nb.code("""
# 14 points everyone sees, 10 held out that nobody sees until the reveal.
sub = cars.sample(24, random_state=7)
seen, held = sub.iloc[:14], sub.iloc[14:]
x_seen, y_seen = seen[["weight"]].values, seen["mpg"].values
x_held, y_held = held[["weight"]].values, held["mpg"].values

class_picks = [1, 2, 3, 5, 8, 9]      # <- replace with the degrees the teams held up

def fit(d, x, y):
    m = make_pipeline(PolynomialFeatures(d), StandardScaler(), LinearRegression())
    return m.fit(x, y)

rows = []
for d in class_picks:
    m = fit(d, x_seen, y_seen)
    rows.append({
        "degree": d,
        "training error": np.mean((m.predict(x_seen) - y_seen) ** 2),
        "held-out error": np.mean((m.predict(x_held) - y_held) ** 2),
    })
board = pd.DataFrame(rows)
print("Leaderboard on the data everyone could see:")
print(board.sort_values("training error")[["degree", "training error"]].to_string(index=False))
""")
nb.md("Now the reveal. Same teams, same fits, the 10 points they never saw.")
nb.code("""
print("Leaderboard on the held-out points:")
print(board.sort_values("held-out error")[["degree", "held-out error"]].to_string(index=False))

grid = np.linspace(x_seen.min(), x_seen.max(), 300).reshape(-1, 1)
fig, ax = plt.subplots(figsize=(7, 4))
for d in class_picks:
    ax.plot(grid, fit(d, x_seen, y_seen).predict(grid), lw=1.4, label=f"degree {d}")
ax.scatter(x_seen, y_seen, color="black", zorder=5, label="the 14 you saw")
ax.scatter(x_held, y_held, color="red", marker="x", s=70, zorder=5, label="the 10 held out")
ax.set_ylim(y_seen.min() - 12, y_seen.max() + 12)
ax.set_xlabel("weight"); ax.set_ylabel("mpg"); ax.legend(fontsize=8, frameon=False)
plt.show()
""")

nb.section(
    "2. Why the curve is U-shaped",
    "Bias and variance are not metaphors. Both are computable if you simulate, because "
    "simulating means you know the truth.",
)
nb.code("""
truth = lambda x: 3.0 / (1 + np.exp(-3.2 * (x - 0.4))) + 0.45 * x
SD, XT = 0.6, np.linspace(-3, 3, 800)
YT = truth(XT)
degrees = range(1, 9)

def curves(n, reps=300, seed=1):
    r = np.random.default_rng(seed)
    P = np.zeros((len(list(degrees)), reps, len(XT)))
    for i in range(reps):
        x = r.uniform(-3, 3, n)
        y = truth(x) + r.normal(0, SD, n)
        for j, d in enumerate(degrees):
            P[j, i] = fit(d, x.reshape(-1, 1), y).predict(XT.reshape(-1, 1))
    return P

P = curves(n=60)
bias2 = ((P.mean(axis=1) - YT) ** 2).mean(axis=1)
var = P.var(axis=1).mean(axis=1)
out = pd.DataFrame({"degree": list(degrees), "bias^2": bias2.round(4),
                    "variance": var.round(4), "total": (bias2 + var).round(4)})
print(out.to_string(index=False))
print("\\nbest degree:", out.loc[out['total'].idxmin(), 'degree'])
""")
nb.md("Bias falls the whole way. Variance rises the whole way. Only the sum has a minimum.")

nb.section(
    "3. Can you afford the truth?",
    "The true curve is fixed. Only the number of rows changes. Watch the best degree move.",
)
nb.code("""
for n in (20, 50, 300):
    P = curves(n=n, reps=250, seed=3)
    err = np.median(((P - YT) ** 2).mean(axis=2), axis=1)
    best = list(degrees)[int(np.argmin(err))]
    print(f"n = {n:>3}   best degree = {best}   "
          f"cost of degree 8 relative to best = {err[-1] / err.min():.1f}x")
""")

nb.section(
    "4. Choosing honestly: the same folds for every family",
    "Comparing families only means something when they face identical folds.",
)
nb.code("""
preds = ["weight", "displacement", "horsepower", "acceleration", "model_year", "cylinder"]
X, y = cars[preds].values, cars["mpg"].values
folds = KFold(5, shuffle=True, random_state=0)          # ONE fold object, reused

candidates = {
    "linear regression": make_pipeline(StandardScaler(), LinearRegression()),
    "lasso (CV-tuned)": make_pipeline(StandardScaler(), LassoCV(cv=5, random_state=0)),
    "random forest": RandomForestRegressor(n_estimators=300, random_state=0),
}
for name, model in candidates.items():
    s = -cross_val_score(model, X, y, cv=folds, scoring="neg_mean_squared_error")
    se = s.std(ddof=1) / np.sqrt(len(s))
    print(f"  {name:<20} CV MSE = {s.mean():6.2f}   SE = {se:4.2f}")
""")
nb.md("**The one-standard-error rule.** If two families land within one SE of each other they are "
      "not distinguishable on this data, and you take the simpler one. Notice that the rule does "
      "*not* fire here: the forest wins by several times its standard error, so this is a real "
      "gap, not noise. That is the signal to go find what the forest is using.")

nb.section(
    "5. Would more data help?",
    "A learning curve answers the question the complexity table raises: is the ceiling "
    "here your model, or your sample size?",
)
nb.code("""
sizes, train_sc, test_sc = learning_curve(
    RandomForestRegressor(n_estimators=200, random_state=0), X, y,
    train_sizes=np.linspace(0.1, 1.0, 8), cv=folds, scoring="neg_mean_squared_error")

fig, ax = plt.subplots(figsize=(6.5, 3.6))
ax.plot(sizes, -train_sc.mean(axis=1), "o-", label="training error")
ax.plot(sizes, -test_sc.mean(axis=1), "s-", label="cross-validated error")
ax.set_xlabel("training rows used"); ax.set_ylabel("MSE"); ax.legend(frameon=False)
plt.show()
print("Still falling at the right edge means more data would still buy you something.")
""")

nb.section(
    "6. The trap: importance is not an effect",
    "Weight and displacement are nearly the same variable. Watch what that does to a ranking "
    "people routinely report as though it were a list of causes.",
)
nb.code("""
from collections import Counter

print("correlation between weight and displacement:",
      round(np.corrcoef(cars['weight'], cars['displacement'])[0, 1], 3))

# Resample the ROWS, which is the instability that actually matters.
tops, shares = [], []
r = np.random.default_rng(0)
for b in range(40):
    idx = r.integers(0, len(y), len(y))
    f = RandomForestRegressor(n_estimators=200, random_state=b).fit(X[idx], y[idx])
    s = pd.Series(f.feature_importances_, index=preds)
    tops.append(s.idxmax()); shares.append(s)

print("\\nMost important variable, across 40 bootstrap resamples:")
for k, v in Counter(tops).most_common():
    print(f"  {k:<14} won {v:>2} times")

S = pd.DataFrame(shares)
print("\\nImportance share, mean and range:")
for c in preds:
    print(f"  {c:<14} {S[c].mean():.3f}   [{S[c].min():.3f}, {S[c].max():.3f}]")
""")
nb.md("Four different variables take the top spot depending on which rows you happened to draw, "
      "and weight's share swings from 0.07 to 0.48. Now watch the two twins split credit.")
nb.code("""
full = RandomForestRegressor(n_estimators=300, random_state=0).fit(X, y)
keep = [p for p in preds if p != "displacement"]
dropped = RandomForestRegressor(n_estimators=300, random_state=0).fit(cars[keep].values, y)

print(f"weight importance, displacement present: {full.feature_importances_[0]:.3f}")
print(f"weight importance, displacement dropped: {dropped.feature_importances_[0]:.3f}")
""")
nb.md("Weight did not become a more important cause of fuel economy when we deleted a column. "
      "Its score went up because it stopped sharing credit with its twin. This is why an "
      "importance score is not something you report as a risk factor.")

nb.section("What to take away")
nb.md("""
1. Flexibility is bought with sample size. Check the ratio before you check the algorithm.
2. Bias falls and variance rises. Only their sum has a minimum, and cross-validation finds it.
3. Compare families on identical folds, and break ties toward the simpler model.
4. A learning curve tells you whether your ceiling is the model or the data.
5. Importance scores rank correlated variables close to arbitrarily. They are not effects.
""")

out = Path(__file__).resolve().parents[1] / "Notebooks" / "Code_Unit13_Choosing_a_Model.ipynb"
nb.write(out)
print("wrote", out)
