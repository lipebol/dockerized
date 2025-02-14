from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv

def welcome():
    return "wooHooo!"

jobs = DAG(
    dag_id="jobs",
    default_args={
        "owner": "lipebol",
        "depends_on_past": True,
        "retries": 5, 
        "retry_delay": timedelta(minutes=5)
    },
    #start_date=datetime(2025, 2, 13, 22, 30),
    #schedule_interval="*/30 * * * *",
    #catchup=False,
    description="",
)

task_1=PythonOperator(
    task_id="Welcome...",
    python_callable=welcome,
    dag=jobs
)

task_1