#!/bin/bash
# Stage 2: Hive storage/preparation and EDA for the Citi Bike project.
# Must be run from the repository root or through main.sh.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

HIVE_JDBC_URL="jdbc:hive2://hadoop-03.uni.innopolis.ru:10001"
HIVE_USER="team19"
HIVE_PASSWORD_FILE="secrets/.hive.pass"

SQOOP_WAREHOUSE_DIR="/user/team19/project/warehouse"
SQOOP_TABLE_DIR="${SQOOP_WAREHOUSE_DIR}/citibike_trips"
HDFS_AVSC_DIR="${SQOOP_WAREHOUSE_DIR}/avsc"

HIVE_WAREHOUSE_DIR="/user/team19/project/hive/warehouse"
HIVE_DB_DIR="${HIVE_WAREHOUSE_DIR}/team19_projectdb.db"
HDFS_EXPORT_DIR="/user/team19/project/hive/exports/stage2"

if [ ! -f "$HIVE_PASSWORD_FILE" ]; then
    echo "Missing Hive password file: $HIVE_PASSWORD_FILE"
    echo "Create it with the first line containing the Hive password for user $HIVE_USER."
    exit 1
fi

if [ ! -f "output/citibike_trips.avsc" ]; then
    echo "Missing output/citibike_trips.avsc. Run Stage 1 before Stage 2."
    exit 1
fi

password="$(head -n 1 "$HIVE_PASSWORD_FILE")"

run_hql() {
    local hql_file="$1"
    echo ">>> Running ${hql_file}"
    beeline \
        -u "$HIVE_JDBC_URL" \
        -n "$HIVE_USER" \
        -p "$password" \
        -f "$hql_file"
}

csv_header() {
    case "$1" in
        q1) echo "ride_year,ride_month,year_month,trip_count" ;;
        q2) echo "weekday_number,weekday_name,trip_count" ;;
        q3) echo "ride_hour,trip_count,avg_ride_duration_minutes" ;;
        q4) echo "rider_type,trip_count,avg_ride_duration_minutes" ;;
        q5) echo "start_station_id,start_station_name,trip_count,avg_ride_duration_minutes" ;;
        q6) echo "rideable_type,trip_count,avg_ride_duration_minutes" ;;
        *)
            echo "Unknown query name: $1" >&2
            return 1
            ;;
    esac
}

collect_csv() {
    local query_name="$1"
    local hdfs_dir="${HDFS_EXPORT_DIR}/${query_name}"
    local local_csv="output/${query_name}.csv"
    local exported_files

    echo ">>> Collecting ${query_name} results into ${local_csv}"

    if ! hdfs dfs -test -d "$hdfs_dir"; then
        echo "Missing HDFS export directory: $hdfs_dir"
        exit 1
    fi

    exported_files="$(hdfs dfs -ls "$hdfs_dir" | awk '$1 ~ /^-/ && $8 !~ /\/_/ {print $8}' | sort)"
    if [ -z "$exported_files" ]; then
        echo "No exported data files found under $hdfs_dir"
        exit 1
    fi

    mkdir -p output
    csv_header "$query_name" > "$local_csv"
    while IFS= read -r exported_file; do
        hdfs dfs -cat "$exported_file" >> "$local_csv"
    done <<< "$exported_files"
}

echo "=== Stage 2: Hive storage/preparation and EDA ==="

echo ">>> Verifying Stage 1 HDFS import at ${SQOOP_TABLE_DIR}"
if ! hdfs dfs -test -d "$SQOOP_TABLE_DIR"; then
    echo "Stage 1 HDFS table directory was not found: $SQOOP_TABLE_DIR"
    echo "Run scripts/stage1.sh before scripts/stage2.sh."
    exit 1
fi

echo ">>> Refreshing Avro schema files in HDFS at ${HDFS_AVSC_DIR}"
hdfs dfs -mkdir -p "$HDFS_AVSC_DIR"
hdfs dfs -rm -f "${HDFS_AVSC_DIR}"/*.avsc 2>/dev/null || true
hdfs dfs -put -f output/*.avsc "$HDFS_AVSC_DIR/"

echo ">>> Cleaning previous Stage 2 Hive and export data"
hdfs dfs -rm -r -f "$HIVE_DB_DIR" "$HDFS_EXPORT_DIR" 2>/dev/null || true
hdfs dfs -mkdir -p "$HIVE_WAREHOUSE_DIR" "$HDFS_EXPORT_DIR"

run_hql "sql/db.hql"

for query_name in q1 q2 q3 q4 q5 q6; do
    run_hql "sql/${query_name}.hql"
    collect_csv "$query_name"
done

echo ">>> Generating EDA charts and narrative report"
mkdir -p output/charts
python3 scripts/stage2_eda_report.py

echo "=== Stage 2 is completed. CSV results are in output/q1.csv ... output/q6.csv ==="
echo "    Charts are in output/charts/ and narrative is at output/stage2_eda_report.md"
