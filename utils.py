# This file contains utility functions used in other files
# Sources of code snippets are provided in the comments of each function.
# Author: Ivan Ivanov

import numpy as np
from itertools import islice

def extract_distances(data: dict):
    """Used for extracting bus, plane and train distances from the data dictionary"""
    return np.array([value[2] for value in data.values()])

def extract_car_distances(data: dict):
    """Used for extracting car distances from the data dictionary"""
    return np.array([value for value in data.values()])

def init_leg(initial_distances_list: list):
    # Percentages for method of transport for initial leg of journey
    # i.e., from home to transport hub
    p_car = 40
    p_taxi = 40
    p_bus = 20

    # Share of students travelling by each method
    car_share = int(len(initial_distances_list) * (p_car / 100))
    taxi_share = int(len(initial_distances_list) * (p_taxi / 100))
    bus_share = int(len(initial_distances_list) * (p_bus / 100))

    # Divide the all_initial list into 3 lists,
    # one for each mode of transport according to the percentages 
    # without overlapping
    # Inspired by answer from senderle: https://stackoverflow.com/questions/312443/how-do-i-split-a-list-into-equally-sized-chunks
    seclist = [car_share, taxi_share, bus_share]
    it = iter(initial_distances_list)
    car_list, taxi_list, bus_list = [list(islice(it, 0, i)) for i in seclist]

    # Sum the distances to get total travelled distances
    # by each method of transport
    total_car = np.sum(car_list)
    total_taxi = np.sum(taxi_list)
    total_bus = np.sum(bus_list)

    return total_car, total_taxi, total_bus

def split_list(lst, chunk_size=100):
    # Source: https://www.altcademy.com/blog/how-to-split-a-list-in-python/#method-4-using-the-enumerate-function
    chunks = [[] for _ in range((len(lst) + chunk_size - 1) // chunk_size)]
    for i, item in enumerate(lst):
        chunks[i // chunk_size].append(item)
    return chunks