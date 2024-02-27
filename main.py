import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import islice
from travel_class import Travel
from preprocess_data import ukpostcode_coords, stops_dict, stations_dict, airports_dict

def main(transport_scot, transport_eng, transport_wales, transport_ni, scot_bus_fleg, scot_car_fleg, scot_taxi_fleg, scot_walk_fleg, eng_car_fleg, eng_taxi_fleg, eng_bus_fleg, eng_walk_fleg, wales_car_fleg, wales_taxi_fleg, wales_bus_fleg, wales_walk_fleg, ni_car_fleg, ni_taxi_fleg, ni_bus_fleg, ni_walk_fleg):
    travel = Travel(stops_dict, stations_dict, airports_dict, ukpostcode_coords)

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

    # Call the land_travel function to get the train travel distances for each postcode
    scotland_rail_data = travel.land_travel(ukpostcode_coords, stations_dict, rail_scotland)[0]
   
    eng_rail_data = travel.land_travel(ukpostcode_coords, stations_dict, rail_eng)[0]
    wales_rail_data = travel.land_travel(ukpostcode_coords, stations_dict, rail_wales)[0]
    ni_rail_data = travel.land_travel(ukpostcode_coords, stations_dict, rail_ni)[0]


    # Call the land_travel function to get the bus travel distances for each postcode
    scotland_bus_data = travel.land_travel(ukpostcode_coords, stops_dict, bus_scotland)[0]

    # Call air_travel function to get the distance to Aberdeen airport for each postcode
    eng_flying_data = travel.air_travel(ukpostcode_coords, airports_dict, plane_eng)[0]
    wales_flying_data = travel.air_travel(ukpostcode_coords, airports_dict, plane_wales)[0]
    ni_flying_data = travel.air_travel(ukpostcode_coords, airports_dict, plane_ni)[0]

    # Call car_travel function to get the distance to the university for each postcode
    scotland_car_data = travel.car_travel(ukpostcode_coords, car_scotland)[0]
    eng_car_data = travel.car_travel(ukpostcode_coords, car_eng)[0]
    wales_car_data = travel.car_travel(ukpostcode_coords, car_wales)[0]
    ni_car_data = travel.car_travel(ukpostcode_coords, car_ni)[0]

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
    total_distance_rail_scotland, total_distance_rail_eng, total_distance_rail_wales, total_distance_rail_ni = 0, 0, 0, 0
    total_distance_bus_scotland = 0
    total_distance_car_scotland, total_distance_car_eng, total_distance_car_wales, total_distance_car_ni = 0, 0, 0, 0
    total_distance_plane_eng, total_distance_plane_wales, total_distance_plane_ni = 0, 0, 0

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
    total_distance_bus_scotland = np.sum(bus_scotland_distances) + total_bus1 + scot_bus_fleg
    total_distance_car_scotland = np.sum(car_scotland_distances) + total_car1 + scot_car_fleg
    total_distance_car_eng = np.sum(car_eng_distances) + total_car2 + eng_car_fleg
    total_distance_car_wales = np.sum(car_wales_distances) + total_car3 + wales_car_fleg
    total_distance_car_ni = np.sum(car_ni_distances) + total_car4 + ni_car_fleg
    total_distance_plane_eng = np.sum(plane_eng_distances)
    total_distance_plane_wales = np.sum(plane_wales_distances)
    total_distance_plane_ni = np.sum(plane_ni_distances)
    # Add taxi, bus where necessary
    total_distance_taxi_scotland = total_taxi1 + scot_taxi_fleg
    total_distance_taxi_eng = total_taxi2 + eng_taxi_fleg
    total_distance_bus_eng = total_bus2 + eng_bus_fleg
    total_distance_taxi_wales = total_taxi3 + wales_taxi_fleg
    total_distance_bus_wales = total_bus3 + wales_bus_fleg
    total_distance_taxi_ni = total_taxi4 + ni_taxi_fleg
    total_distance_bus_ni = total_bus4 + ni_bus_fleg
    total_walk_scotland = scot_walk_fleg
    total_walk_eng = eng_walk_fleg
    total_walk_wales = wales_walk_fleg
    total_walk_ni = ni_walk_fleg

    """=================================Visualisation==================================""" 

    # # Create a dataframe to store the total distances
    # total_distances = pd.DataFrame({'Scotland': [total_distance_rail_scotland, 0, total_distance_bus_scotland, total_distance_car_scotland, total_distance_taxi_scotland, total_walk_scotland],
    #                                 'England': [total_distance_rail_eng, total_distance_plane_eng,  total_distance_bus_eng, total_distance_car_eng, total_distance_taxi_eng, total_walk_eng],
    #                                 'Wales': [total_distance_rail_wales, total_distance_plane_wales,  total_distance_bus_wales, total_distance_car_wales, total_distance_taxi_wales, total_walk_wales],
    #                                 'Northern Ireland': [total_distance_rail_ni, total_distance_plane_ni,  total_distance_bus_ni, total_distance_car_ni, total_distance_taxi_ni, total_walk_ni]},
    #                                 index=['Rail', 'Plane', 'Bus', 'Car', 'Taxi', 'Walk'])

    # # Create a heatmap to visualise the total distances with reversed green to red colour scheme
    # sns.heatmap(total_distances, annot=True, fmt='g', cmap='YlOrRd', cbar_kws={'label': 'Total distance (km)'})
    # plt.title('Total distances travelled by students')
    # # Save the heatmap as a .png file
    # plt.savefig('distances_heatmap.png')

    """=================================Emissions=================================="""

    emission_factors = {'car': 0.18264,  'rail': 0.035463, 'bus': 0.118363, 'coach': 0.027181, 'taxi': 0.148615,
           'ferry': 0.02555, 'plane': 0.03350}
    
    # Calculate the emissions for each mode of transport
    # Emissions = distance * emission factor
    # Emissions are in kgCO2e
    rail_emissions_scotland = total_distance_rail_scotland * emission_factors['rail']
    bus_emissions_scotland = total_distance_bus_scotland * emission_factors['bus']
    car_emissions_scotland = total_distance_car_scotland * emission_factors['car']
    taxi_emissions_scotland = total_distance_taxi_scotland * emission_factors['taxi']
    walk_emissions_scotland = 0
    # Total emissions
    total_emissions_scotland = rail_emissions_scotland + bus_emissions_scotland + car_emissions_scotland + taxi_emissions_scotland + walk_emissions_scotland

    rail_emissions_england = total_distance_rail_eng * emission_factors['rail']
    plane_emissions_england = total_distance_plane_eng * emission_factors['plane']
    car_emissions_england = total_distance_car_eng * emission_factors['car']
    taxi_emissions_england = total_distance_taxi_eng * emission_factors['taxi']
    bus_emissions_england = total_distance_bus_eng * emission_factors['bus']
    walk_emissions_england = 0
    # Total emissions
    total_emissions_england = rail_emissions_england + plane_emissions_england + car_emissions_england + taxi_emissions_england + walk_emissions_england

    rail_emissions_wales = total_distance_rail_wales * emission_factors['rail']
    plane_emissions_wales = total_distance_plane_wales * emission_factors['plane']
    car_emissions_wales = total_distance_car_wales * emission_factors['car']
    taxi_emissions_wales = total_distance_taxi_wales * emission_factors['taxi']
    bus_emissions_wales = total_distance_bus_wales * emission_factors['bus']
    walk_emissions_wales = 0
    # Total emissions
    total_emissions_wales = rail_emissions_wales + plane_emissions_wales + car_emissions_wales + taxi_emissions_wales + walk_emissions_wales

    rail_emissions_ni = total_distance_rail_ni * emission_factors['rail']
    plane_emissions_ni = total_distance_plane_ni * emission_factors['plane']
    car_emissions_ni = total_distance_car_ni * emission_factors['car']
    taxi_emissions_ni = total_distance_taxi_ni * emission_factors['taxi']
    bus_emissions_ni = total_distance_bus_ni * emission_factors['bus']
    walk_emissions_ni = 0

    # Total emissions
    total_emissions_ni = rail_emissions_ni + plane_emissions_ni + car_emissions_ni + taxi_emissions_ni + walk_emissions_ni

    # Create a dataframe to store the separate emissions
    total_emissions = pd.DataFrame({'Scotland': [rail_emissions_scotland, 0, bus_emissions_scotland, car_emissions_scotland, taxi_emissions_scotland, walk_emissions_scotland],
                                    'England': [rail_emissions_england, plane_emissions_england, bus_emissions_england, car_emissions_england, taxi_emissions_england, walk_emissions_england],
                                    'Wales': [rail_emissions_wales, plane_emissions_wales, bus_emissions_wales, car_emissions_wales, taxi_emissions_wales, walk_emissions_wales],
                                    'Northern Ireland': [rail_emissions_ni, plane_emissions_ni, bus_emissions_ni, car_emissions_ni, taxi_emissions_ni, walk_emissions_ni]},
                                    index=['Rail', 'Plane', 'Bus', 'Car', 'Taxi', 'Walk'])
    
    # Create a heatmap to visualise the total emissions with reversed green to red colour scheme
    sns.heatmap(total_emissions, annot=True, fmt='g', cmap='YlOrRd', cbar_kws={'label': 'Total emissions (kgCO2e)'})
    plt.title('Total emissions from student travel')
    # Save the heatmap as a .png file
    plt.savefig('emissions_heatmap.png')

    # Dataframe to store the total emissions
    total_emissions = pd.DataFrame({'Scotland': [total_emissions_scotland],
                                    'England': [total_emissions_england],
                                    'Wales': [total_emissions_wales],
                                    'Northern Ireland': [total_emissions_ni]},
                                    index=['Country'])
    
    # Create a bar chart to visualise the total emissions
    total_emissions.plot(kind='bar')
    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=0)
    plt.ylabel('Total emissions (kgCO2e)')
    plt.title('Total emissions from student travel')
    # Save the bar chart as a .png file
    plt.savefig('emissions_bar_chart.png')




if __name__ == '__main__':
    main()
    