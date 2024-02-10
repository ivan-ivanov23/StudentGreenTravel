import pandas as pd
import numpy as np
from geopy.distance import geodesic

# Coordinates of Aberdeen railway station and university (taken from Google)
aberdeen_uni = (-2.0999, 57.1645)
aberdeen_rail_station = (-2.0983252205325833, 57.14372498503623)
scot_postcodes = ['AB', 'DD', 'DG', 'EH', 'FK', 'G', 'HS', 'IV', 'KA', 'KW', 'KY', 'ML', 'PA', 'PH', 'TD', 'ZE']

# Read ukpostcodes.csv
postcodes = pd.read_csv('data/ukpostcodes.csv')
# Drop index column
#postcodes = postcodes.drop(columns=['id'])
# Drop rows with missing values
postcodes = postcodes.dropna()
# Trim the postcode column
postcodes['postcode'] = postcodes['postcode'].str.replace(' ', '')
# Convert DataFrame columns to numpy arrays for faster processing
postcode_array = postcodes['postcode'].values
latitude_array = postcodes['latitude'].values
longitude_array = postcodes['longitude'].values

# Create a dictionary to store postcode coordinates 
postcode_coords = dict(zip(postcode_array, zip(latitude_array, longitude_array)))

# Read in the airpo csv file
stations = pd.read_csv("data/stations.csv")
# Drop rows with missing values
stations = stations.dropna()
# Convert DataFrame columns to numpy arrays for faster processing
station_name_array = stations['Station'].values
station_latitude_array = stations['Lat'].values
station_longitude_array = stations['Long'].values

# Create a dictionary to store stop coordinates and type
station_coords = dict(zip(station_name_array, zip(station_longitude_array, station_latitude_array)))
# Convert to numpy array for faster processing


def calculate_distances(coords1, coords2_array):
    """Calculate distances between two coordinates and an array of coordinates."""
    distances = []
    # For single postcode coordinates in array of coordinates
    for coords2 in coords2_array:
        # If any of the two are nan
        if np.isnan(coords2).any() or np.isnan(coords1).any():
            # Calcualte distance between coords1 and Aberdeen
            continue
        else:
            # Find distance in km
            distances.append(geodesic(coords1, coords2).km)
    return np.array(distances)

def closest_stop(postcode, postcode_coords, stations_dict):
    """Returns the closest bus stop to the postcode"""
    if 'AB' not in postcode:
        # Calculate the distance between the given postcode and railway stations in the area
        distances = calculate_distances((postcode_coords[postcode][1], postcode_coords[postcode][0]), np.array(list(stations_dict.values())))
        # Find the index of the closest bus stop
        closest_stop_index = np.nanargmin(distances)
        # Find the name of the closest bus stop
        closest_stop_name = list(stations_dict.keys())[closest_stop_index]
        # Return the name of the closest bus stop and the distance to it
        return closest_stop_name, distances[closest_stop_index]
    else:
        return 'Aberdeen', 0


def rail_travel(postcode_coords, stations_dict, addresses):
    """Returns a dictionary with postcodes as keys and closest airports as values"""
    # Dictionary to store postcode as key and closest stop, distance to it, and driving distance to Aberdeen as values
    data = {}
    # List to store invalid postcodes
    invalid_postcodes = []

    # For postcode in column 2 of address file
    for postcode in addresses:
        # Find the closest airport to the postcode
        if postcode in postcode_coords:
            closest_stop_name, distance = closest_stop(postcode, postcode_coords, stations_dict)
            
            # If the closest airport is not Aberdeen (default value for invalid postcodes) and the postcode is not from Scotland or London
            if closest_stop_name != 'Aberdeen':
                # Calculate the distance between the two stops
                travel_distance = geodesic((postcode_coords[postcode][1], postcode_coords[postcode][0]), aberdeen_rail_station).km
                # Distance between Aberdeen bus station and university
                # travel_distance2 = 2.28
                # travel_distance = travel_distance1 + travel_distance2
            else:
                # For default value, set the distance to 0
                travel_distance = 0
            data[postcode] = (closest_stop_name, round(distance, 2), round(travel_distance, 2))
        else:
            # If the postcode is invalid, add it to the list of invalid postcodes
            invalid_postcodes.append(postcode)
            continue
        

    return data, invalid_postcodes

