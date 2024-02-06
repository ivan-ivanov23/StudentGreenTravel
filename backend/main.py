from tkinter.filedialog import askopenfile
from split_postcodes import create_address_df, determine_postcode
from emissions import bus_emissions, plane_emissions
from flying_distance import travel, postcode_coord_dict, airport_coord_dict
from land_distance import land_travel, postcode_coord_dict, stop_coord_dict

def main():
    # Call the create_address_df function and pass the file to it
    addresses = create_address_df(askopenfile(filetypes=[("Excel files", "*.xlsx")]))
    # Call the determine_postcode function and pass the postcode column to it
    scotland, rest = determine_postcode(addresses.iloc[:, 1])

    # Call the land_travel function and pass the postcode coordinates, stop coordinates, and the rest of the postcodes to it
    # The [0] index is used to get the dictionary with postcodes as keys and closest stops/airports as values
    # If the [1] index is used, the list of invalid postcodes is returned
    land = land_travel(postcode_coord_dict, stop_coord_dict, scotland)[0]
    # Call the travel function and pass the postcode coordinates, airport coordinates, and the rest of the postcodes to it
    fly = travel(postcode_coord_dict, airport_coord_dict, rest)[0]

    # Call the bus_emissions function and pass the land dictionary and the emission factors to it
    bus = bus_emissions(land)
    # Call the plane_emissions function and pass the fly dictionary and the emission factors to it
    plane = plane_emissions(fly)

    print('Bus: ', bus)
    print('===========================================================================================================================')
    print('Plane: ', plane)


if __name__ == '__main__':
    main()
