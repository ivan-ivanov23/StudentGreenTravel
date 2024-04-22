# Calculator class that combines all pages and functions of the application
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
from council_areas import get_district, group_district, find_percentage
from style_sheets import main_stylesheet, widget_stylesheet
from utils import create_px, create_dfs, create_go_bar, create_go_table, divide_combo_percentages, create_go_table_dict
from aberdeen import distance_home_uni, divide_aberdeen

basedir = os.path.dirname(__file__)

class Calculator(QWidget):

    # Signals 
    file_selected = pyqtSignal(bool)
    file_prepared = pyqtSignal(bool)
    hundred_percent = pyqtSignal(bool)
    hundred_percent_page3 = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.initializeUI()
        self.scotland = None
        self.wales = None
        self.north_ireland = None
        self.england = None
        self.aberdeen = None
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
        self.page1.button4.clicked.connect(self.prepare_data)
        self.file_selected.connect(self.page1.enable_button4)
        self.file_prepared.connect(self.page1.enable_button1)
        self.page1.default_radio.clicked.connect(self.click_default_radio)

        # Connect signals for page2
        self.page2.next_button2.clicked.connect(lambda: self.go_to_page(2))
        self.page2.submit.clicked.connect(self.check_combo_mid_leg)
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

        # Connect signals for page5
        self.page5.button1.clicked.connect(lambda: self.go_to_page(2))
        self.page5.button2.clicked.connect(lambda: self.go_to_page(0))
        self.page5.button3.clicked.connect(lambda: self.go_to_page(3))
        self.page5.button4.clicked.connect(lambda: self.go_to_page(5))

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
        process = QIcon(os.path.join(basedir, 'icons/process.svg'))


        # Set icons for all buttons
        self.page1.button1.setIcon(dash)
        self.page1.button2.setIcon(file_button)
        self.page1.button3.setIcon(emissions)
        self.page1.button4.setIcon(process)
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
    """@@@ Navigation between pages @@@"""
    def go_to_page(self, i):
        self.stackedLayout.setCurrentIndex(i)

############################################################################################################################################

    """@@@ Main Page (Menu) Methods @@@"""	
    def open_file(self):
        """Open a file explorer to select a file""" 
        file = askopenfile(filetypes=[("Excel files", "*.xlsx")])
        # If the user selected a file, then read it using pandas
        if file:
        # Read address file
            self.addresses = pd.read_excel(file.name, engine='openpyxl')
            # Shuffle dataframe with addresses
            self.addresses = self.addresses.sample(frac=1)
            # Remove white spaces from the postcodes
            self.addresses.iloc[:, 1] = self.addresses.iloc[:, 1].str.replace(' ', '')
            # Add the file name to the label text with the file name without the path
            self.page1.file_label.setText(f"<b>Dataset:</b> {file.name.split('/')[-1]}")
            # Emit signal that a file has been selected
            self.file_selected.emit(True)
        else:
            self.page1.file_label.setText("No file was selected.")
            # Emit a signal that a file has not been selected
            self.file_selected.emit(False)
            self.file_prepared.emit(False)

    def prepare_data(self):
        self.page1.file_label.setText("Please wait while the data is being prepared...")
        # Process the event to show the message
        # Source: https://stackoverflow.com/questions/30823863/pyqt-progress-bar-not-updating-or-appearing-until-100
        QtWidgets.QApplication.processEvents()
        self.scotland, self.wales, self.north_ireland, self.england, self.aberdeen, self.invalid1 = determine_postcode(self.addresses.iloc[:, 1])
        # Call the add_invalid function from the invalid page to add the invalid postcodes
        # pass the invalid postcodes as list 
        self.invalid.extend([self.invalid1])
        # Emit a signal that the data has been preprocessed
        self.file_prepared.emit(True)
        self.page1.file_label.setText("The data is ready for calculations!")


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

