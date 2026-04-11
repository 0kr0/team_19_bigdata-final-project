#!/bin/bash
set -e

# Read PostgreSQL password
password=$(head -n 1 secrets/psql.pass)

# HDFS target directory
HDFS_DIR="/user/team19/project/warehouse"

# Clean up old HDFS warehouse directory (idempotent)
hdfs dfs -rm -r -f "$HDFS_DIR" || true
hdfs dfs -mkdir -p "$HDFS_DIR"

# Sqoop import: all tables from PostgreSQL HDFS as Avro + Snappy
sqoop import-all-tables \
    --connect jdbc:postgresql://hadoop-04.uni.innopolis.ru/team19_projectdb \
    --username team19 \
    --password "$password" \
    --compression-codec snappy \
    --compress \
    --as-avrodatafile \
    --warehouse-dir "$HDFS_DIR" \
    --m 1

# Move generated schema files to output/ folder
mkdir -p output
mv *.avsc *.java output/ 2>/dev/null || true

echo "Sqoop import complete. Data stored in $HDFS_DIR"
echo "Schema files (.avsc, .java) moved to output/"
