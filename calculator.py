# Calculator class that combines all pages and functions of the application
# Sources of code snippets/pictures are provided in the comments of functions.
# Author: Ivan Ivanov

import sys
import os
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QStackedLayout, QMessageBox, QHBoxLayout, QProgressDialog, QProgressBar
from PyQt6.QtCore import pyqtSignal
from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon
from tkinter.filedialog import askopenfile
import pandas as pd
from preprocess_data import determine_postcode, divide_scot_addresses, divide_uk_addresses
from final_leg import assign_scotland, assign_uk
from page1 import MainPage
from page2 import Page2
from page3 import Page3
from results_distance import ResultDistance
from results_emissions import ResultEmissions
from invalid_page import InvalidPage
from main import main
import plotly.express as px
import plotly.graph_objects as go
from council_areas import get_district, group_district, find_percentage
from style_sheets import main_stylesheet, widget_stylesheet

basedir = os.path.dirname(__file__)

class Calculator(QWidget):

    # Signals 
    file_selected = pyqtSignal(bool)
    hundred_percent = pyqtSignal(bool)
    hundred_percent_page3 = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.initializeUI()
        self.scotland = None
        self.wales = None
        self.north_ireland = None
        self.england = None
        self.emission_factors = {'car': 0.18264,  'rail': 0.035463, 'bus': 0.118363, 'coach': 0.027181, 'taxi': 0.148615, 'ferry': 0.02555, 'plane': 0.03350}
        self.invalid = []

    def initializeUI(self):
        """Set up application GUI"""
        self.setMinimumSize(1200, 720)
        self.setWindowTitle("StudentGreenTravel")
        main_icon = QIcon(os.path.join(basedir, 'icons/eco.svg'))
        self.setWindowIcon(main_icon)


        # Layouts for pages
        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        self.layout3 = QVBoxLayout()
        self.layout4 = QHBoxLayout()
        self.layout5 = QVBoxLayout()
        self.layout6 = QVBoxLayout()

        # Stacked layout to hold the pages
        # Source: https://www.tutorialspoint.com/pyqt/pyqt_qstackedwidget.htm 
        self.stackedLayout = QStackedLayout()

        # Create the pages
        self.page1 = MainPage()
        self.page2 = Page2()
        self.page3 = Page3()
        self.page4 = ResultDistance()
        self.page5 = ResultEmissions()
        self.page6 = InvalidPage()


        # Add the pages to the stacked layout and set the stacked layout as the main layout
        self.stackedLayout.addWidget(self.page1)
        self.stackedLayout.addWidget(self.page2)
        self.stackedLayout.addWidget(self.page3)
        self.stackedLayout.addWidget(self.page4)
        self.stackedLayout.addWidget(self.page5)
        self.stackedLayout.addWidget(self.page6)

        # Set the stacked layout as the main layout
        self.setLayout(self.stackedLayout)

        # Connect signals for page1
        self.page1.button1.clicked.connect(lambda: self.go_to_page(1))
        self.page1.button2.clicked.connect(self.open_file)
        self.page1.button3.clicked.connect(self.select_emission_factors)
        self.file_selected.connect(self.page1.enable_buttons1)
        self.page1.default_radio.clicked.connect(self.click_default_radio)

        # Connect signals for page2
        self.page2.next_button2.clicked.connect(lambda: self.go_to_page(2))
        self.page2.submit.clicked.connect(self.check_combo_page2)
        self.page2.back.clicked.connect(lambda: self.go_to_page(0))
        self.hundred_percent.connect(self.page2.enable_page2)

        # Connect signals for page3
        self.page3.back.clicked.connect(lambda: self.go_to_page(1))
        self.page3.calculate_button.clicked.connect(self.go_to_results)
        self.hundred_percent_page3.connect(self.page3.enable_page3)
        self.page3.submit.clicked.connect(self.check_combo_page3)

        # Connect signals for page4
        self.page4.button1.clicked.connect(lambda: self.go_to_page(2))
        self.page4.button2.clicked.connect(lambda: self.go_to_page(0))
        self.page4.button3.clicked.connect(lambda: self.go_to_page(4))
        self.page4.button4.clicked.connect(lambda: self.go_to_page(5))
        self.page4.radio1.clicked.connect(self.click_radio1)
        self.page4.radio2.clicked.connect(self.click_radio2)
        self.page4.radio3.clicked.connect(self.click_radio3)
        self.page4.radio4.clicked.connect(self.click_radio4)

        # Connect signals for page5
        self.page5.button1.clicked.connect(lambda: self.go_to_page(2))
        self.page5.button2.clicked.connect(lambda: self.go_to_page(0))
        self.page5.button3.clicked.connect(lambda: self.go_to_page(3))
        self.page5.button4.clicked.connect(lambda: self.go_to_page(5))
        self.page5.radio1.clicked.connect(self.click_radio1)
        self.page5.radio2.clicked.connect(self.click_radio2)
        self.page5.radio3.clicked.connect(self.click_radio3)
        self.page5.radio4.clicked.connect(self.click_radio4)

        # Connect signals for page6
        self.page6.button1.clicked.connect(lambda: self.go_to_page(3))
        self.page6.button2.clicked.connect(lambda: self.page6.find_invalid_values(self.addresses, self.invalid))
        self.page6.button3.clicked.connect(self.page6.clear)
    

        # Set style for the widgets in the application
        self.setStyleSheet(widget_stylesheet)

        # Set style for the windows
        self.setStyleSheet(main_stylesheet)

        # Get icons from icons folder
        # Source: https://www.svgrepo.com/
        calculate_icon = QIcon(os.path.join(basedir, 'icons/calculator.svg'))
        back = QIcon(os.path.join(basedir, 'icons/back.svg'))
        submit = QIcon(os.path.join(basedir, 'icons/submit.svg'))
        next_button = QIcon(os.path.join(basedir, 'icons/next.svg'))
        file_button = QIcon(os.path.join(basedir, 'icons/file.svg'))
        dash = QIcon(os.path.join(basedir, 'icons/dash.svg'))
        menu = QIcon(os.path.join(basedir, 'icons/menu.svg'))
        one = QIcon(os.path.join(basedir, 'icons/1.svg'))
        two = QIcon(os.path.join(basedir, 'icons/2.svg'))
        emissions = QIcon(os.path.join(basedir, 'icons/emissions.svg'))
        error = QIcon(os.path.join(basedir, 'icons/error.svg'))
        clear = QIcon(os.path.join(basedir, 'icons/clear.svg'))


        # Set icons for all buttons
        self.page1.button1.setIcon(dash)
        self.page1.button2.setIcon(file_button)
        self.page1.button3.setIcon(emissions)
        self.page2.back.setIcon(back)
        self.page3.back.setIcon(back)
        self.page4.button1.setIcon(back)
        self.page4.button2.setIcon(menu)
        self.page4.button3.setIcon(two)
        self.page5.button1.setIcon(back)
        self.page5.button2.setIcon(menu)
        self.page5.button3.setIcon(one)
        self.page3.calculate_button.setIcon(calculate_icon)
        self.page2.submit.setIcon(submit)
        self.page3.submit.setIcon(submit)
        self.page2.next_button2.setIcon(next_button)
        self.page4.button4.setIcon(error)
        self.page5.button4.setIcon(error)
        self.page6.button1.setIcon(back)
        self.page6.button2.setIcon(error)
        self.page6.button3.setIcon(clear)


    """==============================================Methods for pages=============================================="""
    def open_file(self):
        """Open a file explorer to select a file"""
        self.page1.file_label.setText("Please wait while the data is being processed...")
        file = askopenfile(filetypes=[("Excel files", "*.xlsx")])
        # If the user selected a file, then read it using pandas
        if file:
        # Read address file
            self.addresses = pd.read_excel(file.name, engine='openpyxl')
            # Shuffle dataframe with addresses
            self.addresses = self.addresses.sample(frac=1)
            self.addresses.iloc[:, 1] = self.addresses.iloc[:, 1].str.replace(' ', '')
            # Add the file name to the label text with the file name without the path
            self.page1.file_label.setText(f"<b>Dataset:</b> {file.name.split('/')[-1]}")
            self.scotland, self.wales, self.north_ireland, self.england, self.invalid1 = determine_postcode(self.addresses.iloc[:, 1])
            # Call the add_invalid function from the invalid page to add the invalid postcodes
            # pass the invalid postcodes as list 
            self.invalid.extend([self.invalid1])
            # Emit signal that a file has been selected
            self.file_selected.emit(True)
        else:
            self.page1.file_label.setText("No file was selected.")
            # Emit a signal that a file has not been selected
            self.file_selected.emit(False)

    def select_emission_factors(self):
        file = askopenfile(filetypes=[("Excel files", "*.xlsx")])
        # If the user selected a file, then read it using pandas
        if file:
        # Read emission factors file
            factors = pd.read_excel(file.name, engine='openpyxl')
            # Transform the dataframe to a dictionary with key the Method and value the Emission Factor
            factors = factors.set_index('Method')['Factor'].to_dict()
            self.emission_factors = factors
            self.page1.default_radio.setChecked(False)
            self.page1.custom_radio.setChecked(True)
        else:
            self.emission_factors = self.emission_factors
            self.page1.default_radio.setChecked(True)
            self.page1.custom_radio.setChecked(False)
            self.page1.custom_radio.setEnabled(False)

    def click_default_radio(self):
        """If the default radio button is clicked, then set the emission factors to the default ones"""
        self.page1.custom_radio.setChecked(False)
        self.emission_factors = self.emission_factors


    def go_to_page(self, i):
        self.stackedLayout.setCurrentIndex(i)

    def check_trip_combo(self):
        self.num_trips = int(self.page2.trips_combo.currentText())


    def check_combo_page2(self):
        """Check if the sum of the percentages for each country is 100. 
        If it is, then call the menu function. 
        If not, show a message box with an error.""" 
        # Get the percentages for each country
        scot_car = int(self.page2.combo_car_scot.currentText())
        scot_bus = int(self.page2.combo_bus_scot.currentText())
        scot_rail = int(self.page2.combo_rail_scot.currentText())
        uk_plane = int(self.page2.plane_uk.currentText())
        uk_car = int(self.page2.car_uk.currentText())
        uk_rail = int(self.page2.rail_uk.currentText())

        # Sum the percentages for each country
        scot_sum = sum([scot_car, scot_bus, scot_rail])
        uk_sum = sum([uk_plane, uk_car, uk_rail])

        # Call the check_trip_combo() to save the number of trips chosen
        self.check_trip_combo()

        if scot_sum == 100 and uk_sum == 100:
            # Show a message that the data has been submitted
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            success = QIcon('icons/success.svg')
            msg.setWindowIcon(success)
            msg.setText("The data has been submitted!")
            # Add a success icon to the message box
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
            # take the returns from the file explorer function without running it again
            scotland, wales, north_ireland, england = self.get_country_data()
            self.hundred_percent.emit(True)
            # call the divide_address functions for each country
            self.travel_scotland = divide_scot_addresses(scotland, scot_bus, scot_car, scot_rail)
            self.travel_england = divide_uk_addresses(england, uk_plane, uk_car, uk_rail)
            self.travel_wales = divide_uk_addresses(wales, uk_plane, uk_car, uk_rail)
            self.travel_ni = divide_uk_addresses(north_ireland, uk_plane, uk_car, uk_rail)

        else:
            self.hundred_percent.emit(False)
            # Show a message box with the error
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            warning = QIcon('icons/warning.svg')
            msg.setWindowIcon(warning)
            msg.setText("The sum of the percentages for each country must be 100!\nPlease try again.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()

    def get_country_data(self):
        """Return the data from the file explorer function"""
        return self.scotland, self.wales, self.north_ireland, self.england
    
    
    def check_combo_page3(self):
        """Check if the sum of the percentages for each country is 100. If it is, then call the menu function. If not, show a message box with an error.""" 
        # call extract function from page3 to get the percentages for each country
        scot, eng, wales, ni = self.page3.extract_percentages()
        # Divide the percentages into lists for each country
        scot = [int(i) for key, i in scot.items()]
        # [:4] for land and [4:] for air transport
        eng_land = [int(i) for key, i in eng.items()][:4]
        eng_air = [int(i) for key, i in eng.items()][4:]
        wales_land = [int(i) for key, i in wales.items()][:4]
        wales_air = [int(i) for key, i in wales.items()][4:]
        ni_land = [int(i) for key, i in ni.items()][:4]
        ni_air = [int(i) for key, i in ni.items()][4:]

        # Sum of all
        sum_all = sum(scot) + sum(eng_land) + sum(eng_air) + sum(wales_land) + sum(wales_air) + sum(ni_land) + sum(ni_air)

        # If the sum of the percentages for each country is 700 (7 elements * 100), then call the menu function.
        if sum_all == 700:
            # Show a message that the data has been submitted
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            success = QIcon('icons/success.svg')
            msg.setWindowIcon(success)
            msg.setText("The data has been submitted!")
            # Add a success icon to the message box
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
            self.hundred_percent_page3.emit(True)
            # Combine the bus and rail postcodes for Scotland in a list to be used in the final leg function
            scot_bus_rail = self.travel_scotland[0] + self.travel_scotland[2]
            # Call the select_country function
            # Scotland
            self.scot_fleg = assign_scotland(scot_bus_rail, scot[0], scot[1], scot[2], scot[3])

            # England
            eng_rail = self.travel_england[2]
            eng_plane = self.travel_england[0]
            self.eng_fleg_bus_rail, self.eng_fleg_plane = assign_uk(eng_rail, eng_plane, eng_land[0], eng_land[1], eng_land[2], eng_land[3], eng_air[0], eng_air[1], eng_air[2], eng_air[3])
            # Wales
            wales_rail = self.travel_wales[2]
            wales_plane = self.travel_wales[0]
            self.wales_fleg_bus_rail, self.wales_fleg_plane = assign_uk(wales_rail, wales_plane, wales_land[0], wales_land[1], wales_land[2], wales_land[3], wales_air[0], wales_air[1], wales_air[2], wales_air[3])

            # Northern Ireland
            ni_rail = self.travel_ni[2]
            ni_plane = self.travel_ni[0]
            self.ni_fleg_bus_rail, self.ni_fleg_plane = assign_uk(ni_rail, ni_plane, ni_land[0], ni_land[1], ni_land[2], ni_land[3], ni_air[0], ni_air[1], ni_air[2], ni_air[3])

        else:
            self.hundred_percent_page3.emit(False)
            # Show a message box with the error
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            warning = QIcon('icons/warning.svg')
            msg.setWindowIcon(warning)
            msg.setText("The sum of the percentages for each country must be 100!\nPlease try again.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()


    def go_to_results(self):
        """Extract the final leg of the journey for each country"""
        # Crate a progress dialog
        pdg = QProgressDialog()
        pdg.setWindowTitle("Calculating")
        pdg.setLabelText("Please wait while distances and emissions are processed...")
        loading_icon = QIcon('icons/loading.svg')
        pdg.setWindowIcon(loading_icon)
        self.pbar = QProgressBar()
        pdg.setBar(self.pbar)
        pdg.setMinimum(0)
        pdg.setMaximum(100)
        pdg.show()

        self.pbar.setValue(0)
        QtWidgets.QApplication.processEvents()

        # Scotland
        scot_car_fleg = self.scot_fleg[0]
        scot_taxi_fleg = self.scot_fleg[1]
        scot_bus_fleg = self.scot_fleg[2]
        scot_walk_fleg = self.scot_fleg[3]

        # England
        eng_car_fleg = self.eng_fleg_bus_rail[0] + self.eng_fleg_plane[0]
        eng_taxi_fleg = self.eng_fleg_bus_rail[1] + self.eng_fleg_plane[1]
        eng_bus_fleg = self.eng_fleg_bus_rail[2] + self.eng_fleg_plane[2]
        eng_walk_fleg = self.eng_fleg_bus_rail[3] + self.eng_fleg_plane[3]

        # Wales
        wales_car_fleg = self.wales_fleg_bus_rail[0] + self.wales_fleg_plane[0]
        wales_taxi_fleg = self.wales_fleg_bus_rail[1] + self.wales_fleg_plane[1]
        wales_bus_fleg = self.wales_fleg_bus_rail[2] + self.wales_fleg_plane[2]
        wales_walk_fleg = self.wales_fleg_bus_rail[3] + self.wales_fleg_plane[3]

        # Northern Ireland
        ni_car_fleg = self.ni_fleg_bus_rail[0] + self.ni_fleg_plane[0]
        ni_taxi_fleg = self.ni_fleg_bus_rail[1] + self.ni_fleg_plane[1]
        ni_bus_fleg = self.ni_fleg_bus_rail[2] + self.ni_fleg_plane[2]
        ni_walk_fleg = self.ni_fleg_bus_rail[3] + self.ni_fleg_plane[3]

        # Update the progress bar
        self.pbar.setValue(25)
        # This is necessary for showing and updating the progress bar
        # Source: https://stackoverflow.com/questions/30823863/pyqt-progress-bar-not-updating-or-appearing-until-100
        QtWidgets.QApplication.processEvents()

        # Call the main function
        self.emissions, self.distances, self.total_emissions, self.total_distance_dict, self.invalid2 = main(self.emission_factors, self.travel_scotland, self.travel_england, self.travel_wales, self.travel_ni, scot_car_fleg, scot_taxi_fleg, scot_bus_fleg, scot_walk_fleg, eng_car_fleg, eng_taxi_fleg, eng_bus_fleg, eng_walk_fleg, wales_car_fleg, wales_taxi_fleg, wales_bus_fleg, wales_walk_fleg, ni_car_fleg, ni_taxi_fleg, ni_bus_fleg, ni_walk_fleg)
        # Call the add_invalid function from the invalid page to add the invalid postcodes
        self.invalid.extend(self.invalid2)
        # Update the progress bar
        self.pbar.setValue(50)
        QtWidgets.QApplication.processEvents()

        # Scotland
        # Remove postcodes where [:2] == 'AB'
        self.scotland = [i for i in self.scotland if i[:2] != 'AB']
        car_dict, bus_dict, rail_dict, taxi_dict = self.create_council_areas(self.scotland, 'Scotland')

        # Update the progress bar
        self.pbar.setValue(65)
        QtWidgets.QApplication.processEvents()


        df_car = pd.DataFrame(car_dict)
        # Multiply the distances by the self.num_trips
        df_car = df_car * self.num_trips
        df_car = df_car.round(1)
        # Emissions df
        df_car_emissions = df_car * self.emission_factors['car']
        df_car_emissions = df_car_emissions.round(1)

        df_bus = pd.DataFrame(bus_dict)
        df_bus = df_bus * self.num_trips
        df_bus = df_bus.round(1)
        df_bus_emissions = df_bus * self.emission_factors['coach']
        df_bus_emissions = df_bus_emissions.round(1)

        df_rail = pd.DataFrame(rail_dict)
        df_rail = df_rail * self.num_trips
        df_rail = df_rail.round(1)
        df_rail_emissions = df_rail * self.emission_factors['rail']
        df_rail_emissions = df_rail_emissions.round(1)

        df_taxi = pd.DataFrame(taxi_dict)
        df_taxi = df_taxi * self.num_trips
        df_taxi = df_taxi.round(1)
        df_taxi_emissions = df_taxi * self.emission_factors['taxi']
        df_taxi_emissions = df_taxi_emissions.round(1)

        """=======================Scotland Council Distances=========================="""
        self.scot_car = go.Figure(
            data=[go.Bar(x=df_car.columns, y=df_car.iloc[0, :], text=df_car.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Car Travel Distances Across Scottish Councils (km)', xaxis=dict(title='Council Area'), yaxis=dict(title='Distance (km)')),
        )
        # Change the color of the bars
        self.scot_car.update_traces(marker_color='rgb(75, 235, 230)', marker_line_color='rgb(98, 143, 142)', marker_line_width=1.5, opacity=0.6)
        self.scot_bus = go.Figure(
            data=[go.Bar(x=df_bus.columns, y=df_bus.iloc[0, :], text=df_bus.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Bus Travel Distances Across Scottish Councils (km)', xaxis=dict(title='Council Area'), yaxis=dict(title='Distance (km)'))
        )
        self.scot_bus.update_traces(marker_color='rgb(75, 235, 230)', marker_line_color='rgb(98, 143, 142)', marker_line_width=1.5, opacity=0.6)
        self.scot_rail = go.Figure(
            data=[go.Bar(x=df_rail.columns, y=df_rail.iloc[0, :], text=df_rail.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Train Travel Distances Across Scottish Councils (km)', xaxis=dict(title='Council Area'), yaxis=dict(title='Distance (km)'))
        )
        self.scot_rail.update_traces(marker_color='rgb(75, 235, 230)', marker_line_color='rgb(98, 143, 142)', marker_line_width=1.5, opacity=0.6)
        self.scot_taxi = go.Figure(
            data=[go.Bar(x=df_taxi.columns, y=df_taxi.iloc[0, :], text=df_taxi.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Taxi Travel Distances Across Scottish Councils (km)', xaxis=dict(title='Council Area'), yaxis=dict(title='Distance (km)'))
        )
        self.scot_taxi.update_traces(marker_color='rgb(75, 235, 230)', marker_line_color='rgb(98, 143, 142)', marker_line_width=1.5, opacity=0.6)




        """=======================Scotland Council Emissions=========================="""
        self.scot_car_emissions = go.Figure(
            data=[go.Bar(x=df_car_emissions.columns, y=df_car_emissions.iloc[0, :], text=df_car_emissions.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Car Travel Emissions Across Scottish Councils (kg CO2)', xaxis=dict(title='Council Area'), yaxis=dict(title='Emissions (kg CO2)'))
        )
        # self.scot_car_emissions.update_traces(marker_color='rgb(75, 235, 230)', marker_line_color='rgb(98, 143, 142)', marker_line_width=1.5, opacity=0.6)
        self.scot_bus_emissions = go.Figure(
            data=[go.Bar(x=df_bus_emissions.columns, y=df_bus_emissions.iloc[0, :], text=df_bus_emissions.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Bus Travel Emissions Across Scottish Councils (kg CO2)', xaxis=dict(title='Council Area'), yaxis=dict(title='Emissions (kg CO2)'))
        )
        self.scot_rail_emissions = go.Figure(
            data=[go.Bar(x=df_rail_emissions.columns, y=df_rail_emissions.iloc[0, :], text=df_rail_emissions.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Train Travel Emissions Across Scottish Councils (kg CO2)', xaxis=dict(title='Council Area'), yaxis=dict(title='Emissions (kg CO2)'))
        )
        self.scot_taxi_emissions = go.Figure(
            data=[go.Bar(x=df_taxi_emissions.columns, y=df_taxi_emissions.iloc[0, :], text=df_taxi_emissions.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Taxi Travel Emissions Across Scottish Councils (kg CO2)', xaxis=dict(title='Council Area'), yaxis=dict(title='Emissions (kg CO2)'))
        )


        self.pbar.setValue(75)
        QtWidgets.QApplication.processEvents()

        # Do same for England
        car_dict_eng, bus_dict_eng, rail_dict_eng, taxi_dict_eng = self.create_council_areas(self.england, 'England')
        df_car_eng = pd.DataFrame(car_dict_eng)
        df_car_eng = df_car_eng * self.num_trips
        df_car_eng = df_car_eng.round(1)
        df_car_emissions_eng = df_car_eng * self.emission_factors['car']
        df_car_emissions_eng = df_car_emissions_eng.round(1)
        df_bus_eng = pd.DataFrame(bus_dict_eng)
        df_bus_eng = df_bus_eng * self.num_trips
        df_bus_eng = df_bus_eng.round(1)
        df_bus_emissions_eng = df_bus_eng * self.emission_factors['coach']
        df_bus_emissions_eng = df_bus_emissions_eng.round(1)
        df_rail_eng = pd.DataFrame(rail_dict_eng)
        df_rail_eng = df_rail_eng * self.num_trips
        df_rail_eng = df_rail_eng.round(1)
        df_rail_emissions_eng = df_rail_eng * self.emission_factors['rail']
        df_rail_emissions_eng = df_rail_emissions_eng.round(1)
        df_taxi_eng = pd.DataFrame(taxi_dict_eng)
        df_taxi_eng = df_taxi_eng * self.num_trips
        df_taxi_eng = df_taxi_eng.round(1)
        df_taxi_emissions_eng = df_taxi_eng * self.emission_factors['taxi']
        df_taxi_emissions_eng = df_taxi_emissions_eng.round(1)

        """=======================England Council Distances=========================="""
        self.eng_car = go.Figure(
            data=[go.Table( header=dict(values=['Council Area', 'Distance (km)']),
                            cells=dict(values=[df_car_eng.columns, df_car_eng.iloc[0, :]]))],
            layout=go.Layout(title='Car Travel Distances Across English Councils (km)')
        )
        self.eng_bus = go.Figure(
            data=[go.Table( header=dict(values=['Council Area', 'Distance (km)']),
                            cells=dict(values=[df_bus_eng.columns, df_bus_eng.iloc[0, :]]))],
            layout=go.Layout(title='Bus Travel Distances Across English Councils (km)')
        )
        self.eng_rail = go.Figure(
            data=[go.Table( header=dict(values=['Council Area', 'Distance (km)']),
                            cells=dict(values=[df_rail_eng.columns, df_rail_eng.iloc[0, :]]))],
            layout=go.Layout(title='Train Travel Distances Across English Councils (km)')
        )
        self.eng_taxi = go.Figure(
            data=[go.Table( header=dict(values=['Council Area', 'Distance (km)']),
                            cells=dict(values=[df_taxi_eng.columns, df_taxi_eng.iloc[0, :]]))],
            layout=go.Layout(title='Taxi Travel Distances Across English Councils (km)')
        )



        """=======================England Council Emissions=========================="""

        self.eng_car_emissions = go.Figure(
            data=[go.Table( header=dict(values=['Council Area', 'Emissions (kg CO2)']),
                            cells=dict(values=[df_car_emissions_eng.columns, df_car_emissions_eng.iloc[0, :]]))],
            layout=go.Layout(title='Car Travel Emissions Across English Councils (kg CO2)')
        )
        self.eng_bus_emissions = go.Figure(
            data=[go.Table( header=dict(values=['Council Area', 'Emissions (kg CO2)']),
                            cells=dict(values=[df_bus_emissions_eng.columns, df_bus_emissions_eng.iloc[0, :]]))],
            layout=go.Layout(title='Bus Travel Emissions Across English Councils (kg CO2)')
        )
        self.eng_rail_emissions = go.Figure(
            data=[go.Table( header=dict(values=['Council Area', 'Emissions (kg CO2)']),
                            cells=dict(values=[df_rail_emissions_eng.columns, df_rail_emissions_eng.iloc[0, :]]))],
            layout=go.Layout(title='Train Travel Emissions Across English Councils (kg CO2)'))
        
        self.eng_taxi_emissions = go.Figure(
            data=[go.Table( header=dict(values=['Council Area', 'Emissions (kg CO2)']),
                            cells=dict(values=[df_taxi_emissions_eng.columns, df_taxi_emissions_eng.iloc[0, :]]))],
            layout=go.Layout(title='Taxi Travel Emissions Across English Councils (kg CO2)')
        )

        self.pbar.setValue(85)
        QtWidgets.QApplication.processEvents()

        # Do same for Wales
        car_dict_wales, bus_dict_wales, rail_dict_wales, taxi_dict_wales = self.create_council_areas(self.wales, 'Wales')
        df_car_wales = pd.DataFrame(car_dict_wales)
        df_car_wales = df_car_wales * self.num_trips
        df_car_wales = df_car_wales.round(1)
        df_car_emissions_wales = df_car_wales * self.emission_factors['car']
        df_car_emissions_wales = df_car_emissions_wales.round(1)
        df_bus_wales = pd.DataFrame(bus_dict_wales)
        df_bus_wales = df_bus_wales * self.num_trips
        df_bus_wales = df_bus_wales.round(1)
        df_bus_emissions_wales = df_bus_wales * self.emission_factors['coach']
        df_bus_emissions_wales = df_bus_emissions_wales.round(1)
        df_rail_wales = pd.DataFrame(rail_dict_wales)
        df_rail_wales = df_rail_wales * self.num_trips
        df_rail_wales = df_rail_wales.round(1)
        df_rail_emissions_wales = df_rail_wales * self.emission_factors['rail']
        df_rail_emissions_wales = df_rail_emissions_wales.round(1)
        df_taxi_wales = pd.DataFrame(taxi_dict_wales)
        df_taxi_wales = df_taxi_wales * self.num_trips
        df_taxi_wales = df_taxi_wales.round(1)
        df_taxi_emissions_wales = df_taxi_wales * self.emission_factors['taxi']
        df_taxi_emissions_wales = df_taxi_emissions_wales.round(1)

        """=======================Wales Council Distances=========================="""
        self.wales_car = go.Figure(
            data=[go.Bar(x=df_car_wales.columns, y=df_car_wales.iloc[0, :], text=df_car_wales.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Car Travel Distances Across Welsh Councils (km)', xaxis=dict(title='Council Area'), yaxis=dict(title='Distance (km)'))
        )
        self.wales_bus = go.Figure(
            data=[go.Bar(x=df_bus_wales.columns, y=df_bus_wales.iloc[0, :], text=df_bus_wales.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Bus Travel Distances Across Welsh Councils (km)', xaxis=dict(title='Council Area'), yaxis=dict(title='Distance (km)'))
        )
        self.wales_rail = go.Figure(
            data=[go.Bar(x=df_rail_wales.columns, y=df_rail_wales.iloc[0, :], text=df_rail_wales.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Train Travel Distances Across Welsh Councils (km)', xaxis=dict(title='Council Area'), yaxis=dict(title='Distance (km)'))
        )
        self.wales_taxi = go.Figure(
            data=[go.Bar(x=df_taxi_wales.columns, y=df_taxi_wales.iloc[0, :], text=df_taxi_wales.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Taxi Travel Distances Across Welsh Councils (km)', xaxis=dict(title='Council Area'), yaxis=dict(title='Distance (km)'))
        )


        """=======================Wales Council Emissions=========================="""
        self.wales_car_emissions = go.Figure(
            data=[go.Bar(x=df_car_emissions_wales.columns, y=df_car_emissions_wales.iloc[0, :], text=df_car_emissions_wales.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Car Travel Emissions Across Welsh Councils (kg CO2)', xaxis=dict(title='Council Area'), yaxis=dict(title='Emissions (kg CO2)'))
        )
        self.wales_bus_emissions = go.Figure(
            data=[go.Bar(x=df_bus_emissions_wales.columns, y=df_bus_emissions_wales.iloc[0, :], text=df_bus_emissions_wales.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Bus Travel Emissions Across Welsh Councils (kg CO2)', xaxis=dict(title='Council Area'), yaxis=dict(title='Emissions (kg CO2)'))
        )
        self.wales_rail_emissions = go.Figure(
            data=[go.Bar(x=df_rail_emissions_wales.columns, y=df_rail_emissions_wales.iloc[0, :], text=df_rail_emissions_wales.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Train Travel Emissions Across Welsh Councils (kg CO2)', xaxis=dict(title='Council Area'), yaxis=dict(title='Emissions (kg CO2)'))
        )
        self.wales_taxi_emissions = go.Figure(
            data=[go.Bar(x=df_taxi_emissions_wales.columns, y=df_taxi_emissions_wales.iloc[0, :], text=df_taxi_emissions_wales.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Taxi Travel Emissions Across Welsh Councils (kg CO2)', xaxis=dict(title='Council Area'), yaxis=dict(title='Emissions (kg CO2)'))
        )

        self.pbar.setValue(95)
        QtWidgets.QApplication.processEvents()
        
        # Do same for Northern Ireland
        car_dict_ni, bus_dict_ni, rail_dict_ni, taxi_dict_ni = self.create_council_areas(self.north_ireland, 'Northern Ireland')
        df_car_ni = pd.DataFrame(car_dict_ni)
        df_car_ni = df_car_ni * self.num_trips
        df_car_ni = df_car_ni.round(1)
        df_car_emissions_ni = df_car_ni * self.emission_factors['car']
        df_car_emissions_ni = df_car_emissions_ni.round(1)
        df_bus_ni = pd.DataFrame(bus_dict_ni)
        df_bus_ni = df_bus_ni * self.num_trips
        df_bus_ni = df_bus_ni.round(1)
        df_bus_emissions_ni = df_bus_ni * self.emission_factors['coach']
        df_bus_emissions_ni = df_bus_emissions_ni.round(1)
        df_rail_ni = pd.DataFrame(rail_dict_ni)
        df_rail_ni = df_rail_ni * self.num_trips
        df_rail_ni = df_rail_ni.round(1)
        df_rail_emissions_ni = df_rail_ni * self.emission_factors['rail']
        df_rail_emissions_ni = df_rail_emissions_ni.round(1)
        df_taxi_ni = pd.DataFrame(taxi_dict_ni)
        df_taxi_ni = df_taxi_ni * self.num_trips
        df_taxi_ni = df_taxi_ni.round(1)
        df_taxi_emissions_ni = df_taxi_ni * self.emission_factors['taxi']
        df_taxi_emissions_ni = df_taxi_emissions_ni.round(1)

        """=======================Northern Ireland Council Distances=========================="""
        self.ni_car = go.Figure(
            data=[go.Bar(x=df_car_ni.columns, y=df_car_ni.iloc[0, :], text=df_car_ni.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Car Travel Distances Across Northern Irish Councils (km)', xaxis=dict(title='Council Area'), yaxis=dict(title='Distance (km)'))
        )
        self.ni_bus = go.Figure(
            data=[go.Bar(x=df_bus_ni.columns, y=df_bus_ni.iloc[0, :], text=df_bus_ni.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Bus Travel Distances Across Northern Irish Councils (km)', xaxis=dict(title='Council Area'), yaxis=dict(title='Distance (km)'))
        )
        self.ni_rail = go.Figure(
            data=[go.Bar(x=df_rail_ni.columns, y=df_rail_ni.iloc[0, :], text=df_rail_ni.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Train Travel Distances Across Northern Irish Councils (km)', xaxis=dict(title='Council Area'), yaxis=dict(title='Distance (km)'))
        )
        self.ni_taxi = go.Figure(
            data=[go.Bar(x=df_taxi_ni.columns, y=df_taxi_ni.iloc[0, :], text=df_taxi_ni.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Taxi Travel Distances Across Northern Irish Councils (km)', xaxis=dict(title='Council Area'), yaxis=dict(title='Distance (km)'))
        )



        """=======================Northern Ireland Council Emissions=========================="""
        self.ni_car_emissions = go.Figure(
            data=[go.Bar(x=df_car_emissions_ni.columns, y=df_car_emissions_ni.iloc[0, :], text=df_car_emissions_ni.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Car Travel Emissions Across Northern Irish Councils (kg CO2)', xaxis=dict(title='Council Area'), yaxis=dict(title='Emissions (kg CO2)'))
        )
        self.ni_bus_emissions = go.Figure(
            data=[go.Bar(x=df_bus_emissions_ni.columns, y=df_bus_emissions_ni.iloc[0, :], text=df_bus_emissions_ni.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Bus Travel Emissions Across Northern Irish Councils (kg CO2)', xaxis=dict(title='Council Area'), yaxis=dict(title='Emissions (kg CO2)'))
        )
        self.ni_rail_emissions = go.Figure(
            data=[go.Bar(x=df_rail_emissions_ni.columns, y=df_rail_emissions_ni.iloc[0, :], text=df_rail_emissions_ni.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Train Travel Emissions Across Northern Irish Councils (kg CO2)', xaxis=dict(title='Council Area'), yaxis=dict(title='Emissions (kg CO2)'))
        )
        self.ni_taxi_emissions = go.Figure(
            data=[go.Bar(x=df_taxi_emissions_ni.columns, y=df_taxi_emissions_ni.iloc[0, :], text=df_taxi_emissions_ni.iloc[0, :], textposition='auto')],
            layout=go.Layout(title='Taxi Travel Emissions Across Northern Irish Councils (kg CO2)', xaxis=dict(title='Council Area'), yaxis=dict(title='Emissions (kg CO2)'))
        )

        # Connect radio buttons on results page (page4)
        # Source: Answer from ozcanyarimdunya in: https://stackoverflow.com/questions/6784084/how-to-pass-arguments-to-functions-by-the-click-of-button-in-pyqt
        # Scotland travel distances by council
        self.page4.radio5.clicked.connect(lambda: self.set_webpage4(self.scot_car))
        self.page4.radio6.clicked.connect(lambda: self.set_webpage4(self.scot_bus))
        self.page4.radio7.clicked.connect(lambda: self.set_webpage4(self.scot_rail))
        self.page4.radio8.clicked.connect(lambda: self.set_webpage4(self.scot_taxi))
        # England travel distances by council
        self.page4.radio9.clicked.connect(lambda: self.set_webpage4(self.eng_car))
        self.page4.radio10.clicked.connect(lambda: self.set_webpage4(self.eng_bus))
        self.page4.radio11.clicked.connect(lambda: self.set_webpage4(self.eng_rail))
        self.page4.radio12.clicked.connect(lambda: self.set_webpage4(self.eng_taxi))
        # Wales travel distances by council
        self.page4.radio13.clicked.connect(lambda: self.set_webpage4(self.wales_car))
        self.page4.radio14.clicked.connect(lambda: self.set_webpage4(self.wales_bus))
        self.page4.radio15.clicked.connect(lambda: self.set_webpage4(self.wales_rail))
        self.page4.radio16.clicked.connect(lambda: self.set_webpage4(self.wales_taxi))
        # Northern Ireland travel distances by council
        self.page4.radio17.clicked.connect(lambda: self.set_webpage4(self.ni_car))
        self.page4.radio18.clicked.connect(lambda: self.set_webpage4(self.ni_bus))
        self.page4.radio19.clicked.connect(lambda: self.set_webpage4(self.ni_rail))
        self.page4.radio20.clicked.connect(lambda: self.set_webpage4(self.ni_taxi))

        # Connect radio buttons on results page (page5)
        # Scotland travel emissions by council
        self.page5.radio5.clicked.connect(lambda: self.set_webpage5(self.scot_car_emissions))
        self.page5.radio6.clicked.connect(lambda: self.set_webpage5(self.scot_bus_emissions))
        self.page5.radio7.clicked.connect(lambda: self.set_webpage5(self.scot_rail_emissions))
        self.page5.radio8.clicked.connect(lambda: self.set_webpage5(self.scot_taxi_emissions))
        # England travel emissions by council
        self.page5.radio9.clicked.connect(lambda: self.set_webpage5(self.eng_car_emissions))
        self.page5.radio10.clicked.connect(lambda: self.set_webpage5(self.eng_bus_emissions))
        self.page5.radio11.clicked.connect(lambda: self.set_webpage5(self.eng_rail_emissions))
        self.page5.radio12.clicked.connect(lambda: self.set_webpage5(self.eng_taxi_emissions))
        # Wales travel emissions by council
        self.page5.radio13.clicked.connect(lambda: self.set_webpage5(self.wales_car_emissions))
        self.page5.radio14.clicked.connect(lambda: self.set_webpage5(self.wales_bus_emissions))
        self.page5.radio15.clicked.connect(lambda: self.set_webpage5(self.wales_rail_emissions))
        self.page5.radio16.clicked.connect(lambda: self.set_webpage5(self.wales_taxi_emissions))
        # Northern Ireland travel emissions by council
        self.page5.radio17.clicked.connect(lambda: self.set_webpage5(self.ni_car_emissions))
        self.page5.radio18.clicked.connect(lambda: self.set_webpage5(self.ni_bus_emissions))
        self.page5.radio19.clicked.connect(lambda: self.set_webpage5(self.ni_rail_emissions))
        self.page5.radio20.clicked.connect(lambda: self.set_webpage5(self.ni_taxi_emissions))



        #Update the progress bar
        self.pbar.setValue(100)
        QtWidgets.QApplication.processEvents()
        pdg.close()

        # Show the results page
        self.stackedLayout.setCurrentIndex(3)
        
    def click_radio1(self):
        """Set the webview to show the first heatmap with the emissions data"""
        # Create the heatmaps
        df = self.emissions
        # Exclude the Walk values
        df = df.drop('Walk', axis=0)
        df = df * self.num_trips
        # Round the values to 2 decimal places
        df = df.round(1)
        # Source: https://plotly.com/python/heatmaps/
        # Figure to store the heatmap with the emissions
        self.fig1 = px.imshow(df, text_auto=True, aspect='auto', title='Total Emissions (kgCO2e) by Country and Mode of Transport',
                        labels=dict(x="Country", y="Transport", color="Emissions (kgCO2e)"),
                        color_continuous_scale='bupu')

        # Edit the font size and color of the values
        self.fig1.update_traces(textfont_size=16)
        # Source: https://zetcode.com/pyqt/qwebengineview/
        self.page4.webview.setHtml(self.fig1.to_html(include_plotlyjs='cdn'))
        self.page5.webview.setHtml(self.fig1.to_html(include_plotlyjs='cdn'))

    def click_radio2(self):
        """Set the webview to show the second heatmap with the distances data"""
        # Do the same for the distances
        df = self.distances
        df = df * self.num_trips
        df = df.round(1)
        # Figure to store the heatmap with the distances
        self.fig2 = px.imshow(df, text_auto=True, aspect='auto', title='Total Distance (km) by Country and Mode of Transport',
                        labels=dict(x="Country", y="Transport", color="Distance (km)"),
                        color_continuous_scale='bugn')
        
        self.fig2.update_traces(textfont_size=16)
        # Source: https://zetcode.com/pyqt/qwebengineview/
        self.page4.webview.setHtml(self.fig2.to_html(include_plotlyjs='cdn'))
        self.page5.webview.setHtml(self.fig2.to_html(include_plotlyjs='cdn'))

    def click_radio3(self):
        """Set the webview to show the pie chart with the total emissions data"""
         # Pie chart for the total emissions
        # Source: https://plotly.com/python/pie-charts/
        df = self.total_emissions
        df = df * self.num_trips
        df = df.round(1)
        # take names from columns
        names = df.columns
        # Values are the second row
        values = df.iloc[0, :]
        # Figure to store the pie chart with the total emissions
        self.fig3 = px.pie(df, values=values, names=names, title='Total Emissions by Country (in kgCO2e)', labels=dict(names="Country", values="Emissions (kgCO2e)"))
        # Edit the font size and color of the values
        self.fig3.update_traces(textfont_size=16)
        # Source: https://zetcode.com/pyqt/qwebengineview/
        self.page4.webview.setHtml(self.fig3.to_html(include_plotlyjs='cdn'))
        self.page5.webview.setHtml(self.fig3.to_html(include_plotlyjs='cdn'))

    def click_radio4(self):
        """Set the webview to show the pie chart with the emissions per student data"""
        # Pie chart for emissions per student by country
        df = self.total_emissions
        df = df * self.num_trips
        # Divide the total emissions by the number of students for each country
        scot_emissions = df.iloc[0, 0] / len(self.scotland)
        eng_emissions = df.iloc[0, 1] / len(self.england)
        wales_emissions = df.iloc[0, 2] / len(self.wales)
        ni_emissions = df.iloc[0, 3] / len(self.north_ireland)

        # Create a pie chart
        # Source: https://plotly.com/python/pie-charts/
        labels = ['Scotland', 'England', 'Wales', 'Northern Ireland']
        values = [scot_emissions, eng_emissions, wales_emissions, ni_emissions]
        # Round the values to 0 decimal places
        values = [round(i, 1) for i in values]
        # Figure to store the pie chart with the emissions per student
        self.fig4 = px.pie(values=values, names=labels, title='Emissions per Student by Country (in kgCO2e)', labels=dict(names="Country", values="Emissions (kgCO2e)"), color_discrete_sequence=px.colors.sequential.RdBu)
        # Edit the font size and color of the values
        self.fig4.update_traces(textfont_size=16)
        # Source: https://zetcode.com/pyqt/qwebengineview/
        self.page4.webview.setHtml(self.fig4.to_html(include_plotlyjs='cdn'))
        self.page5.webview.setHtml(self.fig4.to_html(include_plotlyjs='cdn'))
   
    def set_webpage4(self, data):
        """Set the webview to show the data from the radio buttons on page4"""
        data = data.to_html(include_plotlyjs='cdn')
        self.page4.webview.setHtml(data)

    def set_webpage5(self, data):
        """Set the webview to show the data from the radio buttons on page5"""
        data = data.to_html(include_plotlyjs='cdn')
        self.page5.webview.setHtml(data)

    def create_council_areas(self, country_posctodes: list, country: str):
        # Scotland
        country_districts = get_district(country_posctodes)
        country_grouped = group_district(country_districts)
        country_percent = find_percentage(country_grouped, country_posctodes)

        # From self.total_distance_dict get the distances for Scotland
        distances = self.total_distance_dict[country]

        # Extract the distances for each mode of transport
        car = distances[3]
        bus = distances[2]
        rail = distances[0]
        taxi = distances[4]

        # Empty dictionaries to store the distances for each mode of transport
        car_dict = {}
        bus_dict = {}
        rail_dict = {}
        taxi_dict = {}

        for key, value in country_percent.items():
            # Divide the total distance for each mode of transport by the percentage of people using it
            car_dict[key] = {'Car' : car * value / 100}
            bus_dict[key] = {'Bus' : bus * value / 100}
            rail_dict[key] = {'Rail' : rail * value / 100}
            taxi_dict[key] = {'Taxi' : taxi * value / 100}

        return car_dict, bus_dict, rail_dict, taxi_dict


"""==============================================Run the app=============================================="""
app = QApplication(sys.argv)
window = Calculator()
window.show()
sys.exit(app.exec())
