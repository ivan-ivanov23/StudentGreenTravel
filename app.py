import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QGridLayout, QComboBox, QMessageBox, QStyle
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from main import main
from tkinter.filedialog import askopenfile
import pandas as pd
from preprocess_data import menu, determine_postcode


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
        #button1.setEnabled(False)
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
        self.setWindowTitle("Emissions Calculator")
        self.main_window = WelcomePage

        layout = QVBoxLayout()
        grid = QGridLayout()
        # Stretch the rows
        grid.setRowStretch(0, 1)

        main_label = QLabel("Select percentages of students travelling by each transport method", self)
        layout.addWidget(main_label)
        # Add stretch to the first row
        grid.setRowStretch(0, 1)

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

        layout.addLayout(grid)
        # add back button
        back_button = QPushButton("Back to Menu", clicked=self.back_to_menu)
        submit_button = QPushButton("Submit travel methods", clicked=self.check_combo)
        layout.addWidget(submit_button)
        layout.addWidget(back_button)
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
                font-weight: bold;
                border: none;
            }
            QComboBox {
                background-color: #74b9ff;
                color: #ffffff;
                font-weight: bold;
                height: 40px;
                border: none;
                border-radius: 5px;
                margin: 5px 0;
            }                                       
        """)



    def back_to_menu(self):
        # Go back to menu but keep the selected file
        self.parent().setCentralWidget(WelcomePage())

    def show_country_data(self):
        print(self.main_window.scotland, self.main_window.wales, self.main_window.north_ireland, self.main_window.england)

    def check_combo(self):
        scot = sum([int(self.bus_scot.currentText()), int(self.car_scot.currentText()), int(self.rail_scot.currentText())])
        uk = sum([int(self.plane_uk.currentText()), int(self.car_uk.currentText()), int(self.rail_uk.currentText())])

        if scot == 100 and uk == 100:
            self.hundred_percent.emit(True)
            # Show a message that the data has been submitted
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("The data has been submitted!")
            # Add a success icon to the message box
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
            # take the returns from the file explorer function without running it again
            scotland, wales, north_ireland, england = self.main_window.get_country_data()
            # call the menu function
            travel_scotland, travel_england, travel_wales, travel_north_ireland = menu(scotland, wales, north_ireland, england, int(self.bus_scot.currentText()), int(self.car_scot.currentText()), int(self.rail_scot.currentText()), int(self.plane_uk.currentText()), int(self.car_uk.currentText()), int(self.rail_uk.currentText()))
            # call the main function
            main(travel_scotland, travel_england, travel_wales, travel_north_ireland)
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
        if hundred_percent:
            self.submit_button.setEnabled(True)
        else:
            self.submit_button.setEnabled(False)


class Page2(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("This is Page 2", self)
        self.back_button = QPushButton("Back to Menu", clicked=self.back_to_menu)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.back_button)

    def back_to_menu(self):
        self.parent().setCentralWidget(WelcomePage())


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
