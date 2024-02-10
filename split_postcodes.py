# This file is for splitting the postcodes into two dataframes: one for Scotland and one for the rest of the UK.

import pandas as pd
import random
from tkinter.filedialog import askopenfile

scot_postcodes = ['AB', 'DD', 'DG', 'EH', 'FK', 'G', 'HS', 'IV', 'KA', 'KW', 'KY', 'ML', 'PA', 'PH', 'TD', 'ZE']
wales_postcodes = ['CF', 'LL', 'NP', 'SA', 'SY']

def create_address_df():
    # Open a file dialog to select the address file
    file = askopenfile(filetypes=[("Excel files", "*.xlsx")])
    # If the user selected a file, then read it using pandas
    if file:
        # Read address file
        addresses = pd.read_excel(file.name, engine='openpyxl')
        # Drop any rows with missing values
        addresses = addresses.dropna()
        # Trim the postcode column
        addresses.iloc[:, 1] = addresses.iloc[:, 1].str.replace(' ', '')
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


scotland, wales, north_ireland, england = determine_postcode()

# print('Scotland: ', scotland)
# print('===============================================================================================================')
# print('Wales: ', wales)
# print('===============================================================================================================')
# print('Northern Ireland: ', north_ireland)
# print('===============================================================================================================')
# print('England: ', england)

# username = int(input("Enter username:"))
# print(username)

# Initial menu to ask if you are working with Scottish or Rest of UK addresses
def menu(scotland, wales, north_ireland, england):
    start = True
    while start:
        print('1. Split Scottish postcodes')
        percent_bus = int(input('Enter what % of Scottish students travel by bus:'))
        percent_car = int(input('Enter what % of Scottish students travel by car:'))
        percent_rail = int(input('Enter what % of Scottish students travel by rail:'))
        if percent_bus + percent_car + percent_rail != 100:
            # Call the menu function again if the percentages don't add up to 100
            print('The percentages do not add up to 100. Try again!')
            print('==================================================')
            menu(scotland, wales, north_ireland, england)
        # randomly divide 'scotland' into 3 parts based on the percentages and make sure they don't overlap
        bus = random.sample(scotland, int(len(scotland) * (percent_bus / 100)))
        # remove the elements of bus from scotland using set difference
        scotland = list(set(scotland) - set(bus))
        car = random.sample(scotland, int(len(scotland) * (percent_car / 100)))
        scotland = list(set(scotland) - set(car))
        rail = random.sample(scotland, int(len(scotland) * (percent_rail / 100)))
        scotland = list(set(scotland) - set(rail))

        print('==================================================')
        print('2. Split rest-of-UK postcodes')
        percent_plane_uk = int(input('Enter what % of Non-Scottish students travel by plane:'))
        percent_car_uk = int(input('Enter what % of Non-Scottish students travel by car:'))
        percent_rail_uk = int(input('Enter what % of Non-Scottish students travel by rail:'))
        if percent_plane_uk + percent_car_uk + percent_rail_uk != 100:
            print('The percentages do not add up to 100. Try again!')
            percent_plane_uk = int(input('Enter what % of students travel by plane:'))
            percent_car_uk = int(input('Enter what % of students travel by car:'))
            percent_rail_uk = int(input('Enter what % of students travel by rail:'))
        # combine 'wales', 'north_ireland', and 'england' into one list
        uk = wales + north_ireland + england
        # randomly divide 'uk' into 3 parts based on the percentages and make sure they don't overlap for car, train and plane
        car_uk = random.sample(uk, int(len(uk) * (percent_car_uk / 100)))
        # remove the elements of car_uk from uk using set difference
        uk = list(set(uk) - set(car_uk))
        rail_uk = random.sample(uk, int(len(uk) * (percent_rail_uk / 100)))
        uk = list(set(uk) - set(rail_uk))
        plane_uk = random.sample(uk, int(len(uk) * (percent_plane_uk / 100)))
        uk = list(set(uk) - set(plane_uk))
            
        
        start = False

    return bus, car, rail, car_uk, rail_uk, plane_uk

bus_scotland, car_scotland, rail_scotland, car_uk, rail_uk, plane_uk = menu(scotland, wales, north_ireland, england)
