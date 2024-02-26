from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize


class Page3(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Create and arrange widgets for Page 3"""
        self.layout3 = QVBoxLayout()
        label = QLabel("Select the travel assumptions for the final leg of the journey.\nFrom Aberdeen transport hub to the University of Aberdeen")

        # Source: https://www.tutorialspoint.com/pyqt/pyqt_qstackedwidget.htm
        # List of countries
        self.leftlist = QListWidget()
        self.leftlist.insertItem(0, 'Scotland')
        self.leftlist.insertItem(1, 'England')
        self.leftlist.insertItem(2, 'Wales')
        self.leftlist.insertItem(3, 'Northern Ireland')
        self.leftlist.setFixedWidth(100)

        # Right side widgets
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()

        # Creating the right side widgets
        self.scotlandUI()
        self.englandUI()
        self.walesUI()
        self.niUI()

        # Adding the widgets to a stacked widget
        self.Stack = QStackedWidget()
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)
        self.Stack.addWidget(self.stack4)

        hbox = QHBoxLayout()
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)


        # Button layout
        button_layout = QHBoxLayout()

        # Back button
        self.back = QPushButton("Back")
        self.result_button = QPushButton("Results")
        button_layout.addWidget(self.back)
        button_layout.addWidget(self.result_button)

        self.layout3.addWidget(label)
        self.layout3.addLayout(hbox)
        self.layout3.addStretch(1)
        self.leftlist.currentRowChanged.connect(self.display)
        self.layout3.addLayout(button_layout)

        self.setLayout(self.layout3)
    
    def scotlandUI(self):
        """UI for Scotland""" 
        layout = QVBoxLayout()
        country = QLabel("Scotland")
        scot_grid = QGridLayout()
        # Reduce space between labels and combo box columns
        scot_grid.setHorizontalSpacing(20)
        scot_grid.setVerticalSpacing(2)
        scot_grid.setRowStretch(0, 1)
        # Align the labels to the right
        scot_grid.setAlignment(Qt.AlignmentFlag.AlignLeft)


        car = QLabel("Car")
        taxi = QLabel("Taxi")
        bus = QLabel("Bus")
        walk = QLabel("Walk")
      
        # Combo boxes
        scot_car_box = QComboBox()
        scot_taxi_box = QComboBox()
        scot_bus_box = QComboBox()
        scot_walk_box = QComboBox()
        
        combos = []
        combos.append(scot_car_box)
        combos.append(scot_taxi_box)
        combos.append(scot_bus_box)
        combos.append(scot_walk_box)


        # Values for combo boxes
        values = [str(i) for i in range(101)]
        # Add % string to the end of each value
        for combo_box in combos:
            combo_box.addItems(values)
            # Set fixed width
            combo_box.setFixedSize(QSize(50, 20))

        scot_grid.addWidget(car, 0, 0)
        scot_grid.addWidget(taxi, 1, 0)
        scot_grid.addWidget(bus, 2, 0)
        scot_grid.addWidget(walk, 3, 0)
        scot_grid.addWidget(scot_car_box, 0, 1)
        scot_grid.addWidget(scot_taxi_box, 1, 1)
        scot_grid.addWidget(scot_bus_box, 2, 1)
        scot_grid.addWidget(scot_walk_box, 3, 1)

        # reate a group box for the grid layout
        scotland_group = QGroupBox("Adjust percentages for each travel method from bus/rail station to university.")
        scotland_group.setLayout(scot_grid)

        layout.addWidget(country)
        layout.addWidget(scotland_group)
        layout.addStretch(1)

        self.stack1.setLayout(layout)
		
    def englandUI(self):
        """UI for England""" 
        layout = QVBoxLayout()
        country = QLabel("England")
        eng_grid_left = QGridLayout()
        # Reduce space between labels and combo box columns
        eng_grid_left.setHorizontalSpacing(20)
        eng_grid_left.setVerticalSpacing(2)
        eng_grid_left.setRowStretch(0, 1)
        # Align the labels to the right
        eng_grid_left.setAlignment(Qt.AlignmentFlag.AlignLeft)

        eng_grid_right = QGridLayout()
        # Reduce space between labels and combo box columns
        eng_grid_right.setHorizontalSpacing(20)
        eng_grid_right.setVerticalSpacing(2)
        eng_grid_right.setRowStretch(0, 1)
        # Align the labels to the right
        eng_grid_right.setAlignment(Qt.AlignmentFlag.AlignLeft)


        car_left = QLabel("Car")
        taxi_left = QLabel("Taxi")
        bus_left = QLabel("Bus")
        walk_left = QLabel("Walk")

        car_right = QLabel("Car")
        taxi_right = QLabel("Taxi")
        bus_right = QLabel("Bus")
        walk_right = QLabel("Walk")
      
        # Combo boxes for left side
        eng_car_box_left = QComboBox()
        eng_taxi_box_left = QComboBox()
        eng_bus_box_left = QComboBox()
        eng_walk_box_left = QComboBox()

        # Combo boxes for right side
        eng_car_box_right = QComboBox()
        eng_taxi_box_right = QComboBox()
        eng_bus_box_right = QComboBox()
        eng_walk_box_right = QComboBox()
        
        combos = []
        combos.append(eng_car_box_left)
        combos.append(eng_taxi_box_left)
        combos.append(eng_bus_box_left)
        combos.append(eng_walk_box_left)
        combos.append(eng_car_box_right)
        combos.append(eng_taxi_box_right)
        combos.append(eng_bus_box_right)
        combos.append(eng_walk_box_right)


        # Values for combo boxes
        values = [str(i) for i in range(101)]
        # Add % string to the end of each value
        for combo_box in combos:
            combo_box.addItems(values)
            # Set fixed width
            combo_box.setFixedSize(QSize(50, 20))

        # Left side
        eng_grid_left.addWidget(car_left, 0, 0)
        eng_grid_left.addWidget(taxi_left, 1, 0)
        eng_grid_left.addWidget(bus_left, 2, 0)
        eng_grid_left.addWidget(walk_left, 3, 0)
        eng_grid_left.addWidget(eng_car_box_left, 0, 1)
        eng_grid_left.addWidget(eng_taxi_box_left, 1, 1)
        eng_grid_left.addWidget(eng_bus_box_left, 2, 1)
        eng_grid_left.addWidget(eng_walk_box_left, 3, 1)

        # Right side
        eng_grid_right.addWidget(car_right, 0, 0)
        eng_grid_right.addWidget(taxi_right, 1, 0)
        eng_grid_right.addWidget(bus_right, 2, 0)
        eng_grid_right.addWidget(walk_right, 3, 0)
        eng_grid_right.addWidget(eng_car_box_right, 0, 1)
        eng_grid_right.addWidget(eng_taxi_box_right, 1, 1)
        eng_grid_right.addWidget(eng_bus_box_right, 2, 1)
        eng_grid_right.addWidget(eng_walk_box_right, 3, 1)


        # Create a group box for the grid layout
        england_group_left = QGroupBox("Adjust percentages for each travel method from bus/rail station to university.")
        england_group_left.setLayout(eng_grid_left)

        # Create a group box for the grid layout
        england_group_right = QGroupBox("Adjust percentages for each travel method from airport to university.")
        england_group_right.setLayout(eng_grid_right)



        layout.addWidget(country)
        layout.addWidget(england_group_left)
        layout.addWidget(england_group_right)
        layout.addStretch(1)
            
        self.stack2.setLayout(layout)
		
    def walesUI(self):
        """UI for Wales""" 
        layout = QVBoxLayout()
        country = QLabel("Wales")
        wales_grid_left = QGridLayout()
        # Reduce space between labels and combo box columns
        wales_grid_left.setHorizontalSpacing(20)
        wales_grid_left.setVerticalSpacing(2)
        wales_grid_left.setRowStretch(0, 1)
        # Align the labels to the right
        wales_grid_left.setAlignment(Qt.AlignmentFlag.AlignLeft)

        wales_grid_right = QGridLayout()
        # Reduce space between labels and combo box columns
        wales_grid_right.setHorizontalSpacing(20)
        wales_grid_right.setVerticalSpacing(2)
        wales_grid_right.setRowStretch(0, 1)
        # Align the labels to the right
        wales_grid_right.setAlignment(Qt.AlignmentFlag.AlignLeft)


        car_left = QLabel("Car")
        taxi_left = QLabel("Taxi")
        bus_left = QLabel("Bus")
        walk_left = QLabel("Walk")

        car_right = QLabel("Car")
        taxi_right = QLabel("Taxi")
        bus_right = QLabel("Bus")
        walk_right = QLabel("Walk")
      
        # Combo boxes for left side
        wales_car_box_left = QComboBox()
        wales_taxi_box_left = QComboBox()
        wales_bus_box_left = QComboBox()
        wales_walk_box_left = QComboBox()

        # Combo boxes for right side
        wales_car_box_right = QComboBox()
        wales_taxi_box_right = QComboBox()
        wales_bus_box_right = QComboBox()
        wales_walk_box_right = QComboBox()
        
        combos = []
        combos.append(wales_car_box_left)
        combos.append(wales_taxi_box_left)
        combos.append(wales_bus_box_left)
        combos.append(wales_walk_box_left)
        combos.append(wales_car_box_right)
        combos.append(wales_taxi_box_right)
        combos.append(wales_bus_box_right)
        combos.append(wales_walk_box_right)


        # Values for combo boxes
        values = [str(i) for i in range(101)]
        # Add % string to the end of each value
        for combo_box in combos:
            combo_box.addItems(values)
            # Set fixed width
            combo_box.setFixedSize(QSize(50, 20))

        # Left side
        wales_grid_left.addWidget(car_left, 0, 0)
        wales_grid_left.addWidget(taxi_left, 1, 0)
        wales_grid_left.addWidget(bus_left, 2, 0)
        wales_grid_left.addWidget(walk_left, 3, 0)
        wales_grid_left.addWidget(wales_car_box_left, 0, 1)
        wales_grid_left.addWidget(wales_taxi_box_left, 1, 1)
        wales_grid_left.addWidget(wales_bus_box_left, 2, 1)
        wales_grid_left.addWidget(wales_walk_box_left, 3, 1)

        # Right side
        wales_grid_right.addWidget(car_right, 0, 0)
        wales_grid_right.addWidget(taxi_right, 1, 0)
        wales_grid_right.addWidget(bus_right, 2, 0)
        wales_grid_right.addWidget(walk_right, 3, 0)
        wales_grid_right.addWidget(wales_car_box_right, 0, 1)
        wales_grid_right.addWidget(wales_taxi_box_right, 1, 1)
        wales_grid_right.addWidget(wales_bus_box_right, 2, 1)
        wales_grid_right.addWidget(wales_walk_box_right, 3, 1)


        # Create a group box for the grid layout
        wales_group_left = QGroupBox("Adjust percentages for each travel method from bus/rail station to university.")
        wales_group_left.setLayout(wales_grid_left)

        # Create a group box for the grid layout
        wales_group_right = QGroupBox("Adjust percentages for each travel method from airport to university.")
        wales_group_right.setLayout(wales_grid_right)



        layout.addWidget(country)
        layout.addWidget(wales_group_left)
        layout.addWidget(wales_group_right)
        layout.addStretch(1)
    
        self.stack3.setLayout(layout)

    def niUI(self):
        """UI for Northern Ireland""" 
        layout = QVBoxLayout()
        country = QLabel("Northern Ireland")
        ni_grid_left = QGridLayout()
        # Reduce space between labels and combo box columns
        ni_grid_left.setHorizontalSpacing(20)
        ni_grid_left.setVerticalSpacing(2)
        ni_grid_left.setRowStretch(0, 1)
        # Align the labels to the right
        ni_grid_left.setAlignment(Qt.AlignmentFlag.AlignLeft)

        ni_grid_right = QGridLayout()
        # Reduce space between labels and combo box columns
        ni_grid_right.setHorizontalSpacing(20)
        ni_grid_right.setVerticalSpacing(2)
        ni_grid_right.setRowStretch(0, 1)
        # Align the labels to the right
        ni_grid_right.setAlignment(Qt.AlignmentFlag.AlignLeft)


        car_left = QLabel("Car")
        taxi_left = QLabel("Taxi")
        bus_left = QLabel("Bus")
        walk_left = QLabel("Walk")

        car_right = QLabel("Car")
        taxi_right = QLabel("Taxi")
        bus_right = QLabel("Bus")
        walk_right = QLabel("Walk")
      
        # Combo boxes for left side
        ni_car_box_left = QComboBox()
        ni_taxi_box_left = QComboBox()
        ni_bus_box_left = QComboBox()
        ni_walk_box_left = QComboBox()

        # Combo boxes for right side
        ni_car_box_right = QComboBox()
        ni_taxi_box_right = QComboBox()
        ni_bus_box_right = QComboBox()
        ni_walk_box_right = QComboBox()
        
        combos = []
        combos.append(ni_car_box_left)
        combos.append(ni_taxi_box_left)
        combos.append(ni_bus_box_left)
        combos.append(ni_walk_box_left)
        combos.append(ni_car_box_right)
        combos.append(ni_taxi_box_right)
        combos.append(ni_bus_box_right)
        combos.append(ni_walk_box_right)


        # Values for combo boxes
        values = [str(i) for i in range(101)]
        # Add % string to the end of each value
        for combo_box in combos:
            combo_box.addItems(values)
            # Set fixed width
            combo_box.setFixedSize(QSize(50, 20))

        # Left side
        ni_grid_left.addWidget(car_left, 0, 0)
        ni_grid_left.addWidget(taxi_left, 1, 0)
        ni_grid_left.addWidget(bus_left, 2, 0)
        ni_grid_left.addWidget(walk_left, 3, 0)
        ni_grid_left.addWidget(ni_car_box_left, 0, 1)
        ni_grid_left.addWidget(ni_taxi_box_left, 1, 1)
        ni_grid_left.addWidget(ni_bus_box_left, 2, 1)
        ni_grid_left.addWidget(ni_walk_box_left, 3, 1)

        # Right side
        ni_grid_right.addWidget(car_right, 0, 0)
        ni_grid_right.addWidget(taxi_right, 1, 0)
        ni_grid_right.addWidget(bus_right, 2, 0)
        ni_grid_right.addWidget(walk_right, 3, 0)
        ni_grid_right.addWidget(ni_car_box_right, 0, 1)
        ni_grid_right.addWidget(ni_taxi_box_right, 1, 1)
        ni_grid_right.addWidget(ni_bus_box_right, 2, 1)
        ni_grid_right.addWidget(ni_walk_box_right, 3, 1)


        # Create a group box for the grid layout
        ni_group_left = QGroupBox("Adjust percentages for each travel method from bus/rail station to university.")
        ni_group_left.setLayout(ni_grid_left)

        # Create a group box for the grid layout
        ni_group_right = QGroupBox("Adjust percentages for each travel method from airport to university.")
        ni_group_right.setLayout(ni_grid_right)



        layout.addWidget(country)
        layout.addWidget(ni_group_left)
        layout.addWidget(ni_group_right)
        layout.addStretch(1)
        self.stack4.setLayout(layout)

    def display(self, i):
        self.Stack.setCurrentIndex(i)