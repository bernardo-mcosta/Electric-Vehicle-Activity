CREATE OR REPLACE EXTERNAL TABLE `dtc-de-course-412223.electric_vehicles.electric_vehicles_data`
WITH PARTITION COLUMNS (transaction_year INT64)
OPTIONS (
    format = 'PARQUET',
    uris = ['gs://electric_vehicles_dtc-de-course-412223/electric_vehicles/*'],
    hive_partition_uri_prefix = 'gs://electric_vehicles_dtc-de-course-412223/electric_vehicles',
    require_hive_partition_filter = false
    );
