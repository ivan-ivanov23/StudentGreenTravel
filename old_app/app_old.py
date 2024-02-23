import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QGridLayout, QComboBox, QMessageBox, QHBoxLayout, QRadioButton
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont
#from main import main
from tkinter.filedialog import askopenfile
import pandas as pd
from preprocess_data import menu, determine_postcode
from final_leg import select_country

class WelcomePage(QWidget):

    file_selected = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.scotland = None
        self.wales = None
        self.north_ireland = None
        self.england = None

        self.title_label = QLabel("Welcome to StudentGreenTravel", self)
        self.title_label.setStyleSheet("font-size: 34px; font-weight: bold; color: #2d3436;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Buttons for menu
        button1 = QPushButton("Emission Calculator", clicked=lambda: self.show_page(Page1(self)))
        button1.setEnabled(False)
        button2 = QPushButton("Display Routes", clicked=lambda: self.show_page(Page2()))
        button2.setEnabled(False)
        button3 = QPushButton("Statistics", clicked=lambda: self.show_page(Page2()))
        button3.setEnabled(False)
        button4 = QPushButton("Select a file", clicked=lambda: self.file_explorer())
    

        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(button1)
        self.button_layout.addWidget(button2)
        self.button_layout.addWidget(button3)
        self.button_layout.addWidget(button4)

        # Make the buttons fixed size
        for i in range(self.button_layout.count()):
            self.button_layout.itemAt(i).widget().setFixedHeight(60)
            self. button_layout.itemAt(i).widget().setFixedWidth(300)

        # Center the buttons
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a label showing the file name
        self.file_label = QLabel("", self)
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.file_label)
        self.setLayout(self.main_layout)


        self.file_selected.connect(self.enable_buttons)

    def show_page(self, page):
        self.parent().setCentralWidget(page)

    def file_explorer(self):
        file = askopenfile(filetypes=[("Excel files", "*.xlsx")])
        # If the user selected a file, then read it using pandas
        if file:
        # Read address file
            addresses = pd.read_excel(file.name, engine='openpyxl')
            addresses.iloc[:, 1] = addresses.iloc[:, 1].str.replace(' ', '')
            # Add the file name to the label text with the file name withouth the path
            self.file_label.setText(f"File: {file.name.split('/')[-1]}")
            # Style the label
            self.file_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #2d3436;")
            self.file_selected.emit(True)
            self.scotland, self.wales, self.north_ireland, self.england = determine_postcode(addresses.iloc[:, 1])
        # If the user didn't select a file, then return an empty dataframe
        else:
            self.file_selected.emit(False)
        
    def get_country_data(self):
        return self.scotland, self.wales, self.north_ireland, self.england

        
    def enable_buttons(self, file_selected):
        if file_selected:
            for i in range(self.button_layout.count()):
                self.button_layout.itemAt(i).widget().setEnabled(True)
        else:
            for i in range(self.button_layout.count()):
                self.button_layout.itemAt(i).widget().setDisabled(True)


            

