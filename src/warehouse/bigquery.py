from google.cloud import bigquery
from datetime import datetime

class BigQueryLoader:

    def __init__(self, project_id: str):

        self.client = bigquery.Client(project=project_id)
        self.project_id = project_id


    def load_from_gcs_prefix(self, table_id: str, gcs_uri: str):

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.PARQUET,
            write_disposition="WRITE_APPEND",
            autodetect=True
        )

        job = self.client.load_table_from_uri(
            gcs_uri,
            table_id,
            job_config=job_config
        )

        job.result()

        # optional: return row count for logging
        table = self.client.get_table(table_id)

        return {
            "uri": gcs_uri,
            "rows": table.num_rows
        }
    
    def run_already_loaded(self, run_id: str) -> bool:

        query = f"""
        SELECT COUNT(1) as cnt
        FROM `{self.project_id}.supermart_dw.ingestion_log`
        WHERE run_id = @run_id AND status = 'SUCCESS'
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("run_id", "STRING", run_id)
            ]
        )

        result = self.client.query(query, job_config=job_config).result()

        for row in result:
            return row.cnt > 0

        return False
    
    def write_ingestion_log(self, run_id: str, gcs_path: str, status: str, row_count: int = None):

        table_id = f"{self.project_id}.supermart_dw.ingestion_log"

        rows = [{
            "run_id": run_id,
            "source": "supermart",
            "gcs_path": gcs_path,
            "status": status,
            "row_count": row_count,
            "loaded_at": datetime.now().isoformat()
        }]

        errors = self.client.insert_rows_json(table_id, rows)

        if errors:
            raise Exception(f"Failed to write ingestion log: {errors}")