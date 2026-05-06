"""Stage 3 model 2: Linear Support Vector Machine.

Spark MLlib only ships LinearSVC; this is the only SVM available in the
distribution. The hyperparameter grid uses regParam (algorithm),
aggregationDepth (model) and tol (model); maxIter is fixed at 100 and
excluded from the count per the rubric ("number of epochs/iterations
excluded from the hyperparameter count").

LinearSVC does not expose a probability column - only rawPrediction (the
margin to the separating hyperplane). The predictions CSV stores the
positive-class margin in the `probability` column for parity with the
other model scripts; downstream consumers should treat it as a margin,
not a probability.
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
from pyspark.ml.classification import LinearSVC
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder


MODEL_NAME = "model2_svm"
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
    svm = LinearSVC(
        featuresCol="features", labelCol="label",
        maxIter=100, standardization=False,
    )
    pipeline = Pipeline(stages=[
        rideable_idx, rideable_ohe, station_idx, assembler, scaler, svm,
    ])

    grid = (
        ParamGridBuilder()
        .addGrid(svm.regParam, [0.001, 0.01, 0.1])
        .addGrid(svm.aggregationDepth, [2, 3, 4])
        .addGrid(svm.tol, [1e-6, 1e-4, 1e-2])
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
    best_svm = best_pipeline.stages[-1]
    best_params = {
        "regParam": best_svm.getOrDefault(best_svm.getParam("regParam")),
        "aggregationDepth": best_svm.getOrDefault(
            best_svm.getParam("aggregationDepth")
        ),
        "tol": best_svm.getOrDefault(best_svm.getParam("tol")),
    }

    predictions = best_pipeline.transform(test)
    auc_roc = eval_roc.evaluate(predictions)
    auc_pr = eval_pr.evaluate(predictions)

    best_pipeline.write().overwrite().save(HDFS_MODEL)

    pos_margin = udf(
        lambda v: float(v[1]) if v is not None else None, DoubleType()
    )
    sample = (
        predictions
        .select(
            "ride_id", "label", "prediction",
            pos_margin("rawPrediction").alias("probability"),
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
