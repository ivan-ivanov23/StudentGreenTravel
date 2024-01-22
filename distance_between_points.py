import pandas as pd
import geopy.distance


# Open addresses file and for each postcode, get the longitude and latitude from ukpostcodes.csv
# Then calculate the distance between the two points
# Read in the addresses file
df = pd.read_excel("Addresses.xlsx", engine='openpyxl')

# Create a new dataframe to store the results
df_results = pd.DataFrame(columns=['Postcode', 'Latitude', 'Longitude', 'Distance'])

# Read in the ukpostcodes.csv file
df_postcodes = pd.read_csv("ukpostcodes.csv")
# Drop the index column
df_postcodes = df_postcodes.drop(columns=['id'])

# print the first Home_Postcode to check it is working
# print(df['Home_Postcode'][0])

result = {}

for i in df['Home_Postcode']:
    for j in df_postcodes['postcode']:
        if i == j:
            # Save the longitude and latitude of the postcode in results dict with key being the postcode
            result[i] = [df_postcodes.loc[df_postcodes['postcode'] == i, 'latitude'].iloc[0], df_postcodes.loc[df_postcodes['postcode'] == i, 'longitude'].iloc[0]]

# print(result)

# Get the longitude and latitude of uni of aberdeen AB24 3FX from ukpostcodes.csv
uni_lat = df_postcodes.loc[df_postcodes['postcode'] == 'AB24 3FX', 'latitude'].iloc[0]
# print("Uni of Aberdeen latitude: ", uni_lat)
uni_long = df_postcodes.loc[df_postcodes['postcode'] == 'AB24 3FX', 'longitude'].iloc[0]
# print("Uni of Aberdeen longitude: ", uni_long)

coords_1 = (uni_lat, uni_long)
# coords_2 is the longitude and latitude of the first postcode in the results dict which is HA9 0WS
# coords_2 = (result['HA9 0WS'][0], result['HA9 0WS'][1])
# Try doing it without hardcoding the postcode
coords_2 = (result[df['Home_Postcode'][0]][0], result[df['Home_Postcode'][0]][1])


# https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
# print(round(geopy.distance.geodesic(coords_1, coords_2).km,2), "km")

import airportsdata
import pgeocode
airports = airportsdata.load('IATA')  # key is the IATA location code
# Add all UK airports to a dict with their city as the key and longitude and latitude as the value
airports_dict = {}
for i in airports:
    if airports[i]['country'] == 'GB':
        airports_dict[airports[i]['city']] = [airports[i]['lat'], airports[i]['lon']]
# print(airports_dict)

# Find distance between coords_2 and all airports
# Create a new dict to store the distances with the airport as the key and the distance as the value
distances = {}
for i in airports_dict:
    distances[i] = round(geopy.distance.geodesic(coords_2, (airports_dict[i][0], airports_dict[i][1])).km,2)

# Select the airport with the smallest distance and print the distance and the airport
# print the postcode that we are using
print('Closest airport to', df['Home_Postcode'][0], 'is: ')
print(min(distances, key=distances.get), min(distances.values()), "km")




