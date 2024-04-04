# This file contains manual tests for all the main functions in the project.
# These tests can be run by executing the file in the terminal.
# Sources of code snippets and data are provided in the comments of functions.
# Lists of postcodes were generated using: https://www.doogal.co.uk/PostcodeGenerator 
# Author: Ivan Ivanov

import pandas as pd
import math
from preprocess_data import determine_postcode, divide_scot_addresses, divide_uk_addresses, airports_dict, stations_dict, stops_dict
from travel_class import Travel, aberdeen_airport, aberdeen_bus_stop, aberdeen_rail_station
from aberdeen import distance_home_uni, divide_aberdeen
from council_areas import get_district, group_district, find_percentage

"""/////////////////////////// TEST OF THE FUNCTIONS IN preprocess_data.py ///////////////////////////"""
print("~.~.~.~.~.~.~.~.~.~.~.~. PREPROCESS_DATA.PY TESTS ~.~.~.~.~.~.~.~.~.~.~.~.")

scottish_postcodes = ["EH11 1EG", "G81 2NR", "HS7 5LE", "DD2 4TZ", "FK15 0LN"]
aberdeen_postcodes = ["AB10 1SN", "AB53 8RL", "AB24 1WU", "AB15 8PU", "AB16 5ST"]
english_postcodes = ["AL1 1AJ", "BA1 1AQ", "BB1 1BB", "BD1 1AA", "BH1 1AA"]
welsh_postcodes = ["CF10 1DD", "LL11 1AA", "NP20 1AA", "SA1 1AA", "SY1 1AA"]
northern_irish_postcodes = ["BT1 1AA", "BT2 1AA", "BT3 1AA", "BT4 1AA", "BT5 1AA"]
invalid_postcodes = ["ZZ1 1AA", "ZZ2 1AA", "ZZ3 1AA", "ZZ4 1AA", "ZZ5 1AA"]

postcodes = pd.Series(scottish_postcodes + aberdeen_postcodes + english_postcodes + welsh_postcodes + northern_irish_postcodes + invalid_postcodes)

###########################################################################################################################
print("=============================== determine_postcode() TEST ===============================")
# Test the determine_postcode function
scotland, wales, north_ireland, england, aberdeen, new_invalid = determine_postcode(postcodes)
    
# Test the valid postcodes
def test_determine_postcode(original_postcodes, country_postcodes, country):
    errors = 0
    for postcode in original_postcodes:
        if postcode not in country_postcodes.tolist():
            errors += 1

    if errors > 0:
        print(f"{errors} postcodes from {country} were not found in the {country} list.")
    
    else:
        print(f"All postcodes from {country} were found in the {country} list.")

test_determine_postcode(scottish_postcodes, scotland, "Scotland")
test_determine_postcode(aberdeen_postcodes, aberdeen, "Aberdeen")
test_determine_postcode(english_postcodes, england, "England")
test_determine_postcode(welsh_postcodes, wales, "Wales")
test_determine_postcode(northern_irish_postcodes, north_ireland, "Northern Ireland")

# Test the invalid postcodes
def test_invalid(original_postcodes, invalid_postcodes):
    errors = 0
    for postcode in original_postcodes:
        if invalid_postcodes[postcode] != 'Uknown country':
            errors += 1

    if errors > 0:
        print(f"{errors} postcodes were not found in the invalid list.")

    else:
        print(f"All invalid postcodes were found in the invalid list.")

test_invalid(invalid_postcodes, new_invalid)
###########################################################################################################################
print("=============================== divide_scot_addresses() TEST ===============================")
# Test the divide_scot_addresses function
p_bus = 20
p_car = 30
# p_rail = 100 - p_bus - p_car = 50

new_scottish_postcodes = ["EH11 1EG", "G81 2NR", "HS7 5LE", "DD2 4TZ", "FK15 0LN", "AB10 1SN", "AB53 8RL", "AB24 1WU", "AB15 8PU", "AB16 5ST"]

