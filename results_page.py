# This is the final page which contains the webview for the ploty heatmaps and 
# the other widgets

from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox, QRadioButton, QPushButton, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
import sys


class ResultPage(QWidget):

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
        # Show an empty page
        self.webview.setHtml("To see a heatmap, select a filter on the right.")
        hbox.addWidget(self.webview)

        # create a group box to hold radio buttons
        group_box = QGroupBox("Filter")
        radio_layout = QVBoxLayout()
        self.radio1 = QRadioButton("Distance by Country")
        self.radio2 = QRadioButton("Emissions by Country")
        self.radio3 = QRadioButton("Total Emissions by Country")
        self.radio4 = QRadioButton("Emissions per Student")
        radio_layout.addWidget(self.radio1)
        radio_layout.addWidget(self.radio2)
        radio_layout.addWidget(self.radio3)
        radio_layout.addWidget(self.radio4)

        # Add stretch to push the radio buttons to the top
        radio_layout.addStretch(1)

        # Add radio buttons to group box
        group_box.setLayout(radio_layout)
        hbox.addWidget(group_box)



        # Button layout
        button_layout = QHBoxLayout()
        self.button1 = QPushButton("Back")
        button_layout.addWidget(self.button1)
        
        # Add hbox layout to main layout
        vbox.addLayout(hbox)
        # Add button layout to main layout
        vbox.addLayout(button_layout)
        self.setLayout(vbox)

#         # Connect the radio buttons to the function
#         self.radio1.clicked.connect(self.click_radio1)
#         self.radio2.clicked.connect(self.click_radio2)

#     def click_radio1(self):
#         self.webview.setHtml("Distance by Country")

#     def click_radio2(self):
#         self.webview.setHtml("Emissions by Country")

# app = QApplication(sys.argv)
# window = ResultPage()
# sys.exit(app.exec())