# class Page1 that inherits from MainWidget
class Page1(QWidget):

    hundred_percent = pyqtSignal(bool)

    def __init__(self, WelcomePage):
        super().__init__()
        self.travel_scotland = None
        self.travel_england = None
        self.travel_wales = None
        self.travel_north_ireland = None


        self.setWindowTitle("Emissions Calculator")
        self.main_window = WelcomePage

        layout = QVBoxLayout()
        grid = QGridLayout()
        # Stretch the rows
        grid.setRowStretch(0, 1)

        main_label = QLabel("Select percentages of students travelling by each transport method", self)
        main_label.setStyleSheet("background-color: #2d3436; color: #ffffff;")
        layout.addWidget(main_label)
        # Add stretch to the first row
        grid.setRowStretch(0, 1)
            
        
        # Scotland
        scotland_label = QLabel("Scotland", self)
        grid.addWidget(scotland_label, 0, 0)

        bus_scot_label = QLabel("Bus %", self)
        grid.addWidget(bus_scot_label, 1, 0)
        self.bus_scot = QComboBox(self)
        for i in range(101):
            self.bus_scot.addItem(str(i))
        grid.addWidget(self.bus_scot, 1, 1)

        car_scot_label = QLabel("Car %", self)
        grid.addWidget(car_scot_label, 2, 0)
        self.car_scot = QComboBox(self)
        for i in range(101):
            self.car_scot.addItem(str(i))
        grid.addWidget(self.car_scot, 2, 1)

        rail_scot_label = QLabel("Train %", self)
        grid.addWidget(rail_scot_label, 3, 0)
        self.rail_scot = QComboBox(self)
        for i in range(101):
            self.rail_scot.addItem(str(i))
        grid.addWidget(self.rail_scot, 3, 1)

        # UK
        uk_label = QLabel("Rest of UK", self)
        grid.addWidget(uk_label, 0, 2)

        plane_uk_label = QLabel("Plane %", self)
        grid.addWidget(plane_uk_label, 1, 2)
        self.plane_uk = QComboBox(self)
        for i in range(101):
            self.plane_uk.addItem(str(i))
        grid.addWidget(self.plane_uk, 1, 3)

        car_uk_label = QLabel("Car %", self)
        grid.addWidget(car_uk_label, 2, 2)
        self.car_uk = QComboBox(self)
        for i in range(101):
            self.car_uk.addItem(str(i))
        grid.addWidget(self.car_uk, 2, 3)

        rail_uk_label = QLabel("Train %", self)
        grid.addWidget(rail_uk_label, 3, 2)
        self.rail_uk = QComboBox(self)
        for i in range(101):
            self.rail_uk.addItem(str(i))
        grid.addWidget(self.rail_uk, 3, 3)


        # Add the grid to the layout
        layout.addLayout(grid)

        
        layout.addStretch(1)

        
        self.button_layout = QHBoxLayout()
        # add back button
        self.back_button = QPushButton("Back to Menu", clicked=self.back_to_menu)
        self.next_button = QPushButton("Next", clicked=lambda: self.show_page(Page2(self)))
        self.next_button.setEnabled(False)
        self.submit_button = QPushButton("Submit", clicked=self.check_combo)
        self.button_layout.addWidget(self.back_button)
        self.button_layout.addWidget(self.submit_button)
        self.button_layout.addWidget(self.next_button)
        layout.addLayout(self.button_layout)

        self.setLayout(layout)
    

        # Connect the signals
        self.hundred_percent.connect(self.enable)

    def show_page(self, page):
        """Function to show the next page in the main window"""
        self.parent().setCentralWidget(page)

    def back_to_menu(self):
        # Go back to menu but keep the selected file
        self.parent().setCentralWidget(WelcomePage())

    def show_country_data(self):
        """Return the data for each country from the file explorer function"""
        print(self.main_window.scotland, self.main_window.wales, self.main_window.north_ireland, self.main_window.england)

    def check_combo(self):
        """Check if the sum of the percentages for each country is 100. If it is, then call the menu function. If not, show a message box with an error.""" 
        scot = sum([int(self.bus_scot.currentText()), int(self.car_scot.currentText()), int(self.rail_scot.currentText())])
        uk = sum([int(self.plane_uk.currentText()), int(self.car_uk.currentText()), int(self.rail_uk.currentText())])

        if scot == 100 and uk == 100:
            # Show a message that the data has been submitted
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("The data has been submitted!")
            # Add a success icon to the message box
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
            # take the returns from the file explorer function without running it again
            scotland, wales, north_ireland, england = self.main_window.get_country_data()
            self.hundred_percent.emit(True)
            # call the menu function
            self.travel_scotland, self.travel_england, self.travel_wales, self.travel_north_ireland = menu(scotland, wales, north_ireland, england, int(self.bus_scot.currentText()), int(self.car_scot.currentText()), int(self.rail_scot.currentText()), int(self.plane_uk.currentText()), int(self.car_uk.currentText()), int(self.rail_uk.currentText()))
            
        else:
            self.hundred_percent.emit(False)
            # Show a message box with the error
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("The sum of the percentages for each country must be 100!\nPlease try again.")
            # Add a warning icon to the message box
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()

    def enable(self, hundred_percent):
        """Enable the next page button if the sum of the percentages for each country is 100"""	
        if hundred_percent:
            # Enable the next button
            self.next_button.setEnabled(True)


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


            self.grid.addWidget(scot_label, 0, 0, 1, 4)
            self.grid.addWidget(land_label, 1, 0)
            self.grid.addWidget(air_label, 1, 2)
            self.grid.addWidget(scot_car, 2, 0)
            self.grid.addWidget(scot_taxi, 3, 0)
            self.grid.addWidget(scot_bus, 4, 0)
            self.grid.addWidget(scot_walk, 5, 0)
            self.grid.addWidget(self.scot_car_box, 2, 1)
            self.grid.addWidget(self.scot_taxi_box, 3, 1)
            self.grid.addWidget(self.scot_bus_box, 4, 1)
            self.grid.addWidget(self.scot_walk_box, 5, 1)

            self.grid.addWidget(uk_car, 2, 2)
            self.grid.addWidget(uk_taxi, 3, 2)
            self.grid.addWidget(uk_bus, 4, 2)
            self.grid.addWidget(uk_walk, 5, 2)

            self.grid.addWidget(self.uk_car_box, 2, 3)
            self.grid.addWidget(self.uk_taxi_box, 3, 3)
            self.grid.addWidget(self.uk_bus_box, 4, 3)
            self.grid.addWidget(self.uk_walk_box, 5, 3)


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




class Page3(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("This is Page 3", self)
        self.back_button = QPushButton("Back to Menu", clicked=self.back_to_menu)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.back_button)

    def back_to_menu(self):
        self.parent().setCentralWidget(WelcomePage())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StudentGreenTravel: Domestic Relocation Emissions Estimator")
        self.setMinimumSize(QSize(800, 600))
        # Max size is size of screen, so no need to set

        self.central_widget = WelcomePage()
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
