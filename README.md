# 🔮 Customer Churn Intelligence Platform

An end-to-end machine learning and business intelligence platform designed to predict customer churn, explain individual risk factors using SHAP (Shapley Additive exPlanations), and provide actionable retention recommendations. 

The platform leverages historical Telco Customer Churn data to train an optimized and calibrated machine learning model, exposes predictions via a high-performance REST API, and presents insights through an interactive, multi-page business intelligence web application.

---

## 📂 Project Architecture & Directory Structure

```
Customer_Churn_Prediction/
│
├── backend/                             # FastAPI Backend Service
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py                # API Endpoints (health, predict, performance, dashboard)
│   │   ├── core/
│   │   │   ├── config.py                # App configuration, settings, and file paths
│   │   │   └── model_loader.py          # ModelBundle manager (loads XGBoost pipelines & SHAP explainer)
│   │   ├── schemas/                     # Pydantic request/response models
│   │   │   ├── request.py               # CustomerInput & BatchCustomerInput validations
│   │   │   ├── response.py              # ChurnPredictionResponse & RiskFactor models
│   │   │   ├── dashboard_schema.py      # Dashboard response formats
│   │   │   └── model_performance_schema.py
│   │   └── services/                    # Business logic & computation engines
│   │       ├── dashboard.py             # Analytical KPI & cohort chart generators
│   │       └── prediction_service.py    # Predictor, SHAP explainer, and recommended actions mapper
│   ├── data/
│   │   └── processed.csv                # Processed customer dataset for the dashboard
│   ├── models_artifacts/                # Serialized model pipelines & metadata copies
│   └── requirements.txt                 # Backend-specific package dependencies
│
├── frontend/                            # Streamlit Web Application
│   ├── app.py                           # Main Dashboard overview & macro trend charts
│   ├── components/                      # Reusable UI component modules
│   │   ├── charts.py                    # Plotly chart visualizations for main page
│   │   ├── filter_data.py               # Cohort filter sidebar widgets & state manager
│   │   └── insights.py                  # Cohort overview charts (Customer Explorer)
│   ├── images/                          # Evaluation plots (confusion matrix, SHAP, feature importance)
│   ├── pages/                           # Streamlit multi-page routes
│   │   ├── 1_Single_Prediction.py       # Ad-hoc customer churn prediction reporting form
│   │   ├── 2_Customer_Explorer.py       # Cohort explorer, lookup tool, and segment downloader
│   │   └── 3_Model_Performance.py       # Training evaluations, matrices, and SHAP diagnostics
│   ├── utils/
│   │   └── sidebar.py                   # Custom sidebar navigation configuration
│   └── requirements.txt                 # Frontend-specific package dependencies
│
├── models/                              # ML model artifacts (XGBoost pipeline, calibrated estimator, metadata)
│   ├── churn_model_metadata.json        # Training performance & hyperparameters
│   ├── churn_model_xgb_calibrated.pkl   # Calibrated Classifier (Isotonic Regression)
│   └── xgb_pipeline.pkl                 # Preprocessor & XGBoost estimator pipeline
│
├── notebooks/                           # Jupyter Notebooks (EDA, tuning, modeling, SHAP)
│   ├── 01_Customer_Churn_EDA.ipynb      # Initial exploratory analysis
│   ├── 02_Customer_Churn_Model_Training.ipynb # Model comparisons, Optuna tuning, and calibration
│   └── 03_Customer_Churn_Prediction.ipynb # Simple verification and predictions example
│
├── requirements.txt                     # Combined package dependencies
└── .gitignore
```

### Key Component Links:
- **FastAPI Entry Point**: [main.py](file:///c:/Projects/Customer_Churn_Prediction/backend/app/main.py)
- **API Router**: [routes.py](file:///c:/Projects/Customer_Churn_Prediction/backend/app/api/routes.py)
- **Prediction Engine**: [prediction_service.py](file:///c:/Projects/Customer_Churn_Prediction/backend/app/services/prediction_service.py)
- **Dashboard Data Engine**: [dashboard.py](file:///c:/Projects/Customer_Churn_Prediction/backend/app/services/dashboard.py)
- **Streamlit App Entry**: [app.py](file:///c:/Projects/Customer_Churn_Prediction/frontend/app.py)
- **Single Prediction Page**: [1_Single_Prediction.py](file:///c:/Projects/Customer_Churn_Prediction/frontend/pages/1_Single_Prediction.py)
- **Customer Explorer Page**: [2_Customer_Explorer.py](file:///c:/Projects/Customer_Churn_Prediction/frontend/pages/2_Customer_Explorer.py)
- **Model Performance Page**: [3_Model_Performance.py](file:///c:/Projects/Customer_Churn_Prediction/frontend/pages/3_Model_Performance.py)
- **Model Training Notebook**: [02_Customer_Churn_Model_Training.ipynb](file:///c:/Projects/Customer_Churn_Prediction/notebooks/02_Customer_Churn_Model_Training.ipynb)

---

## ⚙️ Setup & Installation

Follow these steps to run the complete environment locally.

### 1. Prerequisite Environments
Make sure you have Python 3.10+ installed.

### 2. Clone & Create Virtual Environment
Open your terminal in the project root directory:
```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install root dependencies
pip install -r requirements.txt
```
*(Note: [requirements.txt](file:///c:/Projects/Customer_Churn_Prediction/requirements.txt) includes all libraries required for the notebooks, backend API, and Streamlit frontend.)*

### 3. Run the Backend API
Start the FastAPI server via Uvicorn. The backend reads serialized artifacts from `backend/models_artifacts` and raw data from `backend/data/processed.csv`.
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```
The API documentation will be available locally at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 4. Run the Streamlit Frontend App
In a separate terminal window (with the virtual environment activated):
```bash
cd frontend
streamlit run app.py
```
The application will launch automatically in your default browser at [http://localhost:8501](http://localhost:8501).

> [!TIP]
> By default, the frontend app connects to the backend at `http://localhost:8000/api/v1`. If you deploy the backend API to a remote cloud server, set the `CHURN_API_URL` environment variable to point to the live API URL before launching the app:
> - **Windows (PowerShell):** `$env:CHURN_API_URL="https://your-backend-api.com/api/v1"`
> - **macOS/Linux:** `export CHURN_API_URL="https://your-backend-api.com/api/v1"`

---

## 🧠 Machine Learning & Data Pipeline

The machine learning implementation resides in the `notebooks/` directory.

### 📊 1. Exploratory Data Analysis ([01_Customer_Churn_EDA.ipynb](file:///c:/Projects/Customer_Churn_Prediction/notebooks/01_Customer_Churn_EDA.ipynb))
Performs data quality checks, handles missing values (e.g., in `TotalCharges`), and explores correlations:
- Identifies strong churn drivers (e.g., month-to-month contracts, electronic check billing, fiber optic internet service, and low tenure).
- Documents data characteristics to design effective preprocessing components.

### 🏗️ 2. Pipeline & Model Training ([02_Customer_Churn_Model_Training.ipynb](file:///c:/Projects/Customer_Churn_Prediction/notebooks/02_Customer_Churn_Model_Training.ipynb))
- **Data Preprocessing**: Implements a `ColumnTransformer` from `scikit-learn`:
  - **Ordinal Features** (`Contract`): Encoded sequentially (`Month-to-month`, `One year`, `Two year`).
  - **Categorical Features** (`InternetService`, `PaymentMethod`): Encoded using `OneHotEncoder`.
  - **Numeric Features** (`tenure`, `MonthlyCharges`, `TotalCharges`): Scaled via `StandardScaler`.
  - **Remaining Binary Features**: Passed through directly.
- **Model Comparison**: Compares Logistic Regression, Random Forests, Gradient Boosting, and XGBoost.
- **Hyperparameter Optimization**: Uses `Optuna` to tune XGBoost parameters (learning rate, depth, sub-sample ratios, min child weight, etc.).
- **Probability Calibration**: Since raw XGBoost outputs are not well-calibrated probabilities (essential for risk-based decisions), the model is wrapped in `CalibratedClassifierCV` using **Isotonic Regression** (with 5-fold cross-validation).
- **Threshold Tuning**: Rather than using a generic `0.50` decision threshold, the threshold is optimized (set to `~0.295`) to guarantee a **Recall of at least 75%** on the minority churn class.
- **Explainability**: Builds a SHAP `TreeExplainer` on the XGBoost pipeline to capture both global feature contributions and local, sample-specific force/waterfall values.
- **Serialization**: Saves the pipeline object (`xgb_pipeline.pkl`), calibrated model (`churn_model_xgb_calibrated.pkl`), and training run metadata (`churn_model_metadata.json`) into the [models/](file:///c:/Projects/Customer_Churn_Prediction/models/) and [backend/models_artifacts/](file:///c:/Projects/Customer_Churn_Prediction/backend/models_artifacts/) directories.

---

## ⚡ Backend REST API Service

The backend utilizes `FastAPI` to serve the serialized machine learning components in real-time.

### Model Loading & Execution ([model_loader.py](file:///c:/Projects/Customer_Churn_Prediction/backend/app/core/model_loader.py))
The `ModelBundle` class acts as a single-entry repository:
- Loads the calibrated estimator `churn_model_xgb_calibrated.pkl` and preprocessor pipelines.
- Runs predictions for incoming requests.
- Initializes a `shap.TreeExplainer` on the fitted XGBoost estimator to decompose predictions on the fly.

### Endpoints ([routes.py](file:///c:/Projects/Customer_Churn_Prediction/backend/app/api/routes.py))
1. **`GET /api/v1/health`**: Returns model status, active calibration threshold, and test metrics.
2. **`GET /api/v1/model-performance`**: Serves training metadata to the Streamlit app.
3. **`GET /api/v1/dashboard`**: Pre-calculates macro KPI metrics and chart distributions (e.g., correlation matrices, tenure distributions) based on [processed.csv](file:///c:/Projects/Customer_Churn_Prediction/backend/data/processed.csv).
4. **`POST /api/v1/predict`**: Accepts a customer profile, preprocesses it, scores it, and returns:
   - **Churn status** (`Will Churn` vs `Will Stay`) and **probability**.
   - **Risk Level Category** (`Very Low` to `Critical`) with visual priority ratings.
   - **Top 3 Risk Factors** and **Top 3 Protective Factors** dynamically generated via local SHAP values, mapped to friendly labels (e.g., `ordinal__Contract` ➔ `Month-to-Month Contract`).
   - **Tailored Business Recommendation**: e.g., if month-to-month billing is a high risk factor, it automatically recommends offering a contract upgrade discount.

---

## 🖥️ Frontend Web Application

The frontend is a multi-page `Streamlit` dashboard styled with a clean design, intuitive layouts, and custom interactive widgets.

### 🏡 1. Dashboard Overview ([app.py](file:///c:/Projects/Customer_Churn_Prediction/frontend/app.py))
Displays high-level KPIs and Plotly charts summarizing the historical customer base:
- **KPI Metrics**: Total active customers, baseline churn rate, average monthly charges, average customer tenure, high-risk flagged accounts, and monthly revenue currently at risk.
- **Distribution Charts**: Churn rates relative to Contract Type, Internet Service (Fiber optic vs DSL), and Payment Methods.
- **Feature Correlation Heatmap**: Correlation between numerical features and churn.
- **Contract vs Payment Heatmap**: Cross-tabulation of risk rates to pinpoint dangerous combinations (e.g., Month-to-Month contracts combined with Electronic Check payment methods).

### 🧠 2. Single Prediction ([1_Single_Prediction.py](file:///c:/Projects/Customer_Churn_Prediction/frontend/pages/1_Single_Prediction.py))
An interactive form to score single, hypothetical, or active customer profiles:
- Users input demographic variables, billing charges, and selected add-ons.
- Submits data to the backend's `/predict` API route.
- Renders a visually styled **Customer Churn Prediction Report**:
  - Risk progress bars, risk category indicators, and color-coded status blocks.
  - Interactive lists showing the customer's top risk and protective factors (SHAP contributions).
  - Business translations and direct action guides.

### 🔍 3. Customer Explorer ([2_Customer_Explorer.py](file:///c:/Projects/Customer_Churn_Prediction/frontend/pages/2_Customer_Explorer.py))
Enables segment-based filtering and deep customer lookups:
- **Cohort Filtering**: Sidebar selectors (gender, contract type, payments, tenure range) dynamically filter the base dataset.
- **Cohort Overview**: Shows size, group churn rate, average monthly billing, and average tenure for the active cohort.
- **Cohort Data Table**: Renders the complete tabular view of the filtered customers with direct **CSV download** capabilities.
- **Individual Lookup**: Allows searching for specific customers (by ID) to visualize their demographic characteristics, subscribed services (active/inactive icons), and billing profiles. Automatically flags individual vulnerabilities (e.g., warning if they lack Online Security or Tech Support).

### 📈 4. Model Performance ([3_Model_Performance.py](file:///c:/Projects/Customer_Churn_Prediction/frontend/pages/3_Model_Performance.py))
Provides full transparency into how the underlying model performs:
- **Test Metrics**: Accuracy, Precision, Recall, Macro F1, and ROC-AUC.
- **Evaluation Artifacts**: Displays the Confusion Matrix plot and the raw classification report text.
- **SHAP Diagnostics**: Includes the global SHAP Summary Plot and a representative Waterfall plot to explain global and local feature attribution.
- **Key Takeaways**: Outlines the model's main findings (e.g., True Negatives: 802, True Positives: 278, Churn class recall: 75%).

---

## 📈 Key Findings & Business Insights

The platform surfaces clear operational insights to help retention teams minimize customer attrition:

* **High Risk Factors (Attrition Drivers):**
  * **Month-to-Month Contracts:** Show an exceptionally high churn rate of **42.6%** compared to only **2.8%** for two-year contracts. Shifting customers to longer-term billing is the highest-impact retention tool.
  * **Electronic Check Payments:** Accounts using electronic checks have a **45.1%** churn rate, while auto-payment options have low churn rates (~15% to 17%). Encouraging automatic billing setup via small incentives is highly effective.
  * **Fiber Optic Service:** Fiber optic users exhibit a **41.8%** churn rate compared to **18.9%** for DSL users. This points to potential service satisfaction, pricing, or network issues that demand technical or promotional review.
  * **Short Tenure:** Attrition is heavily front-loaded (median tenure for churned customers is just 10 months). Early-stage onboarding engagement programs are critical.
  
* **Protective Factors (Retention Anchors):**
  * **Add-on Services:** Subscribing to add-ons like **Tech Support** and **Online Security** is heavily associated with lower customer churn. Upselling these services can build customer stickiness.
  * **Long-Term Contracts & Automatic Payments:** Act as the strongest statistical shields against customer churn.
