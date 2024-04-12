from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

from google.cloud.bigquery import SchemaField

@data_exporter
def export_data_to_big_query(df: DataFrame, **kwargs) -> None:
    table_id = 'dtc-de-course-412223.electric_vehicles.dev_gcs_to_bigquery_load_vehicles_gcs_v1'
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        table_id,
        if_exists='replace',
    )