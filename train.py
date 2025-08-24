import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import mlflow
import mlflow.sklearn
import os


def main():
    # track ml runs
    mlflow.set_tracking_uri("file://" + os.path.abspath("mlruns"))
    # load labeled training data
    df = pd.read_parquet("data/training_data.parquet")

    X = df["comment_text"]
    y = df["toxic"]

    # split into train/val sets
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # define the pipeline
    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer()),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )
    # start MLflow run
    with mlflow.start_run():
        # train the model pipeline
        pipeline.fit(X_train, y_train)
        # predict on validation set
        y_pred = pipeline.predict(X_val)
        # calculate metrics
        acc = accuracy_score(y_val, y_pred)
        f1 = f1_score(y_val, y_pred)
        # log params and metrics
        mlflow.log_param("model_type", "LogisticRegression")
        # max_features might be None, log as string to avoid issues
        max_features = pipeline.named_steps["tfidf"].max_features
        mlflow.log_param("tfidf_max_features", str(max_features))
        mlflow.log_metric("val_accuracy", acc)
        mlflow.log_metric("val_f1_score", f1)
        # log and register model to MLflow Model Registry
        mlflow.sklearn.log_model(
            sk_model=pipeline,
            name="model",
            registered_model_name="ToxicCommentModel",
        )
        print(f"Validation accuracy: {acc:.4f}")
        print(f"Validation F1 score: {f1:.4f}")


if __name__ == "__main__":
    main()
