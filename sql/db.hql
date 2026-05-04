SET hive.execution.engine=tez;
SET hive.tez.container.size=4096;
SET hive.tez.java.opts=-Xmx3276m;
SET hive.auto.convert.join=true;
SET hive.auto.convert.join.noconditionaltask.size=536870912;
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;
SET hive.exec.max.dynamic.partitions=2000;
SET hive.exec.max.dynamic.partitions.pernode=1000;
SET hive.exec.max.created.files=100000;
SET hive.enforce.bucketing=true;
SET hive.vectorized.execution.enabled=true;
SET hive.vectorized.execution.reduce.enabled=true;

DROP DATABASE IF EXISTS team19_projectdb CASCADE;

CREATE DATABASE team19_projectdb
LOCATION '/user/team19/project/hive/warehouse/team19_projectdb.db';

USE team19_projectdb;

CREATE EXTERNAL TABLE citibike_trips_raw
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.avro.AvroSerDe'
STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.avro.AvroContainerInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.avro.AvroContainerOutputFormat'
LOCATION '/user/team19/project/warehouse/citibike_trips'
TBLPROPERTIES (
    'avro.schema.url'='hdfs:///user/team19/project/warehouse/avsc/citibike_trips.avsc'
);

DESCRIBE citibike_trips_raw;

DROP TABLE IF EXISTS citibike_trips_optimized;

CREATE EXTERNAL TABLE citibike_trips_optimized (
    ride_id STRING,
    rideable_type STRING,
    started_at_ts TIMESTAMP,
    ended_at_ts TIMESTAMP,
    ride_date STRING,
    ride_weekday INT,
    ride_hour INT,
    ride_duration_minutes DOUBLE,
    start_station_name STRING,
    start_station_id STRING,
    end_station_name STRING,
    end_station_id STRING,
    start_lat DOUBLE,
    start_lng DOUBLE,
    end_lat DOUBLE,
    end_lng DOUBLE,
    member_casual STRING
)
PARTITIONED BY (
    ride_year INT,
    ride_month INT
)
CLUSTERED BY (start_station_id) INTO 8 BUCKETS
STORED AS ORC
LOCATION '/user/team19/project/hive/warehouse/team19_projectdb.db/citibike_trips_optimized'
TBLPROPERTIES (
    'orc.compress'='SNAPPY'
);

INSERT OVERWRITE TABLE citibike_trips_optimized PARTITION (ride_year, ride_month)
SELECT
    ride_id,
    CASE
        WHEN rideable_type IS NULL OR trim(rideable_type) = '' THEN 'unknown'
        ELSE lower(trim(rideable_type))
    END AS rideable_type,
    started_at_ts,
    ended_at_ts,
    CAST(to_date(started_at_ts) AS STRING) AS ride_date,
    CAST(pmod(datediff(to_date(started_at_ts), '1970-01-05'), 7) + 1 AS INT) AS ride_weekday,
    hour(started_at_ts) AS ride_hour,
    ROUND((unix_timestamp(ended_at_ts) - unix_timestamp(started_at_ts)) / 60.0, 2) AS ride_duration_minutes,
    CASE
        WHEN start_station_name IS NULL OR trim(start_station_name) = '' THEN NULL
        ELSE trim(start_station_name)
    END AS start_station_name,
    CASE
        WHEN start_station_id IS NULL OR trim(start_station_id) = '' THEN NULL
        ELSE trim(start_station_id)
    END AS start_station_id,
    CASE
        WHEN end_station_name IS NULL OR trim(end_station_name) = '' THEN NULL
        ELSE trim(end_station_name)
    END AS end_station_name,
    CASE
        WHEN end_station_id IS NULL OR trim(end_station_id) = '' THEN NULL
        ELSE trim(end_station_id)
    END AS end_station_id,
    start_lat,
    start_lng,
    end_lat,
    end_lng,
    CASE
        WHEN member_casual IS NULL OR trim(member_casual) = '' THEN 'unknown'
        ELSE lower(trim(member_casual))
    END AS member_casual,
    year(started_at_ts) AS ride_year,
    month(started_at_ts) AS ride_month
FROM (
    SELECT
        ride_id,
        rideable_type,
        CASE
            WHEN started_at IS NULL THEN NULL
            WHEN started_at > 100000000000 THEN CAST(from_unixtime(CAST(started_at / 1000 AS BIGINT)) AS TIMESTAMP)
            ELSE CAST(from_unixtime(CAST(started_at AS BIGINT)) AS TIMESTAMP)
        END AS started_at_ts,
        CASE
            WHEN ended_at IS NULL THEN NULL
            WHEN ended_at > 100000000000 THEN CAST(from_unixtime(CAST(ended_at / 1000 AS BIGINT)) AS TIMESTAMP)
            ELSE CAST(from_unixtime(CAST(ended_at AS BIGINT)) AS TIMESTAMP)
        END AS ended_at_ts,
        start_station_name,
        start_station_id,
        end_station_name,
        end_station_id,
        start_lat,
        start_lng,
        end_lat,
        end_lng,
        member_casual
    FROM citibike_trips_raw
) typed
WHERE started_at_ts IS NOT NULL
  AND ended_at_ts IS NOT NULL
  AND unix_timestamp(ended_at_ts) >= unix_timestamp(started_at_ts);

MSCK REPAIR TABLE citibike_trips_optimized;

DESCRIBE FORMATTED citibike_trips_optimized;
