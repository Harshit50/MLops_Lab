import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Generate synthetic financial data
np.random.seed(42)
n_samples = 1000

# Features: key financial ratios
data = {
    'debt_to_equity': np.random.uniform(0.1, 5.0, n_samples),
    'operating_margin': np.random.uniform(-0.5, 0.5, n_samples),
    'cash_flow_to_debt': np.random.uniform(-0.2, 1.5, n_samples),
    'working_capital_ratio': np.random.uniform(0.5, 3.0, n_samples)
}
df = pd.DataFrame(data)

# Target: 1 (Distress) if debt is high and cash flow is low, else 0 (Healthy)
df['distress_target'] = np.where(
    (df['debt_to_equity'] > 3.0) & (df['cash_flow_to_debt'] < 0.2), 1, 0
)

# 2. Train the Model
X = df.drop('distress_target', axis=1)
y = df['distress_target']

model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X, y)

# 3. Save the Model as an artifact
joblib.dump(model, 'financial_model.pkl')
print("Model successfully trained and saved as 'financial_model.pkl'")