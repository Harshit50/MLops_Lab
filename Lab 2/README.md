# Airflow Lab: Log Analyzer Pipeline

## 1. Overview
This project demonstrates a fully dockerized **Extract, Transform, Load (ETL)** pipeline using **Apache Airflow**.

Instead of running scripts manually, this project uses Airflow to automate the generation, analysis, and archiving of server logs. The entire infrastructure is defined in code (Infrastructure as Code) using Docker Compose, ensuring a reproducible environment without needing to install Airflow locally.

## 2. Project Structure
The project is organized as follows:

```text
Lab 2/
├── config/                  # Airflow configuration files
├── dags/
│   └── log_analyzer.py      # The Python DAG definition
├── docker-compose.yaml      # Docker infrastructure definition
├── logs/                    # Airflow system logs
├── plugins/                 # Custom Airflow plugins (empty)
├── working_data/            # Mounted volume for input/output files
└── .env                     # Environment variables (AIRFLOW_UID)
```

## 3. Prerequisites
```markdown

```
Before running this project, ensure you have the following installed:
* **Docker Desktop** (Running and active)
* **Git** (Optional, for version control)

## 4. Architecture
This project uses the official **Apache Airflow 2.9.1** Docker image.
* **Executor**: LocalExecutor (Simplified for single-machine labs)
* **Database**: PostgreSQL 13
* **Cache**: Redis (included for compatibility)
* **DAG Logic**: Standard Python Operators

## 5. Installation & Setup

### 1. Setup Environment
Ensure you are in the project directory and your `.env` file is set up with your user ID:
```bash
echo "AIRFLOW_UID=$(id -u)" > .env
```

### 2. Initialize Airflow
Run the initialization command to set up the database and create the default user (`airflow` / `airflow`):
```bash
docker compose up airflow-init
```

### 3. Start the Services
Launch the Airflow Webserver and Scheduler:
```bash
docker compose up
```

## 6. Usage & Running the Pipeline
```markdown
## Usage

### Accessing the UI
1.  Open your browser and navigate to **[http://localhost:8080](http://localhost:8080)**.
2.  **Username**: `airflow`
3.  **Password**: `airflow`

### Running the Pipeline
1.  Find the DAG named **`log_analyzer_pipeline`**.
2.  Toggle the switch to **Unpause** the DAG (turn it Blue).
3.  Click the **Trigger DAG** button (Play icon) under "Actions".

## 7.  Tasks Description
The pipeline consists of three sequential tasks:
1.  **`generate_logs`**: Creates a dummy `server_logs.txt` file with random INFO, WARNING, and ERROR messages.
2.  **`analyze_logs`**: Reads the log file, counts the number of "ERROR" entries, and writes the result to `error_report.txt`.
3.  **`archive_logs`**: Renames the original log file with a timestamp (e.g., `server_logs_20260212.txt`) to simulate data archival.

## 8. Verifying Results
To verify the pipeline ran successfully, check the `working_data/` folder on your local machine. You should see:

* 📄 **`error_report.txt`**: Contains the summary of errors found.
* 📄 **`server_logs_YYYYMMDD_...txt`**: The archived log file.

## Stopping the Project
To stop the containers and save resources:
```bash
docker compose down
```