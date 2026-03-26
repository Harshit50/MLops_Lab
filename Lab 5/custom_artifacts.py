import mlflow
import mlflow.pyfunc
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from mlflow.models.signature import infer_signature
import numpy as np
import json

mlflow.set_tracking_uri("sqlite:///mlflow.db")

class ClinicalModelWrapper(mlflow.pyfunc.PythonModel):
    def __init__(self, model, scaler):
        self.model = model
        self.scaler = scaler
        
    def predict(self, context, model_input):
        scaled_input = self.scaler.transform(model_input)
        return self.model.predict(scaled_input)

if __name__ == "__main__":
    mlflow.set_experiment("Custom_Artifacts_Experiment")
    
    diabetes = load_diabetes()
    X_train, X_test, y_train, y_test = train_test_split(diabetes.data, diabetes.target, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Define hyperparameters explicitly so we can log them
    svm_kernel = 'rbf'
    svm_c = 1.0
    svm_epsilon = 0.2
    
    model = SVR(kernel=svm_kernel, C=svm_c, epsilon=svm_epsilon)
    model.fit(X_train_scaled, y_train)
    
    # Calculate metrics for logging
    y_pred = model.predict(scaler.transform(X_test))
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    
    model_config = {"kernel": svm_kernel, "C": svm_c, "epsilon": svm_epsilon, "dataset": "Diabetes Clinical Data"}
    with open("model_config.json", "w") as f:
        json.dump(model_config, f)
        
    artifacts = {"config_file": "model_config.json"}
    pip_reqs = ["scikit-learn", "cloudpickle", "pandas"]
    
    signature = infer_signature(X_test, y_pred)
    
    with mlflow.start_run(run_name="SVR_Custom_PyFunc"):
        mlflow.log_param("kernel", svm_kernel)
        mlflow.log_param("C", svm_c)
        mlflow.log_param("epsilon", svm_epsilon)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        
        wrapped_model = ClinicalModelWrapper(model, scaler)
        
        mlflow.pyfunc.log_model(
            artifact_path="clinical_svr_model",
            python_model=wrapped_model,
            artifacts=artifacts,
            pip_requirements=pip_reqs,
            signature=signature 
        )
        print(f"Custom PyFunc model logged! RMSE: {rmse:.2f}")