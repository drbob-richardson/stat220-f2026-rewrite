#!/usr/bin/env python3
"""Figures for Module 07: The Normal Distribution and the CLT."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

OUT = Path(__file__).resolve().parents[1] / "Slides"
DATA = Path(__file__).resolve().parents[2] / "data"
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(220)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
BLUE, RED, GREY = "#4878a8", "#c0392b", "#7f8c8d"

# --- 1. CLT: a badly skewed population averages into a bell ---------------
pop = rng.exponential(scale=1.0, size=400000) ** 1.6      # very right-skewed
fig, axes = plt.subplots(1, 4, figsize=(9.6, 2.6))
for ax, n in zip(axes, [1, 2, 10, 50]):
    means = pop[rng.integers(0, len(pop), size=(20000, n))].mean(axis=1)
    ax.hist(means, bins=60, color=BLUE, edgecolor="white", density=True)
    ax.set_title(f"$n = {n}$", fontsize=11)
    ax.set_yticks([])
    ax.set_xlim(0, np.percentile(means, 99.5))
axes[0].set_ylabel("sample means")
fig.suptitle("The population is wildly skewed; the average of it is not", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "fig_m07_clt.pdf")
plt.close(fig)

# --- 2. the 68-95-99.7 picture --------------------------------------------
x = np.linspace(-4, 4, 600)
y = stats.norm.pdf(x)
fig, ax = plt.subplots(figsize=(6.4, 3.2))
ax.plot(x, y, color="black", lw=1.8)
for k, c, lab in [(3, "#dbe6f0", "99.7%"), (2, "#9fc0dd", "95%"), (1, BLUE, "68%")]:
    m = np.abs(x) <= k
    ax.fill_between(x[m], y[m], color=c)
    ax.text(0 if k == 1 else (k - 0.5), 0.02 + 0.02 * k, lab, ha="center", fontsize=9,
            color="white" if k == 1 else "black")
ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
ax.set_xticklabels([r"$-3\sigma$", r"$-2\sigma$", r"$-1\sigma$", r"$\mu$",
                    r"$+1\sigma$", r"$+2\sigma$", r"$+3\sigma$"])
ax.set_yticks([])
ax.set_title("Everything you need to eyeball a normal distribution")
fig.tight_layout()
fig.savefig(OUT / "fig_m07_zrule.pdf")
plt.close(fig)

# --- 3. real data: is it normal? insurance charges vs a normal ------------
ins = pd.read_csv(DATA / "insurance_all.csv")
ch = ins["charges"].values
fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.2))
axes[0].hist(ch, bins=60, color=BLUE, edgecolor="white", density=True)
xs = np.linspace(ch.min(), ch.max(), 300)
axes[0].plot(xs, stats.norm.pdf(xs, ch.mean(), ch.std()), color=RED, lw=2,
             label="normal with the same\nmean and SD")
axes[0].set_xlabel("medical charges ($)")
axes[0].set_yticks([])
axes[0].legend(frameon=False, fontsize=8.5)
axes[0].set_title("Real charges are not normal", fontsize=10.5)

stats.probplot(ch, dist="norm", plot=axes[1])
axes[1].get_lines()[0].set_color(BLUE)
axes[1].get_lines()[0].set_markersize(2.5)
axes[1].get_lines()[1].set_color(RED)
axes[1].set_title("Q-Q plot: the tail peels away", fontsize=10.5)
axes[1].set_ylabel("observed charges")
fig.tight_layout()
fig.savefig(OUT / "fig_m07_realdata.pdf")
plt.close(fig)

# --- 4. heavy tails break the averaging argument --------------------------
fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.0))
for ax, (draws, title) in zip(axes, [
        (rng.normal(0, 1, 5000), "Well-behaved: the average settles"),
        (rng.standard_cauchy(5000), "Heavy tail: it never does")]):
    run = np.cumsum(draws) / np.arange(1, len(draws) + 1)
    ax.plot(run, color=BLUE, lw=1.2)
    ax.axhline(0, color=RED, ls="--", lw=1.2)
    ax.set_xlabel("observations")
    ax.set_title(title, fontsize=10.5)
axes[0].set_ylabel("running average")
fig.tight_layout()
fig.savefig(OUT / "fig_m07_heavytail.pdf")
plt.close(fig)

# --- 5. how big must n be? skew determines it ------------------------------
fig, axes = plt.subplots(1, 3, figsize=(9.0, 2.7))
pops = {
    "coin flips (0/1)": lambda k: rng.integers(0, 2, k),
    "mildly skewed": lambda k: rng.exponential(1, k),
    "one in a hundred": lambda k: (rng.random(k) < 0.01).astype(float),
}
for ax, (name, gen) in zip(axes, pops.items()):
    means = gen(30 * 20000).reshape(20000, 30).mean(axis=1)
    ax.hist(means, bins=40, color=BLUE, edgecolor="white", density=True)
    ax.set_title(f"{name}\nmeans of $n=30$", fontsize=10)
    ax.set_yticks([])
fig.tight_layout()
fig.savefig(OUT / "fig_m07_howbig.pdf")
plt.close(fig)

print("wrote module 07 figures to", OUT)
