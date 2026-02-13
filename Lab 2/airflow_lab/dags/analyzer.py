from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import random
import os

# Define path for shared data
DATA_PATH = "/opt/airflow/working_data"
LOG_FILE = os.path.join(DATA_PATH, "server_logs.txt")
REPORT_FILE = os.path.join(DATA_PATH, "error_report.txt")

def generate_logs(**kwargs):
    """Task 1: Generate a dummy log file."""
    messages = ["INFO: System stable", "WARNING: High memory", "ERROR: Connection failed", "INFO: User logged in"]
    with open(LOG_FILE, "w") as f:
        for _ in range(50):
            entry = random.choice(messages)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {entry}\n")
    print(f"Generated log file at {LOG_FILE}")

def analyze_logs(**kwargs):
    """Task 2: Count ERRORs."""
    error_count = 0
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
        for line in lines:
            if "ERROR" in line:
                error_count += 1
    
    report = f"Log Analysis Report\nTotal Entries: {len(lines)}\nTotal Errors: {error_count}\n"
    with open(REPORT_FILE, "w") as f:
        f.write(report)
    print(f"Analysis complete. Errors found: {error_count}")

def archive_logs(**kwargs):
    """Task 3: Rename/Archive the log file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = os.path.join(DATA_PATH, f"server_logs_{timestamp}.txt")
    os.rename(LOG_FILE, archive_name)
    print(f"Archived to {archive_name}")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

with DAG(
    'log_analyzer_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    t1 = PythonOperator(task_id='generate_logs', python_callable=generate_logs)
    t2 = PythonOperator(task_id='analyze_logs', python_callable=analyze_logs)
    t3 = PythonOperator(task_id='archive_logs', python_callable=archive_logs)

    t1 >> t2 >> t3