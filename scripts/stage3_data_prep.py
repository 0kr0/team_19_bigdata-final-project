"""Stage 3 data preparation.

Reads team19_projectdb.citibike_trips_optimized via Hive, applies row
filters, derives feature columns (haversine trip distance, is_weekend,
binary label), splits 70/30 with a fixed seed, and writes train/test
parquet datasets to HDFS for the model scripts to consume.

The default sample fraction (STAGE3_SAMPLE_FRACTION env var) is 0.05 -
~500K rows out of the 10.2M total - which keeps grid search + 3-fold CV
feasible on a small YARN queue while remaining statistically robust for
AUC metrics. Override the env var to use a different fraction.
"""
import os
import sys

from pyspark.sql import SparkSession


HDFS_TRAIN = "/user/team19/project/data/stage3/train"
HDFS_TEST = "/user/team19/project/data/stage3/test"
SAMPLE_FRACTION = float(os.environ.get("STAGE3_SAMPLE_FRACTION", "0.05"))


def main():
    spark = (
        SparkSession.builder
        .appName("team19-stage3-data-prep")
        .enableHiveSupport()
        .config("spark.sql.catalogImplementation", "hive")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    df = spark.sql("""
        SELECT
            ride_id,
            rideable_type,
            ride_hour,
            ride_weekday,
            ride_month,
            ride_duration_minutes,
            start_station_id,
            start_lat, start_lng, end_lat, end_lng,
            CASE WHEN ride_weekday IN (6, 7) THEN 1 ELSE 0 END AS is_weekend,
            2 * 6371 * ASIN(SQRT(
                POWER(SIN(RADIANS(end_lat - start_lat) / 2), 2) +
                COS(RADIANS(start_lat)) * COS(RADIANS(end_lat)) *
                POWER(SIN(RADIANS(end_lng - start_lng) / 2), 2)
            )) AS trip_distance_km,
            CASE WHEN member_casual = 'member' THEN 1.0 ELSE 0.0 END AS label
        FROM team19_projectdb.citibike_trips_optimized
        WHERE member_casual IN ('member', 'casual')
          AND ride_duration_minutes IS NOT NULL
          AND ride_duration_minutes > 0
          AND ride_duration_minutes <= 240
          AND start_lat IS NOT NULL AND start_lng IS NOT NULL
          AND end_lat IS NOT NULL AND end_lng IS NOT NULL
          AND start_station_id IS NOT NULL
          AND rideable_type IS NOT NULL
    """)

    if 0 < SAMPLE_FRACTION < 1.0:
        df = df.sample(fraction=SAMPLE_FRACTION, seed=42)

    df = df.cache()
    total = df.count()
    print("Stage 3 working set rows: " + str(total))
    if total == 0:
        spark.stop()
        sys.exit("Stage 3 working set is empty after filters.")

    train, test = df.randomSplit([0.7, 0.3], seed=42)

    train.write.mode("overwrite").parquet(HDFS_TRAIN)
    test.write.mode("overwrite").parquet(HDFS_TEST)

    train.limit(1000).toPandas().to_csv("output/train_sample.csv", index=False)
    test.limit(1000).toPandas().to_csv("output/test_sample.csv", index=False)

    print("Train rows: " + str(train.count()))
    print("Test rows: " + str(test.count()))

    spark.stop()


if __name__ == "__main__":
    main()
