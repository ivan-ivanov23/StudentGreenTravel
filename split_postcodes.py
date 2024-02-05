# This file is for splitting the postcodes into two dataframes: one for Scotland and one for the rest of the UK.

import pandas as pd
import numpy as np
from tkinter.filedialog import askopenfile

scot_postcodes = ['AB', 'DD', 'DG', 'EH', 'FK', 'G', 'HS', 'IV', 'KA', 'KW', 'KY', 'ML', 'PA', 'PH', 'TD', 'ZE']
wales_postcodes = ['CF', 'LL', 'NP', 'SA', 'SY']

# open file explorer for excel files only so that it is utf-8 encoded
file = askopenfile(filetypes=[("Excel files", "*.xlsx")])
# If the user selected a file, then read it using pandas
if file:
# Read address file
    addresses = pd.read_excel(file.name, engine='openpyxl')
    # Drop any rows with missing values
    addresses = addresses.dropna()
    # Trim the postcode column
    addresses.iloc[:, 1] = addresses.iloc[:, 1].str.replace(' ', '')
# Else, close the program
else:
    exit()

# empty  array of postcodes for scotland
scotland = []
# empty array of postcodes for the rest of the UK
rest = []

def determine_postcode(postcodes):
    result = []
    for postcode in postcodes:
        # Account for incorrect postcodes
        if not isinstance(postcode, float):
            # If the first one or two characters of the postcode are in the scot_postcodes list
            if postcode[:2] in scot_postcodes or postcode[:1] == 'G':
                scotland.append(postcode)
            else:
                rest.append(postcode)
        else:
            continue

    return scotland, rest

scotland, rest = determine_postcode(addresses.iloc[:, 1])

# Convert scotland and rest to numpy arrays
scotland = np.array(scotland)
rest = np.array(rest)
