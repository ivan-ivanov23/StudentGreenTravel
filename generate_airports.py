# This file was used to generate the airports.csv file which  contains only the public UK airports and their longitude and latitude
# This filtering was done manually in Excel with the help of wikipedia

import airportsdata
import pandas as pd

airports = airportsdata.load('IATA')  # key is the IATA location code
# Add all UK airports to a dict with their city as the key and longitude and latitude as the value
airports_dict = {}
for i in airports:
    if airports[i]['country'] == 'GB':
        airports_dict[airports[i]['name']] = [airports[i]['lat'], airports[i]['lon']]
# print(airports_dict)
        
# Save airports_dict to a csv file
df_airports = pd.DataFrame.from_dict(airports_dict, orient='index', columns=['Latitude', 'Longitude'])
df_airports.to_csv('data/airports.csv')
