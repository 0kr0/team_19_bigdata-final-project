"""Stage 3 specific-sample prediction (rubric's 2-point requirement).

Loads the overall best model selected by stage3.sh (stored as a single
line in output/best_model.txt) and runs it on a single hand-built ride.
The result is written to output/sample_prediction.csv as (feature, value)
rows plus a final 'prediction' row and 'raw_or_probability' row.
"""
import csv

from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel


HDFS_MODELS = "/user/team19/project/models"


SAMPLE = {
    "ride_id": "sample-001",
    "rideable_type": "classic_bike",
    "ride_hour": 18,
    "ride_weekday": 2,
    "ride_month": 6,
    "ride_duration_minutes": 12.5,
    "start_station_id": "6140.05",
    "start_lat": 40.7421,
    "start_lng": -73.9942,
    "end_lat": 40.7368,
    "end_lng": -73.9856,
    "is_weekend": 0,
    "trip_distance_km": 1.85,
}


def main():
    spark = (
        SparkSession.builder
        .appName("team19-stage3-predict-sample")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    with open("output/best_model.txt") as fh:
        best_name = fh.read().strip()
    print("Using best model: " + best_name)

    model = PipelineModel.load(HDFS_MODELS + "/" + best_name)

    sample_df = spark.createDataFrame([SAMPLE])
    prediction_row = model.transform(sample_df).collect()[0]
    prediction = prediction_row["prediction"]

    raw = None
    fields = prediction_row.asDict()
    if "probability" in fields:
        raw = fields["probability"]
    elif "rawPrediction" in fields:
        raw = fields["rawPrediction"]
    raw_str = str(raw) if raw is not None else ""

    with open("output/sample_prediction.csv", "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["feature", "value"])
        for key, value in SAMPLE.items():
            writer.writerow([key, value])
        writer.writerow(["model_used", best_name])
        writer.writerow(["prediction", prediction])
        writer.writerow(["raw_or_probability", raw_str])

    spark.stop()


if __name__ == "__main__":
    main()
