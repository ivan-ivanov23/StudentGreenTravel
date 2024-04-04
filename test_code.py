# This file contains manual tests for all the main functions in the project.
# These tests can be run by executing the file in the terminal.
# Sources of code snippets and data are provided in the comments of functions.
# Author: Ivan Ivanov

import unittest
import pandas as pd
import math
from preprocess_data import determine_postcode, divide_scot_addresses, divide_uk_addresses, airports_dict, stations_dict, stops_dict
from travel_class import Travel, aberdeen_airport, aberdeen_bus_stop, aberdeen_rail_station
from aberdeen import distance_home_uni, divide_aberdeen
from council_areas import get_district, group_district, find_percentage

class PreprocessTest(unittest.TestCase):
    """Class to hold the test methods for preprocess_data.py"""

    def setUp(self):
        # Postcodes for each country and the invalid case
        self.scottish_postcodes = ["EH11 1EG", "G81 2NR", "HS7 5LE", "DD2 4TZ", "FK15 0LN"]
        self.aberdeen_postcodes = ["AB10 1SN", "AB53 8RL", "AB24 1WU", "AB15 8PU", "AB16 5ST"]
        self.english_postcodes = ["AL1 1AJ", "BA1 1AQ", "BB1 1BB", "BD1 1AA", "BH1 1AA"]
        self.welsh_postcodes = ["CF10 1DD", "LL11 1AA", "NP20 1AA", "SA1 1AA", "SY1 1AA"]
        self.northern_irish_postcodes = ["BT1 1AA", "BT2 1AA", "BT3 1AA", "BT4 1AA", "BT5 1AA"]
        self.invalid_postcodes = ["ZZ1 1AA", "ZZ2 1AA", "ZZ3 1AA", "ZZ4 1AA", "ZZ5 1AA"]
        # Combine all postcodes into one series to use in the determine_postcode function
        self.postcodes1 = pd.Series(self.scottish_postcodes + self.aberdeen_postcodes + self.english_postcodes + self.welsh_postcodes + self.northern_irish_postcodes + self.invalid_postcodes)

    def test_determine_postcode(self):
        # Test the determine_postcode function for each country
        scotland, wales, north_ireland, england, aberdeen, new_invalid = determine_postcode(self.postcodes1)
        self.assertEqual(scotland.tolist(), self.scottish_postcodes)
        self.assertEqual(aberdeen.tolist(), self.aberdeen_postcodes)
        self.assertEqual(england.tolist(), self.english_postcodes)
        self.assertEqual(wales.tolist(), self.welsh_postcodes)
        self.assertEqual(north_ireland.tolist(), self.northern_irish_postcodes)
        # Take the keys of the new_invalid dictionary to get the invalid postcodes
        invalid_keys = [key for key, value in new_invalid.items()]
        self.assertEqual(invalid_keys, self.invalid_postcodes)

    def test_divide_scot_addresses(self):
        # Percentages for each transport method
        p_bus = 20
        p_car = 30
        # p_rail = 100 - p_bus - p_car = 50

        # New list of Scottish postcodes generated via https://www.ukpostcode.co.uk/random.htm
        new_scottish_postcodes = ["EH11 1EG", "G81 2NR", "HS7 5LE", "DD2 4TZ", "FK15 0LN", "AB10 1SN", "AB53 8RL", "AB24 1WU", "AB15 8PU", "AB16 5ST"]
        bus_scot, car_scot, train_scot = divide_scot_addresses(new_scottish_postcodes, p_bus, p_car)
        # From 10 postcodes, 20% are for buses, 30% are for cars and the rest are for trains
        # Therefore the results should be: Bus: 2, Car: 3, Rail: 5 postcodes respectively
        self.assertEqual(len(bus_scot), 2)
        self.assertEqual(len(car_scot), 3)
        self.assertEqual(len(train_scot), 5)

    def test_divide_uk_addresses(self):
        # Percentages for each transport method
        p_plane = 50
        p_car_uk = 30
        # p_train_uk = 100 - p_plane - p_car_uk

        # New list of English postcodes generated via https://www.ukpostcode.co.uk/random.htm
        new_english_postcodes = ["SK17 7EQ", "DN12 4HA", "FK17 8HD", "KT6 6QD", "BN8 4HE", "CR5 1PA", "CV23 9RF", "LN11 0PG", "PA15 1AN", "KY12 8AN"]
        plane, car_uk, train_uk = divide_uk_addresses(new_english_postcodes, p_plane, p_car_uk)
        # From 10 postcodes, 50% are for planes, 30% are for cars and the rest are for trains
        # Therefore, the results should be: Plane: 5 , Car: 3, Train: 2 postcodes respectively
        self.assertEqual(len(plane), 5)
        self.assertEqual(len(car_uk), 3)
        self.assertEqual(len(train_uk), 2)


