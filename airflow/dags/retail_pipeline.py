from datetime import datetime
import os

from airflow import DAG
from airflow.operators.bash import BashOperator
    

PROJECT_DIR = os.getcwd()


with DAG(
    dag_id="supermart_retail_pipeline",
    start_date=datetime(2026, 6, 18),
    schedule="0 6 *     * *",   # every day 6AM
    catchup=False,
    tags=["retail", "scraping"],
) as dag:


    scrape_products = BashOperator(
        task_id="scrape_products",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        poetry run python -m scrapy crawl supermart
        """
    )


    upload_gcs = BashOperator(
        task_id="upload_to_gcs",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        poetry run python -m src.jobs.upload_to_gcs
        """
    )


    load_bigquery = BashOperator(
        task_id="load_bigquery",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        poetry run python -m src.jobs.load_to_bigquery
        """
    )


    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command=f"""
        cd {PROJECT_DIR}/dbt/supermart_dbt &&
        poetry run dbt run
        """
    )


    scrape_products >> upload_gcs >> load_bigquery >> run_dbt