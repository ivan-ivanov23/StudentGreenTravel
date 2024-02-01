import pandas as pd
import numpy as np
from geopy.distance import geodesic
from tkinter.filedialog import askopenfile


# Coordinates of Aberdeen airport and university (taken from Google)
aberdeen_airport = (57.2019004822, -2.1977798939)
aberdeen_uni = (57.1645, -2.0999)
gatwick_airport = (51.15380339080233, -0.18165520746018157)
scot_postcodes = ['AB', 'DD', 'DG', 'EH', 'FK', 'G', 'HS', 'IV', 'KA', 'KW', 'KY', 'ML', 'PA', 'PH', 'TD', 'ZE']
london_postcodes = ['E', 'EW', 'EC', 'N', 'NW', 'SE', 'SW', 'W', 'WC', 'EN', 'HA', 'IG', 'KT', 'TW', 'UB', 'WD']

"""=========================================File Explorer window============================================================"""
# open file explorer for excel files only so that it is utf-8 encoded
file = askopenfile(filetypes=[("Excel files", "*.xlsx")])
# If the user selected a file, then read it using pandas
if file:
# Read address file
    addresses = pd.read_excel(file.name, engine='openpyxl')
    # Drop any rows with missing values
    addresses = addresses.dropna()
    # Trim the postcode column
    addresses.iloc[:, 1] = addresses.iloc[:, 1].str.replace(' ', '')
# Else, close the program
else:
    exit()

"""=========================================Read Data============================================================"""
# Read ukpostcodes.csv
postcodes = pd.read_csv('data/ukpostcodes.csv')
# Drop index column
postcodes = postcodes.drop(columns=['id'])
# Trim the postcode column
postcodes['postcode'] = postcodes['postcode'].str.replace(' ', '')
# Convert DataFrame columns to numpy arrays for faster processing
postcode_array = postcodes['postcode'].values
latitude_array = postcodes['latitude'].values
longitude_array = postcodes['longitude'].values

# Create a dictionary to store postcode coordinates 
postcode_coord_dict = dict(zip(postcode_array, zip(latitude_array, longitude_array)))

# Read in the airports csv file
airports = pd.read_csv("data/GBairports.csv")
# Convert DataFrame columns to numpy arrays for faster processing
airport_name_array = airports['Unnamed: 0'].values
airport_latitude_array = airports['Latitude'].values
airport_longitude_array = airports['Longitude'].values

# Create a dictionary to store airport coordinates
airport_coord_dict = dict(zip(airport_name_array, zip(airport_latitude_array, airport_longitude_array)))

"""=========================================Main Functions============================================================"""
def calculate_distances(coords1, coords2_array):
    """Calculate distances between two coordinates and an array of coordinates."""
    distances = []
    # For single postcode coordinates in array of coordinates
    for coords2 in coords2_array:
        # If any of the two are nan
        if np.isnan(coords2).any() or np.isnan(coords1).any():
            distances.append(np.nan)
        else:
            # Find distance in km
            distances.append(geodesic(coords1, coords2).km)
    return np.array(distances)

def closest_airport(postcode, postcode_coords, airports_dict):
    """Returns the closest airport to the postcode"""
    if postcode in postcode_coords:
        # calculate distances in km
        distances = calculate_distances(postcode_coords[postcode], np.array(list(airports_dict.values())))
        # Find the airport with shortest distance to postcode
        closest_idx = np.argmin(distances)
        # Return the airport name and distance of the closest airport
        return list(airports_dict.keys())[closest_idx], distances[closest_idx]
    else:
        # If the postcode is invalid, return Aberdeen airport as the closest with distance 0
        return 'Aberdeen', 0

def travel(postcode_coords, airports_dict):
    """Returns a dictionary with postcodes as keys and closest airports as values"""
    # Dictionary to store postcode as key and closest airport, distance to it, and flying distance to Aberdeen as values
    data = {}

    # For postcode in column 2 of address file
    for postcode in addresses.iloc[:, 1]:
        # Find the closest airport to the postcode
        closest_airport_name, distance = closest_airport(postcode, postcode_coords, airports_dict)
        
        # If the closest airport is not Aberdeen (default value for nan postcodes) and the postcode is not from Scotland or London
        if closest_airport_name != 'Aberdeen' and postcode[:2] not in scot_postcodes and postcode[:2] not in london_postcodes:
            # Calculate the distance between the two airports
            travel_distance1 = geodesic(airports_dict[closest_airport_name], gatwick_airport).km
            # Calculate the distance 2: between Gatwick (layover) and Aberdeen airport
            travel_distance2 = geodesic(gatwick_airport, aberdeen_airport).km
            travel_distance = travel_distance1 + travel_distance2

        # If the closest airport is not Aberdeen (default value for nan postcodes) and the postcode is from Scotland or London
        elif closest_airport_name != 'Aberdeen' and postcode[:2] in scot_postcodes or postcode[:2] in london_postcodes:
            # Calculate the distance 1: between closest airport and Gatwick (layover)
            travel_distance = geodesic(airports_dict[closest_airport_name], aberdeen_airport).km

        else:
            # For default value, set the distance to 0
            travel_distance = 0
        data[postcode] = (closest_airport_name, round(distance, 2), round(travel_distance, 2))
    
    # Print the distance between the Aberdeen airport and the university
    uni_airport_distance = geodesic(aberdeen_airport, aberdeen_uni).km
    data['Airport to University'] = round(uni_airport_distance, 2)

    return data


"""=========================================Execute============================================================"""
info = travel(postcode_coord_dict, airport_coord_dict)
# - 1 because the last entry is the distance between Aberdeen Airport and Univerity
# print(len(info) - 1)