class TravelTest(unittest.TestCase):
    """Class to hold the test methods for travel_class.py"""

    def setUp(self):
        self.travel = Travel(aberdeen_bus_stop, aberdeen_rail_station, aberdeen_airport)

    def test_air_travel_non_london(self):
        # Stadium of Manchester United postcode from Google Maps
        # Closest airport: Manchester Airport
        non_london_postcode = ['M16 0RA']

        airports1, invalid1 = self.travel.air_travel(airports_dict, non_london_postcode)
        # List comprehension to hold only the values of the airports1 dictionary
        result1 = [value for key, values in airports1.items() for value in values]
        # From Google Maps, the distance between Manchester Airport and Manchester United Stadium is 12 km
        # Considering layover the total flight distance is 969 km -> Manchester Airport to Gatwick Airport to Aberdeen Airport
        self.assertEqual(result1[0], 'Manchester Airport')
        # Rounding the result values to be able to compare them
        self.assertAlmostEqual(round(result1[1], 0), 12)
        self.assertAlmostEqual(round(result1[2], 0), 969)
        # The invalid1 lsit should be empty
        self.assertEqual(invalid1, [])

    def test_air_travel_london(self):
        # Random London postcode, generated using https://www.doogal.co.uk/PostcodeGenerator
        london_postcode = ['EC2Y 9AL']

        # Test the air_travel method with London postcode
        airports2, invalid2 = self.travel.air_travel(airports_dict, london_postcode)
        # List comprehension to hold only the values of the airports2 dictionary
        result2 = [value for key, values in airports2.items() for value in values]
        # From Google Maps, the closest airport is London City Airport and is around 10 km
        # There is no layover, so the distance between London City Airport and Aberdeen Airport is around 651 km
        self.assertEqual(result2[0], 'London City Airport')
        # Rounding the result values to be able to compare them
        self.assertAlmostEqual(round(result2[1], 0), 10)
        self.assertAlmostEqual(round(result2[2], 0), 651)
        # The invalid2 lsit should be empty
        self.assertEqual(invalid2, [])

    def test_land_travel_train(self):
        # Test the land_travel method with train travel
        # Random Scottish postcode, generated using https://www.doogal.co.uk/PostcodeGenerator
        train_postcode = ['G42 9BJ']
        aberdeen_rail_station = (57.14372498503623, -2.0983252205325833)

        rail_stations, invalid = self.travel.land_travel(stations_dict, train_postcode, aberdeen_rail_station)
        # List comprehension to hold only the values of the rail_stations dictionary
        rail_result = [value for key, values in rail_stations.items() for value in values]
        # From Google Maps, the closest rail station to the postcode is Mount Florida and is around 300 metres
        # From Google Maps, the distance between Mount Florida and Aberdeen Rail Station is around 197 km
        self.assertEqual(rail_result[0], 'Mount Florida Railway Station')
        # Using math.isclose() and assertTrue() to check the distances
        self.assertTrue(math.isclose(rail_result[1], 0.3, rel_tol=0.1))
        self.assertTrue(math.isclose(rail_result[2], 197, rel_tol=1))
        self.assertEqual(invalid, [])

    def test_land_travel_bus(self):
        # Test the land_travel method with bus travel
        # Random Scottish postcode, generated using https://www.doogal.co.uk/PostcodeGenerator
        bus_postcode = ['EH5 2AX']
        # Same coordinates as rail station due to them being in the same location in Aberdeen
        aberdeen_bus_station = (57.14372498503623, -2.0983252205325833)

        bus_stops, invalid = self.travel.land_travel(stops_dict, bus_postcode, aberdeen_bus_station)
        # List comprehension to hold only the values of the rail_stations dictionary
        bus_result = [value for key, values in bus_stops.items() for value in values]
        # From Google Maps, the closest bus station to the postcode is Edinburgh bus station and is around 4 km
        # From Google Maps, the distance between Edinburgh bus station and Aberdeen bus station is around 200 km
        self.assertEqual(bus_result[0], 'Edinburgh bus station')
        # Using math.isclose() and assertTrue() to check the distances
        self.assertTrue(math.isclose(bus_result[1], 4, rel_tol=0.5))
        self.assertTrue(math.isclose(bus_result[2], 200, rel_tol=1))
        self.assertEqual(invalid, [])

    def test_car_travel(self):
        # Random Scottish postcode, generated using https://www.doogal.co.uk/PostcodeGenerator
        postcode = ['G42 9BJ']
        car_data, invalid = self.travel.car_travel(postcode)
        # From Google Maps, the distance between the postcode and the university is around 250 km
        self.assertTrue(math.isclose(car_data[postcode[0]], 250, rel_tol=1))
        self.assertEqual(invalid, [])

