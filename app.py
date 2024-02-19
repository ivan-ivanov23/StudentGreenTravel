import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QGridLayout, QComboBox, QMessageBox, QHBoxLayout, QRadioButton
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from main import main
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
        button3 = QPushButton("Statistics", clicked=lambda: self.show_page(Page3()))
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




        # Set the stylesheet for the welcome page buttons
        self.setStyleSheet("""
            QPushButton {
                background-color: #0984e3;
                color: #ffffff;
                font-weight: bold;
                height: 40px;
                border: none;
                border-radius: 5px;
                margin: 5px 0;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #74b9ff;
            }
            QPushButton:disabled {
                background-color: #b2bec3;
            }
        """)
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
        
        
        self.setStyleSheet("""
            QWidget {
                border: 2px solid #2d3436;
                border-radius: 5px;
                padding: 2px;
                background-color: #dfe6e9;
            }
            QPushButton {
                background-color: #0984e3;
                color: #ffffff;
                font-weight: bold;
                height: 40px;
                border: none;
                border-radius: 5px;
                margin: 5px 0;
            }
            QPushButton:hover {
                background-color: #74b9ff;
            }
            QPushButton:disabled {
                background-color: #b2bec3;
            }
            QLabel {
                font-size: 16px;
                border: none;
                height: 20px;
            }
            QLabel:disabled {
                background-color: #b2bec3;
            }
            QComboBox {
                background-color: #74b9ff;
                color: #ffffff;
                height: 20px;
                border: none;
                margin: 5px 0;
                padding: 5px;
            }
            QComboBox:disabled {
                background-color: #b2bec3;
            }
            QScrollBar:vertical {
                border: 2px solid #2d3436;
                background: #dfe6e9;
                width: 15px;
                margin: 22px 0;
            }
            QScrollBar::handle:vertical {
                background: #2d3436;
                min-height: 30px;
            }
            QScrollBar::add-line:vertical {
                height: 20px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                height: 20px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }                        
        """)

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
    all_selected = pyqtSignal(bool)

    def __init__(self, Page1):
        super().__init__()
        # Have a reference to the previous page for the back button
        self.page1 = Page1
        self.back_button = QPushButton("Previous", clicked=self.back_to_previous)
        self.submit_button = QPushButton("Submit", clicked=self.check_combo)
        self.show_results_button = QPushButton("Results")
        self.show_results_button.setEnabled(False)


        # Button layout
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.back_button)
        self.button_layout.addWidget(self.submit_button)
        self.button_layout.addWidget(self.show_results_button)

        # Main layout
        layout = QVBoxLayout()

        # Label for the second page
        second_label = QLabel("Select the travel assumptions for the final leg of the journey.\nFrom Aberdeen transport hub to the University of Aberdeen", self)
        second_label.setStyleSheet("background-color: #2d3436; color: #ffffff;")
        layout.addWidget(second_label)

        # A new grid for the second label
        grid2 = QGridLayout()
        # Stretch the rows
        grid2.setRowStretch(0, 1)

        # Scotland combo boxes
        scotland_label2 = QRadioButton("Scotland", self)
        grid2.addWidget(scotland_label2, 0, 0)

        car_scot_label2 = QLabel("Car %", self)
        grid2.addWidget(car_scot_label2, 1, 0)
        self.car_scot2 = QComboBox(self)
        for i in range(101):
            self.car_scot2.addItem(str(i))
        grid2.addWidget(self.car_scot2, 1, 1)

        taxi_scot_label2 = QLabel("Taxi %", self)
        grid2.addWidget(taxi_scot_label2, 2, 0)
        self.taxi_scot2 = QComboBox(self)
        for i in range(101):
            self.taxi_scot2.addItem(str(i))
        grid2.addWidget(self.taxi_scot2, 2, 1)

        bus_scot_label2 = QLabel("Bus %", self)
        grid2.addWidget(bus_scot_label2, 3, 0)
        self.bus_scot2 = QComboBox(self)
        for i in range(101):
            self.bus_scot2.addItem(str(i))
        grid2.addWidget(self.bus_scot2, 3, 1)

        walk_scot_label2 = QLabel("Walk %", self)
        grid2.addWidget(walk_scot_label2, 4, 0)
        self.walk_scot2 = QComboBox(self)
        for i in range(101):
            self.walk_scot2.addItem(str(i))
        grid2.addWidget(self.walk_scot2, 4, 1)

        # England combo boxes
        eng_label2 = QRadioButton("England", self)
        grid2.addWidget(eng_label2, 0, 2)
        
        car_eng_label2 = QLabel("Car %", self)
        grid2.addWidget(car_eng_label2, 1, 2)
        self.car_eng2 = QComboBox(self)
        for i in range(101):
            self.car_eng2.addItem(str(i))
        grid2.addWidget(self.car_eng2, 1, 3)
        
        taxi_eng_label2 = QLabel("Taxi %", self)
        grid2.addWidget(taxi_eng_label2, 2, 2)
        self.taxi_eng2 = QComboBox(self)
        for i in range(101):
            self.taxi_eng2.addItem(str(i))
        grid2.addWidget(self.taxi_eng2, 2, 3)

        bus_eng_label2 = QLabel("Bus %", self)
        grid2.addWidget(bus_eng_label2, 3, 2)
        self.bus_eng2 = QComboBox(self)
        for i in range(101):
            self.bus_eng2.addItem(str(i))
        grid2.addWidget(self.bus_eng2, 3, 3)

        walk_eng_label2 = QLabel("Walk %", self)
        grid2.addWidget(walk_eng_label2, 4, 2)
        self.walk_eng2 = QComboBox(self)
        for i in range(101):
            self.walk_eng2.addItem(str(i))
        grid2.addWidget(self.walk_eng2, 4, 3)
 
        # Wales combo boxes
        wales_label2 = QRadioButton("Wales", self)
        grid2.addWidget(wales_label2, 0, 4)

        car_wales_label2 = QLabel("Car %", self)
        grid2.addWidget(car_wales_label2, 1, 4)
        self.car_wales2 = QComboBox(self)
        for i in range(101):
            self.car_wales2.addItem(str(i))
        grid2.addWidget(self.car_wales2, 1, 5)

        taxi_wales_label2 = QLabel("Taxi %", self)
        grid2.addWidget(taxi_wales_label2, 2, 4)
        self.taxi_wales2 = QComboBox(self)
        for i in range(101):
            self.taxi_wales2.addItem(str(i))
        grid2.addWidget(self.taxi_wales2, 2, 5)

        bus_wales_label2 = QLabel("Bus %", self)
        grid2.addWidget(bus_wales_label2, 3, 4)
        self.bus_wales2 = QComboBox(self)
        for i in range(101):
            self.bus_wales2.addItem(str(i))
        grid2.addWidget(self.bus_wales2, 3, 5)

        walk_wales_label2 = QLabel("Walk %", self)
        grid2.addWidget(walk_wales_label2, 4, 4)
        self.walk_wales2 = QComboBox(self)
        for i in range(101):
            self.walk_wales2.addItem(str(i))
        grid2.addWidget(self.walk_wales2, 4, 5)

        # North Ireland combo boxes
        ni_label2 = QRadioButton("Northern Ireland", self)
        grid2.addWidget(ni_label2, 0, 6)

        car_ni_label2 = QLabel("Car %", self)
        grid2.addWidget(car_ni_label2, 1, 6)
        self.car_ni2 = QComboBox(self)
        for i in range(101):
            self.car_ni2.addItem(str(i))
        grid2.addWidget(self.car_ni2, 1, 7)
        
        taxi_ni_label2 = QLabel("Taxi %", self)
        grid2.addWidget(taxi_ni_label2, 2, 6)
        self.taxi_ni2 = QComboBox(self)
        for i in range(101):
            self.taxi_ni2.addItem(str(i))
        grid2.addWidget(self.taxi_ni2, 2, 7)

        bus_ni_label2 = QLabel("Bus %", self)
        grid2.addWidget(bus_ni_label2, 3, 6)
        self.bus_ni2 = QComboBox(self)
        for i in range(101):
            self.bus_ni2.addItem(str(i))
        grid2.addWidget(self.bus_ni2, 3, 7)

        walk_ni_label2 = QLabel("Walk %", self)
        grid2.addWidget(walk_ni_label2, 4, 6)
        self.walk_ni2 = QComboBox(self)
        for i in range(101):
            self.walk_ni2.addItem(str(i))
        grid2.addWidget(self.walk_ni2, 4, 7)


        # Add the grid to the layout
        layout.addLayout(grid2)
        layout.addStretch(1)
        layout.addLayout(self.button_layout)

        # Set the layout for the page
        self.setLayout(layout)
        # Style the page
        self.setStyleSheet("""
            QWidget {
                border: 2px solid #2d3436;
                border-radius: 5px;
                padding: 2px;
                background-color: #dfe6e9;
            }
            QPushButton {
                background-color: #0984e3;
                color: #ffffff;
                font-weight: bold;
                height: 40px;
                border: none;
                border-radius: 5px;
                margin: 5px 0;
            }
            QPushButton:hover {
                background-color: #74b9ff;
            }
            QPushButton:disabled {
                background-color: #b2bec3;
            }
            QLabel {
                font-size: 16px;
                border: none;
                height: 20px;
            }
            QLabel:disabled {
                background-color: #b2bec3;
            }
            QComboBox {
                background-color: #74b9ff;
                color: #ffffff;
                height: 20px;
                border: none;
                margin: 5px 0;
                padding: 5px;
            }
            QComboBox:disabled {
                background-color: #b2bec3;
            }
            QScrollBar:vertical {
                border: 2px solid #2d3436;
                background: #dfe6e9;
                width: 15px;
                margin: 22px 0;
            }
            QScrollBar::handle:vertical {
                background: #2d3436;
                min-height: 30px;
            }
            QScrollBar::add-line:vertical {
                height: 20px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                height: 20px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }                        
        """)

        # Connect the signals 
        self.all_selected.connect(self.enable)

    def back_to_previous(self):
        """Go back to the previous page"""
        self.parent().setCentralWidget(Page1(self))

    def check_combo(self):
        """Check if the sum of the percentages for each country is 100. If it is, then call the select_country function. If not, show a message box with an error."""
        scotland = sum([int(self.car_scot2.currentText()), int(self.taxi_scot2.currentText()), int(self.bus_scot2.currentText()), int(self.walk_scot2.currentText())])
        england = sum([int(self.car_eng2.currentText()), int(self.taxi_eng2.currentText()), int(self.bus_eng2.currentText()), int(self.walk_eng2.currentText())])
        wales = sum([int(self.car_wales2.currentText()), int(self.taxi_wales2.currentText()), int(self.bus_wales2.currentText()), int(self.walk_wales2.currentText())])
        ni = sum([int(self.car_ni2.currentText()), int(self.taxi_ni2.currentText()), int(self.bus_ni2.currentText()), int(self.walk_ni2.currentText())])

        bus_scotland = self.page1.travel_scotland[0]
        rail_scotland = self.page1.travel_scotland[1]
        scot_bus_rail = bus_scotland + rail_scotland

        rail_england = self.page1.travel_england[2]
        plane_england = self.page1.travel_england[0]
        

        rail_wales = self.page1.travel_wales[2]
        plane_wales = self.page1.travel_wales[0]

        rail_ni = self.page1.travel_north_ireland[2]
        plane_ni = self.page1.travel_north_ireland[0]

        if scotland == 100 and england == 100 and wales == 100 and ni == 100:
            # Show a message that the data has been submitted
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("The data has been submitted!")
            # Add a success icon to the message box
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
            self.all_selected.emit(True)
            # call the select_country function for each country
            # scot_fleg = select_country(scot_bus_rail, [], "Scotland", int(self.car_scot2.currentText()), int(self.taxi_scot2.currentText()), int(self.bus_scot2.currentText()), int(self.walk_scot2.currentText()))
            # eng_bus_rail, eng_plane = select_country(rail_england, plane_england, "England", int(self.car_eng2.currentText()), int(self.taxi_eng2.currentText()), int(self.bus_eng2.currentText()), int(self.walk_eng2.currentText()))
            # wales_bus_rail, wales_plane = select_country(rail_wales, plane_wales, "Wales", int(self.car_wales2.currentText()), int(self.taxi_wales2.currentText()), int(self.bus_wales2.currentText()), int(self.walk_wales2.currentText()))
            # ni_bus_rail, ni_plane = select_country(rail_ni, plane_ni, "Northern Ireland", int(self.car_ni2.currentText()), int(self.taxi_ni2.currentText()), int(self.bus_ni2.currentText()), int(self.walk_ni2.currentText()))
            # print(scot_fleg)

        else:
            self.all_selected.emit(False)
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
