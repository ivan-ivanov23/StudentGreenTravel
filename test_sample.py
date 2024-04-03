import pandas as pd
import math
from preprocess_data import determine_postcode, divide_scot_addresses, divide_uk_addresses, airports_dict, stations_dict
from travel_class import Travel, aberdeen_airport, aberdeen_bus_stop, aberdeen_rail_station
from aberdeen import distance_home_uni, divide_aberdeen
from council_areas import get_district, group_district, find_percentage

"""/////////////////////////// TEST OF THE FUNCTIONS IN preprocess_data.py ///////////////////////////"""

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

###########################################################################################################################
"""/////////////////////////// TEST OF THE FUNCTIONS IN travel_class.py ///////////////////////////"""

# Stadium of Manchester United postcode
# Closest airport: Manchester Airport
postcode = ['M16 0RA']

travel = Travel(aberdeen_bus_stop, aberdeen_rail_station, aberdeen_airport)

print("=============================== air_travel() TEST ===============================")

# Test the air_travel method
airports, invalid = travel.air_travel(airports_dict, postcode)

result = []
for key, value in airports.items():
    for i in value:
        result.append(i)
# From Google Maps, the distance between Manchester Airport and Manchester United Stadium is 12 km
# Considering layover the total flight distance is 969 km -> Manchester Airport to Gatwick Airport to Aberdeen Airport
if result[0] == 'Manchester Airport' and math.isclose(result[1], 12, rel_tol=1) and math.isclose(result[1], 969, rel_tol=1):
    print("The function air_travel() works correctly.")
    print(f"Output: {airports}")
else:
    print("The function air_travel() does not work correctly.")
    print(airports)

###########################################################################################################################
print("=============================== land_travel() TEST ===============================")
# Test the land_travel method
postcode = ['G42 9BJ']
aberdeen_rail_station = (57.14372498503623, -2.0983252205325833)

rail_stations, invalid = travel.land_travel(stations_dict, postcode, aberdeen_rail_station)

result = []
for key, value in rail_stations.items():
    for i in value:
        result.append(i)

# From Google Maps, the closest rail station to the postcode is Mount Florida and is around 300 metres
# From Google Maps, the distance between Mount Florida and Aberdeen Rail Station is around 197 km
if result[0] == 'Mount Florida Railway Station' and math.isclose(result[1], 0.3, rel_tol=0.2) and math.isclose(result[2], 197, rel_tol=1):
    print("The function bus_travel() works correctly.")
    print(f"Output: {rail_stations}")
else:
    print("The function bus_travel() does not work correctly.")
    print(rail_stations)

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

###########################################################################################################################
"""/////////////////////////// TEST OF THE FUNCTIONS IN aberdeen.py ///////////////////////////"""
# Postcode of King street Lidl next ot Seaton Park
students = ['AB241XZ', 'AB106RN', 'AB107JB', 'AB115QN', 'AB116UL', 'AB118RU', 'AB123FJ', 'AB124NQ', 'AB125GL', 'AB243AD']

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
###########################################################################################################################
"""/////////////////////////// TEST OF THE FUNCTIONS IN council_areas.py ///////////////////////////"""
council_postcodes = ["EH11 1EG", "G81 2NR", "DD2 4TZ", "FK15 0LN"]

print("=============================== get_district() TEST ===============================")
# Test the get_district function
districts = get_district(council_postcodes)

# Postcode council areas below are found in https://www.doogal.co.uk/ShowMap 
if districts["EH11 1EG"] == 'City of Edinburgh' and districts["G81 2NR"] == 'West Dunbartonshire' and districts["DD2 4TZ"] == 'Dundee City' and districts["FK15 0LN"] == 'Stirling':
    print("The function get_district() works correctly.")
    print(f"Output: {districts}")
else:
    print("The function get_district() does not work correctly.")
    print(districts)

###########################################################################################################################
print("=============================== group_district() TEST ===============================")
# Test the group_district function
districts['DD2 4RH'] = 'Dundee City'
grouped = group_district(districts)

# The postcodes are grouped by their council areas
# In this case we have 4 council areas and 1 postcode for each apart from Dundee City which has 2 postcodes
# Dundee City: ['DD2 4TZ', 'DD2 4RH']
if len(grouped) == 4 and len(grouped["City of Edinburgh"]) == 1 and len(grouped["West Dunbartonshire"]) == 1 and len(grouped["Dundee City"]) == 2 and len(grouped["Stirling"]) == 1:
    print("The function group_district() works correctly.")
    print(f"Output: {grouped}")
else:
    print("The function group_district() does not work correctly.")
    print(grouped)

###########################################################################################################################
print("=============================== find_percentage() TEST ===============================")
# Test the find_percentage function
percentages = find_percentage(grouped, council_postcodes)

# There are 5 postcodes in total and 4 council areas
# Therefore there should be 25% of postcodes in each council area except Dundee City which has 50%
if percentages['City of Edinburgh'] == 25 and percentages['West Dunbartonshire'] == 25 and percentages['Dundee City'] == 50 and percentages['Stirling'] == 25:
    print("The function find_percentage() works correctly.")
    print(f"Output: {percentages}")
else:
    print("The function find_percentage() does not work correctly.")
    print(percentages)

###########################################################################################################################
print("=============================== END OF TESTS ===============================")




