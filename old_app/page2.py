import sys
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel, QGridLayout, QComboBox, QMessageBox, QHBoxLayout
from PyQt6.QtCore import Qt, QSize
from final_leg import select_country
from page3 import Page3

class Page2(QWidget):

    # Signal to enable the show results button
    grids = []

    def __init__(self, Page1):
        super().__init__()
        # Have a reference to the previous page for the back button
        self.page1 = Page1
        self.setUpMainWindow("Scotland")
        self.setUpMainWindow("England")
        self.setUpMainWindow("Wales")
        self.setUpMainWindow("Northern Ireland")
        self.addGrids()
        self.addButtons()
        self.show()

    def setUpMainWindow(self, country: str):
        """Create and arrange widgets in the main windows"""
        instruction_label = QLabel("Select the travel assumptions for the final leg of the journey.\nFrom Aberdeen transport hub to the University of Aberdeen")
        # instruction_label.setFont(QFont("Arial", 14))
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Create a QVBoxLayout to arrange elements
        self.main_layout = QVBoxLayout()
        # Add the instruction label
        self.main_layout.addWidget(instruction_label)

        # Create a elements for Scotland
        # Labels
        scot_label = QLabel(country)
        # scot_label.setFont(QFont("Arial", 14))
        # Style the label to be with a blue background
        # scot_label.setStyleSheet("background-color: #e6f7ff; border: 1px solid #4da6ff; border-radius: 5px; padding: 5px;")
        scot_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        land_label = QLabel("Assumptions for land travelling students")
        # Background color must be different blue from the main label
        # land_label.setStyleSheet("background-color: #cce6ff; border: 1px solid #4da6ff; border-radius: 5px; padding: 5px;")
        # land_label.setFont(QFont("Arial", 12))
        # Add appropriate background color different from the main label
        
        land_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        air_label = QLabel("Assumptions for air travelling students")
        # air_label.setFont(QFont("Arial", 12))
        # air_label.setStyleSheet("background-color: #cce6ff; border: 1px solid #4da6ff; border-radius: 5px; padding: 5px;")
        air_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        scot_car = QLabel("Car")
        # scot_car.setFont(QFont("Arial", 11))
        scot_car.setAlignment(Qt.AlignmentFlag.AlignLeft)

        
        uk_car = QLabel("Car")
        # uk_car.setFont(QFont("Arial", 11))
        uk_car.setAlignment(Qt.AlignmentFlag.AlignLeft)

        scot_taxi = QLabel("Taxi")
        # scot_taxi.setFont(QFont("Arial", 11))
        scot_taxi.setAlignment(Qt.AlignmentFlag.AlignLeft)

        uk_taxi = QLabel("Taxi")
        # uk_taxi.setFont(QFont("Arial", 11))
        uk_taxi.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        scot_bus = QLabel("Bus")
        # scot_bus.setFont(QFont("Arial", 11))
        scot_bus.setAlignment(Qt.AlignmentFlag.AlignLeft)

        uk_bus = QLabel("Bus")
        # uk_bus.setFont(QFont("Arial", 11))
        uk_bus.setAlignment(Qt.AlignmentFlag.AlignLeft)

        scot_walk = QLabel("Walk")
        # scot_walk.setFont(QFont("Arial", 11))
        scot_walk.setAlignment(Qt.AlignmentFlag.AlignLeft)

        uk_walk = QLabel("Walk")
        # uk_walk.setFont(QFont("Arial", 11))
        uk_walk.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Combo boxes
        self.scot_car_box = QComboBox()
        self.scot_taxi_box = QComboBox()
        self.scot_bus_box = QComboBox()
        self.scot_walk_box = QComboBox()

        self.uk_car_box = QComboBox()
        self.uk_taxi_box = QComboBox()
        self.uk_bus_box = QComboBox()
        self.uk_walk_box = QComboBox()


        combos = []
        combos.append(self.scot_car_box)
        combos.append(self.scot_taxi_box)
        combos.append(self.scot_bus_box)
        combos.append(self.scot_walk_box)
        combos.append(self.uk_car_box)
        combos.append(self.uk_taxi_box)
        combos.append(self.uk_bus_box)
        combos.append(self.uk_walk_box)

        # Values for combo boxes
        values = [str(i) for i in range(101)]
        for combo_box in combos:
            combo_box.addItems(values)
            # Set fixed width
            combo_box.setFixedSize(QSize(50, 20))

        # Grid for Scotland
        if country == "Scotland":
            self.scot_grid = QGridLayout()
            self.scot_grid.setVerticalSpacing(2)
            # Shrink space between columns
            self.scot_grid.setHorizontalSpacing(10)


            # Scot label must take 4 columns
            self.scot_grid.addWidget(scot_label, 0, 0, 1, 4)
            self.scot_grid.addWidget(land_label, 1, 0)
            self.scot_grid.addWidget(scot_car, 2, 0)
            self.scot_grid.addWidget(scot_taxi, 3, 0)
            self.scot_grid.addWidget(scot_bus, 4, 0)
            self.scot_grid.addWidget(scot_walk, 5, 0)
            self.scot_grid.addWidget(self.scot_car_box, 2, 1)
            self.scot_grid.addWidget(self.scot_taxi_box, 3, 1)
            self.scot_grid.addWidget(self.scot_bus_box, 4, 1)
            self.scot_grid.addWidget(self.scot_walk_box, 5, 1)

            # Set grid row width to be smaller
            self.scot_grid.setRowStretch(0, 1)


            self.grids.append(self.scot_grid)

        else:
            self.grid = QGridLayout()
            # Shrink the label rows
            self.grid.setVerticalSpacing(2)
            # Shrink space between columns
            self.grid.setHorizontalSpacing(50)


            # self.grid.addWidget(scot_label, 0, 0, 1, 4)
            # self.grid.addWidget(land_label, 1, 0)
            # self.grid.addWidget(air_label, 1, 2)
            # self.grid.addWidget(scot_car, 2, 0)
            # self.grid.addWidget(scot_taxi, 3, 0)
            # self.grid.addWidget(scot_bus, 4, 0)
            # self.grid.addWidget(scot_walk, 5, 0)
            # self.grid.addWidget(self.scot_car_box, 2, 1)
            # self.grid.addWidget(self.scot_taxi_box, 3, 1)
            # self.grid.addWidget(self.scot_bus_box, 4, 1)
            # self.grid.addWidget(self.scot_walk_box, 5, 1)

            # self.grid.addWidget(uk_car, 2, 2)
            # self.grid.addWidget(uk_taxi, 3, 2)
            # self.grid.addWidget(uk_bus, 4, 2)
            # self.grid.addWidget(uk_walk, 5, 2)

            # self.grid.addWidget(self.uk_car_box, 2, 3)
            # self.grid.addWidget(self.uk_taxi_box, 3, 3)
            # self.grid.addWidget(self.uk_bus_box, 4, 3)
            # self.grid.addWidget(self.uk_walk_box, 5, 3)


            self.grids.append(self.grid)


    def addGrids(self):
        for i in self.grids:
            self.main_layout.addLayout(i)
            self.setLayout(self.main_layout)
        self.main_layout.addStretch(1)

    def addButtons(self):
        self.submit_button = QPushButton("Submit", clicked=self.checkCombos)
        self.show_results_button = QPushButton("Results", clicked=self.showResults)
        self.show_results_button.setEnabled(False)


        # Button layout
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.submit_button)
        self.button_layout.addWidget(self.show_results_button)

        self.main_layout.addLayout(self.button_layout)

    def checkCombos(self):
        # Check if the sum of the values in the combo boxes for each country is equal to 100
        # If true, enable the show results button
        # If false, disable the show results button
        scot_values = [int(self.scot_car_box.currentText()), int(self.scot_taxi_box.currentText()), int(self.scot_bus_box.currentText()), int(self.scot_walk_box.currentText())]
        eng_values = [int(self.uk_car_box.currentText()), int(self.uk_taxi_box.currentText()), int(self.uk_bus_box.currentText()), int(self.uk_walk_box.currentText())]
        wales_values = [int(self.uk_car_box.currentText()), int(self.uk_taxi_box.currentText()), int(self.uk_bus_box.currentText()), int(self.uk_walk_box.currentText())]
        ni_values = [int(self.uk_car_box.currentText()), int(self.uk_taxi_box.currentText()), int(self.uk_bus_box.currentText()), int(self.uk_walk_box.currentText())]

        if sum(scot_values) == 100 and sum(eng_values) == 100 and sum(wales_values) == 100 and sum(ni_values) == 100:
            # Enable the show results button
            self.show_results_button.setEnabled(True)

            # Show a success message
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("All values are valid")
            msg.exec()

        else:
            # Disable the show results button, show an error message
            self.show_results_button.setEnabled(False)

            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("The sum of the values must be equal to 100")
            msg.exec()

    def showResults(self):
        # Get the values from the combo boxes and calculate the distance
        scot_values = [int(self.scot_car_box.currentText()), int(self.scot_taxi_box.currentText()), int(self.scot_bus_box.currentText()), int(self.scot_walk_box.currentText())]
        eng_values = [int(self.uk_car_box.currentText()), int(self.uk_taxi_box.currentText()), int(self.uk_bus_box.currentText()), int(self.uk_walk_box.currentText())]
        wales_values = [int(self.uk_car_box.currentText()), int(self.uk_taxi_box.currentText()), int(self.uk_bus_box.currentText()), int(self.uk_walk_box.currentText())]
        ni_values = [int(self.uk_car_box.currentText()), int(self.uk_taxi_box.currentText()), int(self.uk_bus_box.currentText()), int(self.uk_walk_box.currentText())]

        bus_scotland = self.page1.travel_scotland[0]
        rail_scotland = self.page1.travel_scotland[1]
        scot_bus_rail = bus_scotland + rail_scotland

        rail_england = self.page1.travel_england[2]
        plane_england = self.page1.travel_england[0]
        

        rail_wales = self.page1.travel_wales[2]
        plane_wales = self.page1.travel_wales[0]

        rail_ni = self.page1.travel_north_ireland[2]
        plane_ni = self.page1.travel_north_ireland[0]

        if sum(scot_values) == 100 and sum(eng_values) == 100 and sum(wales_values) == 100 and sum(ni_values) == 100:
            # Show a message that the data has been submitted
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("The data has been submitted!")
            # Add a success icon to the message box
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
            #self.all_selected.emit(True)
            # call the select_country function for each country
            print(int(self.scot_car_box.currentText()))
            print(int(self.scot_taxi_box.currentText()))
            print(int(self.scot_bus_box.currentText()))
            print(int(self.scot_walk_box.currentText())) 
            scot_fleg = select_country(scot_bus_rail, [], "Scotland", int(self.scot_car_box.currentText()), int(self.scot_taxi_box.currentText()), int(self.scot_bus_box.currentText()), int(self.scot_walk_box.currentText()))
            # eng_bus_rail, eng_plane = select_country(rail_england, plane_england, "England", int(self.car_eng2.currentText()), int(self.taxi_eng2.currentText()), int(self.bus_eng2.currentText()), int(self.walk_eng2.currentText()))
            # wales_bus_rail, wales_plane = select_country(rail_wales, plane_wales, "Wales", int(self.car_wales2.currentText()), int(self.taxi_wales2.currentText()), int(self.bus_wales2.currentText()), int(self.walk_wales2.currentText()))
            # ni_bus_rail, ni_plane = select_country(rail_ni, plane_ni, "Northern Ireland", int(self.car_ni2.currentText()), int(self.taxi_ni2.currentText()), int(self.bus_ni2.currentText()), int(self.walk_ni2.currentText()))
            print(scot_fleg)

        else:
            #self.all_selected.emit(False)
            # Show a message box with the error
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("The sum of the percentages for each country must be 100!\nPlease try again.")
            # Add a warning icon to the message box
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()

    def enable(self, all_selected):
        if all_selected:
            self.show_results_button.setEnabled(True)
            self.show_results_button.clicked.connect(lambda: self.show_page(Page3()))

    def show_page(self, page):
        self.parent().setCentralWidget(page)