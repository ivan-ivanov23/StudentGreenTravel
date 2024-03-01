from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWebEngineWidgets import *


class ResultPage(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        hbox = QVBoxLayout(self)

        # Show a web view
        # Source: https://zetcode.com/pyqt/qwebengineview/
        self.webview = QWebEngineView()
        # Show an empty page
        self.webview.setHtml("")
        hbox.addWidget(self.webview)


        # Button layout
        button_layout = QHBoxLayout()
        self.button1 = QPushButton("Back")
        button_layout.addWidget(self.button1)
        self.button2 = QPushButton("Show Results")
        button_layout.addWidget(self.button2)

        # Add button layout to main layout
        hbox.addLayout(button_layout)
        self.setLayout(hbox)

