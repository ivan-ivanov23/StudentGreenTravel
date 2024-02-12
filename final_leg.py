# This file holds the functions for the final leg of the journey
# Need to be able to enter assumptions to the tool on the % split for each of the following 
# Car, Taxi, Bus and Walk for both Scottish and Non-Scottish students

import numpy as np
from itertools import islice

# Function to calculate the final leg of the journey
# Take the list of students (Scotland, England, Wales, NI)
# Find the length of the list
# Prompt the user to enter the % split for each of the following
# Car, Taxi, Bus and Walk for both Scottish and Non-Scottish students
# According to these percentages, calculate the number of students taking each mode of transport with islice
# Find the length of each of these lists
# Multiply the length of each list by the distance of the final leg of the journey according to the mode of transport to find the total distance
# Return the total distance

scot_students, eng_students, wales_students, ni_students = [10], [10], [10], [10]

def options(scot_students, eng_students, wales_students, ni_students):
    countries = ["","Scotland", "England", "Wales", "Northern Ireland"]
    start = True

    while start:
        
        choice = int(input("Which country are you working with?\nEnter 1 for Scotland\nEnter 2 for England\nEnter 3 for Wales\nEnter 4 for Northern Ireland\nEnter 5 for exit\nEnter a number:"))


        if choice == 1:
            choice2 = int(input(f"What were the {countries[choice]} students travelling with from home?\nEnter 1 for bus or 2 for rail\nEnter a number:"))
            if choice2 == 1:
                f_bus_scot = final_leg(scot_students, "Scotland", "bus")
            elif choice2 == 2:
                f_rail_scot = final_leg(scot_students, "Scotland", "rail")
        elif choice == 2:
            choice3 = int(input(f"What were the {countries[choice]} students travelling with from home?\nEnter 1 for bus/rail or 2 for plane\nEnter a number:"))
            if choice3 == 1:
                f_eng_bus = final_leg(eng_students, "England", "bus")
            elif choice3 == 2:
                f_eng_plane = final_leg(eng_students, "England", "plane")
        elif choice == 3:
            choice4 = int(input(f"What were the {countries[choice]} students travelling with from home?\nEnter 1 for bus/rail or 2 for plane\nEnter a number:"))
            if choice4 == 1:
                f_wales_bus = final_leg(wales_students, "Wales", "bus")
            elif choice4 == 2:
                f_wales_plane = final_leg(wales_students, "Wales", "plane")
        elif choice == 4:
            choice5 = int(input(f"What were the {countries[choice]} students travelling with from home?\nEnter 1 for bus/rail or 2 for plane\nEnter a number:"))
            if choice5 == 1:
                f_ni_bus = final_leg(ni_students, "Northern Ireland", "bus")
            elif choice5 == 2:
                f_ni_plane = final_leg(ni_students, "Northern Ireland", "plane")
        elif choice == 5:
            start = False
        else:
            print('Wrong input! Try again!')
            options(scot_students, eng_students, wales_students, ni_students)

    return f_bus_scot, f_rail_scot, f_eng_bus, f_eng_plane, f_wales_bus, f_wales_plane, f_ni_bus, f_ni_plane



def final_leg(students, country: str, transport: str):
    # Distances in km
    airport_uni = 8.1
    station_uni = 3.0

    # Find the len of students
    num_students = len(students)

    # User to choose the % split for each mode of transport
    car = int(input(f"Enter what % of students from {country} travel from transport hub to university by car: "))
    taxi = int(input(f"Enter what % of students from {country} travel from transport hub to university by taxi: "))
    bus = int(input(f"Enter what % of students from {country} travel from transport hub to university by bus: "))
    walk =  int(input(f"Enter what % of students from {country} travel from transport hub to university by walking: "))

    # Calculate the number of students for each mode of transport
    p_car = int(num_students * (car / 100))
    p_taxi = int(num_students * (taxi / 100))
    p_bus = int(num_students * (bus / 100))
    p_walk = int(num_students * (walk / 100))

    # Divide the list of students into 4 parts based on the percentages
    seclist = [p_car, p_taxi, p_bus, p_walk]
    it = iter(students)
    car1, taxi1, bus1, walk1 = [list(islice(it, 0, i)) for i in seclist]

    # Calculate the total distance for each mode of transport
    total_car = np.sum(car1)
    total_taxi = np.sum(taxi1)
    total_bus = np.sum(bus1)
    total_walk = np.sum(walk1)

    
    # Add the distance to the university from the bus/rail station or airport
    if transport == "bus" or transport == "rail":
        total_car *= station_uni
        total_taxi *= station_uni
        total_bus *= station_uni
        total_walk * station_uni
        options(scot_students, eng_students, wales_students, ni_students)

    elif transport == "plane":
        total_car *= airport_uni
        total_taxi *= airport_uni
        total_bus *= airport_uni
        total_walk *= airport_uni
        options(scot_students, eng_students, wales_students, ni_students)

    # Store the total distance for each mode of transport for each country
    if country == "Scotland":
        final_leg_scot = [total_car, total_taxi, total_bus, total_walk]
        return final_leg_scot
    elif country == "England":
        final_leg_eng = [total_car, total_taxi, total_bus, total_walk]
        return final_leg_eng
    elif country == "Wales":
        final_leg_wales = [total_car, total_taxi, total_bus, total_walk]
        return final_leg_wales
    elif country == "Northern Ireland":
        final_leg_ni = [total_car, total_taxi, total_bus, total_walk]
        return final_leg_ni
    

    # Call the options function to select for another country
    options(scot_students, eng_students, wales_students, ni_students)

    
f_bus_scot, f_rail_scot, f_eng_bus, f_eng_plane, f_wales_bus, f_wales_plane, f_ni_bus, f_ni_plane = options(scot_students, eng_students, wales_students, ni_students)

print(f_bus_scot)


