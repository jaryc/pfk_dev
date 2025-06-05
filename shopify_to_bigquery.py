#!/usr/bin/env python3
"""Fetches orders from a Shopify store and loads them into BigQuery."""
import os
import json
from typing import List

import requests
from google.cloud import bigquery

SHOPIFY_STORE = os.getenv("SHOPIFY_STORE_DOMAIN")
ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")

BQ_PROJECT = os.getenv("BQ_PROJECT_ID")
BQ_DATASET = os.getenv("BQ_DATASET")
BQ_TABLE = os.getenv("BQ_TABLE")

ORDERS_ENDPOINT = f"https://{SHOPIFY_STORE}/admin/api/2024-01/orders.json?status=any&limit=5"


def fetch_orders() -> List[dict]:
    """Retrieve a small set of orders from Shopify."""
    headers = {"X-Shopify-Access-Token": ACCESS_TOKEN}
    resp = requests.get(ORDERS_ENDPOINT, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("orders", [])


def load_to_bigquery(orders: List[dict]) -> None:
    """Append orders to the configured BigQuery table."""
    client = bigquery.Client(project=BQ_PROJECT)
    table_ref = f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}"
    errors = client.insert_rows_json(table_ref, orders)
    if errors:
        raise RuntimeError(f"BigQuery insert errors: {errors}")


def main() -> None:
    missing = [k for k in [SHOPIFY_STORE, ACCESS_TOKEN, BQ_PROJECT, BQ_DATASET, BQ_TABLE] if not k]
    if missing:
        raise SystemExit("Missing environment variables for configuration")

    orders = fetch_orders()
    if not orders:
        print("No orders found.")
        return

    load_to_bigquery(orders)
    print(f"Loaded {len(orders)} orders into BigQuery table {BQ_TABLE}")


if __name__ == "__main__":
    main()
