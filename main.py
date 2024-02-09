import threading
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random
from itertools import cycle
from split_postcodes import determine_postcode
from land_distance import postcode_coord_dict, stop_coord_dict, land_travel

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
    # stop_event = threading.Event()  # Event to signal the loading thread to stop

    # # Create a thread to display the loading message
    # loading_thread = threading.Thread(target=loading_message, args=(stop_event,))
    # loading_thread.start()

    # Call the determine_postcode function to get the postcodes for Scotland, Aberdeen, and the rest of the UK
    scotland, rest, aberdeen = determine_postcode()

    # For Scotland
    # 46% of postcodes travel by car
    # 46% of postcodes travel by bus
    # 8% of postcodes travel by train
    # 0% of postcodes travel by plane
    # Create lists of postcodes for each method of transport
    #scotland_car = random.sample(scotland, int(len(scotland) * 0.46))
    scotland_bus = random.sample(scotland, int(len(scotland) * 0.46))
    scotland_rail = random.sample(scotland, int(len(scotland) * 0.08))

    # Use the bus_travel function to get the closest bus stop to each postcode in Scotland
   # scotland_bus_data = land_travel(postcode_coord_dict, stop_coord_dict, scotland_bus)[0]
 
    # For the rest of the UK
    # 25% of postcodes travel by car
    # 25% of postcodes travel by rail
    # 50% of postcodes travel by plane
    rest_bus = random.sample(rest, int(len(rest) * 0.25))
    rest_rail = random.sample(rest, int(len(rest) * 0.25))
    rest_plane = random.sample(rest, int(len(rest) * 0.50))

    # Use the bus_travel function to get the closest bus stop to each postcode in the rest of the UK
    rest_bus_data = land_travel(postcode_coord_dict, stop_coord_dict, rest_bus)
    #print(rest_bus_data)
    






    
    # # Signal the loading thread to stop
    # stop_event.set()
    # # Wait for the loading thread to stop
    # loading_thread.join()

    # return  total_bus, total_train

if __name__ == '__main__':
    main()
