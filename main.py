import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import islice
from split_postcodes import determine_postcode, menu
from rail_distance import postcode_coords, station_coords, rail_travel
from bus_distance import bus_travel, stop_coord_dict, postcode_coord_dict
from car_distance import car_travel, all_postcodes
from flying_distance import travel, airport_coord_dict, postcode_coord_dict

"""=================================Postcode splitting=================================="""
# Divide postcodes into Scottish and rest-of-UK postcodes
scotland, wales, north_ireland, england = determine_postcode()
# Split postcodes into travel methods according to user input
transport_scot, transport_eng, transport_wales, transport_ni = menu(scotland, wales, north_ireland, england)

"""=================================Transport methods=================================="""

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

"""=================================Distance calculations=================================="""

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

"""=================================Initial leg of journey=================================="""

# From all of these above dictionaries, extract the value[1] (the closest stop/airport) and put them in a list
# Then, use the list to extract the distances from the dictionaries and sum them to get the total distance
# travelled by each mode of transport and region
# We dont consider car distances here because the car distance is the distance from the postcode to the university and there is no initial leg of the journey
all_inital_scotland = [value[1] for value in scotland_rail_data.values()] + [value[1] for value in scotland_bus_data.values()]

init_car = 40
init_taxi = 40
init_bus = 20

init_car1 = int(len(all_inital_scotland) * (init_car / 100))
init_taxi1 = int(len(all_inital_scotland) * (init_taxi / 100))
init_bus1 = int(len(all_inital_scotland) * (init_bus / 100))

# Divide the all_initial list into 3 lists, one for each mode of transport according to the percentages without overlapping
seclist1 = [init_car1, init_taxi1, init_bus1]
it1 = iter(all_inital_scotland)
car1, taxi1, bus1 = [list(islice(it1, 0, i)) for i in seclist1]
# Add the distances in each list to get the total distance travelled by each mode of transport
total_car1 = np.sum(car1)
total_taxi1 = np.sum(taxi1)
total_bus1 = np.sum(bus1)

# England
# We dont consider car distances here because the car distance is the distance from the postcode to the university and there is no initial leg of the journey
all_inital_eng = [value[1] for value in eng_rail_data.values()] + [value[1] for value in eng_flying_data.values()]

init_car2 = int(len(all_inital_eng) * (init_car / 100))
init_taxi2 = int(len(all_inital_eng) * (init_taxi / 100))
init_bus2 = int(len(all_inital_eng) * (init_bus / 100))

seclist2 = [init_car2, init_taxi2, init_bus2]

it2 = iter(all_inital_eng)
car2, taxi2, bus2 = [list(islice(it2, 0, i)) for i in seclist2]

total_car2 = np.sum(car2)
total_taxi2 = np.sum(taxi2)
total_bus2 = np.sum(bus2)


# Wales
# We dont consider car distances here because the car distance is the distance from the postcode to the university and there is no initial leg of the journey
all_inital_wales = [value[1] for value in wales_rail_data.values()] + [value[1] for value in wales_flying_data.values()]

init_car3 = int(len(all_inital_wales) * (init_car / 100))
init_taxi3 = int(len(all_inital_wales) * (init_taxi / 100))
init_bus3 = int(len(all_inital_wales) * (init_bus / 100))

seclist3 = [init_car3, init_taxi3, init_bus3]
it3 = iter(all_inital_wales)
car3, taxi3, bus3 = [list(islice(it3, 0, i)) for i in seclist3]
total_car3 = np.sum(car3)
total_taxi3 = np.sum(taxi3)
total_bus3 = np.sum(bus3)


# Northern Ireland
# We dont consider car distances here because the car distance is the distance from the postcode to the university and there is no initial leg of the journey
all_inital_ni = [value[1] for value in ni_rail_data.values()] + [value[1] for value in ni_flying_data.values()]

init_car4 = int(len(all_inital_ni) * (init_car / 100))
init_taxi4 = int(len(all_inital_ni) * (init_taxi / 100))
init_bus4 = int(len(all_inital_ni) * (init_bus / 100))

seclist4 = [init_car4, init_taxi4, init_bus4]
it4 = iter(all_inital_ni)
car4, taxi4, bus4 = [list(islice(it4, 0, i)) for i in seclist4]
total_car4 = np.sum(car4)
total_taxi4 = np.sum(taxi4)
total_bus4 = np.sum(bus4)


"""=================================Initialize Total distances=================================="""
total_distance_rail_scotland, total_distance_rail_eng, total_distance_rail_wales, total_distance_rail_ni = 0
total_distance_bus_scotland = 0
total_distance_car_scotland, total_distance_car_eng, total_distance_car_wales, total_distance_car_ni = 0
total_distance_plane_eng, total_distance_plane_wales, total_distance_plane_ni = 0

""""=================================Converting to NumPy arrays=================================="""	

# Extract mid leg distances from the dictionaries and converts them to numpy arrays (THESE ARE ONLY DISTANCES BETWEEN THE POSTCODES AND THE STOPS/STATIONS/AIRPORTS)
"""NEED TO THINK ABOUT FIRST AND FINAL LEG OF JOURNEY, AND HOW TO CALCULATE THAT"""
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

"""=================================Summing of Total distance values from different transports=================================="""

# Calculate total distances using numpy's sum function
total_distance_rail_scotland = np.sum(rail_scotland_distances)
total_distance_rail_eng = np.sum(rail_eng_distances)
total_distance_rail_wales = np.sum(rail_wales_distances)
total_distance_rail_ni = np.sum(rail_ni_distances)
total_distance_bus_scotland = np.sum(bus_scotland_distances) + total_bus1
total_distance_car_scotland = np.sum(car_scotland_distances) + total_car1
total_distance_car_eng = np.sum(car_eng_distances) + total_car2
total_distance_car_wales = np.sum(car_wales_distances) + total_car3
total_distance_car_ni = np.sum(car_ni_distances) + total_car4
total_distance_plane_eng = np.sum(plane_eng_distances)
total_distance_plane_wales = np.sum(plane_wales_distances)
total_distance_plane_ni = np.sum(plane_ni_distances)
# Add taxi, bus where necessary
total_distance_taxi_scotland = total_taxi1
total_distance_taxi_eng = total_taxi2
total_distance_bus_eng = total_bus2
total_distance_taxi_wales = total_taxi3
total_distance_bus_wales = total_bus3
total_distance_taxi_ni = total_taxi4
total_distance_bus_ni = total_bus4

"""=================================Visualisation==================================""" 

# Create a dataframe to store the total distances
total_distances = pd.DataFrame({'Scotland': [total_distance_rail_scotland, 0, total_distance_bus_scotland, total_distance_car_scotland, total_distance_taxi_scotland],
                                'England': [total_distance_rail_eng, total_distance_plane_eng, total_distance_car_eng, total_distance_taxi_eng, total_distance_bus_eng],
                                'Wales': [total_distance_rail_wales, total_distance_plane_wales, total_distance_car_wales, total_distance_taxi_wales, total_distance_bus_wales],
                                'Northern Ireland': [total_distance_rail_ni, total_distance_plane_ni, total_distance_car_ni, total_distance_taxi_ni, total_distance_bus_ni]},
                                index=['Rail', 'Plane', 'Car', 'Taxi', 'Bus'])

# Create a heatmap to visualise the total distances with reversed green to red colour scheme
sns.heatmap(total_distances, annot=True, fmt='g', cmap='YlOrRd', cbar_kws={'label': 'Total distance (km)'})
plt.title('Total distances travelled by students')
plt.show()





