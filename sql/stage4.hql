-- Stage 4: external Hive tables for Stage 3 ML outputs.
--
-- All tables live in team19_projectdb alongside the Stage 2 tables.
-- Each dataset follows the pattern:
--   <name>_raw  external table (OpenCSVSerde, all columns STRING)
--   <name>      view with properly typed columns for Superset charting
--
-- HDFS data is under /user/team19/project/hive/exports/stage4/<name>/

SET hive.execution.engine=tez;

USE team19_projectdb;

-- ============================================================
-- 1. Evaluation metrics  (evaluation.csv)
--    model_name, metric_name, metric_value
-- ============================================================
DROP VIEW  IF EXISTS stage3_evaluation;
DROP TABLE IF EXISTS stage3_evaluation_raw;

CREATE EXTERNAL TABLE stage3_evaluation_raw (
    model_name   STRING,
    metric_name  STRING,
    metric_value STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    "separatorChar" = ",",
    "quoteChar"     = "\""
)
STORED AS TEXTFILE
LOCATION '/user/team19/project/hive/exports/stage4/evaluation'
TBLPROPERTIES ("skip.header.line.count" = "1");

CREATE VIEW stage3_evaluation AS
SELECT
    model_name,
    metric_name,
    CAST(metric_value AS DOUBLE) AS metric_value
FROM stage3_evaluation_raw;

-- ============================================================
-- 2. Model comparison  (model_comparison.csv)
--    model_name, area_under_roc, area_under_pr,
--    training_time_sec, best_params_json
-- ============================================================
DROP VIEW  IF EXISTS stage3_model_comparison;
DROP TABLE IF EXISTS stage3_model_comparison_raw;

CREATE EXTERNAL TABLE stage3_model_comparison_raw (
    model_name        STRING,
    area_under_roc    STRING,
    area_under_pr     STRING,
    training_time_sec STRING,
    best_params_json  STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    "separatorChar" = ",",
    "quoteChar"     = "\""
)
STORED AS TEXTFILE
LOCATION '/user/team19/project/hive/exports/stage4/model_comparison'
TBLPROPERTIES ("skip.header.line.count" = "1");

CREATE VIEW stage3_model_comparison AS
SELECT
    model_name,
    CAST(area_under_roc    AS DOUBLE) AS area_under_roc,
    CAST(area_under_pr     AS DOUBLE) AS area_under_pr,
    CAST(training_time_sec AS DOUBLE) AS training_time_sec,
    best_params_json
FROM stage3_model_comparison_raw;

-- ============================================================
-- 3. Predictions — all three models combined  (predictions.csv)
--    model_name, ride_id, label, prediction, probability
--    probability = class-1 score (true prob for RF/NB; decision
--    margin for SVM)
-- ============================================================
DROP VIEW  IF EXISTS stage3_predictions;
DROP TABLE IF EXISTS stage3_predictions_raw;

CREATE EXTERNAL TABLE stage3_predictions_raw (
    model_name  STRING,
    ride_id     STRING,
    label       STRING,
    prediction  STRING,
    probability STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    "separatorChar" = ",",
    "quoteChar"     = "\""
)
STORED AS TEXTFILE
LOCATION '/user/team19/project/hive/exports/stage4/predictions'
TBLPROPERTIES ("skip.header.line.count" = "1");

CREATE VIEW stage3_predictions AS
SELECT
    model_name,
    ride_id,
    CAST(label       AS DOUBLE) AS label,
    CAST(prediction  AS DOUBLE) AS prediction,
    CAST(probability AS DOUBLE) AS probability
FROM stage3_predictions_raw;

-- ============================================================
-- 4. Training sample  (train_sample.csv)
--    ride_id, rideable_type, ride_hour, ride_weekday, ride_month,
--    ride_duration_minutes, start_station_id, start_lat, start_lng,
--    end_lat, end_lng, is_weekend, trip_distance_km, label
-- ============================================================
DROP VIEW  IF EXISTS stage3_train_sample;
DROP TABLE IF EXISTS stage3_train_sample_raw;

