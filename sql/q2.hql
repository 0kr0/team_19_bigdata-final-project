SET hive.execution.engine=tez;
SET hive.vectorized.execution.enabled=true;
SET hive.vectorized.execution.reduce.enabled=true;

USE team19_projectdb;

DROP TABLE IF EXISTS q2_results;

CREATE TABLE q2_results (
    weekday_number INT,
    weekday_name STRING,
    trip_count BIGINT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE q2_results
SELECT
    ride_weekday AS weekday_number,
    CASE ride_weekday
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
        WHEN 7 THEN 'Sunday'
        ELSE 'unknown'
    END AS weekday_name,
    COUNT(1) AS trip_count
FROM citibike_trips_optimized
GROUP BY ride_weekday
ORDER BY ride_weekday;

INSERT OVERWRITE DIRECTORY '/user/team19/project/hive/exports/stage2/q2'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT
    weekday_number,
    weekday_name,
    trip_count
FROM q2_results
ORDER BY weekday_number;
