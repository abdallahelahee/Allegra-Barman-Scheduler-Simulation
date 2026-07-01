#!/usr/bin/env python3
"""
analyse.py  —  Allegra the Barman: Scheduling Metrics Analysis
Reads results/FCFS.csv, SJF.csv, PRIORITY.csv, MLFQ.csv
Produces summary statistics + graphs saved to results/
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

SCHEDULERS   = ["FCFS", "SJF", "PRIORITY", "MLFQ"]
COLOURS      = {"FCFS": "#4C72B0", "SJF": "#DD8452",
                "PRIORITY": "#55A868", "MLFQ": "#C44E52"}
METRICS      = ["waitingTime", "turnaroundTime", "responseTime"]
METRIC_LABELS = {
    "waitingTime":    "Waiting Time (ms)",
    "turnaroundTime": "Turnaround Time (ms)",
    "responseTime":   "Response Time (ms)",
}
OUT = "results"

# ── Load ─────────────────────────────────────────────────────────────────────
dfs = {}
for s in SCHEDULERS:
    path = os.path.join(OUT, f"{s}.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing {path} — run run_experiments.sh first.")
    dfs[s] = pd.read_csv(path)
    print(f"Loaded {s}: {len(dfs[s])} orders")

# ── Summary stats ─────────────────────────────────────────────────────────────
print("\n=== Per-Order Metric Summary (ms) ===")
rows = []
for s in SCHEDULERS:
    for m in METRICS:
        col = dfs[s][m]
        rows.append({
            "scheduler": s, "metric": m,
            "mean":   round(col.mean(), 1),
            "median": round(col.median(), 1),
            "std":    round(col.std(), 1),
            "min":    round(col.min(), 1),
            "max":    round(col.max(), 1),
            "p95":    round(col.quantile(0.95), 1),
        })
summary = pd.DataFrame(rows)
print(summary.to_string(index=False))
summary.to_csv(os.path.join(OUT, "summary_stats.csv"), index=False)

# ── Per-patron total waiting time ─────────────────────────────────────────────
print("\n=== Per-Patron Total Waiting Time ===")
patron_rows = []
for s in SCHEDULERS:
    per_patron = dfs[s].groupby("patron")["waitingTime"].sum()
    patron_rows.append({
        "scheduler": s,
        "mean":   round(per_patron.mean(), 1),
        "median": round(per_patron.median(), 1),
        "std":    round(per_patron.std(), 1),
        "max":    round(per_patron.max(), 1),
    })
patron_summary = pd.DataFrame(patron_rows)
print(patron_summary.to_string(index=False))
patron_summary.to_csv(os.path.join(OUT, "patron_wait_summary.csv"), index=False)

# ── Fig 1: Box plots — distribution of all 3 metrics ─────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 6))
fig.suptitle("Per-Order Scheduling Metrics: Distribution Comparison",
             fontsize=14, fontweight="bold")
for ax, metric in zip(axes, METRICS):
    data = [dfs[s][metric].values for s in SCHEDULERS]
    bp   = ax.boxplot(data, patch_artist=True,
                      medianprops=dict(color="black", linewidth=2))
    for patch, s in zip(bp["boxes"], SCHEDULERS):
        patch.set_facecolor(COLOURS[s])
        patch.set_alpha(0.75)
    ax.set_xticklabels(SCHEDULERS, fontsize=11)
    ax.set_ylabel(METRIC_LABELS[metric], fontsize=11)
    ax.set_title(metric.replace("Time", " Time"), fontsize=12)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.set_ylim(0, 8000)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig1_boxplots.png"), dpi=150)
plt.close()
print("Saved fig1_boxplots.png")

# ── Fig 2: Mean & median bar chart ────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 6))
fig.suptitle("Mean vs Median Per-Order Metrics", fontsize=14, fontweight="bold")
x = np.arange(len(SCHEDULERS))
width = 0.35
for ax, metric in zip(axes, METRICS):
    means   = [dfs[s][metric].mean()   for s in SCHEDULERS]
    medians = [dfs[s][metric].median() for s in SCHEDULERS]
    ax.bar(x - width/2, means,   width, label="Mean",
           color=[COLOURS[s] for s in SCHEDULERS], alpha=0.85)
    ax.bar(x + width/2, medians, width, label="Median",
           color=[COLOURS[s] for s in SCHEDULERS], alpha=0.45, edgecolor="black")
    ax.set_xticks(x)
    ax.set_xticklabels(SCHEDULERS, fontsize=11)
    ax.set_ylabel(METRIC_LABELS[metric], fontsize=11)
    ax.set_title(metric.replace("Time", " Time"), fontsize=12)
    ax.legend(["Mean (solid)", "Median (faded)"], fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig2_mean_median.png"), dpi=150)
plt.close()
print("Saved fig2_mean_median.png")

# ── Fig 3: Per-patron total waiting time — fairness ───────────────────────────
fig, ax = plt.subplots(figsize=(8, 6))
patron_data = [dfs[s].groupby("patron")["waitingTime"].sum().values
               for s in SCHEDULERS]
bp = ax.boxplot(patron_data, patch_artist=True,
                medianprops=dict(color="black", linewidth=2))
for patch, s in zip(bp["boxes"], SCHEDULERS):
    patch.set_facecolor(COLOURS[s])
    patch.set_alpha(0.75)
ax.set_xticklabels(SCHEDULERS, fontsize=12)
ax.set_ylabel("Total Waiting Time per Patron (ms)", fontsize=12)
ax.set_title("Fairness: Distribution of Total Patron Waiting Time",
             fontsize=13, fontweight="bold")
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig3_patron_fairness.png"), dpi=150)
plt.close()
print("Saved fig3_patron_fairness.png")

# ── Fig 4: CDF of waiting time — predictability & tail ───────────────────────
fig, ax = plt.subplots(figsize=(9, 6))
for s in SCHEDULERS:
    vals = np.sort(dfs[s]["waitingTime"].values)
    cdf  = np.arange(1, len(vals) + 1) / len(vals)
    ax.plot(vals, cdf, label=s, color=COLOURS[s], linewidth=2)
ax.set_xlabel("Waiting Time (ms)", fontsize=12)
ax.set_ylabel("Cumulative Fraction of Orders", fontsize=12)
ax.set_title("CDF of Waiting Time — Predictability & Tail Behaviour",
             fontsize=13, fontweight="bold")
ax.legend(fontsize=11)
ax.grid(linestyle="--", alpha=0.4)
ax.set_xlim(0, 15000)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig4_cdf_waiting.png"), dpi=150)
plt.close()
print("Saved fig4_cdf_waiting.png")

# ── Fig 5: Std dev per scheduler — predictability summary ────────────────────
fig, axes = plt.subplots(1, 3, figsize=(13, 5))
fig.suptitle("Standard Deviation of Metrics (Predictability)",
             fontsize=13, fontweight="bold")
for ax, metric in zip(axes, METRICS):
    stds   = [dfs[s][metric].std() for s in SCHEDULERS]
    colors = [COLOURS[s] for s in SCHEDULERS]
    ax.bar(SCHEDULERS, stds, color=colors, alpha=0.8, edgecolor="black")
    ax.set_ylabel("Std Dev (ms)", fontsize=11)
    ax.set_title(metric.replace("Time", " Time"), fontsize=12)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig5_std_dev.png"), dpi=150)
plt.close()
print("Saved fig5_std_dev.png")

# ── Fig 6: Max waiting time per patron per scheduler — starvation ─────────────
fig, ax = plt.subplots(figsize=(9, 6))
for s in SCHEDULERS:
    max_per_patron = dfs[s].groupby("patron")["waitingTime"].max().sort_values()
    ax.plot(range(len(max_per_patron)), max_per_patron.values,
            label=s, color=COLOURS[s], linewidth=2, marker="o", markersize=4)
ax.set_xlabel("Patrons (sorted by max wait)", fontsize=12)
ax.set_ylabel("Max Single-Order Wait Time (ms)", fontsize=12)
ax.set_title("Starvation Risk: Worst-Case Wait per Patron",
             fontsize=13, fontweight="bold")
ax.legend(fontsize=11)
ax.grid(linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig6_starvation.png"), dpi=150)
plt.close()
print("Saved fig6_starvation.png")

print("\n✓ All done. Graphs and CSVs are in results/")