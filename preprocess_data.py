# This file contains the functions used to read and preprocess the postcodes of students
# Sources of code snippets are provided in the comments of functions.
# Author: Ivan Ivanov

import math
import pandas as pd
from itertools import islice, accumulate
from utils import split_list
import os
import requests

# Get the absolute path to the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the data directory
data_dir = os.path.join(script_dir, 'data')

# Read ukpostcodes.csv
# Contains Ordnance Survey data © Crown copyright and database right 2021
# Contains Royal Mail data © Royal Mail copyright and database right 2021
# Source: Office for National Statistics licensed under the Open Government Licence v.3.0
ukpostcodes_path = os.path.join(data_dir, 'uk_postcodes.csv')
ukpostcodes = pd.read_csv(ukpostcodes_path, usecols=['postcode', 'latitude', 'longitude'])
ukpostcodes['postcode'] = ukpostcodes['postcode'].str.replace(' ', '')
ukpostcode_coords = dict(zip(ukpostcodes['postcode'], zip(ukpostcodes['latitude'], ukpostcodes['longitude'])))

# Read Scotland_Bus_Stations.csv
bus_stops_path = os.path.join(data_dir, 'scotland_bus_stations.csv')
bus_stops = pd.read_csv(bus_stops_path, usecols=['StationName', 'Latitude', 'Longitude'])
stops_dict = dict(zip(bus_stops['StationName'], zip(bus_stops['Latitude'], bus_stops['Longitude'])))

# Read Railway Stations
rail_stations_path = os.path.join(data_dir, 'rail_stations.csv')
rail_stations = pd.read_csv(rail_stations_path, usecols=['Station', 'Lat', 'Long'])
stations_dict = dict(zip(rail_stations['Station'], zip(rail_stations['Lat'], rail_stations['Long'])))

# Read airports
airports_path = os.path.join(data_dir, 'airports.csv')
airports = pd.read_csv(airports_path, usecols=['Airport', 'Latitude', 'Longitude'])
airports_dict = dict(zip(airports['Airport'], zip(airports['Latitude'], airports['Longitude'])))


scot_postcodes = ['DD', 'DG', 'EH', 'FK', 'G', 'HS', 'IV', 'KA', 'KW', 'KY', 'ML', 'PA', 'PH', 'TD', 'ZE']
eng_postcodes = ['AL', 'BA', 'BB', 'BD', 'BH', 'BL', 'BN', 'BR', 'BS', 'CA', 'CB', 'CH', 'CM', 'CO', 'CR', 'CT', 'CV', 'CW', 'DA', 'DE', 'DH', 'DL', 'DN', 'DT', 'DY', 'EC', 'EN', 'EX', 'FY', 'GL', 'GU', 'HA', 'HD', 'HG', 'HP', 'HR', 'HU', 'HX', 'IG', 'IP', 'KT', 'LA', 'LD', 'LE', 'LN', 'LS', 'LU', 'ME', 'MK', 'NE', 'NG', 'NN', 'NR', 'NW', 'OL', 'OX', 'PE', 'PL', 'PO', 'PR', 'RG', 'RH', 'RM', 'SE', 'SG', 'SK', 'SL', 'SM', 'SN', 'SO', 'SP', 'SR', 'SS', 'ST', 'SW', 'TA', 'TF', 'TN', 'TQ', 'TR', 'TS', 'TW', 'UB', 'WA', 'WC', 'WD', 'WF', 'WN', 'WR', 'WS', 'WV', 'YO']
wales_postcodes = ['CF', 'LL', 'NP', 'SA', 'SY'] 
        
scotland = []
england = []
wales = []
north_ireland = []

# Dictionary to store postcodes and coordinates which are not found in initial csv file
additional_coords = {}

