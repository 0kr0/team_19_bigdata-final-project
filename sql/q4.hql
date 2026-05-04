SET hive.execution.engine=tez;
SET hive.vectorized.execution.enabled=true;
SET hive.vectorized.execution.reduce.enabled=true;

USE team19_projectdb;

DROP TABLE IF EXISTS q4_results;

CREATE TABLE q4_results (
    rider_type STRING,
    trip_count BIGINT,
    avg_ride_duration_minutes DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE q4_results
SELECT
    member_casual AS rider_type,
    COUNT(1) AS trip_count,
    ROUND(AVG(ride_duration_minutes), 2) AS avg_ride_duration_minutes
FROM citibike_trips_optimized
GROUP BY member_casual
ORDER BY trip_count DESC;

INSERT OVERWRITE DIRECTORY '/user/team19/project/hive/exports/stage2/q4'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT
    rider_type,
    trip_count,
    avg_ride_duration_minutes
FROM q4_results
ORDER BY trip_count DESC;
