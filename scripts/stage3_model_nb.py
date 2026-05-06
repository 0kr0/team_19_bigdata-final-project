"""Stage 3 model 3: Naive Bayes classifier.

Naive Bayes in Spark MLlib requires non-negative features, so the pipeline
uses MinMaxScaler instead of StandardScaler. The grid varies modelType
(algorithm), smoothing (model) and ChiSqSelector.numTopFeatures (model);
27 combinations total.
"""
import csv
import json
import time

from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import udf
from pyspark.ml import Pipeline
from pyspark.ml.feature import (
    StringIndexer, OneHotEncoder, VectorAssembler, MinMaxScaler, ChiSqSelector
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
        inputCol="features_raw", outputCol="features_scaled"
    )
    selector = ChiSqSelector(
        featuresCol="features_scaled", outputCol="features",
        labelCol="label",
    )
    nb = NaiveBayes(featuresCol="features", labelCol="label")
    pipeline = Pipeline(stages=[
        rideable_idx, rideable_ohe, station_idx, assembler, scaler,
        selector, nb,
    ])

    grid = (
        ParamGridBuilder()
        .addGrid(nb.modelType, ["multinomial", "gaussian", "bernoulli"])
        .addGrid(nb.smoothing, [0.5, 1.0, 2.0])
        .addGrid(selector.numTopFeatures, [5, 10, 20])
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
    best_selector = best_pipeline.stages[-2]
    best_params = {
        "modelType": best_nb.getOrDefault(best_nb.getParam("modelType")),
        "smoothing": best_nb.getOrDefault(best_nb.getParam("smoothing")),
        "numTopFeatures": best_selector.getOrDefault(
            best_selector.getParam("numTopFeatures")
        ),
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
