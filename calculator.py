import sys
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QStackedLayout, QMessageBox
from PyQt6.QtCore import pyqtSignal
from tkinter.filedialog import askopenfile
import pandas as pd
from preprocess_data import menu, determine_postcode
from final_leg import select_country
from page1 import MainPage
from page2 import Page2
from page3 import Page3
from main import main

"""
Info:

- main page is the menu that is first shown (page1)
- page2 is the second page where the user selects the percentages of students travelling by each transport method
  for Scotland and the rest of the UK
- page3 is the third page where the user selects the travel assumptions for the final leg of the journey 
  from Aberdeen transport hub to the University of Aberdeen

"""

class Calculator(QWidget):

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

    def initializeUI(self):
        """Set up application GUI"""
        self.setFixedSize(800, 600)
        self.setWindowTitle("StudentGreenTravel")

        # Layouts for pages
        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        self.layout3 = QVBoxLayout()

        # Stacked layout to hold the pages
        # Source: https://www.tutorialspoint.com/pyqt/pyqt_qstackedwidget.htm 
        self.stackedLayout = QStackedLayout()

        # Create the pages
        self.page1 = MainPage()
        self.page2 = Page2()
        self.page3 = Page3()

        # Add the pages to the stacked layout and set the stacked layout as the main layout
        self.stackedLayout.addWidget(self.page1)
        self.stackedLayout.addWidget(self.page2)
        self.stackedLayout.addWidget(self.page3)

        self.setLayout(self.stackedLayout)

        # Connect signals for page1
        self.page1.button1.clicked.connect(self.go_to_page2)
        self.page1.button2.clicked.connect(self.open_file)
        self.file_selected.connect(self.enable_buttons1)

        # Connect signals for page2
        self.page2.next_button2.clicked.connect(self.go_to_page3)
        self.page2.submit.clicked.connect(self.check_combo_page2)
        self.page2.back.clicked.connect(self.go_to_page1)
        self.hundred_percent.connect(self.enable_page2)

        # Connect signals for page3
        self.page3.back.clicked.connect(self.go_to_page2)
        self.page3.result_button.clicked.connect(self.go_to_results)
        self.hundred_percent_page3.connect(self.enable_page3)
        self.page3.submit.clicked.connect(self.check_combo_page3)

        # Show the main page
        self.show()

    """==============================================Methods for pages=============================================="""
    def open_file(self):
        file = askopenfile(filetypes=[("Excel files", "*.xlsx")])
        # If the user selected a file, then read it using pandas
        if file:
        # Read address file
            addresses = pd.read_excel(file.name, engine='openpyxl')
            addresses.iloc[:, 1] = addresses.iloc[:, 1].str.replace(' ', '')
            # Add the file name to the label text with the file name withouth the path
            self.page1.file_label.setText(f"File: {file.name.split('/')[-1]}")
            self.scotland, self.wales, self.north_ireland, self.england = determine_postcode(addresses.iloc[:, 1])
            # Style the label
            #self.file_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #2d3436;")
            # Emit signal that a file has been selected
            self.file_selected.emit(True)
            # Call the function to enable the button
            # self.enable_buttons(True)
        else:
            self.page1.file_label.setText("No file was selected.")
            # Emit a signal that a file has not been selected
            self.file_selected.emit(False)


    def enable_buttons1(self, file_selected):
        if file_selected:
            self.page1.button1.setEnabled(True)
        else:
            self.page1.button1.setEnabled(False)

    def go_to_page1(self):
        self.stackedLayout.setCurrentIndex(0)
    
    def go_to_page2(self):
        self.stackedLayout.setCurrentIndex(1)

    def go_to_page3(self):
        self.stackedLayout.setCurrentIndex(2)


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

        if scot_sum == 100 and uk_sum == 100:
            # Show a message that the data has been submitted
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("The data has been submitted!")
            # Add a success icon to the message box
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
            # take the returns from the file explorer function without running it again
            scotland, wales, north_ireland, england = self.get_country_data()
            #print(scotland)
            self.hundred_percent.emit(True)
            # call the menu function
            self.travel_scotland, self.travel_england, self.travel_wales, self.travel_ni = menu(scotland, wales, north_ireland, england, int(self.page2.combo_car_scot.currentText()), int(self.page2.combo_bus_scot.currentText()), int(self.page2.combo_rail_scot.currentText()), int(self.page2.plane_uk.currentText()), int(self.page2.car_uk.currentText()), int(self.page2.rail_uk.currentText()))
            
        else:
            self.hundred_percent.emit(False)
            # Show a message box with the error
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("The sum of the percentages for each country must be 100!\nPlease try again.")
            # Add a warning icon to the message box
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()

    def enable_page2(self, hundred_percent):
        if hundred_percent:
            self.page2.next_button2.setEnabled(True)
        else:
            self.page2.next_button2.setEnabled(False)

    def get_country_data(self):
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
            msg.setText("The data has been submitted!")
            # Add a success icon to the message box
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
            self.hundred_percent_page3.emit(True)
            # Combine the bus and rail postcodes for Scotland in a list to be used in the final leg function
            scot_bus_rail = self.travel_scotland[0] + self.travel_scotland[2]
            # Call the select_country function
            # Scotland
            self.scot_fleg = select_country(scot_bus_rail, [], "Scotland", scot[0], scot[1], scot[2], scot[3], 0, 0, 0, 0)

            # England
            eng_rail = self.travel_england[2]
            eng_plane = self.travel_england[0]
            self.eng_fleg_bus_rail, self.eng_fleg_plane = select_country(eng_rail, eng_plane, "England", eng_land[0], eng_land[1], eng_land[2], eng_land[3], eng_air[0], eng_air[1], eng_air[2], eng_air[3])

            # Wales
            wales_rail = self.travel_wales[2]
            wales_plane = self.travel_wales[0]
            self.wales_fleg_bus_rail, self.wales_fleg_plane = select_country(wales_rail, wales_plane, "Wales", wales_land[0], wales_land[1], wales_land[2], wales_land[3], wales_air[0], wales_air[1], wales_air[2], wales_air[3])

            # Northern Ireland
            ni_rail = self.travel_ni[2]
            ni_plane = self.travel_ni[0]
            self.ni_fleg_bus_rail, self.ni_fleg_plane = select_country(ni_rail, ni_plane, "Northern Ireland", ni_land[0], ni_land[1], ni_land[2], ni_land[3], ni_air[0], ni_air[1], ni_air[2], ni_air[3])

            # NEED to Extract the total distance travelled by each mode of transport in the final leg of the journey as in main.py
            # Sum them as in total distances part of main.py
        else:
            self.hundred_percent_page3.emit(False)
            # Show a message box with the error
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("The sum of the percentages for each country must be 100!\nPlease try again.")
            # Add a warning icon to the message box
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()

    def enable_page3(self, hundred_percent_page3):
        """Enable the result button if you get signal"""
        if hundred_percent_page3:
            self.page3.result_button.setEnabled(True)
        else:
            self.page3.result_button.setEnabled(False)

    def go_to_results(self):
        """Extract the final leg of the journey for each country"""
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

        # Call the main function
        main(self.travel_scotland, self.travel_england, self.travel_wales, self.travel_ni, scot_car_fleg, scot_taxi_fleg, scot_bus_fleg, scot_walk_fleg, eng_car_fleg, eng_taxi_fleg, eng_bus_fleg, eng_walk_fleg, wales_car_fleg, wales_taxi_fleg, wales_bus_fleg, wales_walk_fleg, ni_car_fleg, ni_taxi_fleg, ni_bus_fleg, ni_walk_fleg)


"""==============================================Run the app=============================================="""
app = QApplication(sys.argv)
window = Calculator()
sys.exit(app.exec())
