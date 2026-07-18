import streamlit as st
from streamlit_option_menu import option_menu


PAGES = {
    "Dashboard": "app.py",
    "Single Prediction": "pages/1_Single_Prediction.py",
    "Batch Prediction": "pages/2_Batch_Prediction.py",
    "Customer Analytics": "pages/3_Customer_Analytics.py",
    "Explainable AI": "pages/4_Explainable_AI.py",
    "Model Performance": "pages/5_Model_Performance.py",
    "Prediction History": "pages/6_Prediction_History.py",
}


def render_sidebar(active: str = "Dashboard"):
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-logo-title"><h2>Customer Churn<br>Intelligence Platform</h2></div>',
            unsafe_allow_html=True,
        )
        option_menu(
            menu_title=None,
            options=list(PAGES.keys()),
            icons=["house", "person-check", "layers", "graph-up",
                   "lightbulb", "bar-chart", "clock-history"],
            default_index=list(PAGES.keys()).index(active),
            styles={
                "container": {"background-color": "#0f1116"},
                "nav-link-selected": {"background-color": "#2f6fed"},
            },
        )
        
