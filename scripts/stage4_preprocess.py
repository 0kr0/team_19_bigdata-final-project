"""Stage 4 preprocessing.

Reads Stage 3 output CSVs from output/ and writes Hive-ready versions
to output/stage4/:

  evaluation.csv, model_comparison.csv, train_sample.csv,
  test_sample.csv, sample_prediction.csv  are copied as-is.

  predictions.csv is the union of all three model prediction files
  with a model_name column prepended.  For RF and NB, the 'probability'
  column is the true probability of class 1 (member).  For SVM it is the
  positive-class raw decision margin; the column is kept under the same
  name for schema uniformity across models.
"""
import os
import shutil

import pandas as pd


INPUT_DIR = "output"
OUTPUT_DIR = os.path.join("output", "stage4")

MODEL_PREDICTIONS = [
    ("model1_rf",  "model1_rf_predictions.csv"),
    ("model2_svm", "model2_svm_predictions.csv"),
    ("model3_nb",  "model3_nb_predictions.csv"),
]

COPY_FILES = [
    "evaluation.csv",
    "model_comparison.csv",
    "train_sample.csv",
    "test_sample.csv",
    "sample_prediction.csv",
]


def build_predictions():
    """Combine all three model prediction CSVs into one file."""
    frames = []
    for model_name, filename in MODEL_PREDICTIONS:
        path = os.path.join(INPUT_DIR, filename)
        df = pd.read_csv(path)
        df.insert(0, "model_name", model_name)
        frames.append(df)
    combined = pd.concat(frames, ignore_index=True)
    out = os.path.join(OUTPUT_DIR, "predictions.csv")
    combined.to_csv(out, index=False)
    print("Wrote " + out + " (" + str(len(combined)) + " rows)")


def copy_files():
    """Copy CSVs that need no transformation to output/stage4/."""
    for filename in COPY_FILES:
        src = os.path.join(INPUT_DIR, filename)
        dst = os.path.join(OUTPUT_DIR, filename)
        shutil.copy2(src, dst)
        print("Copied " + dst)


def main():
    if not os.path.isdir(INPUT_DIR):
        raise SystemExit("Missing output/ directory; run stage3.sh first.")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    build_predictions()
    copy_files()


if __name__ == "__main__":
    main()