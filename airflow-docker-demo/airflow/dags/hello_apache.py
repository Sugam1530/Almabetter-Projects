from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import requests

# Define default arguments
default_args = {
    'owner': 'admin',
    'start_date': datetime(2025, 1, 1),
}

# Define the DAG
dag = DAG(
    'hello_apache',
    default_args=default_args,
    schedule_interval='0 17 * * *',
    catchup=False
)

def print_welcome():
    print("Welcome to Sugam's Travel Price Prediction")

def print_date():
    print('We are learning airflow on: {}'.format(datetime.today().date()))

def print_random_quote():
    response = requests.get('https://api.quotable.io/random')
    quote = response.json()['content']
    print('Quote of the day: "{}"'.format(quote))


# define task

print_welcome_task = PythonOperator(
    task_id = 'print_welcome',
    python_callable = print_welcome,
    dag = dag
)

print_date_task = PythonOperator(
    task_id = 'print_date',
    python_callable = print_date,
    dag = dag
)

print_random_quote_task = PythonOperator(
    task_id =  'print_random_quote',
    python_callable = print_random_quote,
    dag = dag
)

print_welcome_task >> print_date_task >> print_random_quote_task
