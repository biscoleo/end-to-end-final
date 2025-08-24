import streamlit as st
import requests

st.title("Toxic Comment Classifier")

input_text = st.text_area("Enter comment to classify:")

if st.button("Predict"):
    if not input_text.strip():
        st.warning("Please enter some text.")
    else:
        # call FastAPI endpoint
        try:
            response = requests.post(
                "http://localhost:8000/predict", json={"text": input_text}
            )
            response.raise_for_status()
            prediction = response.json().get("prediction")
            label = (
                "Toxic"
                if prediction == "1" or prediction == 1
                else "Not toxic"
            )
            st.success(f"Prediction: {label}")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
