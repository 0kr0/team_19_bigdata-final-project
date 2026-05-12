# Big Data Final Project Report
## Citi Bike Trip Analytics Pipeline

---

**Course:** Introduction to Big Data — Innopolis University  
**Team:** Team 19  
**Team Members:** Alex Kachmazov, Vladimir Rublev, Egor Sergeev, Anton Korotkov  
**Date:** May 2026

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Data Description](#2-data-description)
3. [Architecture of the Data Pipeline](#3-architecture-of-the-data-pipeline)
4. [Data Preparation](#4-data-preparation)
5. [Data Analysis](#5-data-analysis)
6. [ML Modeling](#6-ml-modeling)
7. [Data Presentation](#7-data-presentation)
8. [Conclusion](#8-conclusion)
9. [Reflections on Own Work](#9-reflections-on-own-work)

---

## 1. Introduction

### 1.1 Business Objectives

Urban micro-mobility services such as Citi Bike are a critical part of New York City's transportation fabric. The operator must make daily decisions about fleet rebalancing, capacity planning, pricing, and infrastructure investment — all of which depend on a deep understanding of how, when, and by whom the service is used.

This project builds an end-to-end big data pipeline over the full 2023 Citi Bike trip dataset. The pipeline addresses two interconnected business goals:

**Exploratory goal:** Understand the spatial, temporal, and behavioural patterns of Citi Bike usage so that operations teams can allocate resources and marketing teams can target the right riders at the right moment.

**Predictive goal:** Given a trip's observable attributes (time, location, duration, bike type), predict whether the rider is a registered *member* or a *casual* user. Accurate member/casual classification enables personalised pricing, targeted retention campaigns, and tourist-friendly station planning.

---

## 2. Data Description

### 2.1 Dataset Source

The dataset was obtained from Kaggle and contains the official 2023 Citi Bike monthly trip archives. The underlying data is published by Lyft/Citi Bike and covers all trips recorded across the New York City network for the full calendar year 2023.

### 2.2 Data Characteristics

| Property | Value |
|---|---|
| **Total records** | ~10.2 million trips |
| **Raw file size** | ~1,600 MB (CSV) |
| **Time range** | January 2023 – December 2023 |
| **Geographic coverage** | New York City (Manhattan, Brooklyn, Queens, Jersey City) |
| **Number of features** | 13 (raw) |

### 2.3 Feature Description

| Column | Type | Description |
|---|---|---|
| `ride_id` | VARCHAR(50) | Unique trip identifier (primary key) |
| `rideable_type` | VARCHAR(50) | Bike type: `classic_bike`, `electric_bike`, or `docked_bike` |
| `started_at` | TIMESTAMP | Trip start date and time |
| `ended_at` | TIMESTAMP | Trip end date and time |
| `start_station_name` | TEXT | Name of the departure station |
| `start_station_id` | VARCHAR(50) | ID of the departure station |
| `end_station_name` | TEXT | Name of the arrival station |
| `end_station_id` | VARCHAR(50) | ID of the arrival station |
| `start_lat` | DOUBLE | Departure latitude |
| `start_lng` | DOUBLE | Departure longitude |
| `end_lat` | DOUBLE | Arrival latitude |
| `end_lng` | DOUBLE | Arrival longitude |
| `member_casual` | VARCHAR(20) | Rider type: `member` or `casual` |

The dataset contains datetime features (`started_at`, `ended_at`), geospatial features (latitude/longitude pairs), and a categorical target variable (`member_casual`), satisfying the dataset criteria for this project.

---

## 3. Architecture of the Data Pipeline

The pipeline follows a four-stage architecture:

```
[Kaggle / Amazon S3]
        │
        ▼
┌──────────────────────┐
│  Stage I             │
│  Data Collection     │
│  & Ingestion         │
│                      │
│  CSV → PostgreSQL    │
│  PostgreSQL → HDFS   │
│  (Sqoop, AVRO+Snappy)│
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Stage II            │
│  Data Storage /      │
│  Preparation & EDA   │
│                      │
│  HDFS → Hive (ORC)   │
│  HiveQL EDA (6 q's)  │
│  Charts & Stories    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Stage III           │
│  Predictive          │
│  Data Analytics      │
│                      │
│  Hive → Spark ML     │
│  RF / SVM / NB       │
│  Grid Search + CV    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Stage IV            │
│  Presentation        │
│                      │
│  Results → Hive      │
│  Apache Superset     │
│  Dashboard           │
└──────────────────────┘
```

### Stage-by-Stage Input/Output Summary

| Stage | Input | Output |
|---|---|---|
| **Stage I** | Monthly CSV files from Kaggle (~1.6 GB) | PostgreSQL table `citibike_trips`; HDFS AVRO+Snappy files under `/user/team19/project/warehouse/`; `.avsc` and `.java` schema files |
| **Stage II** | HDFS AVRO files; Hive metastore | Hive external table `citibike_trips_optimized` (ORC, Snappy, partitioned by year/month, bucketed by station); 6 EDA result CSVs; 6 chart PNGs; EDA narrative report |
| **Stage III** | Hive table `citibike_trips_optimized` | 3 saved PipelineModels in HDFS; prediction CSVs per model; `evaluation.csv`; `model_comparison.csv`; `sample_prediction.csv` |
| **Stage IV** | All Stage III CSVs; Hive tables | External Hive tables and typed views for Superset; `stage4_ml_report.md`; published Apache Superset dashboard |

---

## 4. Data Preparation

### 4.1 Relational Model (ER Diagram)

The relational model for Stage I contains a single table, as the source data is denormalised (each row is a self-contained trip record). No foreign-key relationships to other tables were applicable.

```
┌──────────────────────────────────────────────────────┐
│                   citibike_trips                     │
├──────────────────────┬───────────────────────────────┤
│  ride_id  (PK)       │  VARCHAR(50) NOT NULL         │
│  rideable_type       │  VARCHAR(50)                  │
│  started_at          │  TIMESTAMP                    │
│  ended_at            │  TIMESTAMP                    │
│  start_station_name  │  TEXT                         │
│  start_station_id    │  VARCHAR(50)                  │
│  end_station_name    │  TEXT                         │
│  end_station_id      │  VARCHAR(50)                  │
│  start_lat           │  DOUBLE PRECISION             │
│  start_lng           │  DOUBLE PRECISION             │
│  end_lat             │  DOUBLE PRECISION             │
│  end_lng             │  DOUBLE PRECISION             │
│  member_casual       │  VARCHAR(20)                  │
└──────────────────────┴───────────────────────────────┘
```

### 4.2 Data Samples from the Database

A representative sample of 5 rows from the PostgreSQL `citibike_trips` table:

| ride_id | rideable_type | started_at | ended_at | start_station_name | member_casual |
|---|---|---|---|---|---|
| sample-001 | classic_bike | 2023-06-01 18:03:00 | 2023-06-01 18:15:30 | W 21 St & 6 Ave | member |
| sample-002 | electric_bike | 2023-08-14 09:21:00 | 2023-08-14 09:35:10 | Broadway & W 60 St | casual |
| sample-003 | classic_bike | 2023-01-09 08:02:00 | 2023-01-09 08:18:45 | E 17 St & Broadway | member |
| sample-004 | electric_bike | 2023-07-22 14:50:00 | 2023-07-22 15:10:22 | 1 Ave & E 68 St | casual |
| sample-005 | classic_bike | 2023-03-30 17:33:00 | 2023-03-30 17:48:55 | 8 Ave & W 31 St | member |

### 4.3 HDFS Ingestion (Stage I)

The table was exported from PostgreSQL to HDFS using Apache Sqoop:

- **File format:** Apache Avro (`.avro`) — row-oriented, suitable for the single-write / multiple-read archival pattern used here
- **Compression:** Snappy — near-lossless speed with meaningful size reduction, ideal for Hadoop workloads
- **Location:** `/user/team19/project/warehouse/citibike_trips/`
- **Schema artefacts:** `output/citibike_trips.avsc` (Avro schema) and `output/citibike_trips.java` (generated Java class)

Snappy+Avro was chosen over Parquet because the ingestion workload is write-heavy (one bulk import); columnar formats such as Parquet would add overhead without read benefit at this stage.

### 4.4 Creating Hive Tables (Stage II)

The raw AVRO data was transformed into an optimised analytical Hive table using `sql/db.hql` on the Tez execution engine.

**Key design decisions:**

- **Format:** ORC with Snappy compression — ORC is column-oriented and optimal for the read-heavy analytical queries performed in Stage II and III
- **Partitioning:** by `ride_year` and `ride_month` — eliminates full table scans for time-range queries
- **Bucketing:** by `start_station_id` into 8 buckets — speeds up station-level group-bys and map-side joins

**Data cleaning applied during the INSERT:**

| Issue | Treatment |
|---|---|
| Null or empty `rideable_type` | Replaced with `'unknown'` |
| Null or empty `member_casual` | Replaced with `'unknown'` |
| Null or blank station names/IDs | Set to `NULL` |
| AVRO timestamps stored as Unix milliseconds | Converted via `from_unixtime` with millisecond detection |
| Trips where `ended_at < started_at` | Filtered out |
| Trips with null start or end timestamps | Filtered out |
| Leading/trailing whitespace in string columns | Stripped with `trim()` |

The resulting table `team19_projectdb.citibike_trips_optimized` has 17 columns (13 original + `ride_date`, `ride_weekday`, `ride_hour`, `ride_duration_minutes` derived during insert) and is partitioned into 24 partitions (12 months × 2 years where applicable).

---

## 5. Data Analysis

All exploratory queries were written in HiveQL and executed on the Tez engine. Results were exported as CSVs and visualised as charts. Each insight is presented with its query logic, chart, and a stakeholder-oriented interpretation.

### Insight 1: Seasonal Demand — Monthly Trip Volume

**Query logic:** `GROUP BY ride_year, ride_month` ordered chronologically; counting trips per month.

![Monthly trip volume](output/charts/q1_monthly_trips.png)

**Interpretation.** Winter months (January and February) show the lowest volume, consistent with cold-weather behaviour, while most other months sit close to the dataset's per-month cap of around one million rides. Two months (June and September) appear lower than their neighbours, suggesting a sampling gap in the underlying monthly archives rather than a real demand drop. For operations, the cold-weather dip is the only robust signal to plan capacity around; the June and September anomalies are a data-quality flag to investigate before drawing seasonal conclusions.

---

### Insight 2: Weekly Rhythm — Trips by Day of Week

**Query logic:** `GROUP BY ride_weekday` with mapped weekday names; ordered Monday–Sunday.

![Weekday distribution](output/charts/q2_weekday_distribution.png)

**Interpretation.** Weekday usage dominates total volume, consistent with commuter behaviour. Weekend volumes are lower but typically yield longer individual trips, suggesting a shift from utility commuting to leisure riding. Marketing campaigns and pricing should differentiate the commuter weekday segment from the leisure weekend segment.

---

### Insight 3: Daily Rhythm — Hourly Volume vs. Ride Length

**Query logic:** `GROUP BY ride_hour` returning both trip count and average duration in minutes.

![Hourly trips and duration](output/charts/q3_hourly_trips_duration.png)

**Interpretation.** Two pronounced rush-hour spikes dominate the day (morning and evening), while average ride duration tends to be longer outside those peaks (leisure trips). The combined view tells operations not just when to rebalance bikes, but also that midday rebalancing must account for longer trip times pulling bikes off the grid for extended periods.

---

### Insight 4: Customer Mix — Members vs. Casuals

**Query logic:** `GROUP BY member_casual` returning trip share and average duration.

![Member vs casual](output/charts/q4_member_vs_casual.png)

**Interpretation.** Members account for the majority of trips, but casual riders consistently take longer trips on average. That mix matters for revenue: members drive volume and predictability while casuals drive per-trip revenue and tourist-area utilisation, suggesting different retention and growth strategies for each segment.

---

### Insight 5: Spatial Demand — Top 20 Start Stations

**Query logic:** `GROUP BY start_station_id, start_station_name` ordered by trip count descending, limited to 20.

![Top 20 start stations](output/charts/q5_top20_stations.png)

**Interpretation.** Demand is concentrated in a small number of stations, predominantly midtown and lower Manhattan transit hubs. These hot spots should be the first priority for capacity expansion, preventive maintenance scheduling, and the rebalancing fleet's daily route planning.

---

### Insight 6: Fleet Mix — Rideable Type Usage and Duration

**Query logic:** `GROUP BY rideable_type` returning trip count and average duration.

![Rideable types](output/charts/q6_rideable_types.png)

**Interpretation.** Classic and electric bikes dominate the trip mix; electric bikes typically support shorter or faster trips while classic bikes carry the bulk of volume. Future fleet investment should weigh marginal demand for e-bikes against their higher unit and maintenance cost, using this usage-intensity data as the primary evidence base.

---

## 6. ML Modeling

### 6.1 Problem Definition

The ML task is **binary classification**: given a trip's observable attributes, predict whether the rider is a registered **member** (`label = 1`) or a **casual** user (`label = 0`). This is a binary classification task so the evaluation metrics are **Area Under ROC** and **Area Under PR**.

### 6.2 Feature Extraction and Data Preprocessing

All preprocessing was implemented as a Spark ML `Pipeline` to ensure consistent transformation of both training and test data.

**Data filtering** (applied in `stage3_data_prep.py` before splitting):

| Filter | Rationale |
|---|---|
| `member_casual IN ('member', 'casual')` | Remove the small number of `'unknown'` records introduced during cleaning |
| `ride_duration_minutes > 0 AND <= 240` | Remove data-entry errors (negative or impossibly long trips) |
| Non-null start/end coordinates | Required for distance calculation |
| Non-null `start_station_id` | Required as a categorical feature |

**Derived features:**

| Feature | Derivation |
|---|---|
| `ride_duration_minutes` | `(ended_at - started_at) / 60` — already computed in Stage II |
| `trip_distance_km` | Haversine formula applied to start/end coordinates |
| `is_weekend` | `1` if `ride_weekday IN (6, 7)`, else `0` |

**Data split:** 70% training / 30% test with seed 42. A 2% stratified sample (~200K rows) of the 10.2M total was used for grid search feasibility on the shared YARN queue.

**Pipeline stages (identical base for all three models):**

1. `StringIndexer` — encodes `rideable_type` (3 categories) to numeric index
2. `OneHotEncoder` — converts the index to a sparse binary vector
3. `StringIndexer` — encodes `start_station_id` (high-cardinality) to numeric index
4. `VectorAssembler` — concatenates all numeric features into a single feature vector:
   - `ride_hour`, `ride_weekday`, `ride_month`, `ride_duration_minutes`, `trip_distance_km`, `start_lat`, `start_lng`, `end_lat`, `end_lng`, `is_weekend`, `rideable_vec`, `station_idx`
5. **Scaler** — model-specific (StandardScaler for RF and SVM; MinMaxScaler for NB)
6. **Classifier** — model-specific

### 6.3 Model Training and Hyperparameter Tuning

All models were trained on YARN cluster (`--master yarn`) using `spark-submit`. Grid search used 3-fold cross-validation optimising for AUC-ROC.

#### Model 1 — Random Forest (RF)

| Hyperparameter | Grid values | Best value |
|---|---|---|
| `numTrees` | 20, 50, 100 | **100** |
| `maxDepth` | 5, 10, 15 | **15** |
| `minInstancesPerNode` | 1, 5, 10 | **10** |

Total combinations: 27 | Cross-validation: 3-fold | Training time: **~2,335 s**

#### Model 2 — Linear SVM (LinearSVC)

| Hyperparameter | Grid values | Best value |
|---|---|---|
| `regParam` | 0.001, 0.01, 0.1 | **0.001** |
| `aggregationDepth` | 2, 4, 8 | **2** |
| `tol` | 0.0001, 0.001, 0.01 | **0.0001** |

Total combinations: 27 | Cross-validation: 3-fold | Training time: **~566 s**

#### Model 3 — Naive Bayes (Gaussian)

| Hyperparameter | Grid values | Best value |
|---|---|---|
| `smoothing` | 0.5, 1.0, 2.0 | **2.0** |
| `scaler_min` | 0.0, 0.05, 0.1 | **0.05** |
| `scaler_max` | 0.5, 1.0, 2.0 | **0.5** |

Total combinations: 27 | Cross-validation: 3-fold | Training time: **~133 s**

### 6.4 Evaluation

All best models were evaluated on the held-out test set (30% of the working sample):

| Model | AUC-ROC | AUC-PR | Training Time (s) |
|---|---|---|---|
| **Random Forest** | **0.7345** | **0.9210** | 2,334.8 |
| Linear SVM | 0.6440 | 0.8795 | 565.7 |
| Naive Bayes | 0.5793 | 0.8538 | 132.6 |

**Best model: Random Forest** (`model1_rf`) — highest AUC-ROC (0.7345) and AUC-PR (0.9210) on the test set.

The Random Forest outperforms both SVM and Naive Bayes, which is expected given the non-linear relationships between trip attributes and rider type (e.g., the interaction between `ride_hour`, `trip_distance_km`, and `start_station_id`). Naive Bayes is the fastest to train but assumes feature independence, which does not hold here.

### 6.5 Sample Prediction

A representative single-trip prediction was made using the best model (RF):

| Feature | Value |
|---|---|
| `ride_id` | sample-001 |
| `rideable_type` | classic_bike |
| `ride_hour` | 18 |
| `ride_weekday` | 2 (Tuesday) |
| `ride_month` | 6 |
| `ride_duration_minutes` | 12.5 |
| `start_station_id` | 6140.05 |
| `start_lat / start_lng` | 40.7421 / -73.9942 |
| `end_lat / end_lng` | 40.7368 / -73.9856 |
| `is_weekend` | 0 |
| `trip_distance_km` | 1.85 |
| **Prediction** | **1.0 (member)** |
| **Probability [casual, member]** | [0.134, 0.866] |

The model predicts with 86.6% confidence that a 12.5-minute Tuesday evening trip on a classic bike is taken by a registered member — consistent with the commuter pattern identified in the EDA.

---

## 7. Data Presentation

### 7.1 Dashboard Overview

The project results are presented in an Apache Superset dashboard titled **"Team 19 — Citi Bike Big Data Pipeline"**. The dashboard is organised into three tabs, each targeting a different audience and set of questions.

### 7.2 Dashboard Structure

**Tab 1 — Data Description**

This tab presents the dataset's characteristics for a non-technical audience. It includes: total record count from the PostgreSQL `citibike_trips` table, column names and data types (queried from `information_schema.columns`), a sample of 20 raw rows, and a text block summarising the data cleaning steps applied in Stage II.

**Tab 2 — Data Insights**

This tab presents all six EDA insights from Stage II using the pre-aggregated Hive result tables (`q1_results` through `q6_results`). Each chart is accompanied by a text block containing the stakeholder story from the EDA report. Chart types: Line (monthly volume), Bar (weekday distribution), Dual-axis Bar+Line (hourly patterns), Pie+Bar (member/casual mix), Horizontal Bar (top stations), Bar+Line (rideable types).

**Tab 3 — ML Modeling Results**

This tab presents the full ML pipeline output for a data-literate audience. It includes: AUC-ROC and AUC-PR bar charts comparing all three models, a model comparison table with best hyperparameters and training times, prediction probability histograms per model, a confusion matrix table, feature distribution charts from the training sample, and the single-trip sample prediction demo.

### 7.3 Key Findings from the Dashboard

- **Members dominate volume but casuals drive duration** — the fleet must serve two distinct use patterns simultaneously.
- **Station concentration** — the top 20 stations account for a disproportionate share of trips, making targeted investment high-ROI.
- **Rush-hour peaks** are sharp and predictable, enabling precise rebalancing schedules.
- **Random Forest is the most accurate rider-type classifier** (AUC-ROC 0.735), but all three models confirm that `ride_hour`, `trip_distance_km`, and `start_station_id` are the strongest predictors of member vs. casual status.

---

## 8. Conclusion

### 8.1 Summary

This project delivered a complete, reproducible big data pipeline over 10.2 million Citi Bike trips from 2023. Starting from raw CSV files on Kaggle, the pipeline ingested data into a distributed PostgreSQL database, transferred it to HDFS in Avro+Snappy format, prepared an optimised ORC/Snappy Hive table with partitioning and bucketing, performed six EDA queries with charts and business stories, trained three Spark ML classifiers with grid search and 3-fold cross-validation, and presented all results in an Apache Superset dashboard.

The best classifier — Random Forest with `numTrees=100`, `maxDepth=15`, `minInstancesPerNode=10` — achieves AUC-ROC of 0.735 and AUC-PR of 0.921 on the held-out test set, demonstrating that rider type can be predicted with meaningful accuracy from trip-level features alone.

---

## 9. Reflections on Own Work

### 9.1 Challenges and Difficulties

**YARN resource saturation (Stage III).** The shared cluster YARN queue was frequently saturated during Stage III grid search. We had to reduce the sample fraction and the Spark executor memory request multiple times before achieving stable job completion. The final working configuration uses a 2% sample (~200K rows) which is statistically sufficient for AUC metrics but smaller than we originally intended.

**Hive metastore connectivity in Spark (Stage III).** Configuring PySpark to connect to the remote Hive metastore required placing `hive-site.xml` explicitly on both the driver and executor classpaths via `spark-submit` flags. This was not documented in the course material and cost significant debugging time.

**Naive Bayes feature compatibility.** The NB model requires non-negative input features. The `ChiSqSelector` step we originally included was incompatible with continuous features in our pipeline and had to be removed. We also had to switch from Bernoulli to Gaussian NB and adjust the MinMaxScaler range to ensure all features were strictly positive.

**Timestamp parsing from AVRO (Stage II).** Sqoop serialised the `started_at` and `ended_at` timestamps as Unix timestamps (integer), and different monthly CSV files used different scales (seconds vs. milliseconds). The HQL insert query required a conditional conversion with millisecond detection.

**June and September data gap (Stage II).** Two months showed significantly lower trip counts than expected. Investigation revealed that the Kaggle archive was missing some monthly files. This was documented in the EDA story rather than fixed, as re-sourcing the data was outside the project scope.

### 9.2 Recommendations

- For future runs, use a dedicated YARN queue or a larger cluster to enable grid search over the full dataset (10.2M rows) rather than a 2% sample.
- The `rideable_type` feature would benefit from normalisation at the source level before ingestion — the raw data contains inconsistent casing and spacing that had to be handled in HQL.
- A fourth model type (e.g., Gradient Boosted Trees) would likely improve AUC-ROC further and would be a natural extension of the Stage III pipeline given that RF already outperforms linear and probabilistic classifiers.
- The Superset dashboard should be connected to live Hive tables so results refresh automatically when models are retrained.

### 9.3 Team Contributions

| Project Task | Description | Alex Kachmazov | Vladimir Rublev | Egor Sergeev | Anton Korotkov | Deliverables | Avg Hours |
|---|---|---|---|---|---|---|---|
| Dataset selection & exploration | Identify CitiBike dataset, verify criteria, submit to TA | 25% | 25% | 25% | 25% | Dataset confirmed | 2 |
| Stage I — PostgreSQL setup | Write `create_tables.sql`, `build_projectdb.py`, load data | 0% | 0% | 0% | 100% | `sql/create_tables.sql`, `scripts/build_projectdb.py` | 6 |
| Stage I — HDFS ingestion | Write `data_ingestion.sh`, verify Sqoop export | 0% | 0% | 0% | 100% | `scripts/data_ingestion.sh`, `.avsc`, `.java` | 4 |
| Stage II — Hive table design | Design ORC schema, partitioning, bucketing, write `db.hql` | 100% | 0% | 0% | 0% | `sql/db.hql` | 8 |
| Stage II — EDA queries & charts | Write 6 HQL queries, generate charts, write narrative | 100% | 0% | 0% | 0% | `sql/q1-q6.hql`, `output/charts/`, `stage2_eda_report.md` | 10 |
| Stage III — Data preprocessing | Feature engineering, Haversine distance, pipeline design | 0% | 100% | 0% | 0% | `scripts/stage3_data_prep.py` | 8 |
| Stage III — RF model | Implement RF pipeline, grid search, CV, evaluation | 0% | 100% | 0% | 0% | `scripts/stage3_model_rf.py`, `models/model1_rf/` | 10 |
| Stage III — SVM model | Implement SVM pipeline, grid search, CV, evaluation | 0% | 100% | 0% | 0% | `scripts/stage3_model_svm.py`, `models/model2_svm/` | 8 |
| Stage III — NB model | Implement NB pipeline, debugging compatibility issues | 0% | 100% | 0% | 0% | `scripts/stage3_model_nb.py`, `models/model3_nb/` | 10 |
| Stage IV — Superset pipeline | Write `stage4.sh`, `stage4_preprocess.py`, `stage4.hql` | 0% | 0% | 100% | 0% | `scripts/stage4*.py`, `sql/stage4.hql` | 8 |
| Dashboard construction | Build and publish Superset dashboard | 0% | 0% | 100% | 0% | Published dashboard | 6 |
| Report writing | Compile full project report | 0% | 0% | 100% | 0% | `report.md` | 6 |
