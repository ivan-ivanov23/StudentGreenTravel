import pandas as pd
import numpy as np
from geopy.distance import geodesic

# Constant locations and their coordinates
aberdeen_uni = (-2.0999, 57.1645)
scot_postcodes = ['AB', 'DD', 'DG', 'EH', 'FK', 'G', 'HS', 'IV', 'KA', 'KW', 'KY', 'ML', 'PA', 'PH', 'TD', 'ZE']
london_postcodes = ['E', 'EW', 'EC', 'N', 'NW', 'SE', 'SW', 'W', 'WC', 'EN', 'HA', 'IG', 'KT', 'TW', 'UB', 'WD']
aberdeen_bus_stop = (-2.095330457035445, 57.14450856576696)
aberdeen_airport = (57.2019004822, -2.1977798939)
gatwick_airport = (51.15380339080233, -0.18165520746018157)
aberdeen_rail_station = (-2.0983252205325833, 57.14372498503623)

# Read ukpostcodes.csv
# Source: https://www.statology.org/pandas-read_csv-usecols/ 
ukpostcodes = pd.read_csv('data/ukpostcodes.csv', usecols=['postcode', 'latitude', 'longitude'])
ukpostcodes['postcode'] = ukpostcodes['postcode'].str.replace(' ', '')
ukpostcode_coords = dict(zip(ukpostcodes['postcode'], zip(ukpostcodes['latitude'], ukpostcodes['longitude'])))

# Read Scotland_Bus_Stations.csv
bus_stops = pd.read_csv("data/Scotland_Bus_Stations.csv", usecols=['StationName', 'Latitude', 'Longitude'])
stops_dict = dict(zip(bus_stops['StationName'], zip(bus_stops['Latitude'], bus_stops['Longitude'])))

# Read Railway Stations
rail_stations = pd.read_csv("data/stations.csv", usecols=['Station', 'Lat', 'Long'])
stations_dict = dict(zip(rail_stations['Station'], zip(rail_stations['Lat'], rail_stations['Long'])))

# Read airports
airports = pd.read_csv("data/GBairports.csv", usecols=['Unnamed: 0', 'Latitude', 'Longitude'])
airports_dict = dict(zip(airports['Unnamed: 0'], zip(airports['Latitude'], airports['Longitude'])))

class Travel:
    
    def __init__(self):
        # Student postcodes
        self.postcodes = None
        # Stops, stations or airports with coordinates
        self.stops = bus_stops
        self.stations = rail_stations
        self.airports = airports
        # UK postcodes with coordinates
        self.ukpostcodes = ukpostcodes


    def calculate_distances(self, coords1, coords2_array):
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
    
    # Takes a postcode, a dictionary of UK postcodes and their coordinates, and a dictionary of stops and their coordinates
    def closest_hub(self, postcode: str, postcodes: dict, stops_wcoords: dict):
        """Returns the closest transport hub to the postcode"""
        if 'AB' not in postcode:
            # Calculate the distance between the given postcode and bus stops
            distances = self.calculate_distances((postcodes[postcode][0], postcodes[postcode][1]), np.array(list(stops_wcoords.values())))
            # Find the index of the closest bus stop
            closest_idx = np.nanargmin(distances)
            # Find the name of the closest bus stop
            closest_hub_name = list(stops_wcoords.keys())[closest_idx]
            # Return the name of the closest bus stop and the distance to it
            return closest_hub_name, distances[closest_idx]
        else:
            return 'Aberdeen', 0
        

    def air_travel(self, postcodes: dict, airports: dict, addresses: list):
        """Returns a dictionary with postcodes as keys and closest airports as values"""
        # Dictionary to store postcode as key and closest airport, distance to it, and flying distance to Aberdeen as values
        data = {}
        # List to store invalid postcodes
        invalid_postcodes = []

        # For postcode in addresses
        for postcode in addresses:
        # Find the closest airport to the postcode
            closest_airport_name, distance = self.closest_hub(postcode, postcodes, airports)
            
            # If the closest airport is not Aberdeen (default value for nan postcodes) and the postcode is not from Scotland or London
            if closest_airport_name != 'Aberdeen' and postcode[:2] not in london_postcodes:
                # Calculate the distance between the two airports
                travel_distance1 = geodesic(airports[closest_airport_name], gatwick_airport).km
                # Calculate the distance 2: between Gatwick (layover) and Aberdeen airport
                travel_distance2 = geodesic(gatwick_airport, aberdeen_airport).km
                travel_distance = travel_distance1 + travel_distance2

            # If the closest airport is not Aberdeen (default value for nan postcodes) and the postcode is from Scotland or London
            elif closest_airport_name != 'Aberdeen' and  postcode[:2] in london_postcodes:
                # Calculate the distance 1: between closest airport and Gatwick (layover)
                travel_distance = geodesic(airports[closest_airport_name], aberdeen_airport).km

            else:
                # If the postcode is invalid, add it to the list of invalid postcodes
                invalid_postcodes.append(postcode)
                continue
            data[postcode] = (closest_airport_name, round(distance, 2), round(travel_distance, 2))


        return data, invalid_postcodes
    
    def land_travel(self, potcodes: dict, stops: dict, addresses: list):
        """Returns a dictionary with postcodes as keys and closest airports as values"""
        # Dictionary to store postcode as key and closest stop, distance to it, and driving distance to Aberdeen as values
        data = {}
        # List to store invalid postcodes
        invalid_postcodes = []

        # For postcode in column 2 of address file
        for postcode in addresses:
            # Find the closest bus stop to the given postcode and the distance to it
            if postcode in potcodes:
                closest_stop_name, distance = self.closest_hub(postcode, potcodes, stops)
                
                # If the closest stop is not Aberdeen, calculate the distance to it
                if closest_stop_name != 'Aberdeen':
                    # Calculate the distance between the two stops
                    travel_distance = geodesic((potcodes[postcode][1], potcodes[postcode][0]), aberdeen_bus_stop).km
        
                else:
                    # For default value, set the distance to 0
                    travel_distance = 0
                data[postcode] = (closest_stop_name, round(distance, 2), round(travel_distance, 2))
            else:
                # If the postcode is invalid, add it to the list of invalid postcodes
                invalid_postcodes.append(postcode)
                continue
            

        return data, invalid_postcodes

    def car_travel(self, postcode_coords: dict, addresses: list):
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
            
    
    
    

# # Create an instance of the Travel class
# travel = Travel()

# # Read the addresses from the file
# addresses = pd.read_excel('data/Test.xlsx', engine='openpyxl')
# # Trim the postcode column
# addresses.iloc[:, 1] = addresses.iloc[:, 1].str.replace(' ', '')
# # Drop NaN values
# addresses = addresses.dropna()

# # Call the closest_hub method to find the closest bus stop to the postcode
# closest_stop = travel.closest_hub('G775AE', ukpostcode_coords, airports_dict)
# print(closest_stop)

# # Call the car_travel method to find the distance between the given postcode and the university
# car_distance = travel.car_travel(ukpostcode_coords, addresses.iloc[:, 1])
# print(car_distance)