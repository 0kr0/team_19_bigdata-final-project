#!/bin/bash
# Must be run from the repository root.

set -e  # Stop on first error

echo "=== Stage 1: Data ingestion ==="

# 1. Data Collection
echo ">>> Step 1/3: Collecting dataset..."
bash scripts/data_collection.sh
echo "=== Data collection complete. ==="

# 2. Build PostgreSQL Database
echo ">>> Step 2/3: Loading data into PostgreSQL..."
python3 scripts/build_projectdb.py
echo "=== PostgreSQL loaded. ==="

# 3. Sqoop Import to HDFS
echo ">>> Step 3/3: Ingesting to HDFS via Sqoop..."
bash scripts/data_ingestion.sh
echo "=== HDFS ingestion complete. ==="

echo "=== Stage 1 is completed. ==="
echo "Made by team #19"
