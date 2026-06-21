from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "Yogesh",
    "start_date": datetime(2025, 1, 1),
    "retries": 2
}

with DAG(

    dag_id="travel_pipeline",

    default_args=default_args,

    schedule="@daily",

    catchup=False,

    description="Travel Data Engineering Pipeline"

) as dag:

    extract_api = BashOperator(

        task_id="extract_api",

        bash_command="python /opt/project/ingestion/extract_api_data.py"

    )

    upload_s3 = BashOperator(

        task_id="upload_to_s3",

        bash_command="python /opt/project/ingestion/upload_to_s3.py"

    )

    extract_api >> upload_s3