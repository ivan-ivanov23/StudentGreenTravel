import sys
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QStackedLayout, QMessageBox
from PyQt6.QtCore import pyqtSignal
from tkinter.filedialog import askopenfile
import pandas as pd
from preprocess_data import menu, determine_postcode
from page1 import MainPage
from page2 import Page2
from page3 import Page3

# Source: https://www.tutorialspoint.com/pyqt/pyqt_qstackedwidget.htm 

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
        self.file_selected.connect(self.enable_buttons)

        # Connect signals for page2
        self.page2.next_button2.clicked.connect(self.go_to_page3)
        self.page2.submit.clicked.connect(self.check_combo_page2)
        self.page2.back.clicked.connect(self.go_to_page1)
        self.hundred_percent.connect(self.enable_page2)

        # Connect signals for page3
        self.page3.back.clicked.connect(self.go_to_page2)
        self.page3.result_button.clicked.connect(self.go_to_results)

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


    def enable_buttons(self, file_selected):
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

    def go_to_results(self):
        self.stackedLayout.setCurrentIndex(3)


    def check_combo_page2(self):
        """Check if the sum of the percentages for each country is 100. If it is, then call the menu function. If not, show a message box with an error.""" 
        scot = sum([int(self.page2.combo_car_scot.currentText()), int(self.page2.combo_bus_scot.currentText()), int(self.page2.combo_rail_scot.currentText())])
        uk = sum([int(self.page2.plane_uk.currentText()), int(self.page2.car_uk.currentText()), int(self.page2.rail_uk.currentText())])

        if scot == 100 and uk == 100:
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

"""==============================================Run the app=============================================="""
app = QApplication(sys.argv)
window = Calculator()
sys.exit(app.exec())
