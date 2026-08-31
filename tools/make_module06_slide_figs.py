#!/usr/bin/env python3
"""Figures for Module 06: Random Variables and Expectation."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

OUT = Path(__file__).resolve().parents[1] / "Slides"
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(220)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
BLUE, RED, GREY = "#4878a8", "#c0392b", "#7f8c8d"

# --- 1. four distributions, four stories ----------------------------------
fig, axes = plt.subplots(2, 2, figsize=(7.8, 4.4))
k = np.arange(0, 16)
axes[0, 0].bar(k, stats.binom.pmf(k, 15, 0.3), color=BLUE)
axes[0, 0].set_title("Binomial: how many of $n$ tries succeed", fontsize=10)
axes[0, 0].set_xlabel("purchases out of 15 visitors")

k2 = np.arange(0, 13)
axes[0, 1].bar(k2, stats.poisson.pmf(k2, 3.2), color=BLUE)
axes[0, 1].set_title("Poisson: how many events in a window", fontsize=10)
axes[0, 1].set_xlabel("support tickets per hour")

x = np.linspace(0, 6, 300)
axes[1, 0].plot(x, stats.expon.pdf(x, scale=1.2), color=BLUE, lw=2)
axes[1, 0].fill_between(x, stats.expon.pdf(x, scale=1.2), color=BLUE, alpha=0.18)
axes[1, 0].set_title("Exponential: how long until the next one", fontsize=10)
axes[1, 0].set_xlabel("hours until next ticket")

x2 = np.linspace(-4, 4, 300)
axes[1, 1].plot(x2, stats.norm.pdf(x2), color=BLUE, lw=2)
axes[1, 1].fill_between(x2, stats.norm.pdf(x2), color=BLUE, alpha=0.18)
axes[1, 1].set_title("Normal: a sum of many small pushes", fontsize=10)
axes[1, 1].set_xlabel("deviation from the mean")
for a in axes.ravel():
    a.set_yticks([])
fig.tight_layout()
fig.savefig(OUT / "fig_m06_dists.pdf")
plt.close(fig)

# --- 2. the flaw of averages (Jensen) -------------------------------------
demand = np.array([20, 100])          # two equally likely demands
capacity = 60
x = np.linspace(0, 130, 300)
# profit: sell min(demand, capacity) at 10, pay 4 per unit of capacity
profit = np.minimum(x, capacity) * 10 - capacity * 4
fig, ax = plt.subplots(figsize=(6.4, 3.4))
ax.plot(x, profit, color=BLUE, lw=2.4, label="profit as a function of demand")
p_each = np.minimum(demand, capacity) * 10 - capacity * 4
ax.plot(demand, p_each, "o", color=RED, ms=8, label="the two possible demands")
ax.plot([60], [np.minimum(60, capacity) * 10 - capacity * 4], "s", color="black", ms=8,
        label="profit at the average demand")
ax.plot([60], [p_each.mean()], "D", color=RED, ms=8, label="average of the two profits")
ax.annotate("", xy=(60, p_each.mean()), xytext=(60, np.minimum(60, capacity) * 10 - capacity * 4),
            arrowprops=dict(arrowstyle="<->", color=GREY))
ax.text(63, (p_each.mean() + 360) / 2, "the gap:\nplanning on the average\noverstates profit",
        fontsize=9, color=GREY)
ax.set_xlabel("demand (units)")
ax.set_ylabel("profit ($)")
ax.legend(fontsize=8.5, loc="lower right", frameon=False)
ax.set_title("Profit at the average demand is not the average profit")
fig.tight_layout()
fig.savefig(OUT / "fig_m06_flaw.pdf")
plt.close(fig)

# --- 3. pooling: sd of the average shrinks like sqrt(n) --------------------
n = np.arange(1, 101)
fig, ax = plt.subplots(figsize=(6.0, 3.2))
ax.plot(n, 1 / np.sqrt(n), color=BLUE, lw=2.4, label="independent risks")
rho = 0.2
ax.plot(n, np.sqrt(rho + (1 - rho) / n), color=RED, lw=2.4, ls="--",
        label="risks correlated at 0.2")
ax.axhline(np.sqrt(rho), color=RED, lw=1, ls=":")
ax.text(62, np.sqrt(rho) + 0.03, "a floor you cannot diversify away", fontsize=9, color=RED)
ax.set_xlabel("number of pooled cases $n$")
ax.set_ylabel("SD of the average")
ax.legend(frameon=False, fontsize=9)
ax.set_title("Averaging kills noise, but only if the pieces are independent")
fig.tight_layout()
fig.savefig(OUT / "fig_m06_pooling.pdf")
plt.close(fig)

# --- 4. skew: the mean is not the typical case ----------------------------
income = rng.lognormal(mean=10.6, sigma=0.85, size=20000)
fig, ax = plt.subplots(figsize=(6.2, 3.2))
ax.hist(income[income < 400000], bins=80, color=BLUE, alpha=0.75, edgecolor="white")
ax.axvline(np.median(income), color="black", lw=2, label=f"median = ${np.median(income):,.0f}")
ax.axvline(income.mean(), color=RED, lw=2, label=f"mean = ${income.mean():,.0f}")
ax.set_xlabel("household income ($)")
ax.set_yticks([])
ax.legend(frameon=False, fontsize=9)
ax.set_title("With skew, nobody earns the average")
fig.tight_layout()
fig.savefig(OUT / "fig_m06_skew.pdf")
plt.close(fig)

print("wrote module 06 figures to", OUT)
