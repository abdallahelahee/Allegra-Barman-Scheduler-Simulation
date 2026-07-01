# 🍸 Allegra the Barman  
## CSC3002F Operating Systems II (2026) — Scheduling Simulation

**Course:** CSC3002F Operating Systems II  
**Institution:** University of Cape Town  
**Lecturer:** Dr. Michelle Kuttel  
**Assignment:** Scheduling Comparison Simulation  
**Title:** *Allegra the Barman: Comparing Scheduling Policies for Bartending*

---

## 📌 Overview

This project implements a simulation-based comparison of classical CPU scheduling algorithms using a bar-service analogy.

In this system:
- 👤 Patrons represent processes  
- 🍹 Drink orders represent CPU bursts  
- 🍸 Allegra the Barman represents the CPU + scheduler  

The system evaluates how different scheduling policies affect performance, fairness, predictability, and starvation.

---

## 🎯 Objective

The goal of this assignment is to experimentally compare:

- First Come First Served (FCFS)
- Shortest Job First (SJF)
- Priority Scheduling
- Multilevel Feedback Queue (MLFQ)

with respect to:

- ⏱ Waiting Time (per order & per patron)
- 🔁 Turnaround Time
- ⚡ Response Time
- 📊 Throughput
- ⚖️ Fairness
- 📉 Predictability
- 🚨 Starvation risk

---

## ⚙️ Simulation Design

The simulation is implemented in Java using a multi-threaded bar environment.

### Key Design Features:
- Each patron runs as a thread
- Each drink order is a scheduling unit
- Non-preemptive execution per drink order
- Fixed context-switch overhead (5 ms)
- Reproducible workloads using seed-based randomness

---

## 📊 Experimental Setup

To ensure fairness:

- Identical workloads used across all schedulers
- 4 patron configurations: 10, 20, 30, 50
- 15 seed values per configuration
- 240 total simulation runs per scheduler
- ~7,398 orders per scheduler dataset

All schedulers were evaluated under identical conditions.

---

## 📁 Metrics Collected

For each drink order:

- Waiting Time = serviceStartTime − arrivalTime  
- Turnaround Time = completionTime − arrivalTime  
- Response Time = first service time − arrivalTime  

Additional metrics:

- Per-patron total waiting time
- Standard deviation (consistency)
- 95th percentile (tail latency)
- Maximum wait (starvation indicator)

---

## 🧪 Validation

The system was validated using:

### ✔ Algorithm correctness checks
- FCFS respects arrival order
- SJF prioritises shortest jobs
- Priority respects patron ordering
- MLFQ demonstrates queue promotion behavior

### ✔ Data integrity checks
- No negative timing values
- serviceStartTime ≥ arrivalTime
- Completion consistency validation

### ✔ Reproducibility
- Identical seed → identical workload generation
- Consistent scheduling across all algorithms

### ✔ Thread safety
- `FILE_LOCK` used to synchronise CSV writes
- Prevents race conditions during concurrent logging

---

## 📈 Analysis Pipeline

A Python script (`analyse.py`) processes simulation outputs:

### Outputs generated:
- Summary statistics (mean, median, std, p95)
- Per-patron fairness analysis
- Box plots of distributions
- CDF curves (predictability analysis)
- Starvation risk plots

Tools used:
- pandas
- matplotlib

---

## 📊 Key Findings

- FCFS provides the most consistent and fair experience
- SJF and Priority reduce average waiting time but introduce severe starvation
- MLFQ balances fairness and responsiveness but increases overall variance
- Throughput is identical across all schedulers due to fixed workload constraints

---

## 🧠 Conclusion

The results demonstrate a fundamental trade-off in scheduling systems:

> Optimising for average performance (SJF, Priority) increases unfairness and starvation risk, while fairness-focused algorithms (FCFS) improve predictability and consistency.

### ✔ Final Recommendation:
**FCFS is the most suitable scheduling algorithm for Allegra the Barman in this scenario**, due to its fairness, simplicity, and predictable performance.

---

## 📂 Repository Structure
- src/ → Java simulation code
- schedulers/ → FCFS, SJF, Priority, MLFQ implementations
- results/ → CSV outputs from experiments
- analysis/ → Python analysis scripts (analyse.py)
- report/ → Full written report (PDF)
- run_experiments.sh → Automation script for batch runs

---

## 👨‍🏫 Academic Context

This project was completed as part of:

**CSC3002F · Operating Systems II (2026)**  
University of Cape Town  

**Lecturer:** Dr. Michelle Kuttel  

Assignment: Scheduling Comparison Simulation  
“Allegra the Barman: Comparing Scheduling Policies for Bartending”

---

## 🤖 AI Usage Statement

Generative AI tools were used for limited assistance in:
- Structuring analysis scripts
- Supporting automation scripting
- Assisting with debugging

All simulations, experimental results, and analysis were generated from actual program execution. No fabricated results or outputs were produced.

---

## 📜 Author

Abdallah Elahee (ELHABD002)
