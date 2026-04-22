SET hive.execution.engine=mr;

USE team19_projectdb;

DROP TABLE IF EXISTS q5_results;

CREATE TABLE q5_results (
    start_station_id STRING,
    start_station_name STRING,
    trip_count BIGINT,
    avg_ride_duration_minutes DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE q5_results
SELECT
    start_station_id,
    regexp_replace(COALESCE(start_station_name, 'unknown'), ',', ' ') AS start_station_name,
    COUNT(1) AS trip_count,
    ROUND(AVG(ride_duration_minutes), 2) AS avg_ride_duration_minutes
FROM citibike_trips_optimized
WHERE start_station_id IS NOT NULL
GROUP BY start_station_id, regexp_replace(COALESCE(start_station_name, 'unknown'), ',', ' ')
ORDER BY trip_count DESC
LIMIT 20;

INSERT OVERWRITE DIRECTORY '/user/team19/project/hive/exports/stage2/q5'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT
    start_station_id,
    start_station_name,
    trip_count,
    avg_ride_duration_minutes
FROM q5_results
ORDER BY trip_count DESC;
