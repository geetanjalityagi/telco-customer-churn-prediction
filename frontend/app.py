import streamlit as st
from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="Customer Churn Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()

st.title("Dashboard Overview")