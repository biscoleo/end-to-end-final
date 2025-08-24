import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from visualizations import load_prediction_logs, plot_target_drift, plot_prediction_latency, calculate_metrics


# db connection using cache_resource (instead of opening a new connection each time. this way is much more efficient)
@st.cache_resource
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432"),
        sslmode='require'
    )

# load latest prediction logs -- up to 5000
@st.cache_data(ttl=600)
def load_prediction_logs(_conn):
    query = """
        SELECT input_text, predicted, true_label, timestamp, prediction_latency_ms
        FROM predictions
        ORDER BY timestamp DESC
        LIMIT 5000;
    """
    return pd.read_sql(query, _conn)

# STREAMLIT UI
st.set_page_config(layout="wide")
st.title("Toxicity Model Monitoring Dashboard")

# connect to DB and load logs
try:
    conn = get_db_connection()
    logs_df = load_prediction_logs(conn)
except Exception as e:
    st.error(f"Failed to load prediction logs: {e}")
    st.stop()

# handle empty logs
if logs_df.empty:
    st.warning("No prediction logs found in the database.")
    st.stop()
else:
    st.success(f"Loaded {len(logs_df)} prediction entries from database.")

# VISUALS
st.subheader("Prediction Latency")
st.pyplot(plot_prediction_latency(logs_df))

st.subheader("Prediction vs. Feedback Distribution")
st.pyplot(plot_target_drift(logs_df))

# metrics
st.subheader("Model Performance")

acc, prec = calculate_metrics(logs_df)

if acc is None:
    st.info("No user feedback available yet to calculate metrics.")
else:
    st.write(f"**Accuracy:** {acc * 100:.2f}%")
    # alert if less than 80% accuracy
    if acc < 0.8:
        st.error("⚠️ ALERT: Accuracy has dropped below 80%!")