def determine_postcode(postcodes):
    postcodes = postcodes.dropna()  # Drop NaN values
    scotland = postcodes[(postcodes.str[:2].isin(scot_postcodes)) | ((postcodes.str[:2] == 'G') & ~(postcodes.str[:2].isin(eng_postcodes)))]
    england = postcodes[(postcodes.str[:2].isin(eng_postcodes)) & ~(postcodes.str[:2].isin(scot_postcodes)) & ~(postcodes.str[:2]).isin(wales_postcodes)]
    wales = postcodes[postcodes.str[:2].isin(wales_postcodes)]
    north_ireland = postcodes[postcodes.str[:2] == 'BT']
    aberdeen = postcodes[postcodes.str[:2] == 'AB']
    # Invalid postcodes are not in scotland, england, wales or north_ireland
    invalid = postcodes[~(postcodes.isin(scotland) | postcodes.isin(england) | postcodes.isin(wales) | postcodes.isin(north_ireland))]
    new_invalid = find_country(invalid)
    return scotland, wales, north_ireland, england, aberdeen, new_invalid

def find_country(postcodes):
    """Finds the admin district for a passed list with postcodes of a country.""" 
    # Inspired by answer from ruddra: https://stackoverflow.com/questions/53472954/using-postcodes-io-api-on-django
    result = {}
    country_postcodes = split_list(postcodes)
    for part in country_postcodes:
        data = {"postcodes": part}
        response = requests.post("https://api.postcodes.io/postcodes", json=data)
        if response.status_code == 200:
            response_json = response.json()
            for item in response_json["result"]:
                # Postcode taken from the query
                postcode = item["query"]
                if item["result"] is None:
                    result[postcode] = 'Uknown country'
                else:
                    if item["result"]["country"] == 'Scotland' or item["result"]["country"] == 'Isle of Man':
                        scotland.append(postcode)
                        additional_coords[postcode] = [item["result"]["latitude"], item["result"]["longitude"]]
                    elif item["result"]["country"] == 'England' or item["result"]["country"] == 'Channel Islands':
                        england.append(postcode)
                        additional_coords[postcode] = [item["result"]["latitude"], item["result"]["longitude"]]
                    elif item["result"]["country"] == 'Wales':
                        wales.append(postcode)
                        additional_coords[postcode] = [item["result"]["latitude"], item["result"]["longitude"]]
                    elif item["result"]["country"] == 'Northern Ireland':
                        north_ireland.append(postcode)
                        additional_coords[postcode] = [item["result"]["latitude"], item["result"]["longitude"]]
                    else:
                        if item["result"]["country"]:
                            result[postcode] = item["result"]["country"]
                        else:
                            result[postcode] = 'Uknown country'
    return result



def divide_scot_addresses(scot_addresses: list,  p_bus, p_car, p_rail):
    """The function divides the list of Scottish postcodes into 3 parts based on the percentages of each transport method."""

    p_bus_scot = math.ceil(len(scot_addresses) * (p_bus / 100))
    p_car_scot = math.ceil(len(scot_addresses) * (p_car / 100))   
    p_rail_scot = len(scot_addresses) - p_bus_scot - p_car_scot

    split_list = [p_bus_scot, p_car_scot, p_rail_scot]

    # Source: Method 3 in https://www.geeksforgeeks.org/python-split-list-in-uneven-groups/
    res = [list(islice(scot_addresses, start, end)) for start, end in zip([0]+list(accumulate(split_list)), accumulate(split_list))]

    return res

def divide_uk_addresses(country: list, p_plane, p_car, p_rail):
    """The function divides the list of UK postcodes into 3 parts based on the percentages of each transport method.
        It is used for England, Wales and Northern Ireland."""

    # Calculate the number of postcodes for each transport method
    p_plane_uk = math.ceil(len(country) * (p_plane / 100))
    p_car_uk = math.ceil(len(country) * (p_car / 100))
    p_rail_uk = len(country) - p_plane_uk - p_car_uk 

    # randomly divide 'uk' into 3 parts based on the percentages
    seclist_uk = [p_plane_uk, p_car_uk, p_rail_uk]

    # Source: Method 3 in https://www.geeksforgeeks.org/python-split-list-in-uneven-groups/
    res_uk = [list(islice(country, start, end)) for start, end in zip([0]+list(accumulate(seclist_uk)), accumulate(seclist_uk))]

    return res_uk
