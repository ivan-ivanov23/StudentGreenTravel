from geopy.distance import geodesic
from itertools import islice, accumulate
import requests
from utils import split_list

aberdeen_uni = (57.1661, -2.1065)


def distance_home_uni(students: list):
    """The function calculates the distance from the students' homes to the university based on the mode of transport they use to travel from home to Aberdeen."""
    distances = {}
    students = split_list(students)
    for part in students:
        data = {"postcodes": part}
        response = requests.post("https://api.postcodes.io/postcodes", json=data)
        if response.status_code == 200:
            response_json = response.json()
            for item in response_json["result"]:
                # Postcode taken from the query
                postcode = item["query"]
                if item["result"] is None:
                    distances[postcode] = 0
                else:
                    lat = item["result"]["latitude"]
                    lon = item["result"]["longitude"]
                    home = (lat, lon)
                    distance = geodesic(home, aberdeen_uni).kilometers
                    distances[postcode] = distance

    return distances


def divide_aberdeen(distances: dict, p_car, p_taxi, p_bus, p_walk):
    len_students = len(distances)
    p_car = int((p_car / 100) * len_students)
    p_taxi = int((p_taxi / 100) * len_students)
    p_bus = int((p_bus / 100) * len_students)
    p_walk = int((p_walk / 100) * len_students)

    seclist = [p_car, p_taxi, p_bus, p_walk]
    
    # Divide the all_initial list into 4 lists,
    # Source: Method 3 in https://www.geeksforgeeks.org/python-split-list-in-uneven-groups/
    res = [list(islice(distances, start, end)) for start, end in zip([0]+list(accumulate(seclist)), accumulate(seclist))]

    car = res[0]
    taxi = res[1]
    bus = res[2]
    walk = res[3]

    # # Calculate the total distance for each mode of transport
    total_car = sum([distances[student] for student in car])
    total_taxi = sum([distances[student] for student in taxi])
    total_bus = sum([distances[student] for student in bus])
    total_walk = sum([distances[student] for student in walk])

    total_car = round(total_car, 1)
    total_taxi = round(total_taxi, 1)
    total_bus = round(total_bus, 1)
    total_walk = round(total_walk, 1)

    total_aberdeen = [total_car, total_taxi, total_bus, total_walk]

    return total_aberdeen


# Test the function
# students = ['AB101XG', 'AB106RN', 'AB107JB', 'AB115QN', 'AB116UL', 'AB118RU', 'AB123FJ', 'AB124NQ', 'AB125GL']
# car = 40
# taxi = 40
# bus = 20
# walk = 0

# distances = distance_home_uni(students)
# print(divide_aberdeen(distances, car, taxi, bus, walk))