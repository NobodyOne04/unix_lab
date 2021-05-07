from datetime import (
    datetime,
    timedelta,
)

from airflow import DAG
from airflow.operators.docker_operator import DockerOperator

from utils.settings import DATA_PATH

default_args = {
    'owner': 'vshapovalov',
    'description': 'Extraction DAG',
    'depend_on_past': False,
    'start_date': datetime(2021, 5, 4),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG('extract_dag', default_args=default_args, schedule_interval="5 * * * *", catchup=False) as dag:
    crawler_task = DockerOperator(
        task_id='crawler',
        image='crawler-imdb:latest',
        api_version='auto',
        auto_remove=True,
        network_mode="bridge",
        volumes=[
            f"{DATA_PATH}:/data"
        ],
        environment={
            'OUTPUT_DIR': '/data/crawler'
        },
    )

    parser_task = DockerOperator(
        task_id='parser',
        image='parser-imdb:latest',
        api_version='auto',
        auto_remove=True,
        network_mode="bridge",
        volumes=[
            f"{DATA_PATH}:/data"
        ],
        environment={
            'INPUT_DIR': '/data/crawler',
            'OUTPUT_DIR': '/data/parser'
        },
    )

    load_task = DockerOperator(
        task_id='load',
        image='hello-world:latest',
        api_version='auto',
        auto_remove=True,
        network_mode="bridge",
        xcom_push=True,
        xcom_all=True
    )

    crawler_task >> parser_task >> load_task
