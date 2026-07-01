#!/bin/bash
# run_experiments.sh
# Runs all 4 scheduling algorithms with identical workloads (same seeds)
# for multiple patron counts, producing reproducible CSVs in results/

SWITCH=5
RUNS=15
PATRON_COUNTS=(10 20 30 50)

rm -rf results
mkdir -p results

echo "============================================"
echo "  Allegra the Barman - Experiment Runner"
echo "  Schedulers: FCFS SJF PRIORITY MLFQ"
echo "  Patron counts: ${PATRON_COUNTS[*]}"
echo "  Seeds (runs): 1..$RUNS"
echo "============================================"

for patrons in "${PATRON_COUNTS[@]}"; do
    for seed in $(seq 1 $RUNS); do
        for sched in 0 1 2 3; do
            make -s run ARGS="$patrons $sched $SWITCH $seed" > /dev/null 2>&1
        done
        echo "  patrons=$patrons  seed=$seed  done"
    done
done

echo ""
echo "All experiments complete. Results in ./results/"
for f in results/*.csv; do
    count=$(tail -n +2 "$f" | wc -l)
    echo "  $f : $count orders recorded"
done