CREATE EXTERNAL TABLE stage3_train_sample_raw (
    ride_id               STRING,
    rideable_type         STRING,
    ride_hour             STRING,
    ride_weekday          STRING,
    ride_month            STRING,
    ride_duration_minutes STRING,
    start_station_id      STRING,
    start_lat             STRING,
    start_lng             STRING,
    end_lat               STRING,
    end_lng               STRING,
    is_weekend            STRING,
    trip_distance_km      STRING,
    label                 STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    "separatorChar" = ",",
    "quoteChar"     = "\""
)
STORED AS TEXTFILE
LOCATION '/user/team19/project/hive/exports/stage4/train_sample'
TBLPROPERTIES ("skip.header.line.count" = "1");

CREATE VIEW stage3_train_sample AS
SELECT
    ride_id,
    rideable_type,
    CAST(ride_hour             AS INT)    AS ride_hour,
    CAST(ride_weekday          AS INT)    AS ride_weekday,
    CAST(ride_month            AS INT)    AS ride_month,
    CAST(ride_duration_minutes AS DOUBLE) AS ride_duration_minutes,
    start_station_id,
    CAST(start_lat             AS DOUBLE) AS start_lat,
    CAST(start_lng             AS DOUBLE) AS start_lng,
    CAST(end_lat               AS DOUBLE) AS end_lat,
    CAST(end_lng               AS DOUBLE) AS end_lng,
    CAST(is_weekend            AS INT)    AS is_weekend,
    CAST(trip_distance_km      AS DOUBLE) AS trip_distance_km,
    CAST(label                 AS DOUBLE) AS label
FROM stage3_train_sample_raw;

-- ============================================================
-- 5. Test sample  (test_sample.csv)  — same schema as train
-- ============================================================
DROP VIEW  IF EXISTS stage3_test_sample;
DROP TABLE IF EXISTS stage3_test_sample_raw;

CREATE EXTERNAL TABLE stage3_test_sample_raw (
    ride_id               STRING,
    rideable_type         STRING,
    ride_hour             STRING,
    ride_weekday          STRING,
    ride_month            STRING,
    ride_duration_minutes STRING,
    start_station_id      STRING,
    start_lat             STRING,
    start_lng             STRING,
    end_lat               STRING,
    end_lng               STRING,
    is_weekend            STRING,
    trip_distance_km      STRING,
    label                 STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    "separatorChar" = ",",
    "quoteChar"     = "\""
)
STORED AS TEXTFILE
LOCATION '/user/team19/project/hive/exports/stage4/test_sample'
TBLPROPERTIES ("skip.header.line.count" = "1");

CREATE VIEW stage3_test_sample AS
SELECT
    ride_id,
    rideable_type,
    CAST(ride_hour             AS INT)    AS ride_hour,
    CAST(ride_weekday          AS INT)    AS ride_weekday,
    CAST(ride_month            AS INT)    AS ride_month,
    CAST(ride_duration_minutes AS DOUBLE) AS ride_duration_minutes,
    start_station_id,
    CAST(start_lat             AS DOUBLE) AS start_lat,
    CAST(start_lng             AS DOUBLE) AS start_lng,
    CAST(end_lat               AS DOUBLE) AS end_lat,
    CAST(end_lng               AS DOUBLE) AS end_lng,
    CAST(is_weekend            AS INT)    AS is_weekend,
    CAST(trip_distance_km      AS DOUBLE) AS trip_distance_km,
    CAST(label                 AS DOUBLE) AS label
FROM stage3_test_sample_raw;

-- ============================================================
-- 6. Sample prediction demo  (sample_prediction.csv)
--    feature, value  (key-value pairs for one hand-built ride)
-- ============================================================
DROP TABLE IF EXISTS stage3_sample_prediction;

CREATE EXTERNAL TABLE stage3_sample_prediction (
    feature STRING,
    value   STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    "separatorChar" = ",",
    "quoteChar"     = "\""
)
STORED AS TEXTFILE
LOCATION '/user/team19/project/hive/exports/stage4/sample_prediction'
TBLPROPERTIES ("skip.header.line.count" = "1");