import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

default_args = {
    'owner': 'admin',
    'start_date': datetime(2025, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False,
    'catchup': False,
}

def call_model_api():
    url = 'http://host.docker.internal:5000/predict'
    data = [
        {
            "distance": 100, 
            "time": 2, 
            "from": "CityA", 
            "to": "CityB", 
            "flightType": "economy", 
            "agency": "AirlineX"
        }
    ]
    
    response = requests.post(url, json=data)
    prediction = response.json()
    print(f"Prediction: {prediction}")

# Define the DAG
dag = DAG(
    'model_prediction_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
)

# Define the task
prediction_task = PythonOperator(
    task_id='call_model_api_task',
    python_callable=call_model_api,
    dag=dag
)

prediction_task
