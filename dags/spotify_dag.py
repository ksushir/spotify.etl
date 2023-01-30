from datetime import timedelta
from airflow import DAG
from airflow.models.baseoperator import BaseOperator
from airflow.operators.python import PythonOperator
import airflow.utils.dates
from spotify_etl import run_spotify_etl
import pendulum



default_args = {
    "owner": "airflow",
    "depends_on_past":False,
    "start_date": pendulum.today('UTC').add(days=-1),
    "email": ["airflow@example.com"],
    "email_on_failure":False,
    "email_on_retry":False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

dag = DAG(
    "spotify_dag",
    default_args=default_args,
    description = "Our first",
    schedule =timedelta(days=1),
    
)

# def just_a_function():
#     print("im going to show you something :)")

run_etl = PythonOperator(
    task_id="whole_spotify_etl",
    python_callable=run_spotify_etl,
    dag=dag,
)

run_etl

