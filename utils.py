# This file contains utility functions used in other files

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
    seclist = [car_share, taxi_share, bus_share]
    it = iter(initial_distances_list)
    car_list, taxi_list, bus_list = [list(islice(it, 0, i)) for i in seclist]

    # Sum the distances to get total travelled distances
    # by each method of transport
    total_car = np.sum(car_list)
    total_taxi = np.sum(taxi_list)
    total_bus = np.sum(bus_list)

    return total_car, total_taxi, total_bus