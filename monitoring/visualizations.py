import matplotlib.pyplot as plt
import numpy as np


def plot_target_drift(df):
    """
    Plot distribution of predicted classes vs true classes over time.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    # Count predictions and true labels
    pred_counts = df["predicted"].value_counts(normalize=True).sort_index()
    true_counts = df["true_label"].value_counts(normalize=True).sort_index()

    # Bar width and positions
    width = 0.35
    x = np.arange(len(pred_counts.index))

    ax.bar(x - width / 2, pred_counts.values, width, label="Predicted")
    ax.bar(x + width / 2, true_counts.values, width, label="True")

    ax.set_xticks(x)
    ax.set_xticklabels(pred_counts.index)
    ax.set_ylabel("Proportion")
    ax.set_title("Prediction vs True Label Distribution")
    ax.legend()
    plt.tight_layout()
    return fig


def plot_prediction_latency(df):
    """
    Plot prediction latency over time.
    """
    fig, ax = plt.subplots(figsize=(10, 4))
    df = df.sort_values("timestamp")

    ax.plot(
        df["timestamp"],
        df["prediction_latency_ms"],
        marker="o",
        linestyle="-",
        markersize=3,
    )
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Latency (ms)")
    ax.set_title("Prediction Latency Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def calculate_metrics(df):
    """
    Calculate accuracy and precision based on true label.
    """
    if df["true_label"].isnull().all():
        return None, None  # No feedback yet

    df_filtered = df.dropna(subset=["true_label"])
    accuracy = (df_filtered["predicted"] == df_filtered["true_label"]).mean()

    # precision
    true_positives = (
        (df_filtered["predicted"] == 1) & (df_filtered["true_label"] == 1)
    ).sum()
    predicted_positives = (df_filtered["predicted"] == 1).sum()

    precision = (
        true_positives / predicted_positives
        if predicted_positives > 0
        else None
    )

    return accuracy, precision
