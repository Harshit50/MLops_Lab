from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

# 1. Initialize FastAPI app
app = FastAPI(
    title="Financial Distress Prediction API",
    description="An API that predicts the likelihood of corporate financial distress using a Random Forest model.",
    version="1.0.0"
)

# 2. Load the trained machine learning model
try:
    model = joblib.load("financial_model.pkl")
except Exception as e:
    model = None

# 3. Define the input data schema using Pydantic
class FinancialDataInput(BaseModel):
    debt_to_equity: float
    operating_margin: float
    cash_flow_to_debt: float
    working_capital_ratio: float

    # Providing a default example for the Swagger UI
    model_config = {
        "json_schema_extra": {
            "example": {
                "debt_to_equity": 3.5,
                "operating_margin": -0.1,
                "cash_flow_to_debt": 0.15,
                "working_capital_ratio": 1.2
            }
        }
    }

# 4. Create a Root (GET) Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Financial Distress Prediction API. Navigate to /docs for the interactive Swagger UI."}

# 5. Create a Prediction (POST) Endpoint
@app.post("/predict")
def predict_distress(data: FinancialDataInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Please run train_model.py first.")
    
    # Convert validated input data to a DataFrame
    input_df = pd.DataFrame([data.model_dump()])
    
    # Make prediction
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1] # Probability of class 1 (Distress)
    
    # Map prediction to human-readable label
    result_label = "Distress" if prediction == 1 else "Healthy"
    
    return {
        "prediction_class": int(prediction),
        "status": result_label,
        "distress_probability": round(float(probability), 4)
    }