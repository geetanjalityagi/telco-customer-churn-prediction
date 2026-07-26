# 🔮 Customer Churn Intelligence Platform

🌐 **Streamlit Web Application**: [Live Demo App](https://telco-customer-churn-prediction-2is3t2nccvfknnypgrzprw.streamlit.app/)  
⚡ **FastAPI Backend Service**: [API Swagger Docs](https://churn-prediction-api-s7jc.onrender.com/docs)

An end-to-end predictive analytics and business intelligence platform designed to predict customer churn, explain individual risk factors using SHAP (Shapley Additive exPlanations), and guide retention teams with actionable business suggestions.

The platform consists of a **Machine Learning Pipeline** (tuned and calibrated XGBoost model), a **FastAPI REST API** backend serving predictions and SHAP explanations in real-time, and a **Streamlit Web Interface** for stakeholders to monitor metrics, score customers, and analyze performance.

---

## 📂 Project Architecture & Components

```
Customer_Churn_Prediction/
│
├── backend/                             # FastAPI REST API Backend
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py                # Endpoints (/health, /predict, /dashboard, /model-performance)
│   │   ├── core/
│   │   │   ├── config.py                # Settings, CORS, and paths configuration
│   │   │   └── model_loader.py          # ModelBundle loads XGBoost, preprocessor, and TreeExplainer
│   │   ├── schemas/                     # Pydantic validation models
│   │   │   ├── request.py               # CustomerInput (validation) 
│   │   │   ├── response.py              # ChurnPredictionResponse & RiskFactor schemas
│   │   │   ├── dashboard_schema.py      # Aggregates structures for the frontend
│   │   │   └── model_performance_schema.py
│   │   └── services/                    # Processing logic
│   │       ├── dashboard.py             # Pre-computes stats and chart distributions from data
│   │       └── prediction_service.py    # Prediction logic, local SHAP attribution, and recommendations
│   ├── data/
│   │   └── processed.csv                # Cohort dataset used by dashboard endpoints
│   ├── models_artifacts/                # Copy of model binaries and pipeline metadata
│   └── requirements.txt                 # Backend-specific package dependencies
│
├── frontend/                            # Streamlit Web Application
│   ├── app.py                           # Multi-page landing (Dashboard Overview)
│   ├── components/                      # UI sub-modules
│   │   ├── charts.py                    # Plotly chart distributions
│   │   ├── filter_data.py               # Session-state cohort filter widgets
│   │   └── insights.py                  # Plotly visualizations for filtered customer cohorts
│   ├── images/                          # Plots (confusion matrix, SHAP, feature importance)
│   ├── pages/                           # Web routes
│   │   ├── 1_Single_Prediction.py       # Customer input form & churn scoring report
│   │   ├── 2_Customer_Explorer.py       # Cohort filters, lookup profiles, and CSV export
│   │   └── 3_Model_Performance.py       # Confusion matrices, reports, and SHAP diagrams
│   ├── utils/
│   │   └── sidebar.py                   # Navigation sidebar logic
│   └── requirements.txt                 # Frontend-specific package dependencies
│
├── models/                              # ML binaries (XGBoost pipelines and calibrated estimators)
│   ├── churn_model_metadata.json        # Test performance metrics, thresholds, feature list
│   ├── churn_model_xgb_calibrated.pkl   # Calibrated model (Isotonic Regression)
│   └── xgb_pipeline.pkl                 # Preprocessor & base XGBoost pipeline
│
├── notebooks/                           # Jupyter Notebooks for pipeline development
│   ├── 01_Customer_Churn_EDA.ipynb      # Demographic and billing churn analysis
│   ├── 02_Customer_Churn_Model_Training.ipynb # Model comparisons, Optuna tuning, and calibration
│   └── 03_Customer_Churn_Prediction.ipynb # Prediction test scripts with SHAP values
│
└── requirements.txt                     # Unified project dependencies
```

### 🔗 Key Source File Links:
* **API Entry**: [main.py](file:///c:/Projects/Customer_Churn_Prediction/backend/app/main.py) | **API Router**: [routes.py](file:///c:/Projects/Customer_Churn_Prediction/backend/app/api/routes.py)
* **Prediction Service**: [prediction_service.py](file:///c:/Projects/Customer_Churn_Prediction/backend/app/services/prediction_service.py) | **Dashboard Aggregator**: [dashboard.py](file:///c:/Projects/Customer_Churn_Prediction/backend/app/services/dashboard.py)
* **Streamlit Entry**: [app.py](file:///c:/Projects/Customer_Churn_Prediction/frontend/app.py) | **Prediction Page**: [1_Single_Prediction.py](file:///c:/Projects/Customer_Churn_Prediction/frontend/pages/1_Single_Prediction.py)
* **Customer Explorer**: [2_Customer_Explorer.py](file:///c:/Projects/Customer_Churn_Prediction/frontend/pages/2_Customer_Explorer.py) | **Performance Diagnostics**: [3_Model_Performance.py](file:///c:/Projects/Customer_Churn_Prediction/frontend/pages/3_Model_Performance.py)
* **Model Training Guide**: [02_Customer_Churn_Model_Training.ipynb](file:///c:/Projects/Customer_Churn_Prediction/notebooks/02_Customer_Churn_Model_Training.ipynb)

---

## 🧠 Machine Learning & Data Pipeline

The machine learning core is detailed in [02_Customer_Churn_Model_Training.ipynb](file:///c:/Projects/Customer_Churn_Prediction/notebooks/02_Customer_Churn_Model_Training.ipynb):

1. **Exploratory Data Analysis**: Evaluates demographic distributions (gender, seniority), billing variables (tenure, charges), and services.
2. **Preprocessing Pipeline**: Builds a structured `ColumnTransformer`:
   - *Ordinal Columns* (`Contract`): Encoded mapping Month-to-month ➔ 0, One-Year ➔ 1, Two-Year ➔ 2.
   - *Nominal Columns* (`InternetService`, `PaymentMethod`): Encoded via `OneHotEncoder`.
   - *Numerical Columns* (`tenure`, `MonthlyCharges`, `TotalCharges`): Scaled via `StandardScaler`.
3. **Model Selection & Tuning**: Compares Logistic Regression, Random Forests, Gradient Boosting, and XGBoost. Integrates `Optuna` to tune XGBoost hyperparameters.
4. **Isotonic Calibration**: Employs `CalibratedClassifierCV` (5-fold CV) to calibrate XGBoost output probabilities, ensuring they represent actual churn frequencies.
5. **Threshold Tuning**: Selects an optimal decision threshold (`~0.295`) to guarantee a **Recall of at least 75%** on the minority churn class.
6. **Explainability**: Builds a SHAP `TreeExplainer` on the tuned XGBoost estimator to output feature contributions for any input profile.

---

## ⚡ Backend REST API Service

The backend utilizes `FastAPI` to serve the models and process aggregates.

### API Endpoint Schemas

#### 1. `GET /api/v1/health`
Returns system status, active model characteristics, and baseline test metrics.

#### 2. `GET /api/v1/model-performance`
Serves training metadata, precision/recall specs, features, and active thresholds to the UI.

#### 3. `GET /api/v1/dashboard`
Fetches pre-calculated stats and distributions for the charts, including correlation matrices and contract-payment heatmaps.

#### 4. `POST /api/v1/predict`
Accepts a customer JSON block and returns predictions.
- **Request Body** ([request.py](file:///c:/Projects/Customer_Churn_Prediction/backend/app/schemas/request.py)):
  ```json
  {
    "SeniorCitizen": 0,
    "Partner": "No",
    "Dependents": "No",
    "tenure": 2,
    "PhoneService": "Yes",
    "MultipleLines": "Yes",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "No",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "Yes",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 95.50,
    "TotalCharges": 191.00
  }
  ```
- **Response Body** ([response.py](file:///c:/Projects/Customer_Churn_Prediction/backend/app/schemas/response.py)):
  - Churn prediction status (`Will Churn` or `Will Stay`) and probability score.
  - Risk Category (`Very Low`, `Low`, `Moderate`, `High`, `Critical`) and retention priority stars.
  - Top 3 Risk and Protective factors based on dynamic local SHAP values, mapped to business-friendly names.
  - Actionable business recommendations triggered by specific key risk factors (e.g., upselling contract terms).

---

## 🖥️ Frontend Streamlit Web Interface

The frontend provides an interactive, business-ready interface divided into four views:

### 🏡 1. Dashboard Overview
Displays high-level KPI metrics (Total Customers, Churn Rate, High-Risk Accounts, Avg Tenure, Revenue at Risk) and Plotly charts summarizing billing patterns, tenure distributions, correlation grids, and contract vs payment combinations.

### 🧠 2. Single Prediction Form
Allows CRM and retention agents to input hypothetical or live customer stats to score churn risk. Renders a styled churn risk report with visual progress bars, SHAP risk attributions, and direct action guidelines.

### 🔍 3. Customer Cohort Explorer
Allows filtering historical data on demographic selectors (gender, partner) and billing contracts. Renders the filtered data table with support for **direct CSV downloading**. Features a **profile lookup** that details a single customer's services and highlights custom loyalty insights.

### 📈 4. Model Performance & SHAP Diagnostics
Displays confusion matrices, classification metrics, feature importances, and global SHAP summaries (summary and waterfall plots) to maintain model transparency.

---

## 🚀 Pre-Deployment & Path Resolution Enhancements

The platform has been enhanced with key features to facilitate deployment:

### 1. Robust File Path Resolution (CWD Protection)
When running on cloud hosting (e.g., Streamlit Cloud), the python working directory changes. The app has been refactored to resolve paths dynamically relative to the execution file:
- [2_Customer_Explorer.py](file:///c:/Projects/Customer_Churn_Prediction/frontend/pages/2_Customer_Explorer.py)
- [dashboard.py](file:///c:/Projects/Customer_Churn_Prediction/backend/app/services/dashboard.py)

### 2. Environment Variable Configuration
The Streamlit frontend app retrieves the backend REST API URL from the environment variable `CHURN_API_URL`, with automatic self-healing logic that appends `/api/v1` if omitted.

---

## ⚙️ Running Locally

### 1. Virtual Environment Setup
```bash
# Create and activate environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install all packages
pip install -r requirements.txt
```

### 2. Start the Backend API
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```
API docs will run at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 3. Start the Frontend App
```bash
cd frontend
streamlit run app.py
```
App will launch at [http://localhost:8501](http://localhost:8501).

> [!TIP]
> To connect your local Streamlit instance to a deployed backend API, launch it with:
> - **Windows (PowerShell):** `$env:CHURN_API_URL="https://your-deployed-backend.com/api/v1"; streamlit run app.py`
> - **macOS/Linux:** `CHURN_API_URL="https://your-deployed-backend.com/api/v1" streamlit run app.py`




## 📊 Key Business Takeaways

* **Month-to-Month Contracts**: Yield a **42.6%** churn rate vs **2.8%** on 2-year terms. *Strategy*: Offer target discounts to upgrade month-to-month contracts to annual terms.
* **Electronic Check Payment Method**: Leads to a **45.1%** churn rate vs **~16%** on automated billing. *Strategy*: Offer small bill credits to enroll check payers in automatic credit/debit payments.
* **Fiber Optic Service**: Premium Fiber optic users show a **41.8%** churn rate. *Strategy*: Monitor Fiber pricing tiers and service quality issues.
* **Onboarding Window**: Retained customers average 38 months tenure, while churned accounts have a median tenure of only 10 months. *Strategy*: Focus customer success efforts on the first 12 months.
