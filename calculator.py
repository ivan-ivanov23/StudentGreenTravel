import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from tkinter.filedialog import askopenfile
import pandas as pd

# Source: https://www.tutorialspoint.com/pyqt/pyqt_qstackedwidget.htm 

class Calculator(QWidget):

    file_selected = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Set up application GUI"""
        self.setFixedSize(800, 600)
        self.setWindowTitle("StudentGreenTravel")

        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        self.layout3 = QVBoxLayout()

        self.stackedLayout = QStackedLayout()

        self.page1 = self.setUpMainWindow()
        self.page2 = self.setUpSecondPage()
        self.page3 = self.setUpThirdPage()

        self.stackedLayout.addWidget(self.page1)
        self.stackedLayout.addWidget(self.page2)
        self.stackedLayout.addWidget(self.page3)

        self.setLayout(self.stackedLayout)

        self.show()

    def setUpMainWindow(self):
        """Create and arrange widgets in the MainWindow"""
        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title label
        title = QLabel("Welcome to StudentGreenTravel!")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2d3436;")
        
        # Buttons
        button1 = QPushButton("Calculate Emissions")
        button1.setEnabled(False)
        button1.clicked.connect(self.go_to_page2)
        button2 = QPushButton("Select a File")
        button2.clicked.connect(self.open_file)

        # File label
        self.file_label = QLabel(" ")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add widgets to layout
        self.main_layout.addWidget(title)
        self.main_layout.addWidget(button1)
        self.main_layout.addWidget(button2)
        self.main_layout.addWidget(self.file_label)

        widget = QWidget()
        widget.setLayout(self.main_layout)

        self.file_selected.connect(self.enable_buttons)
        return widget

    def setUpSecondPage(self):
        """Create and arrange widgets in the SecondPage"""
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

        # Back button
        back = QPushButton("Back")
        back.clicked.connect(self.go_to_page1)
        next_button = QPushButton("Next")
        next_button.clicked.connect(self.go_to_page3)
        button_layout.addWidget(back)
        button_layout.addWidget(next_button)

        # Add the grid and button to the main layout of the page
        self.layout2.addLayout(grid)
        self.layout2.addStretch(1)
        self.layout2.addLayout(button_layout)

        # Return a widget with the layout
        widget = QWidget()
        widget.setLayout(self.layout2)
        return widget
    
    def setUpThirdPage(self):
        label = QLabel("Select the travel assumptions for the final leg of the journey.\nFrom Aberdeen transport hub to the University of Aberdeen")

        # Source: https://www.tutorialspoint.com/pyqt/pyqt_qstackedwidget.htm
        # List of countries
        leftlist = QListWidget()
        leftlist.insertItem(0, 'Scotland')
        leftlist.insertItem(1, 'England')
        leftlist.insertItem(2, 'Wales')
        leftlist.insertItem(3, 'Northern Ireland')
        leftlist.setFixedWidth(100)

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
        hbox.addWidget(leftlist)
        hbox.addWidget(self.Stack)


        # Button layout
        button_layout = QHBoxLayout()

        # Back button
        back = QPushButton("Back")
        back.clicked.connect(self.go_to_page2)
        next_button = QPushButton("Results")
        next_button.clicked.connect(self.go_to_results)
        button_layout.addWidget(back)
        button_layout.addWidget(next_button)

        self.layout3.addWidget(label)
        self.layout3.addLayout(hbox)
        leftlist.currentRowChanged.connect(self.display)
        self.layout3.addStretch(1)
        self.layout3.addLayout(button_layout)
        



        widget = QWidget()
        widget.setLayout(self.layout3)
        return widget
    
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


    def open_file(self):
        file = askopenfile(filetypes=[("Excel files", "*.xlsx")])
        # If the user selected a file, then read it using pandas
        if file:
        # Read address file
            addresses = pd.read_excel(file.name, engine='openpyxl')
            addresses.iloc[:, 1] = addresses.iloc[:, 1].str.replace(' ', '')
            # Add the file name to the label text with the file name withouth the path
            self.file_label.setText(f"File: {file.name.split('/')[-1]}")
            # Style the label
            #self.file_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #2d3436;")
            # Emit signal that a file has been selected
            self.file_selected.emit(True)
        else:
            self.file_label.setText("No file was selected.")
            # Emit a signal that a file has not been selected
            self.file_selected.emit(False)


    def enable_buttons(self, file_selected):
        if file_selected:
            for i in range(self.main_layout.count()):
                self.main_layout.itemAt(i).widget().setEnabled(True)

    def go_to_page1(self):
        self.stackedLayout.setCurrentIndex(0)
    
    def go_to_page2(self):
        self.stackedLayout.setCurrentIndex(1)

    def go_to_page3(self):
        self.stackedLayout.setCurrentIndex(2)

    def go_to_results(self):
        self.stackedLayout.setCurrentIndex(3)

    def display(self, i):
        self.Stack.setCurrentIndex(i)


app = QApplication(sys.argv)
window = Calculator()
sys.exit(app.exec())


# def setUpThirdPage(self):
#     label = QLabel("Select the travel assumptions for the final leg of the journey.\nFrom Aberdeen transport hub to the University of Aberdeen")

#     # Button layout
#     button_layout = QHBoxLayout()

#     # Vbox layout to hold the grids with combo boxes
#     grid_holder = QVBoxLayout()
#     grid_holder.addStretch(0)

#     # Scotland and UK labels
#     scot_label = QLabel("Scotland")
#     land_label = QLabel("Assumptions for land travelling students")
#     air_label = QLabel("Assumptions for air travelling students")
#     eng_label = QLabel("England")
#     wales_label = QLabel("Wales")
#     ni_label = QLabel("Northern Ireland")

#     car = QLabel("Car")
#     taxi = QLabel("Taxi")
#     bus = QLabel("Bus")
#     walk = QLabel("Walk")

#         # Combo boxes
#     scot_car_box = QComboBox()
#     scot_taxi_box = QComboBox()
#     scot_bus_box = QComboBox()
#     scot_walk_box = QComboBox()

#     eng_car_box = QComboBox()
#     eng_taxi_box = QComboBox()
#     eng_bus_box = QComboBox()
#     eng_walk_box = QComboBox()

#     wales_car_box = QComboBox()
#     wales_taxi_box = QComboBox()
#     wales_bus_box = QComboBox()
#     wales_walk_box = QComboBox()

#     ni_car_box = QComboBox()
#     ni_taxi_box = QComboBox()
#     ni_bus_box = QComboBox()
#     ni_walk_box = QComboBox()


#     combos = []
#     combos.append(scot_car_box)
#     combos.append(scot_taxi_box)
#     combos.append(scot_bus_box)
#     combos.append(scot_walk_box)
#     combos.append(eng_car_box)
#     combos.append(eng_taxi_box)
#     combos.append(eng_bus_box)
#     combos.append(eng_walk_box)
#     combos.append(wales_car_box)
#     combos.append(wales_taxi_box)
#     combos.append(wales_bus_box)
#     combos.append(wales_walk_box)
#     combos.append(ni_car_box)
#     combos.append(ni_taxi_box)
#     combos.append(ni_bus_box)
#     combos.append(ni_walk_box)

#     # Values for combo boxes
    # values = [str(i) for i in range(101)]
    # for combo_box in combos:
    #     combo_box.addItems(values)
    #     # Set fixed width
    #     combo_box.setFixedSize(QSize(50, 20))

#     # Scotland
#     scot_grid = QGridLayout()
#     scot_grid.setVerticalSpacing(2)
#     scot_grid.setHorizontalSpacing(10)

#     scot_grid.addWidget(scot_label, 0, 0, 1, 4)
#     scot_grid.addWidget(land_label, 1, 0)
#     scot_grid.addWidget(car, 2, 0)
#     scot_grid.addWidget(taxi, 3, 0)
#     scot_grid.addWidget(bus, 4, 0)
#     scot_grid.addWidget(walk, 5, 0)
#     scot_grid.addWidget(scot_car_box, 2, 1)
#     scot_grid.addWidget(scot_taxi_box, 3, 1)
#     scot_grid.addWidget(scot_bus_box, 4, 1)
#     scot_grid.addWidget(scot_walk_box, 5, 1)

#     scot_grid.setRowStretch(0, 1)

#     # Add the scottish grid to the grid holder
#     grid_holder.addLayout(scot_grid)

#     # England
#     eng_grid = QGridLayout()
#     # Shrink the label rows
#     eng_grid.setVerticalSpacing(2)
#     # Shrink space between columns
#     eng_grid.setHorizontalSpacing(50)


#     eng_grid.addWidget(eng_label, 0, 0, 1, 4)
#     eng_grid.addWidget(land_label, 1, 0)
#     eng_grid.addWidget(air_label, 1, 2)
#     eng_grid.addWidget(car, 2, 0)
#     eng_grid.addWidget(taxi, 3, 0)
#     eng_grid.addWidget(bus, 4, 0)
#     eng_grid.addWidget(walk, 5, 0)
#     eng_grid.addWidget(eng_car_box, 2, 1)
#     eng_grid.addWidget(eng_taxi_box, 3, 1)
#     eng_grid.addWidget(eng_bus_box, 4, 1)
#     eng_grid.addWidget(eng_walk_box, 5, 1)

#     eng_grid.addWidget(car, 2, 2)
#     eng_grid.addWidget(taxi, 3, 2)
#     eng_grid.addWidget(bus, 4, 2)
#     eng_grid.addWidget(walk, 5, 2)

#     eng_grid.addWidget(eng_car_box, 2, 3)
#     eng_grid.addWidget(eng_taxi_box, 3, 3)
#     eng_grid.addWidget(eng_bus_box, 4, 3)
#     eng_grid.addWidget(eng_walk_box, 5, 3)

#     grid_holder.addLayout(eng_grid)

#     # Back button
#     back = QPushButton("Back")
#     back.clicked.connect(self.go_to_page2)
#     next_button = QPushButton("Results")
#     next_button.clicked.connect(self.go_to_results)
#     button_layout.addWidget(back)
#     button_layout.addWidget(next_button)

#     self.layout3.addWidget(label)
#     self.layout3.addLayout(grid_holder)
#     self.layout3.addStretch(1)
#     self.layout3.addLayout(button_layout)



#     widget = QWidget()
#     widget.setLayout(self.layout3)
#     return widget