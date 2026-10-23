from google.cloud import bigquery

# ---- Config: change these only ----
PROJECT_ID = "project-5967f285-2cf3-4932-895"
DATASET    = "sales_dashboard"
TABLE      = "sales_dts"
CSV_PATH   = "data/sales_bq.csv"
# -----------------------------------

table_id = f"{PROJECT_ID}.{DATASET}.{TABLE}"
print("Target table:", table_id)

client = bigquery.Client(project=PROJECT_ID)

schema = [
    bigquery.SchemaField("order_id", "INT64"),
    bigquery.SchemaField("order_date", "DATE"),
    bigquery.SchemaField("customer_id", "STRING"),
    bigquery.SchemaField("region", "STRING"),
    bigquery.SchemaField("product", "STRING"),
    bigquery.SchemaField("category", "STRING"),
    bigquery.SchemaField("quantity", "INT64"),
    bigquery.SchemaField("unit_price", "FLOAT64"),
]

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    schema=schema,
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
)

with open(CSV_PATH, "rb") as f:
    job = client.load_table_from_file(
        f,
        table_id,
        job_config=job_config
    )

job.result()  # Wait for the load to finish

# Rows loaded in this run
rows_loaded = job.output_rows

# Total rows in the destination table
total_rows = client.get_table(table_id).num_rows

print("Rows loaded in this run:", rows_loaded)
print("Total rows in table:", total_rows)