import uuid
from pathlib import Path
from datetime import datetime

from src.storage.gcs_storage import GCSStorage
from src.utils.logger import setup_logger
import os
from dotenv import load_dotenv

load_dotenv()
logger = setup_logger()

def run():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    bucket_name = os.getenv("GCS_BUCKET_NAME")

    storage = GCSStorage(bucket_name, project_id=project_id)
    files = list(Path("src/scraper/data/raw").glob("*.parquet"))

    if not files:
        print("No parquet files found")
        return


    # partition metadata
    date_partition = datetime.now().strftime("%Y-%m-%d")
    run_id = str(uuid.uuid4())[:8]


    for file in files:

        destination = (
            f"raw/"
            f"date={date_partition}/"
            f"run_id={run_id}/"
            f"{file.name}"
        )

        uri = storage.upload_file(
            file_path=str(file),
            destination_blob=destination
        )

        logger.info(f"Uploaded: {uri}")


if __name__ == "__main__":
    run()