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

st.markdown("### Model Summary")
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"**Model type**  \n{info['model_type']}")
    st.markdown(f"**Target column**  \n`{info['target_column']}`")
with c2:
    saved_on = info.get("saved_on", "")
    try:
        saved_on_fmt = datetime.fromisoformat(saved_on).strftime("%b %d, %Y — %H:%M")
    except ValueError:
        saved_on_fmt = saved_on
    st.markdown(f"**Last trained / saved**  \n{saved_on_fmt}")
    st.markdown(f"**Features used**  \n{len(info['feature_columns'])} columns")
 
st.divider()