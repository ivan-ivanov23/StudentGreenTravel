# This file contains the functions to calculate the distance for each mode of transport for the students from Scotland and the rest of the UK.
# Sources of code snippets are provided in the comments of functions.
# Author: Ivan Ivanov

from itertools import islice, accumulate
import math

# Students is a list of students from a country
# mode_of_transport is a string representing the mode of transport the students use to travel from home to Aberdeen
# hub_uni is a float representing the distance from the airport or bus/rail station to the university
def fleg_assumptions(students: list, mode_of_transport: str, hub_uni: float, car: int = 0, taxi: int = 0, bus: int = 0, walk: int = 0):

    num_students = len(students)
    
    # Calculate the number of students for each mode of transport
    p_car = math.ceil((car / 100) * num_students)
    p_taxi = math.ceil((taxi / 100) * num_students)
    p_bus = math.ceil((bus / 100) * num_students)
    p_walk = num_students - p_car - p_taxi - p_bus

    
    seclist = [p_car, p_taxi, p_bus, p_walk]
    # Source: Method 3 in https://www.geeksforgeeks.org/python-split-list-in-uneven-groups/
    res = [list(islice(students, start, end)) for start, end in zip([0]+list(accumulate(seclist)), accumulate(seclist))]

    # Calculate the total distance for each mode of transport
    total_car = len(res[0])
    total_taxi = len(res[1])
    total_bus = len(res[2])
    total_walk = len(res[3])

    # Add the distance to the university from the bus/rail station or airport
    if mode_of_transport == "bus/rail":
        total_car *= hub_uni
        total_taxi *= hub_uni
        total_bus *= hub_uni
        total_walk *= hub_uni
        final_bus_rail = [total_car, total_taxi, total_bus, total_walk]

        return final_bus_rail
    
    elif mode_of_transport == "plane":
        total_car *= hub_uni
        total_taxi *= hub_uni
        total_bus *= hub_uni
        total_walk *= hub_uni
        final_plane = [total_car, total_taxi, total_bus, total_walk]

        return final_plane
    
    else:
        # Call the function again if the mode of transport is invalid
        fleg_assumptions(students, mode_of_transport, hub_uni)


def assign_scotland(bus_rail_students, p_car, p_taxi, p_bus, p_walk):
    """The function assigns the students from Scotland to the mode of transport they use to travel from home to Aberdeen.
       It calls the fleg_assumptions function to calculate the distance for each mode of transport for Scotland."""
    station_uni = 3.0
    bus_rail = fleg_assumptions(bus_rail_students, "bus/rail", station_uni, p_car, p_taxi, p_bus, p_walk)
    return bus_rail

def assign_uk(bus_rail_students, plane_students, p_car, p_taxi, p_bus, p_walk, p_car_plane, p_taxi_plane, p_bus_plane, p_walk_plane):
    """The function assigns the students from England, Wales and Northern Ireland to the mode of transport they use to travel from home to Aberdeen.
         It calls the fleg_assumptions function to calculate the distance for each mode of transport for England, Wales and Northern Ireland."""
    station_uni = 3.0
    airport_uni = 8.1
    bus_rail = fleg_assumptions(bus_rail_students, "bus/rail", station_uni, p_car, p_taxi, p_bus, p_walk)
    plane = fleg_assumptions(plane_students, "plane", airport_uni, p_car_plane, p_taxi_plane, p_bus_plane, p_walk_plane)
    return bus_rail, plane