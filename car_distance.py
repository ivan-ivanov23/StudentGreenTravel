import pandas as pd
import numpy as np
from geopy.distance import geodesic

# Coordinates of Aberdeen airport and university (taken from Google)
aberdeen_uni = (-2.0999, 57.1645)

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
all_postcodes = dict(zip(postcode_array, zip(latitude_array, longitude_array)))

# Function to calculate distance from postcode to uni of Aberdeen
def car_travel(postcode_coords, addresses):
     # Dictionary to store postcode and distance to the university
    car_data = {}
    # List to store invalid postcodes
    invalid_postcodes = []

    # For postcode in column 2 of address file
    for postcode in addresses:
        # Find the distance between the given postcode and the university
        if postcode in postcode_coords:
            # If the postcode is not from Aberdeen, calculate the distance to the university
            if postcode[:2] != 'AB':
                distance = geodesic((postcode_coords[postcode][1], postcode_coords[postcode][0]), aberdeen_uni).km
                car_data[postcode] = round(distance, 2)

            else:
                car_data[postcode] = 0
        else:
            invalid_postcodes.append(postcode)
            continue

    return car_data, invalid_postcodes