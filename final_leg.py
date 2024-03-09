# This file contains the functions to calculate the distance for each mode of transport for the students from Scotland and the rest of the UK.
# Sources of code snippets are provided in the comments of functions.
# Author: Ivan Ivanov

from itertools import islice

# Students is a list of students from a country
# mode_of_transport is a string representing the mode of transport the students use to travel from home to Aberdeen
# hub_uni is a float representing the distance from the airport or bus/rail station to the university
def fleg_assumptions(students: list, mode_of_transport: str, hub_uni: float, car: int = 0, taxi: int = 0, bus: int = 0, walk: int = 0):

    num_students = len(students)
    
    # Calculate the number of students for each mode of transport
    p_car = int((car / 100) * num_students)
    p_taxi = int((taxi / 100) * num_students)
    p_bus = int((bus / 100) * num_students)
    p_walk = int((walk / 100) * num_students)

    # Divide the list of students into 4 parts based on the percentages
    # Inspired by answer from senderle: https://stackoverflow.com/questions/312443/how-do-i-split-a-list-into-equally-sized-chunks
    seclist = [p_car, p_taxi, p_bus, p_walk]
    it = iter(students)
    car1, taxi1, bus1, walk1 = [list(islice(it, 0, i)) for i in seclist]

    # Calculate the total distance for each mode of transport
    total_car = len(car1)
    total_taxi = len(taxi1)
    total_bus = len(bus1)
    total_walk = len(walk1)

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
        print("Invalid mode of transport")
        # Call the function again if the mode of transport is invalid
        fleg_assumptions(students, mode_of_transport, hub_uni)


def assign_scotland(bus_rail_students, pcar, ptaxi, pbus, pwalk):
    """The function assigns the students from Scotland to the mode of transport they use to travel from home to Aberdeen.
       It calls the fleg_assumptions function to calculate the distance for each mode of transport for Scotland."""
    station_uni = 3.0
    bus_rail = fleg_assumptions(bus_rail_students, "bus/rail", station_uni, pcar, ptaxi, pbus, pwalk)
    return bus_rail

def assign_uk(bus_rail_students, plane_students, pcar, ptaxi, pbus, pwalk, pcar_plane, ptaxi_plane, pbus_plane, pwalk_plane):
    """The function assigns the students from England, Wales and Northern Ireland to the mode of transport they use to travel from home to Aberdeen.
         It calls the fleg_assumptions function to calculate the distance for each mode of transport for England, Wales and Northern Ireland."""
    station_uni = 3.0
    airport_uni = 8.1
    bus_rail = fleg_assumptions(bus_rail_students, "bus/rail", station_uni, pcar, ptaxi, pbus, pwalk)
    plane = fleg_assumptions(plane_students, "plane", airport_uni, pcar_plane, ptaxi_plane, pbus_plane, pwalk_plane)
    return bus_rail, plane