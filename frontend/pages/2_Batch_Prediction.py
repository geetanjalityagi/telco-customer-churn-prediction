import streamlit as st
import pandas as pd
from utils.sidebar import render_sidebar

st.set_page_config(page_title="Batch Prediction", page_icon="📂", layout="wide")
render_sidebar("Batch Prediction")

uploaded_file = st.file_uploader(
    label = "Drag and drop CSV or Excel",
    type=["csv", "xlsx"],
    help="Upload a CSV file containing customer information for batch churn prediction."
)