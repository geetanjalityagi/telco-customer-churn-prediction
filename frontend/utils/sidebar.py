import streamlit as st
from streamlit_option_menu import option_menu


PAGES = {
    "Dashboard": "app.py",
    "Single Prediction": "pages/1_Single_Prediction.py",
    "Batch Prediction": "pages/2_Batch_Prediction.py",
    "Customer Analytics": "pages/4_Customer_Analytics.py",
    "Model Performance": "pages/5_Model_Performance.py"
}

def render_sidebar(active: str = "Dashboard"):
    with st.sidebar:
        # Hide default Streamlit sidebar navigation
        st.markdown(
            """
            <style>
                [data-testid="stSidebarNav"] {display: none;}
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-logo-title"><h1>Customer Churn<br>Intelligence Platform</h1></div>',
            unsafe_allow_html=True,
        )
        # st.markdown("""**Customer Churn**\nIntelligence Platform""")
        selected_option = option_menu(
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
        
        if selected_option and selected_option != active:
            st.switch_page(PAGES[selected_option])