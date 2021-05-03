from datetime import (
    datetime,
    timedelta,
)

from airflow import DAG
from airflow.operators.sensors import HivePartitionSensor
from airflow.operators.docker_operator import DockerOperator


default_args = {
    'owner': 'vshapovalov',
    'description': 'Model train DAG',
    'depend_on_past': False,
    'start_date': datetime(2021, 5, 4),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG('train_dag', default_args=default_args, schedule_interval="5 * * * *", catchup=False) as dag:
    wait_hive_commit = HivePartitionSensor(
        task_id='wait_hive_commit',
        table='test',
    )

    learn_task = DockerOperator(
        task_id='train',
        image='word2vec:latest',
        api_version='auto',
        auto_remove=True,
        network_mode="bridge",
        environment={
            'FILE_PATTERN': '/data/films/*.json',
            'ROW_NAME': 'Description',
            'MODEL_PATH': '/data/models'
        },
    )

    deploy_task = DockerOperator(
        task_id='deploy',
        image='hello-world:latest',
        api_version='auto',
        auto_remove=True,
        network_mode="bridge"
    )

    wait_hive_commit >> learn_task >> deploy_task
