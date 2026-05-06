#!/bin/bash
# Stage 3: Spark MLlib classification on Hadoop YARN.
# Must be run from the repository root or through main.sh.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

HDFS_BASE="/user/team19/project"
HDFS_OPTIMIZED_DIR="${HDFS_BASE}/hive/warehouse/team19_projectdb.db/citibike_trips_optimized"
HDFS_DATA_DIR="${HDFS_BASE}/data/stage3"
HDFS_MODELS_DIR="${HDFS_BASE}/models"
HIVE_SITE_XML="/etc/hive/conf/hive-site.xml"

# ---- helpers ----
submit_spark() {
    local script="$1"
    echo ">>> spark-submit ${script}"
    local hive_conf_dir="/etc/hive/conf"
    spark-submit \
        --master yarn \
        --deploy-mode client \
        --name "team19-stage3-$(basename "${script}" .py)" \
        --conf spark.sql.catalogImplementation=hive \
        --conf spark.driver.extraClassPath="${hive_conf_dir}" \
        --conf spark.executor.extraClassPath="${hive_conf_dir}" \
        --conf spark.executor.memory=2g \
        --conf spark.driver.memory=1g \
        --conf spark.executor.cores=2 \
        --num-executors 2 \
        "${script}"
}

# ---- guardrails ----
echo "=== Stage 3: Spark MLlib on YARN ==="

if ! hdfs dfs -test -d "${HDFS_OPTIMIZED_DIR}"; then
    echo "ERROR: Stage 2 Hive table not found at ${HDFS_OPTIMIZED_DIR}"
    echo "Run scripts/stage2.sh before scripts/stage3.sh."
    exit 1
fi

# ---- HDFS cleanup ----
echo ">>> Cleaning previous Stage 3 HDFS outputs"
hdfs dfs -rm -r -f "${HDFS_DATA_DIR}" "${HDFS_MODELS_DIR}" 2>/dev/null || true
hdfs dfs -mkdir -p "${HDFS_DATA_DIR}" "${HDFS_MODELS_DIR}"

# ---- local output reset ----
mkdir -p output models
rm -f output/train_sample.csv output/test_sample.csv \
      output/model*_predictions.csv output/evaluation.csv \
      output/model_comparison.csv output/best_model.txt \
      output/sample_prediction.csv

echo "model_name,metric_name,metric_value" > output/evaluation.csv
echo "model_name,area_under_roc,area_under_pr,training_time_sec,best_params_json" \
    > output/model_comparison.csv

# ---- pipeline ----
submit_spark "scripts/stage3_data_prep.py"

submit_spark "scripts/stage3_model_rf.py"
submit_spark "scripts/stage3_model_svm.py"
submit_spark "scripts/stage3_model_nb.py"

# ---- pick best model ----
echo ">>> Selecting best model by area_under_roc"
python3 - <<'PYEOF'
import csv
best = None
with open("output/model_comparison.csv") as fh:
    reader = csv.DictReader(fh)
    for row in reader:
        roc = float(row["area_under_roc"])
        if best is None or roc > float(best["area_under_roc"]):
            best = row
if best is None:
    raise SystemExit("No model rows found in output/model_comparison.csv")
with open("output/best_model.txt", "w") as fh:
    fh.write(best["model_name"])
print("Best model: " + best["model_name"])
PYEOF

# ---- sample prediction ----
submit_spark "scripts/stage3_predict_sample.py"

# ---- mirror models to local ----
echo ">>> Mirroring HDFS PipelineModels to local models/"
for m in model1_rf model2_svm model3_nb; do
    rm -rf "models/${m}"
    if hdfs dfs -test -d "${HDFS_MODELS_DIR}/${m}"; then
        hdfs dfs -get "${HDFS_MODELS_DIR}/${m}" models/
    else
        echo "WARN: ${HDFS_MODELS_DIR}/${m} missing; not mirroring"
    fi
done

echo "=== Stage 3 is completed. ==="
