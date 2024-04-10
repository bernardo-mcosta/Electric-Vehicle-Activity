if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import numpy as np

@transformer
def transform(data, *args, **kwargs):
        
    schema = {
    "electric_vehicle_type": str,
    "vin_1_10": str,
    "dol_vehicle_id": str,
    "model_year": pd.Int64Dtype(),
    "make": str,
    "model": str,
    "vehicle_primary_use": str,
    "electric_range": pd.Int64Dtype(),
    "odometer_reading": pd.Int64Dtype(),
    "odometer_code": str,
    "new_or_used_vehicle": str,
    "sale_price": pd.Int64Dtype(),
    "base_msrp": pd.Int64Dtype(),
    "transaction_type": str,
    "transaction_year": pd.Int64Dtype(),
    "county": str,
    "city": str,
    "state_of_residence": str,
    "zip": str,
    "meets_2019_hb_2042_sale_price_value_requirement": bool,
    "_2019_hb_2042_sale_price_value_requirement": str,
    "electric_vehicle_fee_paid": str,
    "transportation_electrification_fee_paid": str,
    "hybrid_vehicle_electrification_fee_paid": str,
    "census_tract_2020": str,
    "legislative_district": str,
    "electric_utility": str
    }   

    for column, dtype in schema.items():
        if pd.api.types.is_string_dtype(data[column]):
            print(f'string detected for [{column}], skipping...')
            continue
        try:
            if column == "sale_price" and data[column].dtype == "float64":
                data[column] = data[column].round().astype(pd.Int64Dtype())
                print(f'[{column}] converted from {data[column].dtype} to type {dtype}...')
            else:
                data[column] = data[column].astype(dtype)
                print(f'[{column}] converted from {data[column].dtype} to type {dtype}...')
        except (ValueError, TypeError) as e:
            print(f"Warning: Failed to convert column '{column}' to type '{dtype}'. Error: {e}")

    print('\n')
    data.info()
    return data