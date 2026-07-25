import json
from pathlib import Path
import streamlit as st
from utils.sidebar import render_sidebar

st.set_page_config(page_title="Model Performance", page_icon="📈", layout="wide")

st.title("📈 Model Performance")
st.caption("Training-time metrics for the deployed churn model, as saved by the training notebook.")

render_sidebar("Model Performance")

FRONTEND_DIR = Path(__file__).parent.parent
WORKSPACE_ROOT = FRONTEND_DIR.parent

@st.cache_data(ttl=300)
def load_performance_data():
    # Attempt to load metadata
    metadata_paths = [
        WORKSPACE_ROOT / "backend" / "models_artifacts" / "churn_model_metadata.json",
        WORKSPACE_ROOT / "models" / "churn_model_metadata.json",
        FRONTEND_DIR / "data" / "churn_model_metadata.json",
    ]
    
    metadata = None
    for path in metadata_paths:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                break
            except Exception as e:
                st.warning(f"Failed to read metadata from {path.name}: {e}")
                
    if not metadata:
        raise FileNotFoundError("Could not locate or parse churn_model_metadata.json in any search path.")
        
    # Attempt to load classification report
    report_paths = [
        FRONTEND_DIR / "images" / "model_performance_report.txt",
        WORKSPACE_ROOT / "backend" / "models_artifacts" / "model_performance_report.txt",
    ]
    
    report = ""
    for path in report_paths:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    report = f.read()
                break
            except Exception:
                pass
                
    return metadata, report

try:
    with st.spinner("Loading model performance data..."):
        info, report_content = load_performance_data()
except Exception as e:
    st.error(f"Error loading model performance data: {e}")
    st.info("Ensure the model metadata and report files are present in the workspace.")
    st.stop()

perf = info.get("test_performance", {})

st.subheader("Key Performance Indicators (Test Set)")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="🎯 Accuracy",
        value=f"{perf.get('accuracy', 0.0):.2%}",
        help="Proportion of correct predictions (both churn and non-churn) out of all test cases."
    )

with col2:
    st.metric(
        label="⚖ Precision",
        value=f"{perf.get('precision', 0.0):.2%}",
        help="Proportion of predicted churners who actually churned (minimizes false positives)."
    )

with col3:
    st.metric(
        label="🔍 Recall",
        value=f"{perf.get('recall', 0.0):.2%}",
        help="Proportion of actual churners who were correctly identified (minimizes false negatives)."
    )

with col4:
    st.metric(
        label="📈 F1 Score (Macro)",
        value=f"{perf.get('macro_f1', 0.0):.2%}",
        help="Harmonic mean of precision and recall, macro-averaged across classes."
    )

with col5:
    st.metric(
        label="📊 ROC-AUC",
        value=f"{perf.get('roc_auc', 0.0):.2%}",
        help="Area under the ROC Curve. Measures the model's ability to distinguish between classes."
    )

st.write("")

with st.expander("🔍 Model Metadata & Details"):
    st.markdown(f"**Model Architecture:** `{info.get('model_type', 'N/A')}`")
    st.markdown(f"**Chosen Probability Threshold:** `{info.get('chosen_threshold', 0.0):.4f}`")
    st.markdown(f"**Target Recall Configured:** `{info.get('target_recall_used_for_threshold', 0.0):.1%}`")
    st.markdown(f"**Target Column:** `{info.get('target_column', 'N/A')}`")
    st.markdown(f"**Saved On:** `{info.get('saved_on', 'N/A')}`")

st.divider()

tab1, tab2, tab3 = st.tabs([
    "🎯 Confusion Matrix & Classification Report", 
    "📈 Feature Importance", 
    "💡 SHAP Explainability"
])

with tab1:
    col_img, col_txt = st.columns([1.2, 1.0], gap="large")
    with col_img:
        st.subheader("Confusion Matrix")
        matrix_img_path = FRONTEND_DIR / "images" / "confusion_matrix.png"
        if matrix_img_path.exists():
            st.image(str(matrix_img_path), caption="Confusion Matrix on Test Dataset", use_container_width=True)
        else:
            st.warning("Confusion matrix image not found.")
            
    with col_txt:
        st.subheader("Classification Report")
        if report_content:
            st.code(report_content, language="text")
        else:
            st.info("No text performance report file found.")

with tab2:
    st.subheader("Feature Importance")
    st.write(
        "Feature importance values show which user attributes contributed most to the model's decisions during training."
    )
    feat_img_path = FRONTEND_DIR / "images" / "feature_importance.png"
    if feat_img_path.exists():
        st.image(str(feat_img_path), caption="Top Features contributing to Churn Prediction", use_container_width=True)
    else:
        st.warning("Feature importance image not found.")

with tab3:
    st.subheader("SHAP Interpretability")
    st.write(
        "SHAP (SHapley Additive exPlanations) values decompose a prediction into the impact of each feature."
    )
    
    col_shap1, col_shap2 = st.columns(2, gap="medium")
    with col_shap1:
        st.markdown("#### Summary Plot")
        summary_img_path = FRONTEND_DIR / "images" / "shap_summary_plot.png"
        if summary_img_path.exists():
            st.image(str(summary_img_path), caption="SHAP Summary Plot (Global Impact)", use_container_width=True)
        else:
            st.warning("SHAP summary plot image not found.")
            
    with col_shap2:
        st.markdown("#### Waterfall Plot")
        waterfall_img_path = FRONTEND_DIR / "images" / "shap_waterfall_plot.png"
        if waterfall_img_path.exists():
            st.image(str(waterfall_img_path), caption="SHAP Waterfall Plot for a Representative Sample", use_container_width=True)
        else:
            st.warning("SHAP waterfall plot image not found.")