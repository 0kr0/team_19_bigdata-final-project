# Stage II: Hive Storage, Preparation, and EDA

## Overview

Stage II builds on the Stage I Citi Bike ingestion pipeline. Stage I imports the PostgreSQL table `citibike_trips` into HDFS as Avro + Snappy files under:

```text
/user/team19/project/warehouse/citibike_trips
```

Stage II registers those files in Hive, creates an analytics-ready external table with partitioning and bucketing, runs exploratory data analysis queries, and exports query results as local CSV files in `output/`.

## Inputs

- Stage I HDFS data: `/user/team19/project/warehouse/citibike_trips`
- Local Avro schema: `output/citibike_trips.avsc`
- Hive password file: `secrets/.hive.pass`

The script copies local `.avsc` files into:

```text
/user/team19/project/warehouse/avsc
```

The raw Hive table references the schema through:

```text
hdfs:///user/team19/project/warehouse/avsc/citibike_trips.avsc
```

## Hive Database and Tables

Stage II creates the Hive database:

```text
team19_projectdb
```

with database location:

```text
/user/team19/project/hive/warehouse/team19_projectdb.db
```

### Raw External Table

`citibike_trips_raw` is an external Avro table over the Sqoop output. It is used only as the source table for schema inspection and transformation.

### Optimized External Table

`citibike_trips_optimized` is an external ORC table stored at:

```text
/user/team19/project/hive/warehouse/team19_projectdb.db/citibike_trips_optimized
```

It normalizes the imported schema by deriving:

- `started_at_ts`
- `ended_at_ts`
- `ride_date`
- `ride_year`
- `ride_month`
- `ride_weekday`
- `ride_hour`
- `ride_duration_minutes`
- cleaned station IDs/names
- normalized `member_casual`
- normalized `rideable_type`

The original Sqoop Avro schema stores timestamp columns as `long`; Stage II converts these values into Hive timestamps. The conversion supports millisecond epoch values, with a fallback for second epoch values.

Partitioning:

- `ride_year`
- `ride_month`

Bucketing:

- `start_station_id`
- 8 buckets

All EDA queries use `citibike_trips_optimized`, not the raw Avro table.

## EDA Queries

The following HiveQL files are implemented:

- `sql/q1.hql`: rides by month
- `sql/q2.hql`: rides by weekday
- `sql/q3.hql`: rides by hour of day with average duration
- `sql/q4.hql`: member vs casual distribution with average duration
- `sql/q5.hql`: top 20 start stations
- `sql/q6.hql`: rideable type usage with average duration

Each query:

1. uses `team19_projectdb`,
2. drops the old `qx_results` table,
3. recreates `qx_results`,
4. inserts results from `citibike_trips_optimized`,
5. exports results to an HDFS directory under `/user/team19/project/hive/exports/stage2/qx`.

The Stage II script then collects those HDFS part files into local CSV files with headers:

- `output/q1.csv`
- `output/q2.csv`
- `output/q3.csv`
- `output/q4.csv`
- `output/q5.csv`
- `output/q6.csv`

## Running Stage II

Run from the repository root:

```bash
bash scripts/stage2.sh
```

The script is rerunnable. It safely refreshes:

- HDFS Avro schema files,
- the Hive database metadata,
- the optimized external table location,
- HDFS EDA export directories,
- local `output/q*.csv` files.

## Files

- `scripts/stage2.sh`: Stage II orchestrator
- `sql/db.hql`: Hive database, raw table, optimized table, and data load
- `sql/q1.hql` ... `sql/q6.hql`: EDA result table creation and export
- `output/q1.csv` ... `output/q6.csv`: generated EDA outputs after running Stage II
