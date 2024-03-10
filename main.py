# Main function file that combines the functionality of the other files and produces the final results.
# Author: Ivan Ivanov

import pandas as pd
import numpy as np
from travel_class import Travel
from preprocess_data import ukpostcode_coords, stops_dict, stations_dict, airports_dict
from utils import extract_distances, extract_car_distances, init_leg

def main(emission_factors, transport_scot, transport_eng, transport_wales, transport_ni, scot_bus_fleg, scot_car_fleg, scot_taxi_fleg, scot_walk_fleg, eng_car_fleg, eng_taxi_fleg, eng_bus_fleg, eng_walk_fleg, wales_car_fleg, wales_taxi_fleg, wales_bus_fleg, wales_walk_fleg, ni_car_fleg, ni_taxi_fleg, ni_bus_fleg, ni_walk_fleg):
    travel = Travel(stops_dict, stations_dict, airports_dict, ukpostcode_coords)

    """=================================Transport methods=================================="""
    # Extract the lists of postcodes for each mode of transport and region
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
    invalid = []
    # Call the land_travel function to get the train travel distances for each postcode
    scotland_rail_data = travel.land_travel(ukpostcode_coords, stations_dict, rail_scotland)
    scotland_rail_invalid = scotland_rail_data[1]
    scotland_rail_data = scotland_rail_data[0]
   
    eng_rail_data = travel.land_travel(ukpostcode_coords, stations_dict, rail_eng)
    eng_rail_invalid = eng_rail_data[1]
    eng_rail_data = eng_rail_data[0]

    wales_rail_data = travel.land_travel(ukpostcode_coords, stations_dict, rail_wales)
    wales_rail_invalid = wales_rail_data[1]
    wales_rail_data = wales_rail_data[0]

    ni_rail_data = travel.land_travel(ukpostcode_coords, stations_dict, rail_ni)
    ni_rail_invalid = ni_rail_data[1]
    ni_rail_data = ni_rail_data[0]


    # Call the land_travel function to get the bus travel distances for each postcode
    scotland_bus_data = travel.land_travel(ukpostcode_coords, stops_dict, bus_scotland)
    scotland_bus_invalid = scotland_bus_data[1]
    scotland_bus_data = scotland_bus_data[0]

    # Call air_travel function to get the distance to Aberdeen airport for each postcode
    eng_flying_data = travel.air_travel(ukpostcode_coords, airports_dict, plane_eng)
    eng_flying_invalid = eng_flying_data[1]
    eng_flying_data = eng_flying_data[0]

    wales_flying_data = travel.air_travel(ukpostcode_coords, airports_dict, plane_wales)
    wales_bus_flying_invalid = wales_flying_data[1]
    wales_flying_data = wales_flying_data[0]

    ni_flying_data = travel.air_travel(ukpostcode_coords, airports_dict, plane_ni)
    ni_flying_invalid = ni_flying_data[1]
    ni_flying_data = ni_flying_data[0]

    # Call car_travel function to get the distance to the university for each postcode
    scotland_car_data = travel.car_travel(ukpostcode_coords, car_scotland)
    scotland_car_invalid = scotland_car_data[1]
    scotland_car_data = scotland_car_data[0]

    eng_car_data = travel.car_travel(ukpostcode_coords, car_eng)
    eng_car_invalid = eng_car_data[1]
    eng_car_data = eng_car_data[0]

    wales_car_data = travel.car_travel(ukpostcode_coords, car_wales)
    wales_car_invalid = wales_car_data[1]
    wales_car_data = wales_car_data[0]

    ni_car_data = travel.car_travel(ukpostcode_coords, car_ni)
    ni_car_invalid = ni_car_data[1]
    ni_car_data = ni_car_data[0]

    invalid.extend([scotland_rail_invalid, eng_rail_invalid, wales_rail_invalid, ni_rail_invalid, scotland_bus_invalid, 
                   eng_flying_invalid, wales_bus_flying_invalid, ni_flying_invalid, scotland_car_invalid, eng_car_invalid,
                    wales_car_invalid, ni_car_invalid])

    """=================================Initial leg of journey=================================="""

    """ From all of these above dictionaries, extract the value[1] (the closest stop/airport) and put them in a list
    Then, use the list to extract the distances from the dictionaries and sum them to get the total distance
    travelled by each mode of transport and region.We dont consider car distances here because the car distance 
    is the distance from the postcode to the university and there is no initial leg of the journey. """

    # Scotland
    all_inital_scotland = [value[1] for value in scotland_rail_data.values()] + [value[1] for value in scotland_bus_data.values()] 
    total_car1, total_taxi1, total_bus1 = init_leg(all_inital_scotland)

    # England
    all_inital_eng = [value[1] for value in eng_rail_data.values()] + [value[1] for value in eng_flying_data.values()]
    total_car2, total_taxi2, total_bus2 = init_leg(all_inital_eng)

    # Wales
    all_inital_wales = [value[1] for value in wales_rail_data.values()] + [value[1] for value in wales_flying_data.values()]
    total_car3, total_taxi3, total_bus3 = init_leg(all_inital_wales)

    # Northern Ireland
    all_inital_ni = [value[1] for value in ni_rail_data.values()] + [value[1] for value in ni_flying_data.values()]
    total_car4, total_taxi4, total_bus4 = init_leg(all_inital_ni)

    """=================================Initialize Total distances=================================="""
    total_distance_rail_scotland, total_distance_rail_eng, total_distance_rail_wales, total_distance_rail_ni = 0, 0, 0, 0
    total_distance_bus_scotland = 0
    total_distance_car_scotland, total_distance_car_eng, total_distance_car_wales, total_distance_car_ni = 0, 0, 0, 0
    total_distance_plane_eng, total_distance_plane_wales, total_distance_plane_ni = 0, 0, 0

    """"=================================Converting to NumPy arrays=================================="""	

    # Extract mid leg distances from the dictionaries and converts them to numpy arrays (THESE ARE ONLY DISTANCES BETWEEN THE POSTCODES AND THE STOPS/STATIONS/AIRPORTS)
    rail_scotland_distances = extract_distances(scotland_rail_data)
    rail_eng_distances = extract_distances(eng_rail_data)
    rail_wales_distances = extract_distances(wales_rail_data)
    rail_ni_distances = extract_distances(ni_rail_data)
    bus_scotland_distances = extract_distances(scotland_bus_data)
    car_scotland_distances = extract_car_distances(scotland_car_data)
    car_eng_distances = extract_car_distances(eng_car_data)
    car_wales_distances = extract_car_distances(wales_car_data)
    car_ni_distances = extract_car_distances(ni_car_data)
    plane_eng_distances = extract_distances(eng_flying_data)
    plane_wales_distances = extract_distances(wales_flying_data)
    plane_ni_distances = extract_distances(ni_flying_data)

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

    # Create a dictionary to store the total distances for each country
    total_distances_dict = {'Scotland': [total_distance_rail_scotland, 0, total_distance_bus_scotland, total_distance_car_scotland, total_distance_taxi_scotland, total_walk_scotland],
                        'England': [total_distance_rail_eng, total_distance_plane_eng,  total_distance_bus_eng, total_distance_car_eng, total_distance_taxi_eng, total_walk_eng],
                        'Wales': [total_distance_rail_wales, total_distance_plane_wales,  total_distance_bus_wales, total_distance_car_wales, total_distance_taxi_wales, total_walk_wales],
                        'Northern Ireland': [total_distance_rail_ni, total_distance_plane_ni,  total_distance_bus_ni, total_distance_car_ni, total_distance_taxi_ni, total_walk_ni]}

    """=================================Visualisation==================================""" 

    # Create a dataframe to store the total distances
    total_distances = pd.DataFrame(total_distances_dict,
                                    index=['Rail', 'Plane', 'Bus', 'Car', 'Taxi', 'Walk'])

    """=================================Emissions=================================="""
    
    # Calculate the emissions for each mode of transport
    # Emissions = distance * emission factor
    # Emissions are in kgCO2e
    # Scotland emissions
    rail_emissions_scotland = total_distance_rail_scotland * emission_factors['rail']
    bus_emissions_scotland = total_distance_bus_scotland * emission_factors['coach']
    car_emissions_scotland = total_distance_car_scotland * emission_factors['car']
    taxi_emissions_scotland = total_distance_taxi_scotland * emission_factors['taxi']
    walk_emissions_scotland = 0
    # Total emissions
    total_emissions_scotland = rail_emissions_scotland + bus_emissions_scotland + car_emissions_scotland + taxi_emissions_scotland + walk_emissions_scotland

    # England emissions
    rail_emissions_england = total_distance_rail_eng * emission_factors['rail']
    plane_emissions_england = total_distance_plane_eng * emission_factors['plane']
    car_emissions_england = total_distance_car_eng * emission_factors['car']
    taxi_emissions_england = total_distance_taxi_eng * emission_factors['taxi']
    bus_emissions_england = total_distance_bus_eng * emission_factors['coach']
    walk_emissions_england = 0
    # Total emissions
    total_emissions_england = rail_emissions_england + plane_emissions_england + car_emissions_england + taxi_emissions_england + walk_emissions_england

    # Wales emissions
    rail_emissions_wales = total_distance_rail_wales * emission_factors['rail']
    plane_emissions_wales = total_distance_plane_wales * emission_factors['plane']
    car_emissions_wales = total_distance_car_wales * emission_factors['car']
    taxi_emissions_wales = total_distance_taxi_wales * emission_factors['taxi']
    bus_emissions_wales = total_distance_bus_wales * emission_factors['coach']
    walk_emissions_wales = 0
    # Total emissions
    total_emissions_wales = rail_emissions_wales + plane_emissions_wales + car_emissions_wales + taxi_emissions_wales + walk_emissions_wales

    # Northern Ireland emissions
    rail_emissions_ni = total_distance_rail_ni * emission_factors['rail']
    plane_emissions_ni = total_distance_plane_ni * emission_factors['plane']
    car_emissions_ni = total_distance_car_ni * emission_factors['car']
    taxi_emissions_ni = total_distance_taxi_ni * emission_factors['taxi']
    bus_emissions_ni = total_distance_bus_ni * emission_factors['coach']
    walk_emissions_ni = 0

    # Total emissions
    total_emissions_ni = rail_emissions_ni + plane_emissions_ni + car_emissions_ni + taxi_emissions_ni + walk_emissions_ni

    # Create a dataframe to store the separate emissions
    total_emissions_heatmap = pd.DataFrame({'Scotland': [rail_emissions_scotland, 0, bus_emissions_scotland, car_emissions_scotland, taxi_emissions_scotland, walk_emissions_scotland],
                                    'England': [rail_emissions_england, plane_emissions_england, bus_emissions_england, car_emissions_england, taxi_emissions_england, walk_emissions_england],
                                    'Wales': [rail_emissions_wales, plane_emissions_wales, bus_emissions_wales, car_emissions_wales, taxi_emissions_wales, walk_emissions_wales],
                                    'Northern Ireland': [rail_emissions_ni, plane_emissions_ni, bus_emissions_ni, car_emissions_ni, taxi_emissions_ni, walk_emissions_ni]},
                                    index=['Rail', 'Plane', 'Bus', 'Car', 'Taxi', 'Walk'])
    

    # Dataframe to store the total emissions
    total_emissions = pd.DataFrame({'Scotland': [total_emissions_scotland],
                                    'England': [total_emissions_england],
                                    'Wales': [total_emissions_wales],
                                    'Northern Ireland': [total_emissions_ni]},
                                    index=['Country'])

    # Return the total emissions dataframe
    return total_emissions_heatmap, total_distances, total_emissions, total_distances_dict, invalid


if __name__ == '__main__':
    main()
    