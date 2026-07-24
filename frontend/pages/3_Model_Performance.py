from datetime import datetime
import pandas as pd
import requests
import streamlit as st
from utils.sidebar import render_sidebar

st.set_page_config(page_title="Model Performance", page_icon="📈", layout="centered")

API_BASE_URL = "http://localhost:8000/api/v1"
PERFORMANCE_URL = f"{API_BASE_URL}/model-performance"
 
st.title("📈 Model Performance")
st.caption("Training-time metrics for the deployed churn model, as saved by the training notebook.")

render_sidebar("Model Performance")

@st.cache_data(ttl=300)
def fetch_model_performance():
    resp = requests.get(PERFORMANCE_URL, timeout=15)
    resp.raise_for_status()
    return resp.json()

try:
    with st.spinner("Loading model metadata..."):
        info = fetch_model_performance()
except requests.exceptions.ConnectionError:
    st.error(f"Couldn't reach the API at {PERFORMANCE_URL}. Is the FastAPI backend running?")
    st.stop()
except requests.exceptions.HTTPError as e:
    st.error(f"API returned an error: {e.response.status_code} — {e.response.text}")
    st.stop()
 
perf = info["test_performance"]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("Model Type")
    st.write(info.get("model_type").split(" ")[0])

with col2:
    st.markdown("Accuracy")
    st.write(f"{info.get("test_performance")["accuracy"]:.2f}")

with col3:
    st.markdown("F1 score")
    st.write(f"{info.get("test_performance")["macro_f1"]:.2f}")

with col4:
    st.markdown("ROC Score")
    st.write(f"{info.get("test_performance")["roc_auc"]:.2f}")
