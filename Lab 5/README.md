# Lab 05: MLflow — Diabetes disease progression

## Overview

This lab demonstrates a complete ML lifecycle using **MLflow** on the **Diabetes Clinical Dataset** from Scikit-Learn. The lab covers four distinct MLflow capabilities:

1. **Autologging** — zero-boilerplate experiment tracking with `GradientBoostingRegressor`
2. **Manual Tracking** — explicit logging of parameters, metrics, tags, and artifacts with `ElasticNet`
3. **Model Serving** — deploying a trained model as a local REST API and querying it via HTTP
4. **Custom PyFunc Wrappers** — bundling a `StandardScaler` and `SVR` into a single deployable MLflow model

The dataset (`sklearn.datasets.load_diabetes`) contains 10 clinical features for 442 patients, with the target variable being a quantitative measure of disease progression one year after baseline.

---

## Project Structure

```
Lab 5/
├── requirements.txt            # Python dependencies
├── starter.ipynb               # Part 1: MLflow Autologging (GradientBoostingRegressor)
├── elasticnet_tracking.ipynb   # Part 2: Manual MLflow Tracking (ElasticNet)
├── serving.ipynb               # Part 3: Model Serving via REST API
├── custom_artifacts.py         # Part 4: Custom PyFunc Wrapper (SVR + StandardScaler)
├── model_config.json           # Auto-generated SVR config artifact
├── residuals.png               # Auto-generated residual plot artifact
└── mlflow.db                   # SQLite backend store for MLflow metadata
```

---

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt** includes:
- `mlflow` — experiment tracking, model registry, and serving
- `scikit-learn` — ML models and datasets
- `pandas`, `numpy` — data manipulation
- `matplotlib` — artifact visualization (residual plots)
- `requests` — HTTP client for querying the served model
- `jupyterlab` — notebook environment
- `cloudpickle` — model serialization

### 2. Start JupyterLab

```bash
jupyter lab
```

### 3. Configure the MLflow Tracking URI

All notebooks and scripts point to a local SQLite database as the backend store:

```python
mlflow.set_tracking_uri("sqlite:///mlflow.db")
```

This creates `mlflow.db` in the lab directory on first run.

---

## Part 1 — MLflow Autologging (`starter.ipynb`)

**Goal:** Log a full experiment run with a single line of code using `mlflow.sklearn.autolog()`.

**Model:** `GradientBoostingRegressor` with `n_estimators=100`, `learning_rate=0.1`, `max_depth=3`.

**What gets logged automatically:**
- All hyperparameters
- Training metrics (MSE, R²)
- The fitted model as an artifact

**Key code:**
```python
mlflow.sklearn.autolog()

with mlflow.start_run(run_name="GradientBoosting_Autolog"):
    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    model.fit(X_train, y_train)
```

**Result:** MSE ≈ 2898.44

> **Note:** Autologging artifact upload requires the MLflow tracking server to be running via HTTP. When using a `sqlite://` URI, artifact upload warnings are expected but the run metadata is still saved correctly.

---

## Part 2 — Manual Tracking (`elasticnet_tracking.ipynb`)

**Goal:** Demonstrate granular, explicit control over what gets logged.

**Model:** `ElasticNet` with `alpha=0.5`, `l1_ratio=0.5`.

**Experiment:** `Diabetes_Disease_Progression`

**What is manually logged:**

| MLflow API | What is logged |
|:---|:---|
| `mlflow.log_param()` | `alpha`, `l1_ratio` |
| `mlflow.log_metric()` | `rmse`, `mae`, `r2` |
| `mlflow.set_tag()` | `domain: clinical_healthcare`, `model_type: ElasticNet` |
| `mlflow.log_artifact()` | `residuals.png` — scatter plot of predicted values vs. residuals |
| `mlflow.sklearn.log_model()` | Serialized `ElasticNet` model |

