# Stage I: Data Collection and Ingestion

## Overview

Stage I of the Big Data final project establishes the foundational data pipeline. It automates the acquisition of the 2023 Citi Bike trip dataset, its storage in a distributed relational database (PostgreSQL), and its subsequent ingestion into the Hadoop Distributed File System (HDFS) in a compressed, big‑data‑optimized format. This stage ensures that all subsequent analytical and machine learning tasks operate on consistent, reproducible data.

## Pipeline Steps

1. **Data Collection**  
   The script `scripts/data_collection.sh` downloads the official 2023 Citi Bike trip data archive (1.5 GB) from Amazon S3, extracts the nested monthly zip files, and organizes the resulting CSV files into a unified directory (`data/monthly_trips/`). The download and extraction are skipped if the monthly files are already present, preserving bandwidth and storage.

2. **Relational Database Construction**  
   The Python script `scripts/build_projectdb.py` connects to the team's PostgreSQL instance on the cluster. It executes the SQL DDL defined in `sql/create_tables.sql` to drop (if exists) and recreate the `citibike_trips` table with an appropriate schema. The script then iterates over all monthly CSV files and uses PostgreSQL's `COPY` command to efficiently load the data. The password is read securely from `secrets/psql.pass`.

3. **HDFS Ingestion via Sqoop**  
   The script `scripts/data_ingestion.sh` employs Apache Sqoop to transfer the entire `citibike_trips` table from PostgreSQL to HDFS. The data is stored as Avro files and compressed with the Snappy codec, providing a balance of storage efficiency and read performance. The generated Avro schema (`.avsc`) and Java class (`.java`) are preserved in the `output/` directory for use in later stages.

## Prerequisites

- Access to the IU Hadoop cluster with a minimum of three nodes.
- PostgreSQL database `team19_projectdb` available at `hadoop-04.uni.innopolis.ru:5432`.
- !!! The password for user `team19` need to be stored in `secrets/psql.pass`. It is in the our team telegram chat.
- Python 3 with the `psycopg2-binary` package installed.
- Sufficient disk space in the home directory (approximately 10 GB peak usage) to accommodate the dataset archive, extracted monthly files, and temporary processing.

## Execution

All commands must be issued from the root directory of the repository (`/home/team19/project/`). The master orchestration script `stage1.sh` invokes each sub‑component in the correct order.

```bash
# Ensure scripts are executable
chmod +x scripts/*.sh scripts/*.py

# Run the complete Stage I pipeline
./scripts/stage1.sh
