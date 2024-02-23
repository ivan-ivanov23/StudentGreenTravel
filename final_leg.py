import numpy as np
from itertools import islice

bus_rail_students_scotland = [ "AB", "CD", "EF", "GH", "IJ", "KL" , "MN", "OP", "QR", "ST", "UV", "WX", "YZ"]
plane_students_scotland = [ "MN", "OP", "QR", "ST", "UV", "WX", "YZ", "AB", "CD", "EF", "GH", "IJ", "KL"]
bus_rail_students_england = [ "YZ", "AB", "CD", "EF", "GH", "IJ", "KL", "MN", "OP", "QR", "ST", "UV"]
plane_students_england = ["AK", "BL", "CM", "DN", "EO", "FP", "GQ", "HR", "IS", "JT", "KU", "LV"]
bus_rail_students_wales = [ "GQ", "HR", "IS", "JT", "KU", "LV", "MW", "NX", "OY", "PZ", "QA", "RB"]
plane_students_wales = [ "MW", "NX", "OY", "PZ", "QA", "RB", "SC", "TD", "UE", "VF", "WG", "XH"]
bus_rail_students_ni = [ "SC", "TD", "UE", "VF", "WG", "XH", "YI", "ZJ", "AK", "BL", "CM", "DN"]
plane_students_ni = [ "YI", "ZJ", "AK", "BL", "CM", "DN", "EO", "FP", "GQ", "HR", "IS", "JT"]


# Students is a list of students from a country
# country is a string representing the country which the students are from
# mode_of_transport is a string representing the mode of transport the students use to travel from home to Aberdeen
# hub_uni is a float representing the distance from the airport or bus/rail station to the university
def fleg_assumptions(students: list, country : str, mode_of_transport: str, hub_uni: float, car: int = 0, taxi: int = 0, bus: int = 0, walk: int = 0):

    car = 0
    taxi = 0
    bus = 0
    walk = 0

    num_students = len(students)

    print(f"Currently working with students from: {country} with transport mode: {mode_of_transport}")

    #if mode_of_transport == "bus/rail":

    #     while car + taxi + bus + walk != 100:
    #         print('Please make sure the percentages add up to 100')
    #         try:
    #             car = int(input(f"Enter what % of students from {country} travel from Aberdeen bus/rail station to university by car: "))
    #             taxi = int(input(f"Enter what % of students from {country} travel from Aberdeen bus/rail to university by taxi: "))
    #             bus = int(input(f"Enter what % of students from {country} travel from Aberdeen bus/rail to university by bus: "))
    #             walk =  int(input(f"Enter what % of students from {country} travel from Aberdeen bus/rail to university by walking: "))
    #         except ValueError:
    #             print("Invalid input. Please enter a number")

    #     print("==================================================================================================================================")

    # elif mode_of_transport == "plane":

    #     while car + taxi + bus + walk != 100:
    #         print('Please make sure the percentages add up to 100')
    #         try:
    #             car = int(input(f"Enter what % of students from {country} travel from Aberdeen airport to university by car: "))
    #             taxi = int(input(f"Enter what % of students from {country} travel from Aberdeen airport to university by taxi: "))
    #             bus = int(input(f"Enter what % of students from {country} travel from Aberdeen airport to university by bus: "))
    #             walk =  int(input(f"Enter what % of students from {country} travel from Aberdeen airport to university by walking: "))
    #         except ValueError:
    #             print("Invalid input. Please enter a number")
    #     print("==================================================================================================================================")

    
    # Calculate the number of students for each mode of transport
    p_car = int((car / 100) * num_students)
    p_taxi = int((taxi / 100) * num_students)
    p_bus = int((bus / 100) * num_students)
    p_walk = int((walk / 100) * num_students)

    # Divide the list of students into 4 parts based on the percentages
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
        fleg_assumptions(students, country, mode_of_transport, hub_uni)


def select_country(bus_rail_students, plane_students, country: str, pcar, ptaxi, pbus, pwalk):
    station_uni = 3.0
    airport_uni = 8.1
    if country == "Scotland":
        bus_rail = fleg_assumptions(bus_rail_students, country, "bus/rail", station_uni, pcar, ptaxi, pbus, pwalk)
        return bus_rail
    else:
    # Calculate the distance for each mode of transport for each country
        bus_rail = fleg_assumptions(bus_rail_students, country, "bus/rail", station_uni)
        plane = fleg_assumptions(plane_students, country, "plane", airport_uni)
        return bus_rail, plane


# Execute the function with the students from each country and mode of transport
# scotland = select_country(bus_rail_students_scotland, plane_students_scotland, "Scotland")
#england = select_country(bus_rail_students_england, plane_students_england, "England")
# wales = select_country(bus_rail_students_wales, plane_students_wales, "Wales")
# ni = select_country(bus_rail_students_ni, plane_students_ni, "Northern Ireland")

# print(f"Scotland: {scotland}")
#print(f"England: {england}")
# print(f"Wales: {wales}")
# print(f"Northern Ireland: {ni}")