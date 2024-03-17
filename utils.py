# This file contains utility functions used in other files
# Sources of code snippets are provided in the comments of functions.
# Author: Ivan Ivanov

import numpy as np
from itertools import islice, accumulate
import math
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    car_share = math.ceil(len(initial_distances_list) * (p_car / 100))
    taxi_share = math.ceil(len(initial_distances_list) * (p_taxi / 100))
    bus_share = len(initial_distances_list) - car_share - taxi_share

    # Divide the all_initial list into 3 lists,
    # one for each mode of transport according to the percentages 
    # without overlapping
    # Inspired by  Method 3 in https://www.geeksforgeeks.org/python-split-list-in-uneven-groups/
    seclist = [car_share, taxi_share, bus_share]
    res = [list(islice(initial_distances_list, start, end)) for start, end in zip([0]+list(accumulate(seclist)), accumulate(seclist))]

    # Sum the distances to get total travelled distances
    # by each method of transport
    total_car = np.sum(res[0])
    total_taxi = np.sum(res[1])
    total_bus = np.sum(res[2])

    return total_car, total_taxi, total_bus

def split_list(lst, chunk_size=100):
    # Source: https://www.altcademy.com/blog/how-to-split-a-list-in-python/#method-4-using-the-enumerate-function
    chunks = [[] for _ in range((len(lst) + chunk_size - 1) // chunk_size)]
    for i, item in enumerate(lst):
        chunks[i // chunk_size].append(item)
    return chunks

def create_dfs(transport: dict, emission_factor: float, num_trips: int):
    df_transport = pd.DataFrame(transport)
    # Multiply the distances by the number of trips to get the total distance
    df_transport = df_transport * num_trips
    # Multiply the distances by the emission factor to get the emissions
    df_emissions = df_transport * emission_factor
    df_transport = round(df_transport, 1)
    df_emissions = round(df_emissions, 1)
    return df_transport, df_emissions

def create_px(df: pd.DataFrame, title: str, color_vals: str, color_scheme: str):
    fig = px.imshow(df, text_auto=True, aspect='auto', title=title,
                    labels=dict(x="Country", y="Transport", color=color_vals),
                    color_continuous_scale=color_scheme)
    fig.update_traces(textfont_size=16)

    return fig

def create_go_bar(df: pd.DataFrame, title, ytitle):
    fig = go.Figure(
        data=[go.Bar(x=df.columns, y=df.iloc[0, :], text=df.iloc[0, :], textposition='auto')],
        layout=go.Layout(title=title, xaxis=dict(title='Council Area'), yaxis=dict(title=ytitle))
    )
    fig.update_xaxes(categoryorder='category ascending')
    return fig

def create_go_table(df: pd.DataFrame, values: list, title: str):
    fig = go.Figure(
            data=[go.Table( header=dict(values=values),
                            cells=dict(values=[df.columns, df.iloc[0, :]]))],
            layout=go.Layout(title=title)
        )
    fig.update_xaxes(categoryorder='category ascending')
    return fig

def divide_combo_percentages(dict1: dict):
    dict_land = [int(i) for key, i in dict1.items()][:4]
    dict_air = [int(i) for key, i in dict1.items()][4:]
    return dict_land, dict_air