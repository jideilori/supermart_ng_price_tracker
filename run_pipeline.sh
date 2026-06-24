#!/bin/bash

set -e  # stop immediately if any command fails

echo "======================================"
echo "🚀 Retail Data Pipeline Starting"
echo "======================================"

# Step 1: Run the Scrapy spider to collect fresh product data
echo ""
echo "📡 Step 1: Running Scrapy spider..."
poetry run python -m scrapy crawl supermart

echo ""
echo "✅ Scraping completed successfully"

# Step 2: Upload the generated Parquet files to Google Cloud Storage
echo ""
echo "☁️ Step 2: Uploading Parquet files to GCS..."
poetry run python -m src.jobs.upload_to_gcs

echo ""
echo "✅ Upload completed successfully"

# Step 3: Load the latest uploaded data into BigQuery
echo ""
echo "📦 Step 3: Loading data into BigQuery..."
poetry run python -m src.jobs.load_to_bigquery

echo ""
echo "✅ BigQuery load completed successfully"

echo ""
echo "======================================"
echo "🎉 Pipeline finished successfully"
echo "======================================"