import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Fetches data from Socrata API in chunks defined by "limit" and combines them into a DataFrame.
    Returns:
      pd.DataFrame: Combined DataFrame containing all data.
    """
    
    vehicles_dtypes = {
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


    parse_dates = ['date_of_vehicle_sale','transaction_date']  

    limit = 5
    offset = 0
    data_all = []

    while offset < 15:
    #while True:
        url = f"https://data.wa.gov/resource/rpr4-cgyd.json?$limit={limit}&$offset={offset}"
        response = requests.get(url)

        if response.status_code == 200:
            data_chunk = pd.read_json(io.StringIO(response.text), convert_dates=parse_dates)
            if len(data_chunk) == 0:
                print("No more data available")
                break
            data_all.append(data_chunk)
            print(f"Records {offset + 1} to {offset + limit} loaded...")
            offset += limit   
        else:
            print(f"Failed to fetch data with status code: {response.status_code}")
            break
    
    data_concat = pd.concat(data_all)
    data_concat = data_concat.convert_dtypes()
    print(data_concat.info())
    return data_concat
    

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
