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
        self.invalid_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white; background-color: #2C2C2C; padding: 10px; border-radius: 5px; margin-bottom: 10px;")
        layout.addWidget(self.invalid_label)

        # Create list widget to hold invalid postcodes
        self.invalid_list = QListWidget()
        self.invalid_list.setStyleSheet("font-size: 14px; color: #2d3436; margin-bottom: 10px; border-radius: 5px; background-color: #dfe6e9; padding: 5px;")

        instruction = QLabel("""
            <b>Tip:</b> Click the '<b>Show Invalid Postcodes</b>' button to display the invalid postcodes.
            <br>
            The list below will display the row number in the used dataset and its contents.
            <br>
            Click the '<b>Clear</b>' button to clear the list of invalid postcodes.
        """)
        instruction.setStyleSheet("font-size: 14px; color: #2d3436; margin-bottom: 10px; border-radius: 5px; background-color: #D7D7D7; padding: 5px;")

        # Layout for buttons
        self.button_layout = QHBoxLayout()
        self.button1 = QPushButton("Back")
        self.button2 = QPushButton("Show Invalid Postcodes")
        self.button3 = QPushButton("Clear")
        self.button_layout.addWidget(self.button1)
        self.button_layout.addWidget(self.button2)
        self.button_layout.addWidget(self.button3)

        # Add button layout to main layout
        layout.addWidget(self.invalid_label)
        layout.addWidget(instruction)
        layout.addWidget(self.invalid_list)
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
