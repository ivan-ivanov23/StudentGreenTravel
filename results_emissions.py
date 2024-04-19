# Second page with results which shows emissions by council area of countries
# Sources of code snippets are provided in the comments of functions.
# Author: Ivan Ivanov

from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox, QRadioButton, QPushButton, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView


class ResultEmissions(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()   

    def initializeUI(self):
        # Main layout of the page
        vbox = QVBoxLayout()

        # Layout to hold the webview and radio buttons
        hbox = QHBoxLayout()

        # Show a web view
        # Source: https://zetcode.com/pyqt/qwebengineview/
        self.webview = QWebEngineView()
        self.webview.setHtml("<b>Tip:</b> Select from the options on the right to view the data.")
        hbox.addWidget(self.webview)

        # layout the hold the group boxes
        vbox1 = QVBoxLayout()

        # create a group box to hold radio buttons
        group_box = QGroupBox("Total Council Emissions")
        group_box.setFixedWidth(200)
        radio_layout = QVBoxLayout()
        self.radio1 = QRadioButton("Scotland Council Emissions")
        self.radio2 = QRadioButton("England Council Emissions")
        self.radio3 = QRadioButton("Wales Council Emissions")
        self.radio4 = QRadioButton("N.Ireland Council Emissions")

        radio_layout.addWidget(self.radio1)
        radio_layout.addWidget(self.radio2)
        radio_layout.addWidget(self.radio3)
        radio_layout.addWidget(self.radio4)


        # Scotland specific data
        group_box2 = QGroupBox("Scotland Data")
        group_box2.setFixedWidth(200)
        radio_layout2 = QVBoxLayout()
        self.radio5 = QRadioButton("Car Emissions (Council)")
        self.radio6 = QRadioButton("Bus Emissions (Council)")
        self.radio7 = QRadioButton("Train Emissions (Council)")
        self.radio8 = QRadioButton("Taxi Emissions (Council)")

        radio_layout2.addWidget(self.radio5)
        radio_layout2.addWidget(self.radio6)
        radio_layout2.addWidget(self.radio7)
        radio_layout2.addWidget(self.radio8)


        # England specific data
        group_box3 = QGroupBox("England Data")
        group_box3.setFixedWidth(200)
        radio_layout3 = QVBoxLayout()
        self.radio9 = QRadioButton("Car Emissions (Council)")
        self.radio10 = QRadioButton("Bus Emissions (Council)")
        self.radio11 = QRadioButton("Train Emissions (Council)")
        self.radio12 = QRadioButton("Taxi Emissions (Council)")

        radio_layout3.addWidget(self.radio9)
        radio_layout3.addWidget(self.radio10)
        radio_layout3.addWidget(self.radio11)
        radio_layout3.addWidget(self.radio12)


        # Wales specific data
        group_box4 = QGroupBox("Wales Data")
        group_box4.setFixedWidth(200)
        radio_layout4 = QVBoxLayout()
        self.radio13 = QRadioButton("Car Emissions (Council)")
        self.radio14 = QRadioButton("Bus Emissions (Council)")
        self.radio15 = QRadioButton("Train Emissions (Council)")
        self.radio16 = QRadioButton("Taxi Emissions (Council)")

        radio_layout4.addWidget(self.radio13)
        radio_layout4.addWidget(self.radio14)
        radio_layout4.addWidget(self.radio15)
        radio_layout4.addWidget(self.radio16)


        # Northern Ireland specific data
        group_box5 = QGroupBox("Northern Ireland Data")
        group_box5.setFixedWidth(200)
        radio_layout5 = QVBoxLayout()
        self.radio17 = QRadioButton("Car Emissions (Council)")
        self.radio18 = QRadioButton("Bus Emissions (Council)")
        self.radio19 = QRadioButton("Train Emissions (Council)")
        self.radio20 = QRadioButton("Taxi Emissions (Council)")

        radio_layout5.addWidget(self.radio17)
        radio_layout5.addWidget(self.radio18)
        radio_layout5.addWidget(self.radio19)
        radio_layout5.addWidget(self.radio20)


        # Add radio buttons to group box
        group_box.setLayout(radio_layout)
        group_box2.setLayout(radio_layout2)
        group_box3.setLayout(radio_layout3)
        group_box4.setLayout(radio_layout4)
        group_box5.setLayout(radio_layout5)
        vbox1.addWidget(group_box)
        vbox1.addWidget(group_box2)
        vbox1.addWidget(group_box3)
        vbox1.addWidget(group_box4)
        vbox1.addWidget(group_box5)
        hbox.addLayout(vbox1)


        # Button layout
        button_layout = QHBoxLayout()
        self.button1 = QPushButton("Back")
        self.button2 = QPushButton("Menu")
        self.button3 = QPushButton("Show Council Distances")
        self.button4 = QPushButton("Show Invalid Data")
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)
        button_layout.addWidget(self.button4)
        button_layout.addWidget(self.button3)
        
        # Add hbox layout to main layout
        vbox.addLayout(hbox)
        # Add button layout to main layout
        vbox.addLayout(button_layout)
        self.setLayout(vbox)
        