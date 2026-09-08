from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


DBT_PROJECT_DIR = "/opt/airflow/dbt/ecommerce_dbt"
DBT_PROFILES_DIR = "/home/airflow/.dbt"
PROJECT_DIR = "/opt/airflow"

with DAG(
    dag_id="ecommerce_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="0 2 * * *",
    catchup=False,
    tags=["ecommerce", "python", "dbt", "duckdb"],
) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command=f"""
            python {PROJECT_DIR}/src/ingestion/extract.py
        """,
    )
    
    load = BashOperator(
        task_id="load",
        bash_command=f"""
            python {PROJECT_DIR}/src/ingestion/load.py
        """,
    )
    
    load_to_duckdb = BashOperator(
        task_id="load_to_duckdb",
        bash_command=f"""
            python {PROJECT_DIR}/src/ingestion/load_to_duckdb.py
        """,
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=f"""
            cd {DBT_PROJECT_DIR}
            dbt build --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    extract >> load >> load_to_duckdb >> dbt_build