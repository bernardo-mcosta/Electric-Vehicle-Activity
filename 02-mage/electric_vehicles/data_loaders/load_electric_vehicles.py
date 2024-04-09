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

    limit = 50000
    offset = 0
    data_all = []

    while True:
        url = f"https://data.wa.gov/resource/rpr4-cgyd.json?$limit={limit}&$offset={offset}"
        response = requests.get(url)

        if response.status_code == 200:
            data_chunk = pd.read_json(io.StringIO(response.text))#, convert_dates=parse_dates)
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
    
    print(data_concat.info())
    return data_concat