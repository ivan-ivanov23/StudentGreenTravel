# Travel class for the travel distances and closest transport hubs for each mode of transport and each student's postcode
# Author: Ivan Ivanov

import numpy as np
from geopy.distance import geodesic
import sqlite3
import requests

# Constant locations and their coordinates
aberdeen_uni = (57.1645, -2.0999)
aberdeen_bus_stop = (57.14450856576696, -2.095330457035445)
aberdeen_airport = (57.2019004822, -2.1977798939)
gatwick_airport = (51.15380339080233, -0.18165520746018157)
aberdeen_rail_station = (57.14372498503623, -2.0983252205325833)

# London postcodes are used to determine if a postcode is in London
london_postcodes = ['E', 'EW', 'EC', 'N', 'NW', 'SE', 'SW', 'W', 'WC', 'EN', 'HA', 'IG', 'KT', 'TW', 'UB', 'WD']

class Travel:
    
    def __init__(self, bus_stops, rail_stations, airports):
        # Student postcodes
        self.postcodes = None
        # Stops, stations or airports with coordinates
        self.stops = bus_stops
        self.stations = rail_stations
        self.airports = airports


    def calculate_distances(self, coords1, coords2_array):
        """Calculate distances between two coordinates and an array of coordinates."""
        distances = []
        # For single postcode coordinates in array of coordinates
        for coords2 in coords2_array:
            if np.isnan(coords2).any():
                continue
            # Find distance in km
            longitude = coords1[0]
            latitude = coords1[1]
            distances.append(geodesic((longitude, latitude), (coords2[1], coords2[0])).km)
        return np.array(distances)
    
    # Takes a postcode, a dictionary of UK postcodes and their coordinates, and a dictionary of stops and their coordinates
    def closest_hub(self,postcode: str, postcode_fetch: dict, stops_wcoords: dict):
        """Returns the closest transport hub to the postcode"""
        # Calculate the distance between the given postcode and bus stops
        longitude = postcode_fetch[0]
        latitude = postcode_fetch[1]
        distances = self.calculate_distances([longitude, latitude], np.array(list(stops_wcoords.values())))
        # Find the index of the closest bus stop
        closest_idx = np.nanargmin(distances)
        # Find the name of the closest bus stop
        closest_hub_name = list(stops_wcoords.keys())[closest_idx]
        # Return the name of the closest bus stop and the distance to it
        return closest_hub_name, distances[closest_idx]
    
    def find_coordinates(self, postcode):
        """Finds the coordinates for postcodes that are not in database"""
        response = requests.get(f'https://api.postcodes.io/postcodes/{postcode}')
        if response.status_code == 200:
            response_json = response.json()
            if response_json["result"] is None:
                return 0, 0
            else:
                return response_json["result"]["longitude"], response_json["result"]["latitude"]
        else:
            return 0, 0
            
    def air_travel(self, airports: dict, addresses: list):
        """Returns a dictionary with postcodes as keys and closest airports as values"""
        
        data = {}
        invalid_postcodes = []
        # Connect to database
        conn = sqlite3.connect('data/postcodes.db')
        cursor = conn.cursor()

        # For postcode in addresses
        for postcode in addresses:
            cursor.execute("SELECT latitude, longitude FROM postcodes WHERE postcode = ?", (postcode,))
            postcode_coords = cursor.fetchone()
            if postcode_coords is None:
                longitude, latitude = self.find_coordinates(postcode)
                if (longitude, latitude) == (0, 0):
                    invalid_postcodes.append(postcode)
                    continue
            else:
                longitude = postcode_coords[1]
                latitude = postcode_coords[0]
            
            # Find the closest airport to the postcode and distance to it
            closest_airport_name, distance_to = self.closest_hub(postcode, [longitude, latitude], airports)

            # if the postcode is not in London
            if postcode[:2] not in london_postcodes:
                # Calculate the distance between Gatwick (layover) and Aberdeen airport
                travel_distance1 = geodesic(airports[closest_airport_name], gatwick_airport).km
                gatwick_aberdeen = 685.68
                travel_distance = travel_distance1 + gatwick_aberdeen
            
            elif postcode[:2] in london_postcodes:
                # Calculate the distance between closest airport and Aberdeen airport
                travel_distance = geodesic(airports[closest_airport_name], aberdeen_airport).km

            else:
                invalid_postcodes.append(postcode)
                continue

            data[postcode] = (closest_airport_name, distance_to,travel_distance)

        conn.close()

        return data, invalid_postcodes
    

    def land_travel(self, stops: dict, addresses: list, aberdeen_hub: tuple):
        """Returns a dictionary with postcodes as keys and closest airports as values"""
        
        data = {}
        invalid_postcodes = []

        conn = sqlite3.connect('data/postcodes.db')
        cursor = conn.cursor()

        # For postcode in column 2 of address file
        for postcode in addresses:
            cursor.execute("SELECT longitude, latitude FROM postcodes WHERE postcode = ?", (postcode,))
            postcode_coords = cursor.fetchone()
            if postcode_coords is None:
                longitude, latitude = self.find_coordinates(postcode)
                if (longitude, latitude) == (0, 0):
                    invalid_postcodes.append(postcode)
                    continue

                
            else:
                longitude = postcode_coords[1]
                latitude = postcode_coords[0]
                

            closest_stop_name, distance_to = self.closest_hub(postcode, [latitude, longitude], stops)

            # If the closest stop is not Aberdeen, calculate the distance to it
            if closest_stop_name != 'Aberdeen':
                travel_distance = geodesic(stops[closest_stop_name], aberdeen_hub).km
            
            elif closest_stop_name == 'Aberdeen':
                # Calculate the distance to the university
                travel_distance = geodesic(aberdeen_hub, aberdeen_uni).km

            else:
                invalid_postcodes.append(postcode)
                continue
            
            data[postcode] = (closest_stop_name, distance_to, travel_distance)

        conn.close()

        return data, invalid_postcodes
    
    def car_travel(self, addresses: list):
        # Dictionary to store postcode and distance to the university
        car_data = {}
        # List to store invalid postcodes
        invalid_postcodes = []

        conn = sqlite3.connect('data/postcodes.db')
        cursor = conn.cursor()

        # For postcode in column 2 of address file
        for postcode in addresses:
            cursor.execute("SELECT latitude, longitude FROM postcodes WHERE postcode = ?", (postcode,))
            postcode_coords = cursor.fetchone()
            if postcode_coords is None:
                longitude, latitude = self.find_coordinates(postcode)
                if (longitude, latitude) == (0, 0):
                    invalid_postcodes.append(postcode)
                    continue
            else:
                longitude = postcode_coords[1]
                latitude = postcode_coords[0]

            # Find the distance between the given postcode and the university
            distance = geodesic((latitude, longitude), aberdeen_uni).km
            car_data[postcode] = distance
        
        # Close the connection
        conn.close()

        return car_data, invalid_postcodes
    

