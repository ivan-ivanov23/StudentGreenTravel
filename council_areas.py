import requests

# def get_district(country_postcodes: list):
#     """Finds the admin district for a passed list with postcodes of a country.""" 
#     # Inspired by: https://stackoverflow.com/questions/16877422/whats-the-best-way-to-parse-a-json-response-from-the-requests-library 
#     result = {}
#     for postcode in country_postcodes:
#         url = f"https://api.postcodes.io/postcodes/{postcode}"
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             admin_district = data.get("result", {}).get("admin_district")
#             result[postcode] = admin_district
#         else:
#             result[postcode] = None

#     print(result)
    
#     return result

def get_district(country_postcodes):
    """Finds the admin district for a passed list with postcodes of a country.""" 
    result = {}
    country_postcodes = split_list(country_postcodes)
    for part in country_postcodes:
        data = {"postcodes": part}
        response = requests.post("https://api.postcodes.io/postcodes", json=data)
        if response.status_code == 200:
            response_json = response.json()
            for item in response_json["result"]:
                postcode = item["query"]  # Use "query" instead of "postcode"
                if item["result"] is None:
                    result[postcode] = None
                else:
                    district = item["result"]["admin_district"]
                    result[postcode] = district

    #print(result)
    return result

def split_list(lst, chunk_size=100):
    chunks = [[] for _ in range((len(lst) + chunk_size - 1) // chunk_size)]
    for i, item in enumerate(lst):
        chunks[i // chunk_size].append(item)
    return chunks
    


def group_district(districts: dict):
    """Groups the postcodes by their admin district."""
    # Source: https://www.tutorialspoint.com/python-group-similar-keys-in-dictionary
    result = {}
    for postcode, district in districts.items():
        if district in result:
            result[district].append(postcode)
        else:
            result[district] = [postcode]
    return result

def find_percentage(ordered: dict, country_postcodes: list):
    """Finds the percentage of postcodes in each admin district in respect to all postcodes for country."""
    total = len(country_postcodes)
    result = {}
    for district, postcodes in ordered.items():
        count = len(postcodes)
        percentage = (count / total) * 100
        result[district] = percentage
    return result


# Example list of Scottish postcodes
scot = ["PO7 5GE", "PE11 3FQ",
"NE20 9SZ",
"AB11 6HS",
"SG27PB",
"AB25 1XF",
"HP9 2DJ",
"UB5 6NA",
"TR7 2AA",
"L36 3XR",
"SW6 4HE",
"NE66 2LP",
"W5 1JG",
"SY13 1HP",
"NR11PR",
"E11 4RW",
"AB245RQ",
"E2 8FB",
"TS5 6QU",
"IG1 3NJ"]


# districts = get_district(scot)
# print(districts)
# grouped = group_district(districts)
# print(grouped)
# percent = find_percentage(grouped, scot)
# print(percent)
