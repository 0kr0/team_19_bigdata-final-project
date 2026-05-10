#!/bin/bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

HIVE_JDBC_URL="jdbc:hive2://hadoop-03.uni.innopolis.ru:10001"
HIVE_USER="team19"
HIVE_PASSWORD_FILE="secrets/.hive.pass"

HDFS_STAGE4_DIR="/user/team19/project/hive/exports/stage4"

# ---- guards ----
if [ ! -f "$HIVE_PASSWORD_FILE" ]; then
    echo "Missing Hive password file: $HIVE_PASSWORD_FILE"
    echo "Create it with the first line containing the Hive password for user $HIVE_USER."
    exit 1
fi

REQUIRED_FILES=(
    output/evaluation.csv
    output/model_comparison.csv
    output/model1_rf_predictions.csv
    output/model2_svm_predictions.csv
    output/model3_nb_predictions.csv
    output/train_sample.csv
    output/test_sample.csv
    output/sample_prediction.csv
)
for f in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$f" ]; then
        echo "ERROR: Missing Stage 3 output: $f"
        echo "Run scripts/stage3.sh before scripts/stage4.sh."
        exit 1
    fi
done

password="$(head -n 1 "$HIVE_PASSWORD_FILE")"

echo "=== Stage 4: Superset data preparation ==="

# ---- preprocess ----
echo ">>> Preprocessing Stage 3 CSVs for Hive ingestion"
rm -rf output/stage4
python3 scripts/stage4_preprocess.py

# ---- HDFS upload ----
echo ">>> Uploading processed CSVs to HDFS at ${HDFS_STAGE4_DIR}"
hdfs dfs -rm -r -f "${HDFS_STAGE4_DIR}" 2>/dev/null || true

for table in evaluation model_comparison predictions train_sample test_sample sample_prediction; do
    hdfs dfs -mkdir -p "${HDFS_STAGE4_DIR}/${table}"
    hdfs dfs -put -f "output/stage4/${table}.csv" "${HDFS_STAGE4_DIR}/${table}/"
done

# ---- Hive tables ----
echo ">>> Creating Hive tables and views in team19_projectdb"
beeline \
    -u "$HIVE_JDBC_URL" \
    -n "$HIVE_USER" \
    -p "$password" \
    -f sql/stage4.hql

# ---- report ----
echo ">>> Generating Stage 4 ML report"
python3 scripts/stage4_report.py

echo "=== Stage 4 is completed. ==="
echo "    Hive tables created in team19_projectdb (prefix: stage3_)"
echo "    Report: output/stage4_ml_report.md"