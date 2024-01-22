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
            
# coords_2 is the longitude and latitude of the first postcode in the results dict which is HA9 0WS
coords_2 = (result[df['Home_Postcode'][0]][0], result[df['Home_Postcode'][0]][1])

airports_dict = {}
# Read in the airports csv file
df_airports = pd.read_csv("GBairports.csv")
# Add the airports to the airports_dict with the airport name as the key and the longitude and latitude as the value
for i in df_airports['Unnamed: 0']:
    airports_dict[i] = [df_airports.loc[df_airports['Unnamed: 0'] == i, 'Latitude'].iloc[0], df_airports.loc[df_airports['Unnamed: 0'] == i, 'Longitude'].iloc[0]]



# Find distance between coords_2 and all airports
# Create a new dict to store the distances with the airport as the key and the distance as the value
distances = {}
for i in airports_dict:
    # https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    distances[i] = round(geopy.distance.geodesic(coords_2, (airports_dict[i][0], airports_dict[i][1])).km,2)


# Select the airport with the smallest distance and print the distance and the airport
# print the postcode that we are using
print('Closest airport to', df['Home_Postcode'][0], 'is:', min(distances, key=distances.get), "~", min(distances.values()),"km")
airport = min(distances, key=distances.get)

# Get the longitude and latitude of the airport and of aberdeen airport
cur_airport = (airports_dict[airport][0], airports_dict[airport][1])
# Data from GBairports.csv
aberdeen_airport = (57.2019004822,-2.1977798939)

# Calculate the distance between the two airports
travel_distance = round(geopy.distance.distance(cur_airport, aberdeen_airport).km,2)
print('Distance between', airport, 'and Aberdeen Airport is:', travel_distance, 'km')

# University of Aberdeen longitude and latitude from Google Maps
aberdeen_uni = (57.1645,-2.0999)
# Calculate the distance between the aberdeen_uni and aberdeen_airport
uni_distance = round(geopy.distance.distance(aberdeen_uni, aberdeen_airport).km,2)
print('Distance between University of Aberdeen and Aberdeen Airport is:', uni_distance, 'km')
