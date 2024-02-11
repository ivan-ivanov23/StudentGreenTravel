# This file calculates the distance between the postcode and the closest bus station, 
# and the distance between the bus station and Aberdeen bus station.
# At the end of the dictionary that is printed, the distance between the Aberdeen bus station and the university is printed.

import pandas as pd
import numpy as np
from geopy.distance import geodesic

# Coordinates of Aberdeen bus station and university (taken from Google Maps)
aberdeen_uni = (-2.0999, 57.1645)
scot_postcodes = ['AB', 'DD', 'DG', 'EH', 'FK', 'G', 'HS', 'IV', 'KA', 'KW', 'KY', 'ML', 'PA', 'PH', 'TD', 'ZE']
aberdeen_bus_stop = (-2.095330457035445, 57.14450856576696)

# Read ukpostcodes.csv
postcodes = pd.read_csv('data/ukpostcodes.csv')
# Trim the postcode column
postcodes['postcode'] = postcodes['postcode'].str.replace(' ', '')
# Convert DataFrame columns to numpy arrays for faster processing
postcode_array = postcodes['postcode'].values
latitude_array = postcodes['latitude'].values
longitude_array = postcodes['longitude'].values

# Create a dictionary to store postcode coordinates 
postcode_coord_dict = dict(zip(postcode_array, zip(latitude_array, longitude_array)))

# Read in the csv file that holds the coordinates of the bus station
stops = pd.read_csv("data/Scotland_Bus_Stations.csv")
# Convert DataFrame columns to numpy arrays for faster processing
stop_name_array = stops['StationName'].values
stop_latitude_array = stops['Latitude'].values
stop_longitude_array = stops['Longitude'].values

# Create a dictionary to store stop coordinates and type
stop_coord_dict = dict(zip(stop_name_array, zip(stop_longitude_array, stop_latitude_array)))

def calculate_distances(coords1, coords2_array):
    """Calculate distances between two coordinates and an array of coordinates."""
    distances = []
    # For single postcode coordinates in array of coordinates
    for coords2 in coords2_array:
        # If any of the two are nan
        if np.isnan(coords2).any() or np.isnan(coords1).any():
            continue
        else:
            # Find distance in km
            distances.append(geodesic(coords1, coords2).km)
    return np.array(distances)

def closest_stop(postcode, postcode_coords, stops_dict):
    """Returns the closest bus stop to the postcode"""
    if 'AB' not in postcode:
        # Calculate the distance between the given postcode and bus stops
        distances = calculate_distances((postcode_coords[postcode][1], postcode_coords[postcode][0]), np.array(list(stops_dict.values())))
        # Find the index of the closest bus stop
        closest_stop_index = np.nanargmin(distances)
        # Find the name of the closest bus stop
        closest_stop_name = list(stops_dict.keys())[closest_stop_index]
        # Return the name of the closest bus stop and the distance to it
        return closest_stop_name, distances[closest_stop_index]
    else:
        return 'Aberdeen', 0


def bus_travel(postcode_coords, stops_dict, addresses):
    """Returns a dictionary with postcodes as keys and closest airports as values"""
    # Dictionary to store postcode as key and closest stop, distance to it, and driving distance to Aberdeen as values
    data = {}
    # List to store invalid postcodes
    invalid_postcodes = []

    # For postcode in column 2 of address file
    for postcode in addresses:
        # Find the closest bus stop to the given postcode and the distance to it
        if postcode in postcode_coords:
            closest_stop_name, distance = closest_stop(postcode, postcode_coords, stops_dict)
            
            # If the closest stop is not Aberdeen, calculate the distance to it
            if closest_stop_name != 'Aberdeen':
                # Calculate the distance between the two stops
                travel_distance = geodesic((postcode_coords[postcode][1], postcode_coords[postcode][0]), aberdeen_bus_stop).km
    
            else:
                # For default value, set the distance to 0
                travel_distance = 0
            data[postcode] = (closest_stop_name, round(distance, 2), round(travel_distance, 2))
        else:
            # If the postcode is invalid, add it to the list of invalid postcodes
            invalid_postcodes.append(postcode)
            continue
        

    return data, invalid_postcodes

