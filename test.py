import requests
import pandas as pd
from utils import split_list
from council_areas import *
import math

# address = pd.read_excel('datasets/UK & Home Student Data 2022-2023.xlsx')

# # Turn the postcodes into a list
# postcodes = address['Home_Postcode'].tolist()

# # For each postcode in the list, find the country its longitude and latitude from postcodes.io
# result = {}
# country_postcodes = split_list(postcodes)
# for part in country_postcodes:
#     data = {"postcodes": part}
#     response = requests.post("https://api.postcodes.io/postcodes", json=data)
#     if response.status_code == 200:
#         response_json = response.json()
#         for item in response_json["result"]:
#             # Postcode taken from the query
#             postcode = item["query"]
#             if item["result"] is None:
#                 result[postcode] = 'Uknown location'
#             else:
#                 if item["result"]["longitude"] and item["result"]["latitude"]:
#                     result[postcode] = (item["result"]["longitude"], item["result"]["latitude"])
#                 else:
#                     result[postcode] = 'Uknown location'

# print(result)

postcodes = pd.read_excel('datasets/Test.xlsx')
# Drop nan values
postcodes = postcodes.dropna()
# Take the second column of the excel file
postcodes = postcodes.iloc[:, 1].tolist()


council = get_district(postcodes)
grouped = group_district(council)
percent = find_percentage(grouped, postcodes)

total_distance = 10000
car_distance = 5000
bus_distance = 2000
train_distance = 3000

car = {}
bus = {}
train = {}

rounding_error = 0
for key, value in percent.items():
    car[key] = value * car_distance / 100
    bus[key] = value * bus_distance / 100
    train[key] = value * train_distance / 100

total_car = sum(car.values())
total_bus = sum(bus.values())
total_train = sum(train.values())

# Round the total distance
total_new = round(total_car + total_bus + total_train)


# Compare total distances
if total_distance == total_new:
    print('The total distance is the same')
else:
    print(f'The total distance is not the same. The distance initially was {total_distance} and now it is {total_new}')
    

if car_distance != total_car:
    # Add the rounding error to the car['Uknown district']
    car['Uknown district'] += car_distance - total_car

if bus_distance != total_bus:
    # Add the rounding error to the bus['Uknown district']
    bus['Uknown district'] += bus_distance - total_bus

if train_distance != total_train:
    # Add the rounding error to the train['Uknown district']
    train['Uknown district'] += train_distance - total_train

total_new = sum(car.values()) + sum(bus.values()) + sum(train.values())

# Compare total distances
if total_distance == total_new:
    print('The total distance is the same')
else:
    print(f'The total distance is not the same. The distance initially was {total_distance} and now it is {total_new}')

