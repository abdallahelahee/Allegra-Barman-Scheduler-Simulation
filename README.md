# Allegra the Barman 🍸  
### Scheduling Algorithm Simulation (FCFS, SJF, Priority, MLFQ)

This project simulates and evaluates classic operating system scheduling algorithms using a multi-threaded bar service model where drink orders represent CPU bursts and a barman acts as the scheduler.

---

## 🧠 Overview

The system models a high-load bar environment where patron threads generate drink orders at random intervals. Each scheduling algorithm is evaluated under identical workloads to ensure fair comparison.

---

## ⚙️ Scheduling Algorithms Compared

- First Come First Serve (FCFS)
- Shortest Job First (SJF)
- Priority Scheduling
- Multilevel Feedback Queue (MLFQ)

---

## 📊 Metrics Evaluated

- Waiting Time
- Turnaround Time
- Response Time
- Per-patron Total Wait Time
- Standard Deviation (consistency)
- 95th Percentile (tail latency)
- Starvation analysis

---

## 🧪 Experimental Design

- 4 patron counts: 10, 20, 30, 50
- 15 seed values per configuration
- Fully reproducible workload generation
- 240 total simulation runs per scheduler
- 7,398+ orders per scheduler

---

## 📈 Analysis

All results were generated using a Python analysis pipeline (`analyse.py`) using:
- pandas
- matplotlib

Outputs include:
- Box plots
- CDF curves
- Mean vs median comparisons
- Fairness and starvation analysis

---

## 🧵 Concurrency & Correctness

- Thread-safe logging using `FILE_LOCK`
- CSV integrity validation
- Deterministic execution via seeded randomness

---

## 📌 Key Finding

FCFS provides the best overall balance of:
- fairness
- predictability
- starvation prevention

SJF and Priority improve average performance but introduce severe tail latency and starvation risk.

---

## 👨‍💻 Technologies

- Java (multi-threaded simulation)
- Python (pandas, matplotlib)
- Bash scripting (automation)
- CSV-based data pipeline

---

## 📄 Report

Full technical report is included in `/report`:
- experimental methodology
- full statistical analysis
- graphs and validation results

---

## 📜 Author

Abdallah Elahee (ELHABD002)
CSC3002F Operating Systems 2 Assignment
