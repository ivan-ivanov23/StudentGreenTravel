import requests    

def get_district(country_postcodes: list):
    """Finds the admin district for a passed list with postcodes of a country.""" 
    #Inspired by: https://stackoverflow.com/questions/16877422/whats-the-best-way-to-parse-a-json-response-from-the-requests-library 
    result = {}
    # Zip the postcodes into equal parts of 100 because the API only accepts 100 postcodes at a time
    country_postcodes = split_list(country_postcodes)
    for part in country_postcodes:
        data = {"postcodes": part}
        response = requests.post("https://api.postcodes.io/postcodes", data=data)
        if response.status_code == 200:
            response = response.json()
            for item in response["result"]:
                postcode = item["result"]["postcode"]
                if item["result"] is None:
                    result[postcode] = "Unknown"
                else:
                    district = item["result"]["admin_district"]
                    result[postcode] = district
    
    return result

def split_list(lst):
    return list(zip(*[iter(lst)] * 100))