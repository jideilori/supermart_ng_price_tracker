#!/bin/bash

set -e  # stop immediately if any command fails

echo "======================================"
echo "🚀 Retail Data Pipeline Starting"
echo "======================================"

# Step 1: Run Scrapy spider
echo ""
echo "📡 Step 1: Running Scrapy spider..."
# poetry run python -m scrapy crawl supermart

echo ""
echo "✅ Scraping completed successfully"

# Step 2: Run GCS upload job
echo ""
echo "☁️ Step 2: Uploading Parquet files to GCS..."
poetry run python -m src.jobs.upload_to_gcs

echo ""
echo "✅ Upload completed successfully"

echo ""
echo "======================================"

poetry run python -m src.jobs.load_to_bigquery



echo ""
echo "======================================"
echo "🎉 Pipeline finished successfully"
echo "======================================"