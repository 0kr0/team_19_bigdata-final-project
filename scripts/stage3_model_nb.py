"""Stage 3 model 3: Naive Bayes classifier (Gaussian variant).

Naive Bayes in Spark MLlib supports four modelTypes; only "gaussian" is
robust to our pipeline's mix of continuous lat/lng/duration columns.
"multinomial" and "complement" reject negative values, but Spark's
MinMaxScaler can produce slightly-negative outputs when a CV validation
fold contains values below the training fold's minimum. "bernoulli"
requires strict {0, 1} features. Sticking to "gaussian" keeps the
pipeline working across all 27 grid combinations.

Grid (27 combinations = 3^3):
- nb.smoothing in {0.5, 1.0, 2.0}        - algorithm hyperparameter
                                            (Laplace smoothing).
- scaler.min  in {0.0, 0.05, 0.1}        - model hyperparameter
                                            (preprocessing floor).
- scaler.max  in {0.5, 1.0, 2.0}         - model hyperparameter
                                            (preprocessing ceiling).
"""
import csv
import json
import time

from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import udf
from pyspark.ml import Pipeline
from pyspark.ml.feature import (
    StringIndexer, OneHotEncoder, VectorAssembler, MinMaxScaler
)
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder


MODEL_NAME = "model3_nb"
HDFS_TRAIN = "/user/team19/project/data/stage3/train"
HDFS_TEST = "/user/team19/project/data/stage3/test"
HDFS_MODEL = "/user/team19/project/models/" + MODEL_NAME


def main():
    spark = (
        SparkSession.builder
        .appName("team19-stage3-" + MODEL_NAME)
        .enableHiveSupport()
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    train = spark.read.parquet(HDFS_TRAIN)
    test = spark.read.parquet(HDFS_TEST)

    rideable_idx = StringIndexer(
        inputCol="rideable_type", outputCol="rideable_idx",
        handleInvalid="keep",
    )
    rideable_ohe = OneHotEncoder(
        inputCols=["rideable_idx"], outputCols=["rideable_vec"],
        handleInvalid="keep",
    )
    station_idx = StringIndexer(
        inputCol="start_station_id", outputCol="station_idx",
        handleInvalid="keep",
    )
    assembler = VectorAssembler(
        inputCols=[
            "ride_hour", "ride_weekday", "ride_month",
            "ride_duration_minutes", "trip_distance_km",
            "start_lat", "start_lng", "end_lat", "end_lng", "is_weekend",
            "rideable_vec", "station_idx",
        ],
        outputCol="features_raw",
        handleInvalid="keep",
    )
    scaler = MinMaxScaler(
        inputCol="features_raw", outputCol="features",
    )
    nb = NaiveBayes(
        featuresCol="features", labelCol="label", modelType="gaussian"
    )
    pipeline = Pipeline(stages=[
        rideable_idx, rideable_ohe, station_idx, assembler, scaler, nb,
    ])

    grid = (
        ParamGridBuilder()
        .addGrid(nb.smoothing, [0.5, 1.0, 2.0])
        .addGrid(scaler.min, [0.0, 0.05, 0.1])
        .addGrid(scaler.max, [0.5, 1.0, 2.0])
        .build()
    )
    eval_roc = BinaryClassificationEvaluator(
        labelCol="label", rawPredictionCol="rawPrediction",
        metricName="areaUnderROC",
    )
    eval_pr = BinaryClassificationEvaluator(
        labelCol="label", rawPredictionCol="rawPrediction",
        metricName="areaUnderPR",
    )
    cv = CrossValidator(
        estimator=pipeline,
        estimatorParamMaps=grid,
        evaluator=eval_roc,
        numFolds=3,
        seed=42,
        parallelism=1,
    )

    started = time.time()
    cv_model = cv.fit(train)
    elapsed = time.time() - started

    best_pipeline = cv_model.bestModel
    best_nb = best_pipeline.stages[-1]
    best_scaler = best_pipeline.stages[-2]
    best_params = {
        "smoothing": best_nb.getOrDefault(best_nb.getParam("smoothing")),
        "scaler_min": best_scaler.getOrDefault(best_scaler.getParam("min")),
        "scaler_max": best_scaler.getOrDefault(best_scaler.getParam("max")),
    }

    predictions = best_pipeline.transform(test)
    auc_roc = eval_roc.evaluate(predictions)
    auc_pr = eval_pr.evaluate(predictions)

    best_pipeline.write().overwrite().save(HDFS_MODEL)

    pos_prob = udf(
        lambda v: float(v[1]) if v is not None else None, DoubleType()
    )
    sample = (
        predictions
        .select(
            "ride_id", "label", "prediction",
            pos_prob("probability").alias("probability"),
        )
        .limit(10000)
    )
    sample.toPandas().to_csv(
        "output/" + MODEL_NAME + "_predictions.csv", index=False
    )

    with open("output/evaluation.csv", "a", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([MODEL_NAME, "areaUnderROC", auc_roc])
        writer.writerow([MODEL_NAME, "areaUnderPR", auc_pr])

    with open("output/model_comparison.csv", "a", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([
            MODEL_NAME, auc_roc, auc_pr, elapsed, json.dumps(best_params)
        ])

    spark.stop()


if __name__ == "__main__":
    main()
