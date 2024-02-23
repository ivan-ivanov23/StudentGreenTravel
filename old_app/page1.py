from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QComboBox, QHBoxLayout, QMessageBox
from PyQt6.QtCore import pyqtSignal
from preprocess_data import menu
from old_app.welcomepage import WelcomePage
from old_app.page2 import Page2


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
        self.next_button = QPushButton("Next", clicked=lambda: self.show_page(Page2()))
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