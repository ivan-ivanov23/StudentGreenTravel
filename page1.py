from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class MainPage(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Create and arrange widgets in the MainWindow"""
        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo = QIcon("icons/eco.svg")
        logo_label = QLabel()
        logo_label.setPixmap(logo.pixmap(100, 100))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title label
        title = QLabel("StudentGreenTravel")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2d3436;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Buttons
        self.button1 = QPushButton("Calculate Emissions")
        self.button1.setFixedSize(300, 50)
        self.button1.setEnabled(False)
        self.button2 = QPushButton("Select a File")
        self.button2.setFixedSize(300, 50)

        # File label
        self.file_label = QLabel(" ")
        self.file_label.setStyleSheet("color: #2d3436; font-size: 14px")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Small label to show the author and year
        author_label = QLabel("© 2024 by I.Ivanov")
        # align it at the right edge of the window
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        author_label.setStyleSheet("color: #2d3436; font-size: 12px")
        
        # Add widgets to layout
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(logo_label)
        self.main_layout.addWidget(title)
        self.main_layout.addWidget(self.button1)
        self.main_layout.addWidget(self.button2)
        self.main_layout.addWidget(self.file_label)
        # add stretch to push the author label to the bottom but it should not affect the other widgets
        self.main_layout.addStretch(1)

        self.main_layout.addWidget(author_label)

        self.setLayout(self.main_layout)

    def enable_buttons1(self, file_selected):
        """Enable the next button if a file has been selected """
        if file_selected:
            self.button1.setEnabled(True)
        else:
            self.button1.setEnabled(False)