def test_divide_scot_addresses(scot_addresses, p_bus, p_car):
    p_bus_scot, p_car_scot, p_rail_scot = divide_scot_addresses(scot_addresses, p_bus, p_car)
    return {"Bus": p_bus_scot, "Car": p_car_scot, "Rail": p_rail_scot}

# From 10 postcodes, 20% are for buses, 30% are for cars and the rest are for trains
# Therefore the results should be: Bus: 2, Car: 3, Rail: 5 postcodes respectively
res = test_divide_scot_addresses(new_scottish_postcodes, p_bus, p_car)
bus_percent = len(res["Bus"])
car_percent = len(res["Car"])
rail_percent = len(res["Rail"])

if bus_percent == 2 and car_percent == 3 and rail_percent == 5:
    print("The function divide_scot_addresses() works correctly.")
    print(f"Output: {res}")
else:
    print("The function divide_scot_addresses() does not work correctly.")
    print(res)

###########################################################################################################################
print("=============================== divide_uk_addresses() TEST ===============================")
# Test the divide_uk_addresses function
p_plane = 50
p_car = 30
# p_train = 100 - p_plane - p_car = 20

new_eng = ["SK17 7EQ", "DN12 4HA", "FK17 8HD", "KT6 6QD", "BN8 4HE", "CR5 1PA", "CV23 9RF", "LN11 0PG", "PA15 1AN", "KY12 8AN"]

def test_divide_scot_addresses(eng_addresses, p_plane, p_car):
    p_bus_eng, p_car_eng, p_rail_eng = divide_uk_addresses(eng_addresses, p_plane, p_car)
    return {"Plane": p_bus_eng, "Car": p_car_eng, "Train": p_rail_eng}

# From 10 postcodes, 50% are for planes, 30% are for cars and the rest are for trains
# Therefore the results should be: Plane: 5, Car: 3, Train: 2 postcodes respectively
res = test_divide_scot_addresses(new_eng, p_plane, p_car)
plane_percent = len(res["Plane"])
car_percent = len(res["Car"])
train_percent = len(res["Train"])

if plane_percent == 5 and car_percent == 3 and train_percent == 2:
    print("The function divide_uk_addresses() works correctly.")
    print(f"Output: {res}")
else:
    print("The function divide_uk_addresses() does not work correctly.")
    print(res)

print("")
###########################################################################################################################
"""/////////////////////////// TEST OF THE FUNCTIONS IN travel_class.py ///////////////////////////"""
print("~.~.~.~.~.~.~.~.~.~.~.~. TRAVEL_CLASS.PY TESTS ~.~.~.~.~.~.~.~.~.~.~.~.")
# Stadium of Manchester United postcode
# Closest airport: Manchester Airport
non_london_postcode = ['M16 0RA']

# Initialize the Travel class
travel = Travel(aberdeen_bus_stop, aberdeen_rail_station, aberdeen_airport)

print("=============================== air_travel() TEST1 ===============================")

# Test the air_travel method with non-London postcode
airports1, invalid1 = travel.air_travel(airports_dict, non_london_postcode)

result1 = []
for key, value in airports1.items():
    for i in value:
        result1.append(i)
# From Google Maps, the distance between Manchester Airport and Manchester United Stadium is 12 km
# Considering layover the total flight distance is 969 km -> Manchester Airport to Gatwick Airport to Aberdeen Airport
if result1[0] == 'Manchester Airport' and math.isclose(result1[1], 12, rel_tol=1) and math.isclose(result1[1], 969, rel_tol=1):
    print("The function air_travel() works correctly.")
    print(f"Output: {airports1}")
else:
    print("The function air_travel() does not work correctly.")
    print(airports1)

print("=============================== air_travel() TEST2 ===============================")
# Random london postcode, generated using https://www.doogal.co.uk/PostcodeGenerator
london_postcode = ['EC2Y 9AL']

