from google.cloud import storage
from pathlib import Path
import re

class GCSStorage:
    
    def __init__(self, bucket_name:str, project_id:str=None):

        self.client = storage.Client(project=project_id)
        self.bucket = self.client.bucket(bucket_name)

    def upload_file (self,file_path:str, destination_blob:str, overwrite:bool=True):

        file_path = Path(file_path)
        blob = self.bucket.blob(destination_blob)

        # safety check
        if not overwrite and blob.exists():
            return f"SKIPPED (exists): gs://{self.bucket.name}/{destination_blob}"

        blob.upload_from_filename(str(file_path))

        return f"gs://{self.bucket.name}/{destination_blob}"
    

    def list_latest_run_prefix(self, base_prefix: str):

        blobs = self.client.list_blobs(self.bucket, prefix=base_prefix)

        paths = [b.name for b in blobs]
        
        if not paths:
            raise ValueError("No data found in GCS")        

        pure_chronological_sort = sorted(paths, key=self.extract_timestamp)
        latest_path = pure_chronological_sort[-1]
        print(f"Latest path: {latest_path}")
        # extract prefix up to run_id folder
        parts = latest_path.split("/")

        # rebuild: raw/supermart/date=.../run_id=...
        return "/".join(parts[:5])

    def extract_timestamp(self, path):
        # Finds the 8 digits, underscore, 6 digits pattern (e.g., 20260618_112121)
        match = re.search(r'products_(\d{8}_\d{6})', path)
        return match.group(1) if match else path

