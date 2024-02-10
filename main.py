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
bus_scotland, car_scotland, rail_scotland, car_uk, rail_uk, plane_uk = menu(scotland, wales, north_ireland, england)

# Call the rail_travel function to get the closest stop to each postcode
scotland_rail_data = rail_travel(postcode_coords, station_coords, rail_scotland)[0]

uk_rail_data = rail_travel(postcode_coords, station_coords, rail_uk)[0]


# Call bus_travel function to get the closest stop to each postcode
scotland_bus_data = bus_travel(postcode_coord_dict, stop_coord_dict, bus_scotland)[0]

# Call travel function to get the closest airport to each postcode for the rest of the UK
uk_flying_data = travel(postcode_coord_dict, airport_coord_dict, plane_uk)[0]

# Call car_travel function to get the distance to the university for each postcode
scotland_car_data = car_travel(all_postcodes, car_scotland)[0]
uk_car_data = car_travel(all_postcodes, car_uk)[0]

total_distance_rail_scotland = 0
total_distance_rail_uk = 0
total_distance_bus_scotland = 0
total_distance_car_scotland = 0
total_distance_car_uk = 0
total_distance_plane_uk = 0

# Extract distances from the dictionaries and convert them to numpy arrays (THESE ARE ONLY DISTANCES BETWEEN THE POSTCODES AND THE STOPS/STATIONS/AIRPORTS)
"""NEED TO THINK ABOUT FIRST AND FINAL LEG OF JOURNEY, AND HOW TO CALCULATE THAT"""
rail_scotland_distances = np.array([value[2] for value in scotland_rail_data.values()])
rail_uk_distances = np.array([value[2] for value in uk_rail_data.values()])
bus_scotland_distances = np.array([value[2] for value in scotland_bus_data.values()])
car_scotland_distances = np.array([value for value in scotland_car_data.values()])
car_uk_distances = np.array([value for value in uk_car_data.values()])
plane_uk_distances = np.array([value[2] for value in uk_flying_data.values()])

# Calculate total distances using numpy's sum function
total_distance_rail_scotland = np.sum(rail_scotland_distances)
total_distance_rail_uk = np.sum(rail_uk_distances)
total_distance_bus_scotland = np.sum(bus_scotland_distances)
total_distance_car_scotland = np.sum(car_scotland_distances)
total_distance_car_uk = np.sum(car_uk_distances)
total_distance_plane_uk = np.sum(plane_uk_distances)

# Create a dataframe to store the total distances
total_distances = pd.DataFrame({'Scotland': [total_distance_rail_scotland, total_distance_bus_scotland, total_distance_car_scotland, 0],
                                'Rest of UK': [total_distance_rail_uk, 0, total_distance_car_uk, total_distance_plane_uk]},
                                index=['Rail', 'Bus', 'Car', 'Plane'])

# Create a heatmap to visualise the total distances
sns.heatmap(total_distances, annot=True, fmt='g', cmap='coolwarm')
plt.title('Total distances travelled by students')
plt.show()





