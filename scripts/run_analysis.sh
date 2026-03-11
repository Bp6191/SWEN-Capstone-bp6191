#!/bin/bash

# Master script to run complete logging evolution analysis
# Usage: ./run_analysis.sh

# Configuration
SYSTEMS=("redis" "clickhouse" "rocksdb" "envoy" "tikv")
REPOS_DIR="./repos"
RESULTS_DIR="./results"

# Create directories
mkdir -p $REPOS_DIR
mkdir -p $RESULTS_DIR

echo "=== LOGGING EVOLUTION ANALYSIS ==="
echo "=================================="
echo ""

# Clone repositories (if not already cloned)
echo "Step 1: Cloning repositories..."
cd $REPOS_DIR

if [ ! -d "redis" ]; then
    echo "Cloning Redis..."
    git clone https://github.com/redis/redis.git
fi

if [ ! -d "clickhouse" ]; then
    echo "Cloning ClickHouse..."
    git clone https://github.com/ClickHouse/ClickHouse.git clickhouse
fi

if [ ! -d "rocksdb" ]; then
    echo "Cloning RocksDB..."
    git clone https://github.com/facebook/rocksdb.git
fi

if [ ! -d "envoy" ]; then
    echo "Cloning Envoy..."
    git clone https://github.com/envoyproxy/envoy.git
fi

if [ ! -d "tikv" ]; then
    echo "Cloning TiKV..."
    git clone https://github.com/tikv/tikv.git
fi

cd ..

echo ""
echo "Step 2: Extracting logging commits..."

# Extract logging commits for each system
for system in "${SYSTEMS[@]}"
do
    echo "Processing $system..."
    python3 extract_log_commits.py "$REPOS_DIR/$system" "$RESULTS_DIR/${system}_commits.csv"
    echo ""
done

echo ""
echo "Step 3: Analyzing evolution trends..."

# Analyze evolution for each system
for system in "${SYSTEMS[@]}"
do
    echo "Analyzing $system..."
    python3 analyze_evolution.py "$RESULTS_DIR/${system}_commits.csv" "$RESULTS_DIR/${system}_analysis"
    echo ""
done

echo ""
echo "=== ANALYSIS COMPLETE ==="
echo "Results saved in $RESULTS_DIR/"
echo ""
echo "Next steps:"
echo "1. Review CSV files for each system"
echo "2. Compare trends across systems"
echo "3. Visualize results (temporal trends, categories, churn)"