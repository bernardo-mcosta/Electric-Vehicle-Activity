import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/home/src/credentials/keys.json'

bucket_name = 'electric_vehicles_dtc-de-course-412223'
project_id = 'dtc-de-course-412223'
table_name = 'electric_vehicles'

root_path = f'{bucket_name}/{table_name}'

@data_exporter
def export_data(data, *args, **kwargs):

    table = pa.Table.from_pandas(data)

    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['transaction_year'],
        filesystem=gcs
    )