**Key code:**
```python
with mlflow.start_run(run_name="ElasticNet_Manual_Tracking"):
    mlflow.log_param("alpha", alpha)
    mlflow.log_param("l1_ratio", l1_ratio)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("mae", mae)
    mlflow.log_metric("r2", r2)
    mlflow.set_tag("domain", "clinical_healthcare")
    mlflow.log_artifact("residuals.png")
    mlflow.sklearn.log_model(model, "elasticnet_model")
```

To view logged experiments in the MLflow UI:
```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```
Then open `http://localhost:5000` in your browser.

---

## Part 3 — Model Serving (`serving.ipynb`)

**Goal:** Serve a logged MLflow model as a local REST API and query it with new patient data.

### Step 1: Serve the Model

Find a run ID from the MLflow UI or CLI, then serve:

```bash
mlflow models serve \
  --model-uri "runs:/<RUN_ID>/elasticnet_model" \
  --port 5002 \
  --no-conda
```

### Step 2: Send Predictions via HTTP POST

```python
import requests, json
import pandas as pd
from sklearn.datasets import load_diabetes

diabetes = load_diabetes()
sample_data = pd.DataFrame(diabetes.data[:3], columns=diabetes.feature_names)

payload = {"dataframe_split": sample_data.to_dict(orient="split")}
url = "http://127.0.0.1:5002/invocations"
headers = {"Content-Type": "application/json"}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print("Predictions:", response.json())
```

**Sample output:**
```
Status Code: 200
Predictions: {'predictions': [154.47, 151.66, 154.06]}
```

---

## Part 4 — Custom PyFunc Wrapper (`custom_artifacts.py`)

**Goal:** Bundle preprocessing (scaling) and a model into a single, self-contained MLflow artifact that handles raw (unscaled) input at inference time.

**Model:** `SVR` (kernel=`rbf`, C=`1.0`, epsilon=`0.2`) with a `StandardScaler` applied before prediction.

**Experiment:** `Custom_Artifacts_Experiment`

### The Custom Wrapper

```python
class ClinicalModelWrapper(mlflow.pyfunc.PythonModel):
    def __init__(self, model, scaler):
        self.model = model
        self.scaler = scaler

    def predict(self, context, model_input):
        scaled_input = self.scaler.transform(model_input)
        return self.model.predict(scaled_input)
```

### What is logged

| Item | Details |
|:---|:---|
| Parameters | `kernel`, `C`, `epsilon` |
| Metrics | `rmse`, `mae` |
| Custom artifact | `model_config.json` — JSON file with model configuration |
| Model | `ClinicalModelWrapper` (SVR + scaler) logged via `mlflow.pyfunc.log_model()` |
| Signature | Input/output schema inferred from test data |
| Pip requirements | `scikit-learn`, `cloudpickle`, `pandas` |

**Run the script:**
```bash
python custom_artifacts.py
```

**Sample output:**
```
Custom PyFunc model logged! RMSE: 53.16
```

---

## Viewing All Experiments

After running all parts, launch the MLflow UI to compare runs across experiments:

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

Navigate to `http://localhost:5000` to see:
- `Default` — Autologging run from `starter.ipynb`
- `Diabetes_Disease_Progression` — Manual tracking run from `elasticnet_tracking.ipynb`
- `Custom_Artifacts_Experiment` — PyFunc run from `custom_artifacts.py`

---

## Concepts Summary

| Concept | Where Demonstrated |
|:---|:---|
| `mlflow.sklearn.autolog()` | `starter.ipynb` |
| `mlflow.log_param/metric/artifact` | `elasticnet_tracking.ipynb` |
| `mlflow.set_tag()` | `elasticnet_tracking.ipynb` |
| `mlflow.sklearn.log_model()` | `elasticnet_tracking.ipynb` |
| `mlflow models serve` | `serving.ipynb` |
| REST API inference (`/invocations`) | `serving.ipynb` |
| `mlflow.pyfunc.PythonModel` | `custom_artifacts.py` |
| `mlflow.pyfunc.log_model()` | `custom_artifacts.py` |
| Model signatures | `custom_artifacts.py` |
| Custom JSON artifacts | `custom_artifacts.py` |
