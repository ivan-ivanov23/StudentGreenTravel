from flying_distance import *
from land_distance import *
import numpy as np

land = land_travel(postcode_coord_dict, stop_coord_dict)
fly = travel(postcode_coord_dict, airport_coord_dict)

# TODO
# If postcode is in Scotland, it should consider not flying
# Make it calculate emissions based on road travel distance and air travel distance


# Emissions factors in kgCO2e per passenger km
# Source: https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2023
# The car factor is averaged over all vehicle types 
# Bus is local bus and coach is long distance bus
# Plane factor is for domestic flights as we are only considering flights within the UK
emission_factors = {'car': 0.18264,  'rail': 0.035463, 'bus': 0.118363, 'coach': 0.027181, 'taxi': 0.148615,
           'ferry': 0.02555, 'plane': 0.03350}

# Calculate land travel emissions
def bus_emissions(data: dict, factors: dict):
    # Dictionary to store the results in kgCO2e for each postcode
    bus_result = {}
    for key, value in data.items():
        # Coach emissions are just the lastlue in the tuple of values in land.items * the coach factor
        # Use numpy to calculate the emissions
        coach = np.multiply(value[-1], factors['coach'])
        # Local bus = distance from postcode to bus station + distance from Aberdeen bus station to university
        # Account for students that are from Aberdeen and travel 0 distance to the city
        if value[-1] != 0: 
            bus = (value[1] + 2.28) * factors['bus']
            # Total emissions
            bus_result[key] = round(coach + bus, 2)
        else:
            bus_result[key] = 0

    return bus_result

def plane_emissions(data: dict, factors: dict):
    # Dictionary to store the results in kgCO2e for each postcode
    plane_result = {}
    for key, value in data.items():
    # Coach emissions are just the lastlue in the tuple of values in land.items * the coach factor
        # Use numpy to calculate the emissions
        plane = np.multiply(value[-1], factors['plane'])
        # Local bus = distance from postcode to bus station + distance from Aberdeen airport to university
        # Account for students that are from Aberdeen and travel 0 distance to the city
        bus = (value[1] + 7.24) * factors['bus']
        # Total emissions
        plane_result[key] = round(plane + bus, 2)

    return plane_result

print('Bus: ', bus_emissions(land, emission_factors))

print('Plane: ', plane_emissions(fly, emission_factors))
