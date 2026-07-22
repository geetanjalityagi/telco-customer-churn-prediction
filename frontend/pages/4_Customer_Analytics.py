import streamlit as st
from utils.sidebar import render_sidebar

st.set_page_config(page_title="Customer Analytics",page_icon="🔍", layout="wide")
render_sidebar("Customer Analytics")