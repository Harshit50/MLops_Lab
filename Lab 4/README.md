# MLOps Lab 4: Docker Lab

## Overview
This lab demonstrates the fundamental MLOps practice of **containerizing a Machine Learning workload** using Docker. 

While it is easy to train a model on a local machine, "Dependency Hell" (conflicting library versions) often makes it difficult to run that same code on another machine or in production. By wrapping the training script and its exact dependencies into a Docker container, we ensure **reproducibility, portability, and isolation**.

This specific project trains a Decision Tree classifier on the classic Iris Flower dataset and saves the resulting model as a serialized `.pkl` file.

## Project Structure
```text
Lab 4/
├── Dockerfile               # Blueprint for the Docker image
├── ReadMe.md                # Project documentation
├── output.txt               # Captured output from the container run
└── src/
    ├── main.py              # The ML training script
    └── requirements.txt     # Locked Python dependencies
```

## Prerequisites
* **Docker Desktop** installed and actively running.
* **Git** (for version control and repository management).

## Tech Stack & Dependencies
* **Base Image:** `python:3.10-slim` (A lightweight Linux environment).
* **Machine Learning:** `scikit-learn==1.3.0`
* **Data Processing:** `numpy==1.26.4`
* **Serialization:** `joblib==1.3.2`

## How to Run the Project

### Step 1: Build the Docker Image
Navigate to the root directory of this lab (where the `Dockerfile` is located) and run the following command to build the image:
```bash
docker build -t iris-lab:v1 .
```

### Step 2: Run the Docker Container
Execute the training script inside the isolated container:
```bash
docker run iris-lab:v1
```

### Excpected Output
Upon successful execution, the terminal will display:
```Plaintext
Loading Iris dataset...
Training Decision Tree classifier...
Decision Tree model training successful! Accuracy: 100.00%
Model successfully saved as iris_dt_model.pkl inside the container.
```

## MLOps Concepts Demonstrated
1. Ephemeral Containers: Unlike a web server (which runs continuously), this container is designed to execute a single task (training the model) and then gracefully shut down. In Docker Desktop, this container will show a status of Exited (0), indicating a successful, completed run without crashes.

2. Dependency Management: By explicitly defining requirements.txt inside the Dockerfile, we guarantee the model trains on the exact same library versions every single time, regardless of the host machine's local Python environment.

