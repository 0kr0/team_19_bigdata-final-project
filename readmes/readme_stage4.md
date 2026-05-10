# Stage IV: Superset Dashboard

## Overview

Stage IV delivers an Apache Superset dashboard that presents the full
Citi Bike pipeline to business stakeholders. It is organised into three
sections:

1. **Data Description** — dataset characteristics queried from PostgreSQL
2. **Data Insights** — all six EDA charts from Stage II with conclusions
3. **ML Modeling Results** — model comparison, hyperparameter tuning,
   predictions, and evaluation metrics from Stage III

`scripts/stage4.sh` automates the data preparation work (Hive table
creation). The Superset dashboard itself is built manually in the
Superset UI after the tables are available.

## Prerequisites

- Stages I, II, and III must have run successfully.
- `output/evaluation.csv`, `output/model_comparison.csv`,
  `output/model*_predictions.csv`, `output/train_sample.csv`,
  `output/test_sample.csv`, and `output/sample_prediction.csv` must exist.
- `secrets/.hive.pass` must exist with the Hive password on the first line.

## Running Stage IV

```bash
bash scripts/stage4.sh
```

The script:
1. Preprocesses Stage III CSVs into `output/stage4/` — combines the three
   model prediction files into one `predictions.csv` with a `model_name`
   column added.
2. Uploads all six CSV files to HDFS under
   `/user/team19/project/hive/exports/stage4/<table>/`.
3. Runs `sql/stage4.hql` via Beeline to create external Hive tables and
   typed views in `team19_projectdb`.
4. Runs `scripts/stage4_report.py` to generate
   `output/stage4_ml_report.md`.

## Hive Tables and Views

All objects are created in `team19_projectdb`. Each dataset gets a raw
external table (all columns STRING, OpenCSVSerde) and a typed view that
casts columns to their proper numeric types for Superset.

| View (use in Superset)    | Description                                          |
|---------------------------|------------------------------------------------------|
| `stage3_evaluation`       | Per-model AUC-ROC and AUC-PR metrics                 |
| `stage3_model_comparison` | Model training times and best hyperparameters         |
| `stage3_predictions`      | Combined predictions from all three models (~30 000 rows); `probability` = class-1 score (true probability for RF/NB, decision margin for SVM) |
| `stage3_train_sample`     | 1 000-row training sample with all feature columns   |
| `stage3_test_sample`      | 1 000-row test sample with all feature columns       |
| `stage3_sample_prediction`| Single-ride prediction demo in key-value format      |

Always use the views (no `_raw` suffix) when creating Superset datasets —
they expose properly typed numeric columns.

## Superset Setup (Manual Steps)

### 1. Add Database Connections

In **Settings → Database Connections** add:

- **PostgreSQL** — connects to the Stage I database (`team19_projectdb`
  in PostgreSQL) for the Data Description charts.
- **Hive / HiveServer2** — `jdbc:hive2://hadoop-03.uni.innopolis.ru:10001`
  with user `team19` and the Hive password; gives access to
  `team19_projectdb` Hive tables for Stage II and Stage III charts.

### 2. Add Datasets

For each table/view you want to chart, go to **Data → Datasets → + Dataset**
and select the database, schema (`team19_projectdb`), and table name.

**PostgreSQL datasets** (Data Description section):
- `citibike_trips` — raw trip table; use SQL Editor to count rows,
  inspect column types (`information_schema.columns`), and pull samples.

**Hive datasets** (Data Insights section):
- `citibike_trips_optimized` — main analytical table (Stage II EDA charts)
- `q1_results` … `q6_results` — pre-aggregated EDA result tables

**Hive datasets** (ML Modeling Results section):
- `stage3_evaluation`
- `stage3_model_comparison`
- `stage3_predictions`
- `stage3_train_sample`
- `stage3_test_sample`
- `stage3_sample_prediction`

### 3. Create the Dashboard

**Dashboard title:** `Team 19 — Citi Bike Big Data Pipeline`

Use **Tabs** to split the dashboard into three screens. Within each tab
use **Rows**, **Columns**, **Headers**, and **Dividers** to organise
the charts, and **Text** blocks for markdown commentary.

---

#### Tab 1 — Data Description

| Chart | Type | Dataset | Notes |
|---|---|---|---|
| Record count per table | Big Number | PostgreSQL — `information_schema.tables` | Filter to `public` schema |
| Column datatypes | Table | PostgreSQL — `information_schema.columns` | Filter to `citibike_trips` |
| Sample rows | Table | PostgreSQL — `citibike_trips` | LIMIT 20 |
| Data cleaning summary | Text block | — | Describe normalisation applied in Stage II (`db.hql`) |

---

#### Tab 2 — Data Insights

Recreate the six Stage II EDA insights. Use the pre-aggregated Hive
result tables (`q1_results` … `q6_results`) for fast queries.

| Chart | Type | Dataset | Key columns |
|---|---|---|---|
| Monthly trip volume | Line | `q1_results` | x = `year_month`, y = `trip_count` |
| Trips by day of week | Bar | `q2_results` | x = `weekday_name`, y = `trip_count` |
| Hourly volume vs avg duration | Dual-axis Bar+Line | `q3_results` | x = `ride_hour` |
| Member vs casual share | Pie + Bar | `q4_results` | `rider_type`, `trip_count`, `avg_ride_duration_minutes` |
| Top 20 start stations | Horizontal bar | `q5_results` | x = `trip_count`, y = `start_station_name` |
| Rideable type usage | Bar+Line | `q6_results` | `rideable_type`, `trip_count`, `avg_ride_duration_minutes` |

Add a **Text** block under each chart with the 2–4 sentence stakeholder
story from `output/stage2_eda_report.md`.

---

#### Tab 3 — ML Modeling Results

| Chart | Type | Dataset | Key columns |
|---|---|---|---|
| AUC-ROC by model | Bar | `stage3_evaluation` | Filter `metric_name = 'areaUnderROC'`; x = `model_name`, y = `metric_value` |
| AUC-PR by model | Bar | `stage3_evaluation` | Filter `metric_name = 'areaUnderPR'` |
| Model comparison table | Table | `stage3_model_comparison` | All columns |
| Training time comparison | Bar | `stage3_model_comparison` | x = `model_name`, y = `training_time_sec` |
| Prediction distribution | Histogram | `stage3_predictions` | x = `probability`; filter by `model_name` |
| Confusion matrix counts | Table or Pivot | `stage3_predictions` | `label`, `prediction`, COUNT(*); filter by `model_name` |
| Feature distribution — ride hour | Bar | `stage3_train_sample` | GROUP BY `ride_hour`, AVG(`label`) |
| Feature distribution — duration | Histogram | `stage3_train_sample` | `ride_duration_minutes`; colour by `label` |
| Feature distribution — distance | Histogram | `stage3_train_sample` | `trip_distance_km`; colour by `label` |
| Sample prediction demo | Table | `stage3_sample_prediction` | All rows |

### 4. Apply CSS and Publish

- Apply a CSS template in **Edit Dashboard → CSS** to match a
  clean corporate style.
- When finished, click **... → Publish** to make the dashboard
  visible to all users.

## Files

| File | Purpose |
|---|---|
| `scripts/stage4.sh` | Stage IV orchestrator |
| `scripts/stage4_preprocess.py` | CSV preprocessing (combines predictions) |
| `scripts/stage4_report.py` | Generates `output/stage4_ml_report.md` |
| `sql/stage4.hql` | External Hive table and view definitions |
| `output/stage4/` | Hive-ready CSVs (created at runtime) |
| `output/stage4_ml_report.md` | ML results narrative (created at runtime) |