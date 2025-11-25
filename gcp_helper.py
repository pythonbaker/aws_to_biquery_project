from google.cloud import bigquery
from google.oauth2 import service_account

credentialsPath = r'gcp-key.json'
credentials = service_account.Credentials.from_service_account_file(credentialsPath)
bq_client = bigquery.Client(credentials=credentials)

schema = [
    bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
]

def bq_table(table_id, schema):

    table = bigquery.Table(table_id, schema=schema)
    table = bq_client.create_table(table)  # Make an API request.
    print(

    "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )
