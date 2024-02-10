# This file is for splitting the postcodes into two dataframes: one for Scotland and one for the rest of the UK.

import pandas as pd
from tkinter.filedialog import askopenfile
from itertools import islice

scot_postcodes = ['AB', 'DD', 'DG', 'EH', 'FK', 'G', 'HS', 'IV', 'KA', 'KW', 'KY', 'ML', 'PA', 'PH', 'TD', 'ZE']
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
        # addresses = check_postcodes(addresses)
        return addresses.iloc[:, 1]
    # If the user didn't select a file, then return an empty dataframe
    else:
        return pd.DataFrame()    
        

def determine_postcode():
    # Empty arrays to hold postcodes
    scotland = []
    england = []
    wales = []
    north_ireland = []

    # Addresses from file
    postcodes = create_address_df()

    for postcode in postcodes:
        # Account for incorrect postcodes
        if not isinstance(postcode, float) :
            # If the first one or two characters of the postcode are in the scot_postcodes list
            if postcode[:2] in scot_postcodes or postcode[:1] == 'G':
                scotland.append(postcode)
            elif postcode[:2] in wales_postcodes:
                wales.append(postcode)
            elif postcode[:2] == 'BT':
                north_ireland.append(postcode)
            else:
                england.append(postcode)
                
        else:
            continue

    return scotland, wales, north_ireland, england



# Initial menu to ask if you are working with Scottish or Rest of UK addresses
def menu(scotland, wales, north_ireland, england):
    start = True
    while start:
        print('1. Split Scottish postcodes')
        percent_bus = int(input('Enter what % of Scottish students travel by bus:'))
        percent_car = int(input('Enter what % of Scottish students travel by car:'))
        percent_rail = int(input('Enter what % of Scottish students travel by rail:'))

        # Calculate the number of postcodes for each transport method
        p_bus_scotland = int(len(scotland) * (percent_bus / 100))
        p_car_scotland = int(len(scotland) * (percent_car / 100))
        p_rail_scotland = int(len(scotland) * (percent_rail / 100))

        # Source: https://stackoverflow.com/questions/38861457/splitting-a-list-into-uneven-groups
        seclist = [p_bus_scotland, p_car_scotland, p_rail_scotland]
        it = iter(scotland)
        # randomly divide 'scotland' into 3 parts based on the percentages and make sure they don't overlap with islice
        bus, car, rail = [list(islice(it, 0, i)) for i in seclist]

        # List of lists to store the postcodes for each transport method
        transport_scot = [bus, car, rail]

        print('==================================================')
        print('2. Split rest-of-UK postcodes')
        percent_plane_uk = int(input('Enter what % of Non-Scottish students travel by plane:'))
        percent_car_uk = int(input('Enter what % of Non-Scottish students travel by car:'))
        percent_rail_uk = int(input('Enter what % of Non-Scottish students travel by rail:'))

        # Calculate the number of postcodes for each transport method
        p_plane_eng = int(len(england) * (percent_plane_uk / 100))
        p_car_eng = int(len(england) * (percent_car_uk / 100))
        p_rail_eng = int(len(england) * (percent_rail_uk / 100))
        # randomly divide 'uk' into 3 parts based on the percentages
        seclist_uk = [p_plane_eng, p_car_eng, p_rail_eng]

        # Iterator to split the list into 3 parts
        it_england = iter(england)
        # randomly divide 'england' into 3 parts based on the percentages and make sure they don't overlap with islice
        plane_eng, car_eng, rail_eng = [list(islice(it_england, 0, i)) for i in seclist_uk]

        # List of lists to store the postcodes for each transport method
        transport_eng = [plane_eng, car_eng, rail_eng]

        # Wales
        p_plane_wales = int(len(wales) * (percent_plane_uk / 100))
        p_car_wales = int(len(wales) * (percent_car_uk / 100))
        p_rail_wales = int(len(wales) * (percent_rail_uk / 100))

        # randomly divide 'wales' into 3 parts based on the percentages
        seclist_wales = [p_plane_wales, p_car_wales, p_rail_wales]
        it_wales = iter(wales)
        # randomly divide 'wales' into 3 parts based on the percentages and make sure they don't overlap with islice
        plane_wales, car_wales, rail_wales = [list(islice(it_wales, 0, i)) for i in seclist_wales]

        # List of lists to store the postcodes for each transport method
        transport_wales = [plane_wales, car_wales, rail_wales]

        # Northern Ireland
        p_plane_ni = int(len(north_ireland) * (percent_plane_uk / 100))
        p_car_ni = int(len(north_ireland) * (percent_car_uk / 100))
        p_rail_ni = int(len(north_ireland) * (percent_rail_uk / 100))

        # randomly divide 'north_ireland' into 3 parts based on the percentages
        seclist_ni = [p_plane_ni, p_car_ni, p_rail_ni]
        it_ni = iter(north_ireland)
        # randomly divide 'north_ireland' into 3 parts based on the percentages and make sure they don't overlap with islice
        plane_ni, car_ni, rail_ni = [list(islice(it_ni, 0, i)) for i in seclist_ni]

        # List of lists to store the postcodes for each transport method
        transport_ni = [plane_ni, car_ni, rail_ni]                
        
        # Stop the loop
        start = False

    return transport_scot, transport_eng, transport_wales, transport_ni
