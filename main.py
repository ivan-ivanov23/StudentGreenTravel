import threading
import time
import pandas as pd
from itertools import cycle
from split_postcodes import determine_postcode
from emissions import bus_emissions, plane_emissions
from flying_distance import travel, postcode_coord_dict, airport_coord_dict
from bus_distance import land_travel, postcode_coord_dict, stop_coord_dict
from rail_distance import rail_travel, postcode_coords, station_coords
from total_distance import total_distance, create_heatmap

def loading_message(stop_event):
    # Cycle of loading states
    loading_states = cycle(["Loading.", "Loading..", "Loading...", "Loading...."])
    
    # This function displays a cycling loading message while the main function is running
    while not stop_event.is_set():
        loading_state = next(loading_states)
        print(loading_state, end="\r")  # Use carriage return to overwrite the previous line
        # Sleep for 0.3 seconds
        time.sleep(0.3)
        # If the loading message is "Loading...", start from the beginning
        if loading_state == "Loading....":
            # Sleep for 0.5 seconds
            time.sleep(0.5)
            # clear the line
            print(" " * len(loading_state), end="\r")
            # Start from the beginning
            loading_states = cycle(["Loading.", "Loading..", "Loading...", "Loading...."])

def main():
    stop_event = threading.Event()  # Event to signal the loading thread to stop

    # Create a thread to display the loading message
    loading_thread = threading.Thread(target=loading_message, args=(stop_event,))
    loading_thread.start()

    # Call the determine_postcode function to get the postcodes for Scotland and the rest of the UK
    scotland, rest = determine_postcode()
    # Stop main function if there are no postcodes

    # Call the land_travel function and pass the postcode coordinates, stop coordinates, and the rest of the postcodes to it
    # The [0] index is used to get the dictionary with postcodes as keys and closest stops/airports as values
    # If the [1] index is used, the list of invalid postcodes is returned
    land = land_travel(postcode_coord_dict, stop_coord_dict, scotland)[0]
    # Call the travel function and pass the postcode coordinates, airport coordinates, and the rest of the postcodes to it
    fly = travel(postcode_coord_dict, airport_coord_dict, rest)[0]
    # Call the rail_travel function and pass the postcode coordinates, stop coordinates, and the rest of the postcodes to it
    rail = rail_travel(postcode_coords, station_coords, rest)[0]
    print(rail)
    

    # Call the total_distance function and pass the land and fly dictionaries to it
    total_distances_plane = total_distance(fly)
    #total_distances_bus = total_distance(land)
    
    # Create a heatmap of the UK showing the total distance travelled by bus and plane by country
    #create_heatmap(total_distances_bus, total_distances_plane)

    # Call the bus_emissions function and pass the land dictionary and the emission factors to it
    #bus = bus_emissions(land)
    # Call the plane_emissions function and pass the fly dictionary and the emission factors to it
    plane = plane_emissions(fly)

    # Print the results
    # print('\nBus: ', bus)
    # print('===========================================================================================================================')
    # print('Plane: ', plane)

    # Save the results to separate dataframes
    #bus_df = pd.DataFrame(bus.items(), columns=['Postcode', 'Emissions'])
    plane_df = pd.DataFrame(plane.items(), columns=['Postcode', 'Emissions'])

    
    # Signal the loading thread to stop
    stop_event.set()
    # Wait for the loading thread to stop
    loading_thread.join()

    return  plane_df

if __name__ == '__main__':
    main()
