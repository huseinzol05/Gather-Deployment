from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
import logging

DAG = DAG(
    dag_id = 'simple_xcom',
    start_date = datetime(2017, 10, 26),
    schedule_interval = None,
)


def push_function(**context):
    msg = 'the_message'
    logging.info("message to push: '%s'" % msg)
    print("message to push: '%s'" % msg)
    task_instance = context['task_instance']
    task_instance.xcom_push(key = 'the_message', value = msg)


push_task = PythonOperator(
    task_id = 'push_task',
    python_callable = push_function,
    provide_context = True,
    dag = DAG,
)


def pull_function(**kwargs):
    ti = kwargs['ti']
    msg = ti.xcom_pull(task_ids = 'push_task', key = 'the_message')
    logging.info("received message: '%s'" % msg)
    print("received message: '%s'" % msg)


pull_task = PythonOperator(
    task_id = 'pull_task',
    python_callable = pull_function,
    provide_context = True,
    dag = DAG,
)

push_task >> pull_task
