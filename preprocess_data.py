import pandas as pd
import pandas as pd
from tkinter.filedialog import askopenfile
from itertools import islice

# Read ukpostcodes.csv
# Source: https://www.statology.org/pandas-read_csv-usecols/ 
ukpostcodes = pd.read_csv('data/ukpostcodes.csv', usecols=['postcode', 'latitude', 'longitude'])
ukpostcodes['postcode'] = ukpostcodes['postcode'].str.replace(' ', '')
ukpostcode_coords = dict(zip(ukpostcodes['postcode'], zip(ukpostcodes['latitude'], ukpostcodes['longitude'])))

# Read Scotland_Bus_Stations.csv
bus_stops = pd.read_csv("data/Scotland_Bus_Stations.csv", usecols=['StationName', 'Latitude', 'Longitude'])
stops_dict = dict(zip(bus_stops['StationName'], zip(bus_stops['Latitude'], bus_stops['Longitude'])))

# Read Railway Stations
rail_stations = pd.read_csv("data/stations.csv", usecols=['Station', 'Lat', 'Long'])
stations_dict = dict(zip(rail_stations['Station'], zip(rail_stations['Lat'], rail_stations['Long'])))

# Read airports
airports = pd.read_csv("data/GBairports.csv", usecols=['Unnamed: 0', 'Latitude', 'Longitude'])
airports_dict = dict(zip(airports['Unnamed: 0'], zip(airports['Latitude'], airports['Longitude'])))

scot_postcodes = ['AB', 'DD', 'DG', 'EH', 'FK', 'G', 'HS', 'IV', 'KA', 'KW', 'KY', 'ML', 'PA', 'PH', 'TD', 'ZE']
eng_postcodes = ['AL', 'B', 'BA', 'BB', 'BD', 'BH', 'BL', 'BN', 'BR', 'BS', 'CA', 'CB', 'CF', 'CH', 'CM', 'CO', 'CR', 'CT', 'CV', 'CW', 'DA', 'DE', 'DH', 'DL', 'DN', 'DT', 'DY', 'E', 'EC', 'EN', 'EX', 'FY', 'GL', 'GU', 'HA', 'HD', 'HG', 'HP', 'HR', 'HU', 'HX', 'IG', 'IP', 'KT', 'L', 'LA', 'LD', 'LE', 'LN', 'LS', 'LU', 'M', 'ME', 'MK', 'N', 'NE', 'NG', 'NN', 'NP', 'NR', 'NW', 'OL', 'OX', 'PE', 'PL', 'PO', 'PR', 'RG', 'RH', 'RM', 'S', 'SE', 'SG', 'SK', 'SL', 'SM', 'SN', 'SO', 'SP', 'SR', 'SS', 'ST', 'SW', 'TA', 'TF', 'TN', 'TQ', 'TR', 'TS', 'TW', 'UB', 'W', 'WA', 'WC', 'WD', 'WF', 'WN', 'WR', 'WS', 'WV', 'YO']
wales_postcodes = ['CF', 'LL', 'NP', 'SA', 'SY']


def create_address_df():
    # Open a file dialog to select the address file
    file = askopenfile(filetypes=[("Excel files", "*.xlsx")])
    # If the user selected a file, then read it using pandas
    if file:
        # Read address file
        addresses = pd.read_excel(file.name, engine='openpyxl')
        # Trim the postcode column
        addresses.iloc[:, 1] = addresses.iloc[:, 1].str.replace(' ', '')

        # Call the check_postcodes function to check for incorrect postcodes
        return addresses.iloc[:, 1]
    # If the user didn't select a file, then return an empty dataframe
    else:
        return pd.DataFrame()    
        

def determine_postcode(postcodes):
    # postcodes = create_address_df().dropna()  # Drop NaN values
    scotland = postcodes[postcodes.str[:2].isin(scot_postcodes) | (postcodes.str[:1] == 'G')]
    england = postcodes[(postcodes.str[:2].isin(eng_postcodes) | (postcodes.str[:1].isin(eng_postcodes)))]
    wales = postcodes[postcodes.str[:2].isin(wales_postcodes)]
    north_ireland = postcodes[postcodes.str[:2] == 'BT']
    return scotland, wales, north_ireland, england


def divide_scot_addresses(scot_addresses: list,  p_bus, p_car, p_rail):
    """The function divides the list of Scottish postcodes into 3 parts based on the percentages of each transport method."""
    # Scotland
    percent_bus = p_bus
    percent_car = p_car
    percent_rail = p_rail

    # Calculate the number of postcodes for each transport method
    p_bus_scotland = int(len(scot_addresses) * (percent_bus / 100))
    p_car_scotland = int(len(scot_addresses) * (percent_car / 100))
    p_rail_scotland = int(len(scot_addresses) * (percent_rail / 100))

    # Source: https://stackoverflow.com/questions/38861457/splitting-a-list-into-uneven-groups
    seclist = [p_bus_scotland, p_car_scotland, p_rail_scotland]
    it = iter(scot_addresses)
    # randomly divide 'scotland' into 3 parts based on the percentages and make sure they don't overlap with islice
    bus, car, rail = [list(islice(it, 0, i)) for i in seclist]

    # List of lists to store the postcodes for each transport method
    transport_scot = [bus, car, rail]

    return transport_scot

def divide_uk_addresses(country: list, p_plane, p_car, p_rail):
    """The function divides the list of UK postcodes into 3 parts based on the percentages of each transport method.
        It is used for England, Wales and Northern Ireland."""
    percent_plane_uk = p_plane
    percent_car_uk = p_car
    percent_rail_uk = p_rail

    # Calculate the number of postcodes for each transport method
    p_plane_eng = int(len(country) * (percent_plane_uk / 100))
    p_car_eng = int(len(country) * (percent_car_uk / 100))
    p_rail_eng = int(len(country) * (percent_rail_uk / 100))
    # randomly divide 'uk' into 3 parts based on the percentages
    seclist_uk = [p_plane_eng, p_car_eng, p_rail_eng]

    # Iterator to split the list into 3 parts
    it = iter(country)
    # randomly divide 'england' into 3 parts based on the percentages and make sure they don't overlap with islice
    plane_eng, car_eng, rail_eng = [list(islice(it, 0, i)) for i in seclist_uk]

    # List of lists to store the postcodes for each transport method
    transport = [plane_eng, car_eng, rail_eng]

    return transport
