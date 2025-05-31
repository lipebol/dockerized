from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from common.initialize import Starting
from flows.convert_date_using_pyarrow.python.main import settings
from flows.convert_date_using_pyarrow.python.transform import Transform


with DAG(
    dag_id="convert_date_using_pyarrow",
    default_args={"owner": "lipebol", "depends_on_past": True},
    start_date=datetime.now(), catchup=False, description=""
):
    
    task_1=PythonOperator(
        task_id="Requirements...",
        python_callable=Starting(settings()).init
    )

    task_2=PythonOperator(
        task_id="Transform...",
        python_callable=Transform(settings()).convert_date_using_pyarrow
    )


task_1 >> task_2