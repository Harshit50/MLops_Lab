# Financial Distress Prediction API

## Overview
This project demonstrates the core principles of deploying a machine learning model using FastAPI. It features a complete pipeline: generating synthetic financial data, training a Random Forest classifier to predict corporate financial distress, serializing the model, and serving it via a RESTful API with strict input validation using Pydantic.

## Project Structure
* `requirements.txt`: Lists all Python dependencies required to run the project.
* `train_model.py`: Script to generate data, train the Random Forest model, and save it as an artifact (`financial_model.pkl`).
* `app.py`: The FastAPI application that loads the trained model and defines the prediction endpoints.
* `test.py`: A Python script using the `requests` library to programmatically test the API with error handling.

## Setup Instructions

### 1. Install Dependencies
Ensure you have Python installed. It is recommended to use a virtual environment. Install the required packages by running:
```bash
pip install -r requirements.txt
```

## Execution Steps

To run this project, you must follow these steps in order:

### Step 1: Train and Export the Model
Before starting the API, you need to generate the machine learning model artifact. Run the training script:
```bash
python train_model.py
```
*Expected Output:* You should see a message confirming the model was trained, and a new file named `financial_model.pkl` will appear in your directory.

### Step 2: Start the FastAPI Server
Launch the Uvicorn server to host the API locally:
```bash
uvicorn app:app --reload
```
*Note: Leave this terminal window open and running. If you close it or press `Ctrl+C`, the API will go offline.*

### Step 3: Test the API
You can test the API in two different ways:

**Method A: Interactive Swagger UI (Browser)**
1. Open your web browser and navigate to: `http://127.0.0.1:8000/docs`
2. Click on the `POST /predict` endpoint to expand it.
3. Click **"Try it out"**.
4. The request body will pre-fill with sample financial data. Click **"Execute"** to see the model's prediction in the server response.

**Method B: Programmatic Testing (Python Script)**
1. Open a **new, separate terminal window** (keep the Uvicorn server running in the first one).
2. Run the automated test script:
```bash
python test.py
```
*Expected Output:* The script will send a POST request to the local server and print the JSON response, displaying the distress prediction and probability.
