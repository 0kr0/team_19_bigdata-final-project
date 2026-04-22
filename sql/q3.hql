SET hive.execution.engine=mr;

USE team19_projectdb;

DROP TABLE IF EXISTS q3_results;

CREATE TABLE q3_results (
    ride_hour INT,
    trip_count BIGINT,
    avg_ride_duration_minutes DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE q3_results
SELECT
    ride_hour,
    COUNT(1) AS trip_count,
    ROUND(AVG(ride_duration_minutes), 2) AS avg_ride_duration_minutes
FROM citibike_trips_optimized
GROUP BY ride_hour
ORDER BY ride_hour;

INSERT OVERWRITE DIRECTORY '/user/team19/project/hive/exports/stage2/q3'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT
    ride_hour,
    trip_count,
    avg_ride_duration_minutes
FROM q3_results
ORDER BY ride_hour;
