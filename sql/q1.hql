SET hive.execution.engine=tez;
SET hive.vectorized.execution.enabled=true;
SET hive.vectorized.execution.reduce.enabled=true;

USE team19_projectdb;

DROP TABLE IF EXISTS q1_results;

CREATE TABLE q1_results (
    ride_year INT,
    ride_month INT,
    year_month STRING,
    trip_count BIGINT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE q1_results
SELECT
    ride_year,
    ride_month,
    concat(CAST(ride_year AS STRING), '-', lpad(CAST(ride_month AS STRING), 2, '0')) AS year_month,
    COUNT(1) AS trip_count
FROM citibike_trips_optimized
GROUP BY ride_year, ride_month
ORDER BY ride_year, ride_month;

INSERT OVERWRITE DIRECTORY '/user/team19/project/hive/exports/stage2/q1'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT
    ride_year,
    ride_month,
    year_month,
    trip_count
FROM q1_results
ORDER BY ride_year, ride_month;
