import requests
from utils import split_list
import pandas as pd

def get_long_lat(postcodes: list):
    """Finds the longitude and latitude for a list of postcodes and returns a dictionary with the postcodes as keys and the country as values."""
    # Inspired by answer from ruddra: https://stackoverflow.com/questions/53472954/using-postcodes-io-api-on-django
    result = {}
    for part in postcodes:
        data = {"postcodes": part}
        # Make a query to the postcodes.io API with parameter filter=postcode,longitude,latitude
        response = requests.post("https://api.postcodes.io/postcodes", json=data)
        if response.status_code == 200:
            response_json = response.json()
            for item in response_json["result"]:
                postcode = item["query"]
                if item["result"] is None:
                    continue
                else:
                    longitude = item["result"]["longitude"]
                    latitude = item["result"]["latitude"]
                    result[postcode] = (longitude, latitude)



    return result

# Read the csv file with postcodes
postcodes = pd.read_excel('datasets/Test.xlsx', usecols=[1])
postcodes = postcodes.dropna()
# drop float values
postcodes = postcodes[postcodes.iloc[:, 0].apply(lambda x: isinstance(x, str))]
postcodes.iloc[:, 0] = postcodes.iloc[:, 0].str.replace(' ', '')
postcodes = postcodes.iloc[:, 0].tolist()
postcodes = split_list(postcodes, 50)
last = postcodes[-1]
postcodes = postcodes[:-1]
result = get_long_lat(postcodes)
print(result)