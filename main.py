import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from split_postcodes import determine_postcode, menu
from rail_distance import postcode_coords, station_coords, rail_travel
from bus_distance import bus_travel, stop_coord_dict, postcode_coord_dict
from car_distance import car_travel, all_postcodes
from flying_distance import travel, airport_coord_dict, postcode_coord_dict

# Divide postcodes into Scottish and rest-of-UK postcodes
scotland, wales, north_ireland, england = determine_postcode()
# Split postcodes into travel methods according to user input
transport_scot, transport_eng, transport_wales, transport_ni = menu(scotland, wales, north_ireland, england)

rail_scotland = transport_scot[2]
bus_scotland = transport_scot[0]
car_scotland = transport_scot[1]

rail_eng = transport_eng[2]
car_eng = transport_eng[1]
plane_eng = transport_eng[0]

rail_wales = transport_wales[2]
car_wales = transport_wales[1]
plane_wales = transport_wales[0]

rail_ni = transport_ni[2]
car_ni = transport_ni[1]
plane_ni = transport_ni[0]


# Call the rail_travel function to get the closest stop to each postcode
scotland_rail_data = rail_travel(postcode_coords, station_coords, rail_scotland)[0]
#print(scotland_rail_data)

eng_rail_data = rail_travel(postcode_coords, station_coords, rail_eng)[0]
# print(eng_rail_data)
wales_rail_data = rail_travel(postcode_coords, station_coords, rail_wales)[0]
ni_rail_data = rail_travel(postcode_coords, station_coords, rail_ni)[0]


# Call bus_travel function to get the closest stop to each postcode
scotland_bus_data = bus_travel(postcode_coord_dict, stop_coord_dict, bus_scotland)[0]

# Call travel function to get the closest airport to each postcode for the rest of the UK
eng_flying_data = travel(postcode_coord_dict, airport_coord_dict, plane_eng)[0]
wales_flying_data = travel(postcode_coord_dict, airport_coord_dict, plane_wales)[0]
ni_flying_data = travel(postcode_coord_dict, airport_coord_dict, plane_ni)[0]

# Call car_travel function to get the distance to the university for each postcode
scotland_car_data = car_travel(all_postcodes, car_scotland)[0]
eng_car_data = car_travel(all_postcodes, car_eng)[0]
wales_car_data = car_travel(all_postcodes, car_wales)[0]
ni_car_data = car_travel(all_postcodes, car_ni)[0]

total_distance_rail_scotland = 0
total_distance_rail_eng = 0
total_distance_rail_wales = 0
total_distance_rail_ni = 0
total_distance_bus_scotland = 0
total_distance_car_scotland = 0
total_distance_car_eng = 0
total_distance_car_wales = 0
total_distance_car_ni = 0
total_distance_plane_eng = 0
total_distance_plane_wales = 0
total_distance_plane_ni = 0

# Extract distances from the dictionaries and convert them to numpy arrays (THESE ARE ONLY DISTANCES BETWEEN THE POSTCODES AND THE STOPS/STATIONS/AIRPORTS)
"""NEED TO THINK ABOUT FIRST AND FINAL LEG OF JOURNEY, AND HOW TO CALCULATE THAT"""
"""NEED TO MODIFY split_postcodes.py TO DIVIDE UK INTRO ENGLAND, WALES, AND NORTHERN IRELAND"""
rail_scotland_distances = np.array([value[2] for value in scotland_rail_data.values()])
rail_eng_distances = np.array([value[2] for value in eng_rail_data.values()])
rail_wales_distances = np.array([value[2] for value in wales_rail_data.values()])
rail_ni_distances = np.array([value[2] for value in ni_rail_data.values()])
bus_scotland_distances = np.array([value[2] for value in scotland_bus_data.values()])
car_scotland_distances = np.array([value for value in scotland_car_data.values()])
car_eng_distances = np.array([value for value in eng_car_data.values()])
car_wales_distances = np.array([value for value in wales_car_data.values()])
car_ni_distances = np.array([value for value in ni_car_data.values()])
plane_eng_distances = np.array([value[2] for value in eng_flying_data.values()])
plane_wales_distances = np.array([value[2] for value in wales_flying_data.values()])
plane_ni_distances = np.array([value[2] for value in ni_flying_data.values()])

# Calculate total distances using numpy's sum function
total_distance_rail_scotland = np.sum(rail_scotland_distances)
total_distance_rail_eng = np.sum(rail_eng_distances)
total_distance_rail_wales = np.sum(rail_wales_distances)
total_distance_rail_ni = np.sum(rail_ni_distances)
total_distance_bus_scotland = np.sum(bus_scotland_distances)
total_distance_car_scotland = np.sum(car_scotland_distances)
total_distance_car_eng = np.sum(car_eng_distances)
total_distance_car_wales = np.sum(car_wales_distances)
total_distance_car_ni = np.sum(car_ni_distances)
total_distance_plane_eng = np.sum(plane_eng_distances)
total_distance_plane_wales = np.sum(plane_wales_distances)
total_distance_plane_ni = np.sum(plane_ni_distances)

# Create a dataframe to store the total distances
total_distances = pd.DataFrame({'Scotland': [total_distance_rail_scotland, total_distance_bus_scotland, total_distance_car_scotland, 0],
                                'England': [total_distance_rail_eng, 0, total_distance_car_eng, total_distance_plane_eng],
                                'Wales': [total_distance_rail_wales, 0, total_distance_car_wales, total_distance_plane_wales],
                                'Northern Ireland': [total_distance_rail_ni, 0, total_distance_car_ni, total_distance_plane_ni]},
                                index=['Rail', 'Bus', 'Car', 'Plane'])

# Create a heatmap to visualise the total distances
sns.heatmap(total_distances, annot=True, fmt='g', cmap='coolwarm')
plt.title('Total distances travelled by students')
plt.show()