# Test the air_travel method with London postcode
airports2, invalid2 = travel.air_travel(airports_dict, london_postcode)
result2 = []
for key, value in airports2.items():
    for i in value:
        result2.append(i)

# From Google Maps, the closest airport is London City Airport and is around 10 km
# There is no layover, so the distance between London City Airport and Aberdeen Airport is around 650 km
if result2[0] == 'London City Airport' and math.isclose(result2[1], 10, rel_tol=1) and math.isclose(result2[1], 650, rel_tol=1):
    print("The function air_travel() works correctly.")
    print(f"Output: {airports2}")
else:
    print("The function air_travel() does not work correctly.")
    print(airports2)


###########################################################################################################################
print("=============================== land_travel() TEST1 ===============================")
# Test the land_travel method with train travel
train_postcode = ['G42 9BJ']
aberdeen_rail_station = (57.14372498503623, -2.0983252205325833)

rail_stations, invalid = travel.land_travel(stations_dict, train_postcode, aberdeen_rail_station)

result1 = []
for key, value in rail_stations.items():
    for i in value:
        result1.append(i)

# From Google Maps, the closest rail station to the postcode is Mount Florida and is around 300 metres
# From Google Maps, the distance between Mount Florida and Aberdeen Rail Station is around 197 km
if result1[0] == 'Mount Florida Railway Station' and math.isclose(result1[1], 0.3, rel_tol=0.2) and math.isclose(result1[2], 197, rel_tol=1):
    print("The function bus_travel() works correctly.")
    print(f"Output: {rail_stations}")
else:
    print("The function bus_travel() does not work correctly.")
    print(rail_stations)

print("=============================== land_travel() TEST2 ===============================")
bus_postcode = ['EH5 2AX']
aberdeen_bus_station = (57.14372498503623, -2.0983252205325833)

bus_stops, invalid = travel.land_travel(stops_dict, bus_postcode, aberdeen_bus_station)

result2 = []
for key, value in bus_stops.items():
    for i in value:
        result2.append(i)

# From Google Maps, the closest bus station to the postcode is Edinburgh bus station and is around 4 km
# From Google Maps, the distance between Edinburgh bus station and Aberdeen bus station is around 200 km
if result2[0] == 'Edinburgh bus station' and math.isclose(result2[1], 4, rel_tol=1) and math.isclose(result2[2], 200, rel_tol=1):
    print("The function bus_travel() works correctly.")
    print(f"Output: {bus_stops}")
else:
    print("The function bus_travel() does not work correctly.")
    print(bus_stops)

###########################################################################################################################
print("=============================== car_travel() TEST ===============================")
# Test the car_travel method
postcode = ['G42 9BJ']
aberdeen_uni = (57.1645, -2.0999)

car_data, invalid = travel.car_travel(postcode)

# From Google Maps, the distance between the postcode and the university is around 220 km
if math.isclose(car_data[postcode[0]], 250, rel_tol=1):
    print("The function car_travel() works correctly.")
    print(f"Output: {car_data}")
else:
    print("The function car_travel() does not work correctly.")
    print(car_data)

print("")
###########################################################################################################################
"""/////////////////////////// TEST OF THE FUNCTIONS IN aberdeen.py ///////////////////////////"""
print("~.~.~.~.~.~.~.~.~.~.~.~. ABERDEEN.PY TESTS ~.~.~.~.~.~.~.~.~.~.~.~.")
# Postcode of King street Lidl next ot Seaton Park
students = ['AB241XZ', 'AB106RN', 'AB107JB', 'AB115QN', 'AB116UL', 'AB118RU', 'AB123FJ', 'AB124NQ', 'AB125GL', 'AB243AD']
# AB124NQ is invalid postcode, so the distance should be 0

car = 40
taxi = 40
bus = 10
walk = 10

