from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout, QListWidget
from PyQt6.QtCore import Qt
import pandas as pd

class InvalidPage(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()
        

    def initializeUI(self):
        layout = QVBoxLayout()
        self.invalid_label = QLabel(f"Invalid Postcodes")
        self.invalid_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.invalid_label)
        self.setLayout(layout)

        # Create list widget to hold invalid postcodes
        self.invalid_list = QListWidget()
        layout.addWidget(self.invalid_list)

        # Layout for buttons
        self.button_layout = QHBoxLayout()
        self.button1 = QPushButton("Back")
        self.button2 = QPushButton("Show Invalid Postcodes")
        self.button3 = QPushButton("Clear")
        self.button_layout.addWidget(self.button1)
        self.button_layout.addWidget(self.button2)
        self.button_layout.addWidget(self.button3)

        # Add button layout to main layout
        layout.addLayout(self.button_layout)
        self.setLayout(layout)

    def find_invalid_values(self, dataframe, invalid_values):
        self.invalid_list.clear()
        # Combine the list of lists invalid_values into a single list
        invalid_postcodes = [item for sublist in invalid_values for item in sublist]

        if len(invalid_postcodes) == 0:
            self.invalid_list.addItem("No invalid postcodes found.")
        else:
            # Iterate over each row in the dataframe
            for index, row in dataframe.iterrows():
                # Check each value in the row for validity
                for value in row:
                    if value in invalid_postcodes:
                        self.invalid_list.addItem(f"{index + 2}: {row.tolist()}")
                        break
    
    def clear(self):
        self.invalid_list.clear()
