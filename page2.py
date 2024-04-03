# Code for the second page of the application (Mid leg assumptions page)
# # Sources of code snippets/pictures are provided in the comments of functions.
# Author: Ivan Ivanov

from PyQt6.QtWidgets import QVBoxLayout, QLabel, QComboBox, QGridLayout, QHBoxLayout, QPushButton, QWidget
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap
import os
from style_sheets import page_header_stylesheet, page_instruction_stylesheet, page2_label_stylesheet, page2_transport_stylesheet, page2_comobo_stylesheet

basedir = os.path.dirname(__file__)


class Page2(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()
        # Call the method to get the selected percentages from the combo boxes
        self.get_percentages()

    def initializeUI(self):
        """Create and arrange widgets in the SecondPage"""
        self.layout2 = QVBoxLayout()
        # Title label
        label = QLabel("Assumptions for Middle Leg of the Journey")
        label.setStyleSheet(page_header_stylesheet)
        self.layout2.addWidget(label)

        # Picture of the final leg of the journey
        mid_leg_pic = QLabel(self)
        pixmap = QPixmap(os.path.join(basedir, "pictures/mid.png"))
        mid_leg_pic.setPixmap(pixmap)
        mid_leg_pic.setAlignment(Qt.AlignmentFlag.AlignCenter)


        instruction1 = QLabel("""
            <b>Tip:</b> Select or enter the number of study-related trips a student makes on average per year.<br>
                        Please, select at least 2 trips (one at the start of the academic year and one at the end) and at most 10 trips.""")
        instruction1.setStyleSheet(page_instruction_stylesheet)
        self.layout2.addWidget(instruction1)


        # Number of trips combo box
        trips_label = QLabel("Number of trips")
        trips_label.setStyleSheet(page2_label_stylesheet)
        trips_label.setFixedWidth(270)
        self.trips_combo = QComboBox()
        self.trips_combo.setFixedSize(QSize(50, 20))
        for i in range(1, 11):
            val = str(i)
            self.trips_combo.addItem(val)
        self.layout2.addWidget(trips_label)
        self.layout2.addWidget(self.trips_combo)

        instruction2 = QLabel("""
            <b>Tip:</b> The initial leg of the journey (from home address to local transportation hub) is already pre-defined:
            <br>
            40% of students travel by car, 40% by taxi, and 20% by bus.
            <br><br>
            Select or enter the percentage of students traveling by each transport method 
            for the middle leg of their journey, from the transportation hub in their city to Aberdeen.
            <br><br>
            The percentages selected under the 'Scotland' section will be used for the Scottish students,
            <br>
            and the percentages selected under the 'Rest of UK' section will be used for the students from England, Wales, and Northern Ireland.
            <br>
            Once you have selected the percentages for the middle leg of the journey, click '<b>Submit</b>' to confirm your choices.
        """)
        instruction2.setStyleSheet(page_instruction_stylesheet)
        self.layout2.addWidget(instruction2)

        # Main grid to hold the scotland and uk grids
        main_grid = QGridLayout()
        main_grid.setHorizontalSpacing(100)
        main_grid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Scotland grid
        grid1 = QGridLayout()
        grid1.setHorizontalSpacing(25)
        grid1.setVerticalSpacing(6)
        grid1.setColumnStretch(1, 1)
        grid1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Rest of UK grid
        grid2 = QGridLayout()
        grid2.setHorizontalSpacing(25)
        grid2.setVerticalSpacing(6)
        grid2.setColumnStretch(1, 1)
        grid2.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # Scotland combo boxes and labels
        scotland_label = QLabel("Scotland")
        scotland_label.setStyleSheet(page2_label_stylesheet)
        grid1.addWidget(scotland_label, 0, 0, 1, 2)

        bus_scotland_label = QLabel("Bus %")
        bus_scotland_label.setStyleSheet(page2_transport_stylesheet)
        grid1.addWidget(bus_scotland_label, 1, 0)
        self.combo_bus_scot = QComboBox()
        self.combo_bus_scot.setStyleSheet(page2_comobo_stylesheet)
        for i in range(101):
            val = str(i)
            self.combo_bus_scot.addItem(val)
        grid1.addWidget(self.combo_bus_scot, 1, 1)

        car_scotland_label = QLabel("Car %", self)
        car_scotland_label.setStyleSheet(page2_transport_stylesheet)
        grid1.addWidget(car_scotland_label, 2, 0)
        self.combo_car_scot = QComboBox(self)
        self.combo_car_scot.setStyleSheet(page2_comobo_stylesheet)
        for i in range(101):
            val = str(i)
            self.combo_car_scot.addItem(val)
        grid1.addWidget(self.combo_car_scot, 2, 1)

        rail_scotland_label = QLabel("Train %", self)
        rail_scotland_label.setStyleSheet(page2_transport_stylesheet)
        grid1.addWidget(rail_scotland_label, 3, 0)
        self.combo_rail_scot = QComboBox(self)
        self.combo_rail_scot.setStyleSheet(page2_comobo_stylesheet)
        for i in range(101):
            val = str(i)
            self.combo_rail_scot.addItem(val)
        grid1.addWidget(self.combo_rail_scot, 3, 1)

        # label to show the percentages out of 100 that the user has selected
        self.scot_select = 0
        self.percent_label = QLabel(f"Selected: {self.scot_select}%")
        self.percent_label.setStyleSheet("font-size: 14px; color: #2d3436; font: bold")
        grid1.addWidget(self.percent_label, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)


        # UK
        uk_label = QLabel("Rest of UK", self)
        uk_label.setStyleSheet(page2_label_stylesheet)
        grid2.addWidget(uk_label, 0, 0, 1, 2)

        plane_uk_label = QLabel("Plane %", self)
        plane_uk_label.setStyleSheet(page2_transport_stylesheet)
        grid2.addWidget(plane_uk_label, 1, 0)
        self.plane_uk = QComboBox(self)
        self.plane_uk.setStyleSheet(page2_comobo_stylesheet)
        for i in range(101):
            self.plane_uk.addItem(str(i))
        grid2.addWidget(self.plane_uk, 1, 1)

        car_uk_label = QLabel("Car %", self)
        car_uk_label.setStyleSheet(page2_transport_stylesheet)
        grid2.addWidget(car_uk_label, 2, 0)
        self.car_uk = QComboBox(self)
        self.car_uk.setStyleSheet(page2_comobo_stylesheet)
        for i in range(101):
            self.car_uk.addItem(str(i))
        grid2.addWidget(self.car_uk, 2, 1)

        rail_uk_label = QLabel("Train %", self)
        rail_uk_label.setStyleSheet(page2_transport_stylesheet)
        grid2.addWidget(rail_uk_label, 3, 0)
        self.rail_uk = QComboBox(self)
        self.rail_uk.setStyleSheet(page2_comobo_stylesheet)
        for i in range(101):
            self.rail_uk.addItem(str(i))
        grid2.addWidget(self.rail_uk, 3, 1)

        # label to show the percentages out of 100 that the user has selected
        self.uk_select = 0
        self.uk_percent_label = QLabel(f"Selected: {self.uk_select}%")
        self.uk_percent_label.setStyleSheet("font-size: 14px; color: #2d3436; font: bold")
        grid2.addWidget(self.uk_percent_label, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        # Add the grids to the main grid
        main_grid.addLayout(grid1, 0, 0)
        main_grid.addLayout(grid2, 0, 2)


        # Button layout
        button_layout = QHBoxLayout()

        # Buttons
        self.back = QPushButton("Back")
        self.submit = QPushButton("Submit")
        self.next_button2 = QPushButton("Next")
        self.next_button2.setEnabled(False)

        # Add buttons to layout
        button_layout.addWidget(self.back)
        button_layout.addWidget(self.submit)
        button_layout.addWidget(self.next_button2)

        # Add the grid and button to the main layout of the page
        self.layout2.addLayout(main_grid)
        self.layout2.addStretch(1)
        self.layout2.addWidget(mid_leg_pic)
        self.layout2.addLayout(button_layout)

        self.setLayout(self.layout2)

    def enable_page2(self, hundred_percent):
        """Enable the next button if you get signal on page2"""
        if hundred_percent:
            self.next_button2.setEnabled(True)
        else:
            self.next_button2.setEnabled(False)

    def get_percentages(self):
        """Once a value from a combo box is selected, this method will update the scot_select or uk_select labels"""
        # Inspired by answer from Cholavendhan: https://stackoverflow.com/questions/6061893/how-do-you-get-the-current-text-contents-of-a-qcombobox
        self.combo_bus_scot.currentIndexChanged.connect(self.update_percent_label)
        self.combo_car_scot.currentIndexChanged.connect(self.update_percent_label)
        self.combo_rail_scot.currentIndexChanged.connect(self.update_percent_label)
        self.plane_uk.currentIndexChanged.connect(self.update_uk_percent_label)
        self.car_uk.currentIndexChanged.connect(self.update_uk_percent_label)
        self.rail_uk.currentIndexChanged.connect(self.update_uk_percent_label)

    def update_percent_label(self):
        """Update the label to show the percentages out of 100 that the user has selected"""
        # Inspired by find() method in: https://www.geeksforgeeks.org/pyqt5-getting-the-text-of-selected-item-in-combobox/
        scot_bus = int(self.combo_bus_scot.currentText())
        scot_car = int(self.combo_car_scot.currentText())
        scot_rail = int(self.combo_rail_scot.currentText())
        self.scot_select = scot_bus + scot_car + scot_rail

        # Check if the sum is over 100. If so, mark it in red
        if self.scot_select > 100:
            self.percent_label.setStyleSheet("font-size: 14px; color: red; font: bold")
        elif self.scot_select == 100:
            self.percent_label.setStyleSheet("font-size: 14px; color: green; font: bold")
        else:
            self.percent_label.setStyleSheet("font-size: 14px; color: #2d3436; font: bold")
        
        self.percent_label.setText(f"Selected: {self.scot_select}%")

    def update_uk_percent_label(self):
        # Inspired by find() method in: https://www.geeksforgeeks.org/pyqt5-getting-the-text-of-selected-item-in-combobox/
        """Update the label to show the percentages out of 100 that the user has selected"""
        uk_plane = int(self.plane_uk.currentText())
        uk_car = int(self.car_uk.currentText())
        uk_rail = int(self.rail_uk.currentText())
        self.uk_select = uk_plane + uk_car + uk_rail
        
        # Check if the sum is over 100. If so, mark it in red
        if self.uk_select > 100:
            self.uk_percent_label.setStyleSheet("font-size: 14px; color: red; font: bold")
        elif self.uk_select == 100:
            self.uk_percent_label.setStyleSheet("font-size: 14px; color: green; font: bold")
        else:
            self.uk_percent_label.setStyleSheet("font-size: 14px; color: #2d3436; font: bold")
        
        self.uk_percent_label.setText(f"Selected: {self.uk_select}%")