print("=============================== distance_home_uni() TEST ===============================")
# Test the distance_home_uni function
distances = distance_home_uni(students)
# From Google Maps, the distance between the postcode and the university is around 1 km
if math.isclose(distances[students[0]], 1, rel_tol=1):
    print("The function distance_home_uni() works correctly.")
    print(f"Output: {distances[students[0]]}")
    print(f"Invalid postcode: AB124NQ has distance {distances['AB124NQ']}")

else:
    print("The function distance_home_uni() does not work correctly.")
    print(distances[students[0]])


###########################################################################################################################
print("=============================== divide_aberdeen() TEST ===============================")

# Test the divide_aberdeen function
result = divide_aberdeen(distances, car, taxi, bus, walk)
print(f'Distances between studetns homes and uni: {distances}')
# Due to 40% of students using cars, 40% using taxis, 10% using buses and 10% walking
# there should be 4 students using cars, 4 using taxis, 1 using buses and 1 walking
# So for each list of transport, the total distance is callculated by summing the distances of each student
# For the first 4 students (car), total distance should be around 12km
# For the next 4 students (taxi), total distance should be around 15km
# For the next student (bus), total distance should be around 12km
# For the last student (walk), total distance should be around 1km or under it
if math.isclose(result[0], 12, rel_tol=1) and math.isclose(result[1], 15, rel_tol=1) and math.isclose(result[2], 12, rel_tol=1) and math.isclose(result[3], 1, rel_tol=1):
    print("The function divide_aberdeen() works correctly.")
    print(f"Output: {result}")
else:
    print("The function divide_aberdeen() does not work correctly.")
    print(result)

print("")
###########################################################################################################################
"""/////////////////////////// TEST OF THE FUNCTIONS IN council_areas.py ///////////////////////////"""
print("~.~.~.~.~.~.~.~.~.~.~.~. COUNCIL_AREAS.PY TESTS ~.~.~.~.~.~.~.~.~.~.~.~.")

council_postcodes = ["EH11 1EG", "G81 2NR", "DD2 4TZ", "FK15 0LN", "AB0 0XX"]
# AB0 0XX is an invalid postcode and should not be found in the list of districts

print("=============================== get_district() TEST ===============================")
# Test the get_district function
districts = get_district(council_postcodes)

# Postcode council areas below are found in https://www.doogal.co.uk/ShowMap 
if districts["EH11 1EG"] == 'City of Edinburgh' and districts["G81 2NR"] == 'West Dunbartonshire' and districts["DD2 4TZ"] == 'Dundee City' and districts["FK15 0LN"] == 'Stirling' and districts["AB0 0XX"] == 'Uknown district':
    print("The function get_district() works correctly.")
    print(f"Output: {districts}")
else:
    print("The function get_district() does not work correctly.")
    print(districts)

###########################################################################################################################
print("=============================== group_district() TEST ===============================")
# Test the group_district function
grouped = group_district(districts)

# The postcodes are grouped by their council areas
# In this case we have 5 council areas and 1 postcode for each
if len(grouped) == 5 and len(grouped["City of Edinburgh"]) == 1 and len(grouped["West Dunbartonshire"]) == 1 and len(grouped["Dundee City"]) == 1 and len(grouped["Stirling"]) == 1 and len(grouped["Uknown district"]) == 1:
    print("The function group_district() works correctly.")
    print(f"Output: {grouped}")
else:
    print("The function group_district() does not work correctly.")
    print(grouped)

###########################################################################################################################
print("=============================== find_percentage() TEST ===============================")
# Test the find_percentage function
percentages = find_percentage(grouped, council_postcodes)

# There are 5 postcodes in total and 5 council areas
# Therefore there should be 20% of postcodes in each council area
if percentages['City of Edinburgh'] == 20 and percentages['West Dunbartonshire'] == 20 and percentages['Dundee City'] == 20 and percentages['Stirling'] == 20:
    print("The function find_percentage() works correctly.")
    print(f"Output: {percentages}")
else:
    print("The function find_percentage() does not work correctly.")
    print(percentages)

print("")
###########################################################################################################################
print("=============================== END OF TESTS ===============================")




