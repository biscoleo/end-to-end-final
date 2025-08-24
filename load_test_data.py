import pandas as pd
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000/predict")


def send_test_data(parquet_path):
    df = pd.read_parquet(parquet_path)
    for _, row in df.iterrows():
        data = {"text": row["comment_text"], "true_label": str(row["toxic"])}
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            print(f"Logged: {data['text'][:30]}...")
        else:
            print(f"Failed for: {data['text'][:30]} - {response.text}")


if __name__ == "__main__":
    load_path = "data/training_data.parquet"
    send_test_data(load_path)
