"""Stage 3 model 1: Random Forest classifier.

Reads the Stage 3 train/test parquet sets from HDFS, builds a Spark
PipelineModel (preprocessing + classifier), runs grid search with 3-fold
cross validation on 27 hyperparameter combinations, evaluates on the test
set, persists the best model and appends per-model metrics to the
stage-level CSVs.
"""
import csv
import json
import time

from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import udf
from pyspark.ml import Pipeline
from pyspark.ml.feature import (
    StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler
)
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder


MODEL_NAME = "model1_rf"
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
    scaler = StandardScaler(
        inputCol="features_raw", outputCol="features",
        withMean=False, withStd=True,
    )
    rf = RandomForestClassifier(
        featuresCol="features", labelCol="label", seed=42,
    )
    pipeline = Pipeline(stages=[
        rideable_idx, rideable_ohe, station_idx, assembler, scaler, rf,
    ])

    grid = (
        ParamGridBuilder()
        .addGrid(rf.numTrees, [20, 50, 100])
        .addGrid(rf.maxDepth, [5, 10, 15])
        .addGrid(rf.minInstancesPerNode, [1, 5, 10])
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
        parallelism=2,
    )

    started = time.time()
    cv_model = cv.fit(train)
    elapsed = time.time() - started

    best_pipeline = cv_model.bestModel
    best_rf = best_pipeline.stages[-1]
    best_params = {
        "numTrees": best_rf.getNumTrees,
        "maxDepth": best_rf.getOrDefault(best_rf.getParam("maxDepth")),
        "minInstancesPerNode": best_rf.getOrDefault(
            best_rf.getParam("minInstancesPerNode")
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
