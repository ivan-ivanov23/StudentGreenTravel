import pandas as pd
import geopy.distance

# Coordinates of Aberdeen airport and university (taken from Google)
aberdeen_airport = (57.2019004822,-2.1977798939)
aberdeen_uni = (57.1645,-2.0999)

# Read address file
addresses = pd.read_excel('data/Addresses.xlsx', engine='openpyxl')

# Read ukpostcodes.csv
postcodes = pd.read_csv('data/ukpostcodes.csv')
# Drop index column
postcodes = postcodes.drop(columns=['id'])

def postcode_coords(addresses, postcodes):
    """Returns a dictionary with postcodes as key and coordinates as value"""
    # Result dictionary to store distances
    result = {}

    for i in addresses['Home_Postcode']:
        for j in postcodes['postcode']:
            if i == j:
                # Save the longitude and latitude of the postcode in results dict with key being the postcode
                result[i] = [postcodes.loc[postcodes['postcode'] == i, 'latitude'].iloc[0], postcodes.loc[postcodes['postcode'] == i, 'longitude'].iloc[0]]

    return result

# Read in the airports csv file
airports = pd.read_csv("data/GBairports.csv")

def airports_coords(airports):
    """Returns a dictionary with UK public airports as key and coordinates as value"""
    airports_dict = {}

    # Add the airports to the airports_dict with the airport name as the key and the longitude and latitude as the value
    for i in airports['Unnamed: 0']:
        airports_dict[i] = [airports.loc[airports['Unnamed: 0'] == i, 'Latitude'].iloc[0], airports.loc[airports['Unnamed: 0'] == i, 'Longitude'].iloc[0]]

    return airports_dict


def calculate_distances(postcode, postcode_coords, airports_dict):
    distances = {}
    coords = (postcode_coords[postcode][0], postcode_coords[postcode][1])
    # Find distance between coords and all airports
    # Create a new dict to store the distances with the airport as the key and the distance as the value
    for i in airports_dict:
        # https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
        distances[i] = round(geopy.distance.geodesic(coords, (airports_dict[i][0], airports_dict[i][1])).km,2)

    return distances


def closest_airport(postcode, postcode_coords, airports_dict):
    """Returns the closest airport to the postcode"""
    distances = calculate_distances(postcode, postcode_coords, airports_dict)
    return min(distances, key=distances.get)


def travel(closest_airport, postcode_coords, airports_dict):
    """Returns a dictionary with postcodes as key and closest airport as value"""
    for i in addresses['Home_Postcode']:
        airport = closest_airport(i, postcode_coords(addresses, postcodes), airports_coords(airports))
        distance = min(calculate_distances(i, postcode_coords(addresses, postcodes), airports_coords(airports)).values())
        print(f'Closest airport to {i} is {airport} ~ {distance} km')
        # Get longitude and latitude of the airport
        cur_airport = (airports_dict[airport][0], airports_dict[airport][1])
        # Calculate the distance between the two airports
        travel_distance = round(geopy.distance.distance(cur_airport, aberdeen_airport).km,2)
        print(f'The distance between {airport} and Aberdeen airport is {travel_distance} km')
        print('====================================================================================================')
        
    # Print the distance between the Aberdeen airport and the university
    uni_airport_distance = round(geopy.distance.distance(aberdeen_airport, aberdeen_uni).km,2)
    print(f'The distance between Aberdeen airport and the university is {uni_airport_distance} km')


travel(closest_airport, postcode_coords, airports_coords(airports))


    