#Test the air_travel method
# travel = Travel(aberdeen_bus_stop, aberdeen_rail_station, aberdeen_airport)

# # Read Test.xlsx
# import pandas as pd
# from preprocess_data import airports_dict, stops_dict, stations_dict, determine_postcode
# postcodes = pd.read_excel('datasets/Test.xlsx', usecols=[1])
# postcodes = postcodes.dropna()
# # drop float values
# postcodes = postcodes[postcodes.iloc[:, 0].apply(lambda x: isinstance(x, str))]
# postcodes = postcodes.iloc[:, 0]#.tolist()

# scotland, wales, north_ireland, england, aberdeen, new_invalid = determine_postcode(postcodes)

# #Test the air_travel method
# airports, invalid = travel.air_travel(airports_dict, england)
# print(f"airports: {airports}")
# print("===========================================================================================================================")
# print(f"invalid: {invalid}")

# Test the land_travel method
# stops, invalid = travel.land_travel(stations_dict, scotland, aberdeen_rail_station)
# print(f"stops: {stops}")
# print("===========================================================================================================================")
# print(f"invalid: {invalid}")

# Test the car_travel method	
# car, invalid = travel.car_travel(scotland)
# print(f"car: {car}")
# print("===========================================================================================================================")
# print(f"invalid: {invalid}")
