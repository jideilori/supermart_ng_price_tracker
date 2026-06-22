import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
from datetime import datetime


class ParquetArrowPipeline:

    def __init__(self):

        self.batch_size = 20
        self.items = []
        self.output_dir = Path("src/scraper/data/raw")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.writer = None
        self.file_path = None


    def open_spider(self, spider):
        """
        Called once when spider starts
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.file_path = self.output_dir / f"products_{timestamp}.parquet"


    def process_item(self, item, spider):
        self.items.append(dict(item))
        if len(self.items) >= self.batch_size:
            self.flush(spider)
        return item


    def flush(self, spider):
        if not self.items:
            return
        # Convert Python dicts → Arrow RecordBatch
        batch = pa.RecordBatch.from_pylist(self.items)

        # Initialize writer once
        if self.writer is None:

            self.writer = pq.ParquetWriter(
                self.file_path,
                batch.schema,
                compression="snappy"
            )

        # Write batch
        self.writer.write_batch(batch)
        spider.logger.info(
            f"Wrote {len(self.items)} records to {self.file_path}"
        )
        self.items = []


    def close_spider(self, spider):
        # flush remaining items
        if self.items:
            self.flush(spider)

        if self.writer:
            self.writer.close()

        spider.logger.info(
            f"Finished writing parquet: {self.file_path}"
        )