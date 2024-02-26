from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import Qt


class MainPage(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Create and arrange widgets in the MainWindow"""
        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title label
        title = QLabel("Welcome to StudentGreenTravel!")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2d3436;")
        
        # Buttons
        self.button1 = QPushButton("Calculate Emissions")
        self.button1.setEnabled(False)
        self.button2 = QPushButton("Select a File")

        # File label
        self.file_label = QLabel(" ")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add widgets to layout
        self.main_layout.addWidget(title)
        self.main_layout.addWidget(self.button1)
        self.main_layout.addWidget(self.button2)
        self.main_layout.addWidget(self.file_label)

        self.setLayout(self.main_layout)