SET hive.execution.engine=tez;
SET hive.vectorized.execution.enabled=true;
SET hive.vectorized.execution.reduce.enabled=true;

USE team19_projectdb;

DROP TABLE IF EXISTS q6_results;

CREATE TABLE q6_results (
    rideable_type STRING,
    trip_count BIGINT,
    avg_ride_duration_minutes DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE q6_results
SELECT
    rideable_type,
    COUNT(1) AS trip_count,
    ROUND(AVG(ride_duration_minutes), 2) AS avg_ride_duration_minutes
FROM citibike_trips_optimized
GROUP BY rideable_type
ORDER BY trip_count DESC;

INSERT OVERWRITE DIRECTORY '/user/team19/project/hive/exports/stage2/q6'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT
    rideable_type,
    trip_count,
    avg_ride_duration_minutes
FROM q6_results
ORDER BY trip_count DESC;
