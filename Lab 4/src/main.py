import os
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib

def main():
    # 1. Load the Iris dataset
    print("Loading Iris dataset...")
    X, y = load_iris(return_X_y=True)

    # 2. Split data into training (80%) and testing (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Initialize and train the Decision Tree model
    print("Training Decision Tree classifier...")
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    # 4. Evaluate the model
    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    print(f"Decision Tree model training successful! Accuracy: {acc * 100:.2f}%")

    # 5. Save the trained model
    model_filename = 'iris_dt_model.pkl'
    joblib.dump(model, model_filename)
    print(f"Model successfully saved as {model_filename} inside the container.")

if __name__ == "__main__":
    main()