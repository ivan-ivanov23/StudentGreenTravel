from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox, QRadioButton, QPushButton, QWidget, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView


class ResultPage2(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Results")
        self.setGeometry(100, 100, 800, 600)
        self.initializeUI()
        self.show()        

    def initializeUI(self):
        # Main layout of the page
        vbox = QVBoxLayout(self)

        # Layout to hold the webview and radio buttons
        hbox = QHBoxLayout()

        # Show a web view
        # Source: https://zetcode.com/pyqt/qwebengineview/
        self.webview = QWebEngineView()
        hbox.addWidget(self.webview)

        # layout the hold the group boxes
        vbox1 = QVBoxLayout()

        # create a group box to hold radio buttons
        group_box = QGroupBox("Basic Data")
        group_box.setFixedWidth(200)
        radio_layout = QVBoxLayout()
        self.radio1 = QRadioButton("Emissions by Country")
        self.radio2 = QRadioButton("Distance by Country")
        self.radio3 = QRadioButton("Total Emissions by Country")
        self.radio4 = QRadioButton("Emissions per Student")

        radio_layout.addWidget(self.radio1)
        radio_layout.addWidget(self.radio2)
        radio_layout.addWidget(self.radio3)
        radio_layout.addWidget(self.radio4)


        # Scotland specific data
        group_box2 = QGroupBox("Scotland Data")
        group_box2.setFixedWidth(200)
        radio_layout2 = QVBoxLayout()
        self.radio5 = QRadioButton("Car Emissions (Coucil)")
        self.radio6 = QRadioButton("Bus Emissions (Coucil)")
        self.radio7 = QRadioButton("Train Emissions (Coucil)")
        self.radio8 = QRadioButton("Taxi Emissions (Coucil)")

        radio_layout2.addWidget(self.radio5)
        radio_layout2.addWidget(self.radio6)
        radio_layout2.addWidget(self.radio7)
        radio_layout2.addWidget(self.radio8)


        # England specific data
        group_box3 = QGroupBox("England Data")
        group_box3.setFixedWidth(200)
        radio_layout3 = QVBoxLayout()
        self.radio9 = QRadioButton("Car Emissions (Coucil)")
        self.radio10 = QRadioButton("Bus Emissions (Coucil)")
        self.radio11 = QRadioButton("Train Emissions (Coucil)")
        self.radio12 = QRadioButton("Taxi Emissions (Coucil)")

        radio_layout3.addWidget(self.radio9)
        radio_layout3.addWidget(self.radio10)
        radio_layout3.addWidget(self.radio11)
        radio_layout3.addWidget(self.radio12)


        # Wales specific data
        group_box4 = QGroupBox("Wales Data")
        group_box4.setFixedWidth(200)
        radio_layout4 = QVBoxLayout()
        self.radio13 = QRadioButton("Car Emissions (Coucil)")
        self.radio14 = QRadioButton("Bus Emissions (Coucil)")
        self.radio15 = QRadioButton("Train Emissions (Coucil)")
        self.radio16 = QRadioButton("Taxi Emissions (Coucil)")

        radio_layout4.addWidget(self.radio13)
        radio_layout4.addWidget(self.radio14)
        radio_layout4.addWidget(self.radio15)
        radio_layout4.addWidget(self.radio16)


        # Northern Ireland specific data
        group_box5 = QGroupBox("Northern Ireland Data")
        group_box5.setFixedWidth(200)
        radio_layout5 = QVBoxLayout()
        self.radio17 = QRadioButton("Car Emissions (Coucil)")
        self.radio18 = QRadioButton("Bus Emissions (Coucil)")
        self.radio19 = QRadioButton("Train Emissions (Coucil)")
        self.radio20 = QRadioButton("Taxi Emissions (Coucil)")

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
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)
        button_layout.addWidget(self.button3)
        
        # Add hbox layout to main layout
        vbox.addLayout(hbox)
        # Add button layout to main layout
        vbox.addLayout(button_layout)
        self.setLayout(vbox)
        