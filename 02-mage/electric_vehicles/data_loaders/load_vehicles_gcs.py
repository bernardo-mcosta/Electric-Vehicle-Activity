from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

import pyarrow as pa
import pyarrow.parquet as pq
import os

schema = pa.schema([
    ('electric_vehicle_type', pa.string()),
    ('vin_1_10', pa.string()),
    ('dol_vehicle_id', pa.string()),
    ('model_year', pa.int64()),
    ('make', pa.string()),
    ('model', pa.string()),
    ('vehicle_primary_use', pa.string()),
    ('electric_range', pa.int64()),
    ('odometer_reading', pa.int64()),
    ('odometer_code', pa.string()),
    ('new_or_used_vehicle', pa.string()),
    ('sale_price', pa.int64()),
    ('date_of_vehicle_sale', pa.string()),
    ('base_msrp', pa.int64()),
    ('transaction_type', pa.string()),
    ('transaction_year', pa.int64()),
    ('county', pa.string()),
    ('city', pa.string()),
    ('state_of_residence', pa.string()),
    ('zip', pa.string()),
    ('meets_2019_hb_2042_sale_price_value_requirement', pa.bool_()),
    ('2019_hb_2042_sale_price_value_requirement', pa.string()),
    ('electric_vehicle_fee_paid', pa.string()),
    ('transportation_electrification_fee_paid', pa.string()),
    ('hybrid_vehicle_electrification_fee_paid', pa.string()),
    ('census_tract_2020', pa.string()),
    ('legislative_district', pa.string()),
    ('electric_utility', pa.string()),
    ('transaction_date', pa.string()),
])

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/home/src/credentials/keys.json'

project_id = 'dtc-de-course-412223'
bucket_name = 'electric_vehicles_dtc-de-course-412223'
table_name = 'electric_vehicles'

root_path = f'{bucket_name}/{table_name}' 

@data_loader
def load_from_google_cloud_storage(*args, **kwargs):
    
    gcs = pa.fs.GcsFileSystem()

    dataset = pq.ParquetDataset(root_path, filesystem=gcs, schema = schema)

    data = dataset.read_pandas().to_pandas()

    return data