class AberdeenTest(unittest.TestCase):
    """Class to hold the test methods for aberdeen.py"""

    def setUp(self):
        # List of Aberdeen postcodes generated via https://www.ukpostcode.co.uk/random.htm
        # AB000XX is invalid postcode, so the distance should be 0
        self.students = ['AB241XZ', 'AB106RN', 'AB107JB', 'AB115QN', 'AB116UL', 'AB118RU', 'AB123FJ', 'AB000XX', 'AB125GL', 'AB243AD']
        # Percentages for each travel method
        self.car = 40
        self.taxi = 40
        self.bus = 10
        self.walk = 10   

    def test_distance_home_uni(self):
        distances = distance_home_uni(self.students)
        # List comprehension to hold only the values of the distances dictionary
        student_results = [value for key, value in distances.items()]
        # Expected distances for each postcode were calculated using https://www.doogal.co.uk/MeasureDistances
        # Using math.isclose() and assertTrue() to check the distances
        self.assertTrue(math.isclose(student_results[0], 1, rel_tol=0.2))
        self.assertTrue(math.isclose(student_results[1], 3, rel_tol=0.2))
        self.assertTrue(math.isclose(student_results[2], 4.8, rel_tol=0.2))
        self.assertTrue(math.isclose(student_results[3], 2.5, rel_tol=0.2))
        self.assertTrue(math.isclose(student_results[4], 3.1, rel_tol=0.2))
        self.assertTrue(math.isclose(student_results[5], 3.6, rel_tol=0.2))
        self.assertTrue(math.isclose(student_results[6], 7.6, rel_tol=0.2))
        # Invalid postcode is at position 7 and distance should be 0
        self.assertTrue(math.isclose(student_results[7], 0, rel_tol=0.2))
        self.assertTrue(math.isclose(student_results[8], 13, rel_tol=0.2))
        self.assertTrue(math.isclose(student_results[9], 0.3, rel_tol=0.05))

    def test_divide_aberdeen(self):
        distances = distance_home_uni(self.students)
        result = divide_aberdeen(distances, self.car, self.taxi, self.bus, self.walk)
        # Due to 40% of students using cars, 40% using taxis, 10% using buses and 10% walking
        # there should be 4 students using cars, 4 using taxis, 1 using buses and 1 walking
        # So for each list of transport, the total distance is callculated by summing the distances of each student
        # For the first 4 students (car), total distance should be around 12km
        # For the next 4 students (taxi), total distance should be around 15km
        # For the next student (bus), total distance should be around 12km
        # For the last student (walk), total distance should be around 0.3 km or under it
        self.assertTrue(math.isclose(result[0], 12, rel_tol=0.1))
        self.assertTrue(math.isclose(result[1], 15, rel_tol=0.1))
        self.assertTrue(math.isclose(result[2], 12, rel_tol=0.1))
        self.assertTrue(math.isclose(result[3], 0.3, rel_tol=0.01))
        

class CouncilTest(unittest.TestCase):
    """Class to hold the test methods for council_areas.py"""

    def setUp(self):
        # Postcodes from different council areas in Scotland, generated using https://www.doogal.co.uk/PostcodeGenerator
        # The last postcode is invalid
        self.council_postcodes = ["EH11 1EG", "G81 2NR", "DD2 4TZ", "FK15 0LN", "AB0 0XX"]

    def test_get_district(self):
        districts = get_district(self.council_postcodes)
        # Postcode council areas of each postcode below were found using https://www.doogal.co.uk/ShowMap 
        self.assertEqual(districts["EH11 1EG"], 'City of Edinburgh')
        self.assertEqual(districts["G81 2NR"], 'West Dunbartonshire')
        self.assertEqual(districts["DD2 4TZ"], 'Dundee City')
        self.assertEqual(districts["FK15 0LN"], 'Stirling')
        self.assertEqual(districts["AB0 0XX"], 'Unknown district')

    def test_group_district(self):
        districts = get_district(self.council_postcodes)
        grouped = group_district(districts)
        # There should be 5 council areas in total, including the invalid one
        self.assertEqual(len(grouped.values()), 5)
        # There should be 1 postcode for each council area
        self.assertEqual(len(grouped["City of Edinburgh"]), 1)
        self.assertEqual(len(grouped["West Dunbartonshire"]), 1)
        self.assertEqual(len(grouped["Dundee City"]), 1)
        self.assertEqual(len(grouped["Stirling"]), 1)
        self.assertEqual(len(grouped["Unknown district"]), 1)

    def test_find_percentages(self):
        districts = get_district(self.council_postcodes)
        grouped = group_district(districts)
        percentages = find_percentage(grouped, self.council_postcodes)
        # There are 5 council areas and 1 postcode for each of it
        # Therefore, the percentage of each postcode in relation to total postcodes should be 20%
        self.assertEqual(percentages['City of Edinburgh'], 20)
        self.assertEqual(percentages['West Dunbartonshire'], 20)
        self.assertEqual(percentages['Dundee City'], 20)
        self.assertEqual(percentages['Stirling'], 20)
        self.assertEqual(percentages['Unknown district'], 20)


if __name__ == '__main__':
    unittest.main()