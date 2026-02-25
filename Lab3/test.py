import requests
import json

# 1. Define the URL for your local predict endpoint
url = "http://127.0.0.1:8000/predict"

# 2. Create the payload
financial_data = {
    "debt_to_equity": 3.5,
    "operating_margin": -0.1,
    "cash_flow_to_debt": 0.15,
    "working_capital_ratio": 1.2
}

print(f"Sending data to {url}...\n")

try:
    # 3. Attempt to send the POST request to the API
    response = requests.post(url, json=financial_data)

    # 4. Check the status code and print the results
    if response.status_code == 200:
        print("✅ Success! The model returned the following prediction:")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"❌ Request failed with status code {response.status_code}")
        print(response.text)

# Catch the specific error when the FastAPI server is offline
except requests.exceptions.ConnectionError:
    print("🚨 Connection Error: Could not connect to the API.")
    print("👉 Fix: Please make sure your FastAPI server is running in a separate terminal window using 'uvicorn app:app --reload'.")

# Catch any other unexpected errors just in case
except Exception as e:
    print(f"🚨 An unexpected error occurred: {e}")