# Load and filter Stops.csv
import pandas as pd
import numpy as np

# Read Stops.csv
stops = pd.read_csv('data/Stops.csv')
# Drop all columns apart from CommonName, StopType, Latitude, Longitude
stops = stops[['CommonName', 'StopType', 'Latitude', 'Longitude']]

#print(stops)

# Filter stops to only include BCT, RSE, RLY, RPL, BCE, BST, BCS, BCQ stops
stops = stops[stops['StopType'].isin(['BCT', 'RSE', 'RLY', 'RPL', 'BCE', 'BST', 'BCS', 'BCQ'])]

# Drop all rows with NaN values
stops = stops.dropna()

# Save filtered stops to csv
stops.to_csv('data/FilteredStops.csv')