############################################################################################################################################
    
    """@@@ Page2 (Mid Leg Journey) Methods @@@"""
    def check_trip_combo(self):
        """Check the number of trips chosen by the user"""
        self.num_trips = int(self.page2.trips_combo.currentText())

    def check_combo_mid_leg(self):
        """Check if the sum of the percentages for each country is 100. 
        If it is, then call the menu function. 
        If not, show a message box with an error.""" 
        # Get the percentages for Scotland and Rest of UK
        # Rest of UK percentages are the same for England, Wales and Northern Ireland
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
            success = QIcon(os.path.join(basedir, 'icons/success.svg'))
            msg.setWindowIcon(success)
            msg.setText("The data has been submitted!")
            # Add a success icon to the message box
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()

            self.hundred_percent.emit(True)

            # call the divide_address functions for each country
            self.travel_scotland = divide_scot_addresses(self.scotland, scot_bus, scot_car)
            self.travel_england = divide_uk_addresses(self.england, uk_plane, uk_car)
            self.travel_wales = divide_uk_addresses(self.wales, uk_plane, uk_car)
            self.travel_ni = divide_uk_addresses(self.north_ireland, uk_plane, uk_car)

        else:
            self.hundred_percent.emit(False)
            # Show a message box with the error
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            warning = QIcon(os.path.join(basedir, 'icons/warning.svg'))
            msg.setWindowIcon(warning)
            msg.setText("The sum of the percentages for each country must be 100!\nPlease try again.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()

############################################################################################################################################
    
    """@@@  Page 3 (Final Leg of Journey) Methods @@@"""
    def check_combo_page3(self):
        """Check if the sum of the percentages for each country is 100. If it is, then call the menu function. If not, show a message box with an error.""" 
        # call extract function from page3 to get the percentages for each country
        self.p_scot, self.p_eng, self.p_wales, self.p_ni, self.p_abe = self.page3.extract_percentages()

        # Sum of all
        sum_all = sum(self.p_scot.values()) + sum(self.p_eng.values()) + sum(self.p_wales.values()) + sum(self.p_ni.values()) + sum(self.p_abe.values())

        # If the sum of the percentages for each country is 800 (8 elements * 100), then call the menu function.
        if sum_all == 800:
            # Show a message that the data has been submitted
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            success = QIcon(os.path.join(basedir, 'icons/success.svg'))
            msg.setWindowIcon(success)
            msg.setText("The data has been submitted!")
            # Add a success icon to the message box
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
            self.hundred_percent_page3.emit(True)

        else:
            self.hundred_percent_page3.emit(False)
            # Show a message box with the error
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            warning = QIcon(os.path.join(basedir, 'icons/warning.svg'))
            msg.setWindowIcon(warning)
            msg.setText("The sum of the percentages for each country must be 100!\nPlease try again.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()

############################################################################################################################################
    
    """@@@  Page 4&5 (Results) Methods @@@"""
    def go_to_results(self):
        """Extract the final leg of the journey for each country"""
        # Crate a progress dialog
        pdg = QProgressDialog()
        pdg.setWindowTitle("Calculating")
        pdg.setLabelText("Please wait while distances and emissions are processed...")
        loading_icon = QIcon(os.path.join(basedir, 'icons/loading.svg'))
        pdg.setWindowIcon(loading_icon)
        self.pbar = QProgressBar()
        pdg.setBar(self.pbar)
        pdg.setMinimum(0)
        pdg.setMaximum(100)
        pdg.show()

        self.pbar.setValue(5)
        QtWidgets.QApplication.processEvents()

        """-------------Get Final Leg Data-------------"""

        # Divide the percentages into lists for each country
        scot = [int(i) for key, i in self.p_scot.items()]
        # Divide the percentages into lists for Aberdeen
        abe = [int(i) for key, i in self.p_abe.items()]
        # Call the divide_percentages function to divide the percentages into lists for each country and mode of transport
        eng_land, eng_air = divide_combo_percentages(self.p_eng)
        wales_land, wales_air = divide_combo_percentages(self.p_wales)
        ni_land, ni_air = divide_combo_percentages(self.p_ni)

        # Aberdeen
        aberdeen_values = self.aberdeen.values.tolist()
        aberdeen_distances = distance_home_uni(aberdeen_values)
        aberdeen_fleg = divide_aberdeen(aberdeen_distances, abe[0], abe[1], abe[2], abe[3])

        # Scotland
        # Combine the bus and rail postcodes for Scotland in a list to be used in the final leg function
        scot_bus_rail = self.travel_scotland[0] + self.travel_scotland[2]
        scot_fleg = assign_scotland(scot_bus_rail, scot[0], scot[1], scot[2])

        scot_car_fleg = scot_fleg[0] + aberdeen_fleg[0]
        scot_taxi_fleg = scot_fleg[1] + aberdeen_fleg[1]
        scot_bus_fleg = scot_fleg[2] + aberdeen_fleg[2]
        scot_walk_fleg = scot_fleg[3] + aberdeen_fleg[3]

        # England
        eng_rail = self.travel_england[2]
        eng_plane = self.travel_england[0]
        eng_fleg_bus_rail, eng_fleg_plane = assign_uk(eng_rail, eng_plane, eng_land[0], eng_land[1], eng_land[2], eng_air[0], eng_air[1], eng_air[2])
        
        eng_car_fleg = eng_fleg_bus_rail[0] + eng_fleg_plane[0]
        eng_taxi_fleg = eng_fleg_bus_rail[1] + eng_fleg_plane[1]
        eng_bus_fleg = eng_fleg_bus_rail[2] + eng_fleg_plane[2]
        eng_walk_fleg = eng_fleg_bus_rail[3] + eng_fleg_plane[3]

        # Wales
        wales_rail = self.travel_wales[2]
        wales_plane = self.travel_wales[0]
        wales_fleg_bus_rail, wales_fleg_plane = assign_uk(wales_rail, wales_plane, wales_land[0], wales_land[1], wales_land[2], wales_air[0], wales_air[1], wales_air[2])

        wales_car_fleg = wales_fleg_bus_rail[0] + wales_fleg_plane[0]
        wales_taxi_fleg = wales_fleg_bus_rail[1] + wales_fleg_plane[1]
        wales_bus_fleg = wales_fleg_bus_rail[2] + wales_fleg_plane[2]
        wales_walk_fleg = wales_fleg_bus_rail[3] + wales_fleg_plane[3]

        # Northern Ireland
        ni_rail = self.travel_ni[2]
        ni_plane = self.travel_ni[0]
        ni_fleg_bus_rail, ni_fleg_plane = assign_uk(ni_rail, ni_plane, ni_land[0], ni_land[1], ni_land[2], ni_air[0], ni_air[1], ni_air[2])

        ni_car_fleg = ni_fleg_bus_rail[0] + ni_fleg_plane[0]
        ni_taxi_fleg = ni_fleg_bus_rail[1] + ni_fleg_plane[1]
        ni_bus_fleg = ni_fleg_bus_rail[2] + ni_fleg_plane[2]
        ni_walk_fleg = ni_fleg_bus_rail[3] + ni_fleg_plane[3]

        self.pbar.setValue(15)
        # This is necessary for showing and updating the progress bar
        # Source: https://stackoverflow.com/questions/30823863/pyqt-progress-bar-not-updating-or-appearing-until-100
        QtWidgets.QApplication.processEvents()

        # Call the main function
        self.emissions, self.distances, self.total_emissions, self.total_distance_dict, all_invalid = main(self.emission_factors, self.travel_scotland, self.travel_england, self.travel_wales, self.travel_ni, scot_car_fleg, scot_taxi_fleg, scot_bus_fleg, scot_walk_fleg, eng_car_fleg, eng_taxi_fleg, eng_bus_fleg, eng_walk_fleg, wales_car_fleg, wales_taxi_fleg, wales_bus_fleg, wales_walk_fleg, ni_car_fleg, ni_taxi_fleg, ni_bus_fleg, ni_walk_fleg)
        self.invalid.extend([all_invalid])
        # Update the progress bar
        self.pbar.setValue(25)
        QtWidgets.QApplication.processEvents()

        """-------------Create the dataframes & figures for Base Data-------------"""	
        # Base emissions
        # Add Aberdeen emissions to the Scotland emissions
        aberdeen_car_emissions = aberdeen_fleg[0] * self.emission_factors['car']
        aberdeen_taxi_emissions = aberdeen_fleg[1] * self.emission_factors['taxi']
        aberdeen_bus_emissions = aberdeen_fleg[2] * self.emission_factors['bus']
        aberdeen_total_emissions = sum([aberdeen_car_emissions, aberdeen_taxi_emissions, aberdeen_bus_emissions])
        # Add the emissions for each mode of transport to the Scotland emissions
        scot_car_emissions = self.emissions['Scotland'].iloc[3] + aberdeen_car_emissions
        scot_taxi_emissions = self.emissions['Scotland'].iloc[4] + aberdeen_taxi_emissions
        scot_bus_emissions = self.emissions['Scotland'].iloc[2] + aberdeen_bus_emissions
        base_emissions = self.emissions
        base_emissions = base_emissions.drop('Walk', axis=0)
        base_emissions = base_emissions * self.num_trips
        base_emissions_fig = create_px(base_emissions, 'Total Emissions (kgCO2e) by Country and Method of Transport', 'Emissions (kgCO2e)', 'bupu')
        # Radio button 1
        self.page4.radio1.clicked.connect(lambda: self.display_figure(self.page4, base_emissions_fig))
        self.page5.radio1.clicked.connect(lambda: self.display_figure(self.page5, base_emissions_fig))

        # Base distances
        # Add Aberdeen distances to the Scotland distances
        self.distances['Scotland'].iloc[3] += aberdeen_fleg[0]
        self.distances['Scotland'].iloc[2] += aberdeen_fleg[2]
        self.distances['Scotland'].iloc[4] += aberdeen_fleg[1]
        self.distances['Scotland'].iloc[5] += aberdeen_fleg[3]

        base_distances = self.distances
        base_distances = base_distances * self.num_trips
        base_distances_fig = create_px(base_distances, 'Total Distance (km) by Country and Method of Transport', 'Distance (km)', 'bugn')
        # Radio button 2
        self.page4.radio2.clicked.connect(lambda: self.display_figure(self.page4, base_distances_fig))
        self.page5.radio2.clicked.connect(lambda: self.display_figure(self.page5, base_distances_fig))

        # Total emissions pie
        # Add the Aberdeen emissions to the Scotland emissions
        self.total_emissions['Scotland'] = self.total_emissions['Scotland'] + aberdeen_total_emissions
        total_emissions = self.total_emissions
        total_emissions = total_emissions * self.num_trips
        names = total_emissions.columns
        values = total_emissions.iloc[0, :]
        total_emissions_pie = px.pie(total_emissions, values=values, names=names, title='Total Emissions by Country (in kgCO2e)', labels=dict(names="Country", values="Emissions (kgCO2e)"))
        total_emissions_pie.update_traces(textfont_size=16)
        # Radio button 3
        self.page4.radio3.clicked.connect(lambda: self.display_figure(self.page4, total_emissions_pie))
        self.page5.radio3.clicked.connect(lambda: self.display_figure(self.page5, total_emissions_pie))

        # Emissions per student by country
        per_student = self.total_emissions
        per_student = per_student * self.num_trips
         # Divide the total emissions by the number of students for each country
        total_scot_students = len(self.scotland) + len(self.aberdeen)
        scot_emissions = per_student.iloc[0, 0] / total_scot_students
        eng_emissions = per_student.iloc[0, 1] / len(self.england)
        wales_emissions = per_student.iloc[0, 2] / len(self.wales)
        ni_emissions = per_student.iloc[0, 3] / len(self.north_ireland)

        # Create a pie chart
        # Source: https://plotly.com/python/pie-charts/
        labels = ['Scotland', 'England', 'Wales', 'Northern Ireland']
        values = [scot_emissions, eng_emissions, wales_emissions, ni_emissions]
        # Round the values to 0 decimal places
        values = [round(i, 1) for i in values]
        # Figure to store the pie chart with the emissions per student
        per_student = px.pie(values=values, names=labels, title='Emissions per Student by Country (in kgCO2e)', labels=dict(names="Country", values="Emissions (kgCO2e)"), color_discrete_sequence=px.colors.sequential.RdBu)
        # Edit the font size and color of the values
        per_student.update_traces(textfont_size=16)
        # Radio button 4
        self.page4.radio4.clicked.connect(lambda: self.display_figure(self.page4, per_student))
        self.page5.radio4.clicked.connect(lambda: self.display_figure(self.page5, per_student))

        # Update the progress bar
        self.pbar.setValue(35)
        QtWidgets.QApplication.processEvents()

        """-------------Create the dataframes & figures for Councils-------------"""
        # Scotland
        car_dict, bus_dict, rail_dict, taxi_dict, total_ems = self.create_council_areas(self.scotland, 'Scotland')
 
        # Create a dictionary with the total distance for each mode of transport for Scotland + Aberdeen
        new_car = {}
        new_car.update(car_dict)
        new_car['Aberdeen City'] = aberdeen_fleg[0]

        new_bus = {}
        new_bus.update(bus_dict)
        new_bus['Aberdeen City'] = aberdeen_fleg[2]

        new_taxi = {}
        new_taxi.update(taxi_dict)
        new_taxi['Aberdeen City'] = aberdeen_fleg[1]

        # Add the Aberdeen emissions to the total_ems dictionary
        total_ems['Aberdeen City'] = aberdeen_total_emissions

        df_car, df_car_emissions = create_dfs(new_car, self.emission_factors['car'], self.num_trips)
        df_bus, df_bus_emissions = create_dfs(new_bus, self.emission_factors['coach'], self.num_trips)
        df_rail, df_rail_emissions = create_dfs(rail_dict, self.emission_factors['rail'], self.num_trips)
        df_taxi, df_taxi_emissions = create_dfs(new_taxi, self.emission_factors['taxi'], self.num_trips)

        # Council distances
        scot_car = create_go_bar(df_car, 'Car Travel Distances Across Scottish Councils', 'Distance (km)')
        scot_bus = create_go_bar(df_bus, 'Bus Travel Distances Across Scottish Councils', 'Distance (km)')
        scot_rail = create_go_bar(df_rail, 'Rail Travel Distances Across Scottish Councils', 'Distance (km)')
        scot_taxi = create_go_bar(df_taxi, 'Taxi Travel Distances Across Scottish Councils', 'Distance (km)')

        # Page 4 Radio buttons 5, 6, 7, 8
        self.page4.radio5.clicked.connect(lambda: self.display_figure(self.page4, scot_car))
        self.page4.radio6.clicked.connect(lambda: self.display_figure(self.page4, scot_bus))
        self.page4.radio7.clicked.connect(lambda: self.display_figure(self.page4, scot_rail))
        self.page4.radio8.clicked.connect(lambda: self.display_figure(self.page4, scot_taxi))

        # Council emissions
        scot_car_emissions = create_go_bar(df_car_emissions, 'Car Travel Emissions Across Scottish Councils', 'Emissions (kgCO2e)')
        scot_bus_emissions = create_go_bar(df_bus_emissions, 'Bus Travel Emissions Across Scottish Councils', 'Emissions (kgCO2e)')
        scot_rail_emissions = create_go_bar(df_rail_emissions, 'Rail Travel Emissions Across Scottish Councils', 'Emissions (kgCO2e)')
        scot_taxi_emissions = create_go_bar(df_taxi_emissions, 'Taxi Travel Emissions Across Scottish Councils', 'Emissions (kgCO2e)')

        # Page 5 Radio buttons 5,6,7,8
        self.page5.radio5.clicked.connect(lambda: self.display_figure(self.page5, scot_car_emissions))
        self.page5.radio6.clicked.connect(lambda: self.display_figure(self.page5, scot_bus_emissions))
        self.page5.radio7.clicked.connect(lambda: self.display_figure(self.page5, scot_rail_emissions))
        self.page5.radio8.clicked.connect(lambda: self.display_figure(self.page5, scot_taxi_emissions))

        # Table for total emissions by council area
        total_emissions_table = create_go_table_dict(total_ems, 'Total Emissions (kgCO2e) by Scottish Council Area')
        # Radio button 1
        self.page5.radio1.clicked.connect(lambda: self.display_figure(self.page5, total_emissions_table))
        
        self.pbar.setValue(45)
        QtWidgets.QApplication.processEvents()

        # England
        car_dict_eng, bus_dict_eng, rail_dict_eng, taxi_dict_eng, total_ems_eng = self.create_council_areas(self.england, 'England')
        df_car_eng, df_car_emissions_eng = create_dfs(car_dict_eng, self.emission_factors['car'], self.num_trips)
        df_bus_eng, df_bus_emissions_eng = create_dfs(bus_dict_eng, self.emission_factors['coach'], self.num_trips)
        df_rail_eng, df_rail_emissions_eng = create_dfs(rail_dict_eng, self.emission_factors['rail'], self.num_trips)
        df_taxi_eng, df_taxi_emissions_eng = create_dfs(taxi_dict_eng, self.emission_factors['taxi'], self.num_trips)

        # Council distances
        values_distance = ['Council Area', 'Distance (km)']
        eng_car = create_go_table(df_car_eng, values_distance, 'Car Travel Distances Across English Councils')
        eng_bus = create_go_table(df_bus_eng, values_distance, 'Bus Travel Distances Across English Councils')
        eng_rail = create_go_table(df_rail_eng, values_distance, 'Rail Travel Distances Across English Councils')
        eng_taxi = create_go_table(df_taxi_eng, values_distance, 'Taxi Travel Distances Across English Councils')

        # Page 4 radio buttons 9, 10, 11, 12
        self.page4.radio9.clicked.connect(lambda: self.display_figure(self.page4, eng_car))
        self.page4.radio10.clicked.connect(lambda: self.display_figure(self.page4, eng_bus))
        self.page4.radio11.clicked.connect(lambda: self.display_figure(self.page4, eng_rail))
        self.page4.radio12.clicked.connect(lambda: self.display_figure(self.page4, eng_taxi))

        # Council emissions
        values = ['Council Area', 'Emissions (kgCO2e)']
        eng_car_emissions = create_go_table(df_car_emissions_eng, values, 'Car Travel Emissions Across English Councils')
        eng_bus_emissions = create_go_table(df_bus_emissions_eng, values, 'Bus Travel Emissions Across English Councils')
        eng_rail_emissions = create_go_table(df_rail_emissions_eng, values, 'Rail Travel Emissions Across English Councils')
        eng_taxi_emissions = create_go_table(df_taxi_emissions_eng, values, 'Taxi Travel Emissions Across English Councils')

        # Page 5 Radio buttons 9, 10, 11, 12
        self.page5.radio9.clicked.connect(lambda: self.display_figure(self.page5, eng_car_emissions))
        self.page5.radio10.clicked.connect(lambda: self.display_figure(self.page5, eng_bus_emissions))
        self.page5.radio11.clicked.connect(lambda: self.display_figure(self.page5, eng_rail_emissions))
        self.page5.radio12.clicked.connect(lambda: self.display_figure(self.page5, eng_taxi_emissions))

        # Table for total emissions by council area
        total_emissions_table_eng = create_go_table_dict(total_ems_eng, 'Total Emissions (kgCO2e) by English Council Area')
        # Radio button 2
        self.page5.radio2.clicked.connect(lambda: self.display_figure(self.page5, total_emissions_table_eng))
        
        self.pbar.setValue(55)
        QtWidgets.QApplication.processEvents()
        
        # Wales
        car_dict_wales, bus_dict_wales, rail_dict_wales, taxi_dict_wales, total_ems_wales = self.create_council_areas(self.wales, 'Wales')
        df_car_wales, df_car_emissions_wales = create_dfs(car_dict_wales, self.emission_factors['car'], self.num_trips)
        df_bus_wales, df_bus_emissions_wales = create_dfs(bus_dict_wales, self.emission_factors['coach'], self.num_trips)
        df_rail_wales, df_rail_emissions_wales = create_dfs(rail_dict_wales, self.emission_factors['rail'], self.num_trips)
        df_taxi_wales, df_taxi_emissions_wales = create_dfs(taxi_dict_wales, self.emission_factors['taxi'], self.num_trips)

        # Council distances
        wales_car = create_go_bar(df_car_wales, 'Car Travel Distances Across Welsh Councils', 'Distance (km)')
        wales_bus = create_go_bar(df_bus_wales, 'Bus Travel Distances Across Welsh Councils', 'Distance (km)')
        wales_rail = create_go_bar(df_rail_wales, 'Rail Travel Distances Across Welsh Councils', 'Distance (km)')
        wales_taxi = create_go_bar(df_taxi_wales, 'Taxi Travel Distances Across Welsh Councils', 'Distance (km)')

        # Page 4 radio buttons 13, 14, 15, 16
        self.page4.radio13.clicked.connect(lambda: self.display_figure(self.page4, wales_car))
        self.page4.radio14.clicked.connect(lambda: self.display_figure(self.page4, wales_bus))
        self.page4.radio15.clicked.connect(lambda: self.display_figure(self.page4, wales_rail))
        self.page4.radio16.clicked.connect(lambda: self.display_figure(self.page4, wales_taxi))

        # Council emissions
        wales_car_emissions = create_go_bar(df_car_emissions_wales, 'Car Travel Emissions Across Welsh Councils', 'Emissions (kgCO2e)')
        wales_bus_emissions = create_go_bar(df_bus_emissions_wales, 'Bus Travel Emissions Across Welsh Councils', 'Emissions (kgCO2e)')
        wales_rail_emissions = create_go_bar(df_rail_emissions_wales, 'Rail Travel Emissions Across Welsh Councils', 'Emissions (kgCO2e)')
        wales_taxi_emissions = create_go_bar(df_taxi_emissions_wales, 'Taxi Travel Emissions Across Welsh Councils', 'Emissions (kgCO2e)')

        # Page 5 Radio buttons 13, 14, 15, 16
        self.page5.radio13.clicked.connect(lambda: self.display_figure(self.page5, wales_car_emissions))
        self.page5.radio14.clicked.connect(lambda: self.display_figure(self.page5, wales_bus_emissions))
        self.page5.radio15.clicked.connect(lambda: self.display_figure(self.page5, wales_rail_emissions))
        self.page5.radio16.clicked.connect(lambda: self.display_figure(self.page5, wales_taxi_emissions))

        # Table for total emissions by council area
        total_emissions_table_wales = create_go_table_dict(total_ems_wales, 'Total Emissions (kgCO2e) by Welsh Council Area')
        # Radio button 3
        self.page5.radio3.clicked.connect(lambda: self.display_figure(self.page5, total_emissions_table_wales))
 
        self.pbar.setValue(75)
        QtWidgets.QApplication.processEvents()
        
        # Northern Ireland
        car_dict_ni, bus_dict_ni, rail_dict_ni, taxi_dict_ni, total_ems_ni = self.create_council_areas(self.north_ireland, 'Northern Ireland')
        df_car_ni, df_car_emissions_ni = create_dfs(car_dict_ni, self.emission_factors['car'], self.num_trips)
        df_bus_ni, df_bus_emissions_ni = create_dfs(bus_dict_ni, self.emission_factors['coach'], self.num_trips)
        df_rail_ni, df_rail_emissions_ni = create_dfs(rail_dict_ni, self.emission_factors['rail'], self.num_trips)
        df_taxi_ni, df_taxi_emissions_ni = create_dfs(taxi_dict_ni, self.emission_factors['taxi'], self.num_trips)

        # Council distances
        ni_car = create_go_bar(df_car_ni, 'Car Travel Distances Across Northern Irish Councils', 'Distance (km)')
        ni_bus = create_go_bar(df_bus_ni, 'Bus Travel Distances Across Northern Irish Councils', 'Distance (km)')
        ni_rail = create_go_bar(df_rail_ni, 'Rail Travel Distances Across Northern Irish Councils', 'Distance (km)')
        ni_taxi = create_go_bar(df_taxi_ni, 'Taxi Travel Distances Across Northern Irish Councils', 'Distance (km)')

        # Page 4 radio buttons 17, 18, 19, 20
        self.page4.radio17.clicked.connect(lambda: self.display_figure(self.page4, ni_car))
        self.page4.radio18.clicked.connect(lambda: self.display_figure(self.page4, ni_bus))
        self.page4.radio19.clicked.connect(lambda: self.display_figure(self.page4, ni_rail))
        self.page4.radio20.clicked.connect(lambda: self.display_figure(self.page4, ni_taxi))

        # Council emissions
        ni_car_emissions = create_go_bar(df_car_emissions_ni, 'Car Travel Emissions Across Northern Irish Councils', 'Emissions (kgCO2e)')
        ni_bus_emissions = create_go_bar(df_bus_emissions_ni, 'Bus Travel Emissions Across Northern Irish Councils', 'Emissions (kgCO2e)')
        ni_rail_emissions = create_go_bar(df_rail_emissions_ni, 'Rail Travel Emissions Across Northern Irish Councils', 'Emissions (kgCO2e)')
        ni_taxi_emissions = create_go_bar(df_taxi_emissions_ni, 'Taxi Travel Emissions Across Northern Irish Councils', 'Emissions (kgCO2e)')

        # Page 5 Radio buttons 17, 18, 19, 20
        self.page5.radio17.clicked.connect(lambda: self.display_figure(self.page5, ni_car_emissions))
        self.page5.radio18.clicked.connect(lambda: self.display_figure(self.page5, ni_bus_emissions))
        self.page5.radio19.clicked.connect(lambda: self.display_figure(self.page5, ni_rail_emissions))
        self.page5.radio20.clicked.connect(lambda: self.display_figure(self.page5, ni_taxi_emissions))

        # Table for total emissions by council area
        total_emissions_table_ni = create_go_table_dict(total_ems_ni, 'Total Emissions (kgCO2e) by Northern Irish Council Area')
        # Radio button 4
        self.page5.radio4.clicked.connect(lambda: self.display_figure(self.page5, total_emissions_table_ni))
        
        self.pbar.setValue(100)
        QtWidgets.QApplication.processEvents()

        # Show the results page
        self.stackedLayout.setCurrentIndex(3)
 
    def display_figure(self, page, figure):
        """Maybe add the figures and radiobuttons to lists
        and loop over them to connect them to the radio buttons"""
        page.webview.setHtml(figure.to_html(include_plotlyjs='cdn'))


    def create_council_areas(self, country_posctodes: list, country: str):
        # Get the districts for each country
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
        total_emissions = {}

        for key, value in country_percent.items():
            # Divide the total distance for each mode of transport by the percentage of people using it
            car_dict[key] = {'Car' : car * (value / 100)}
            bus_dict[key] = {'Bus' : bus * (value / 100)}
            rail_dict[key] = {'Rail' : rail * (value / 100)}
            taxi_dict[key] = {'Taxi' : taxi * (value / 100)}
            total_emissions[key] = car_dict[key]['Car'] * self.emission_factors['car'] + bus_dict[key]['Bus'] * self.emission_factors['coach'] + rail_dict[key]['Rail'] * self.emission_factors['rail'] + taxi_dict[key]['Taxi'] * self.emission_factors['taxi']

        total_car = sum(car_dict[key]['Car'] for key in car_dict)
        total_bus = sum(bus_dict[key]['Bus'] for key in bus_dict)
        total_rail = sum(rail_dict[key]['Rail'] for key in rail_dict)

        # Get the total distance for each mode of transport for the country from self.total_distances
        init_total_car = self.total_distance_dict[country][3]
        init_total_bus = self.total_distance_dict[country][2]
        init_total_rail = self.total_distance_dict[country][0]

        # If the total distance for each mode of transport is not the same as the sum of the distances for each council area
        # add the difference to the Uknown council area
        if total_car != init_total_car:
            car_dict['Unknown'] = {'Car' : init_total_car - total_car}
        if total_bus != init_total_bus:
            bus_dict['Unknown'] = {'Bus' : init_total_bus - total_bus}
        if total_rail != init_total_rail:
            rail_dict['Unknown'] = {'Rail' : init_total_rail - total_rail}

        return car_dict, bus_dict, rail_dict, taxi_dict, total_emissions

"""==============================================Run the app=============================================="""
app = QApplication(sys.argv)
window = Calculator()
window.show()
sys.exit(app.exec())
