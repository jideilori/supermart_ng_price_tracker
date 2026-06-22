import os
from dotenv import load_dotenv

from src.storage.gcs_storage import GCSStorage
from src.warehouse.bigquery import BigQueryLoader

load_dotenv()


def run():

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    bucket = os.getenv("GCS_BUCKET_NAME")

    gcs_reader = GCSStorage(bucket, project_id)
    loader = BigQueryLoader(project_id)

    table_id = f"{project_id}.supermart_dw.raw_products"

    # STEP 1: find latest run automatically
    latest_prefix = gcs_reader.list_latest_run_prefix(
        base_prefix="raw/"
    )

    run_id = latest_prefix.split("run_id=")[-1].split("/")[0]

    gcs_uri = f"gs://{bucket}/{latest_prefix}"


    # STEP 2: CHECK IF ALREADY LOADED
    if loader.run_already_loaded(run_id):
        print(f"Run {run_id} already loaded. Skipping.")
        return


    try:
        # STEP 3: LOAD DATA
        print(f"Loading run {run_id} into BigQuery...")

        result = loader.load_from_gcs_prefix(table_id, gcs_uri)

        # STEP 4: WRITE SUCCESS LOG
        loader.write_ingestion_log(
            run_id=run_id,
            gcs_path=gcs_uri,
            status="SUCCESS",
            row_count=result.get("rows")
        )

        print(f"Load completed: {result}")


    except Exception as e:

        # STEP 5: WRITE FAILURE LOG
        loader.write_ingestion_log(
            run_id=run_id,
            gcs_path=gcs_uri,
            status="FAILED",
            row_count=None
        )

        raise e


if __name__ == "__main__":
    run()