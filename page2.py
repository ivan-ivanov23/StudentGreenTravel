from PyQt6.QtWidgets import QVBoxLayout, QLabel, QComboBox, QGridLayout, QHBoxLayout, QPushButton, QWidget


class Page2(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Create and arrange widgets in the SecondPage"""
        self.layout2 = QVBoxLayout()
        # Title label
        label = QLabel("Select percentages of students travelling by each transport method")
        self.layout2.addWidget(label)

        # Grid layout for the combo boxes
        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setRowStretch(0, 1)

        # Scotland combo boxes and labels
        scotland_label = QLabel("Scotland")
        grid.addWidget(scotland_label, 0, 0)

        bus_scotland_label = QLabel("Bus %")
        grid.addWidget(bus_scotland_label, 1, 0)
        self.combo_bus_scot = QComboBox()
        for i in range(101):
            val = str(i)
            self.combo_bus_scot.addItem(val)
        grid.addWidget(self.combo_bus_scot, 1, 1)

        car_scotland_label = QLabel("Car %", self)
        grid.addWidget(car_scotland_label, 2, 0)
        self.combo_car_scot = QComboBox(self)
        for i in range(101):
            val = str(i)
            self.combo_car_scot.addItem(val)
        grid.addWidget(self.combo_car_scot, 2, 1)

        rail_scotland_label = QLabel("Train %", self)
        grid.addWidget(rail_scotland_label, 3, 0)
        self.combo_rail_scot = QComboBox(self)
        for i in range(101):
            val = str(i)
            self.combo_rail_scot.addItem(val)
        grid.addWidget(self.combo_rail_scot, 3, 1)


        # UK
        uk_label = QLabel("Rest of UK", self)
        grid.addWidget(uk_label, 0, 2)

        plane_uk_label = QLabel("Plane %", self)
        grid.addWidget(plane_uk_label, 1, 2)
        self.plane_uk = QComboBox(self)
        for i in range(101):
            self.plane_uk.addItem(str(i))
        grid.addWidget(self.plane_uk, 1, 3)

        car_uk_label = QLabel("Car %", self)
        grid.addWidget(car_uk_label, 2, 2)
        self.car_uk = QComboBox(self)
        for i in range(101):
            self.car_uk.addItem(str(i))
        grid.addWidget(self.car_uk, 2, 3)

        rail_uk_label = QLabel("Train %", self)
        grid.addWidget(rail_uk_label, 3, 2)
        self.rail_uk = QComboBox(self)
        for i in range(101):
            self.rail_uk.addItem(str(i))
        grid.addWidget(self.rail_uk, 3, 3)

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
        self.layout2.addLayout(grid)
        self.layout2.addStretch(1)
        self.layout2.addLayout(button_layout)

        self.setLayout(self.layout2)