import pandas as pd
import numpy as np
from geopy.distance import geodesic

# Coordinates of Aberdeen airport and university (taken from Google)
aberdeen_airport = (57.2019004822, -2.1977798939)
aberdeen_uni = (57.1645, -2.0999)

# Read address file
addresses = pd.read_excel('data/UK & Home Student Data 2022-2023.xlsx', engine='openpyxl')
# Drop any rows with missing values
addresses = addresses.dropna()
# Trim the postcode column
addresses['Home_Postcode'] = addresses['Home_Postcode'].str.replace(' ', '')


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

def calculate_distances(coords1, coords2_array):
    """Calculate distances between two coordinates and an array of coordinates."""
    # If the coordinates are not in the postcode dictionary, give them a default value of 999999
    return np.array([geodesic(coords1, coords2).km for coords2 in coords2_array])

def closest_airport(postcode, postcode_coords, airports_dict):
    """Returns the closest airport to the postcode"""
    distances = calculate_distances(postcode_coords[postcode], np.array(list(airports_dict.values())))
    closest_idx = np.argmin(distances)
    return list(airports_dict.keys())[closest_idx], distances[closest_idx]

def travel(postcode_coords, airports_dict):
    """Returns a dictionary with postcodes as keys and closest airports as values"""
    for postcode in addresses['Home_Postcode']:
        closest_airport_name, distance = closest_airport(postcode, postcode_coords, airports_dict)
        print(f'Closest airport to {postcode} is {closest_airport_name} ~ {distance:.2f} km')
        
        # Calculate the distance between the two airports
        travel_distance = geodesic(airports_dict[closest_airport_name], aberdeen_airport).km
        print(f'The distance between {closest_airport_name} and Aberdeen airport is {travel_distance:.2f} km')
        print('====================================================================================================')
    
    # Print the distance between the Aberdeen airport and the university
    uni_airport_distance = geodesic(aberdeen_airport, aberdeen_uni).km
    print(f'The distance between Aberdeen airport and the university is {uni_airport_distance:.2f} km')

# Execute
travel(postcode_coord_dict, airport_coord_dict)
