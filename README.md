# pfk_dev

PFK Development for eCommerce Magento

This repository now includes a small Python script for extracting data from a
Shopify store and loading it into Google BigQuery.

## Setup

1. Install Python 3.7+ and pip.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set the following environment variables with your credentials:
   - `SHOPIFY_STORE_DOMAIN` (e.g., `myshop.myshopify.com`)
   - `SHOPIFY_ACCESS_TOKEN` (private app access token)
   - `BQ_PROJECT_ID` (Google Cloud project ID)
   - `BQ_DATASET` (BigQuery dataset name)
   - `BQ_TABLE` (BigQuery table name)

## Running the script

Execute `shopify_to_bigquery.py` to fetch recent orders and append them to the
specified BigQuery table:

```bash
python3 shopify_to_bigquery.py
```

Edit the script if you need to customize which Shopify endpoint is queried or
which fields are inserted into BigQuery.
