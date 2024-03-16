# Code for the third page of the application (Final leg assumptions page)
# Sources of code snippets are provided in the comments of functions.
# Author: Ivan Ivanov

from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QStackedWidget, QListWidget, 
                             QLabel, QWidget, QComboBox, QGridLayout, QGroupBox, QPushButton)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
import os

basedir = os.path.dirname(__file__)

class Page3(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()
        self.get_combo_values(self.scot_combos, self.scot_select, self.percent_scot_label)
        self.get_combo_values(self.eng_combos1, self.eng_select1, self.percent_eng_label1)
        self.get_combo_values(self.eng_combos2, self.eng_select2, self.percent_eng_label2)
        self.get_combo_values(self.wales_combos1, self.wales_select1, self.percent_wales_label1)
        self.get_combo_values(self.wales_combos2, self.wales_select2, self.percent_wales_label2)
        self.get_combo_values(self.ni_combos1, self.ni_select1, self.percent_ni_label1)
        self.get_combo_values(self.ni_combos2, self.ni_select2, self.percent_ni_label2)
        self.get_combo_values(self.aberdeen_combos, self.aberdeen_select, self.percent_aberdeen_label)

    def initializeUI(self):
        """Create and arrange widgets for Page 3"""
        self.layout3 = QVBoxLayout()
        label = QLabel("Assumptions for Final Leg of the Journey")
        label.setStyleSheet("font-size: 16px; font-weight: bold; color: white; background-color: #2C2C2C; padding: 10px; border-radius: 5px; margin-bottom: 10px;")

        # Picture of the final leg of the journey
        fin_leg_pic = QLabel()
        # Load the pixmap
        fin_leg_pic.setFixedSize(QSize(785, 107))
        pixmap = QPixmap(os.path.join(basedir, "pictures/fin.png"))
        # Resize the pixmap to fit within the label size while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(fin_leg_pic.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        # Set the pixmap to the label
        fin_leg_pic.setPixmap(scaled_pixmap)
        
        
        instruction = QLabel("""
                             <b>Tip:</b> Select or enter the percentage of students traveling by each transport method 
                             for the final leg of their journey. That is from the bus/rail station or airport to the university.
                             <br>
                             Please, do this for each of the countries in the list on the left. 
                             <br><br>
                             Additionally, you can check the '<b>Include Aberdeen</b>' box to include the city of Aberdeen in the list and 
                             make assumptions for students living there.
                            <br><br>
                             Once you have selected the percentages for the middle leg of the journey, click '<b>Submit</b>' to confirm your choices.
                             """)
        instruction.setStyleSheet("font-size: 14px; color: #2d3436; margin-bottom: 10px; border-radius: 5px; background-color: #D7D7D7; padding: 5px;")

        # Source: https://www.tutorialspoint.com/pyqt/pyqt_qstackedwidget.htm
        # List of countries
        self.leftlist = QListWidget()
        self.leftlist.insertItem(0, 'Aberdeen City')
        self.leftlist.insertItem(1, 'Scotland')
        self.leftlist.insertItem(2, 'England')
        self.leftlist.insertItem(3, 'Wales')
        self.leftlist.insertItem(4, 'Northern Ireland')

        self.leftlist.setFixedWidth(150)
        self.leftlist.setFixedHeight(250)
        self.leftlist.setStyleSheet("background-color: #dfe6e9; border-radius: 5px; font-size: 14px; color: #2d3436; padding: 5px; margin-bottom: 10px;")

        # Right side widgets
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()
        self.stack5 = QWidget()

        # Creating the right side widgets
        self.aberdeenUI()
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
        self.Stack.addWidget(self.stack5)

        hbox = QHBoxLayout()
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)

        # Label to say that it is calculating
        self.calculating_label = QLabel("")
        self.calculating_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # Button layout
        button_layout = QHBoxLayout()

        # Back button
        self.back = QPushButton("Back")
        self.submit = QPushButton("Submit")
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.setDisabled(True)
        button_layout.addWidget(self.back)
        button_layout.addWidget(self.submit)
        button_layout.addWidget(self.calculate_button)

        self.layout3.addWidget(label)
        self.layout3.addWidget(fin_leg_pic)
        self.layout3.addWidget(instruction)
        self.layout3.addLayout(hbox)
        self.layout3.addStretch(1)
        self.leftlist.currentRowChanged.connect(self.display)
        self.layout3.addWidget(self.calculating_label)
        self.layout3.addLayout(button_layout)

        self.setLayout(self.layout3)

    def aberdeenUI(self):
        """UI for Aberdeen"""
        layout = QVBoxLayout()
        city = QLabel("Aberdeen City")
        city.setStyleSheet("font-weight: bold; font-size: 18px; color: #2d3436; margin-bottom: 10px; border-radius: 5px; background-color: #dfe6e9; padding: 5px;")
        aberdeen_grid = QGridLayout()
        # Reduce space between labels and combo box columns
        aberdeen_grid.setHorizontalSpacing(20)
        aberdeen_grid.setVerticalSpacing(6)
        aberdeen_grid.setRowStretch(0, 1)
        # Align the labels to the right
        aberdeen_grid.setAlignment(Qt.AlignmentFlag.AlignCenter)


        car = QLabel("Car %")
        car.setStyleSheet("font-size: 14px; color: #2d3436")
        taxi = QLabel("Taxi %")
        taxi.setStyleSheet("font-size: 14px; color: #2d3436")
        bus = QLabel("Bus %")
        bus.setStyleSheet("font-size: 14px; color: #2d3436")
        walk = QLabel("Walk %")
        walk.setStyleSheet("font-size: 14px; color: #2d3436")
      
        # Combo boxes
        self.aberdeen_car_box = QComboBox()
        self.aberdeen_taxi_box = QComboBox()
        self.aberdeen_bus_box = QComboBox()
        self.aberdeen_walk_box = QComboBox()
        
        self.aberdeen_combos = {'car': self.aberdeen_car_box, 'taxi': self.aberdeen_taxi_box, 'bus': self.aberdeen_bus_box, 'walk': self.aberdeen_walk_box}


        # Values for combo boxes
        values = [str(i) for i in range(101)]
        # Add % string to the end of each value
        for key, combo_box in self.aberdeen_combos.items():
            combo_box.addItems(values)
            # Set fixed width
            combo_box.setFixedSize(QSize(50, 20))

        aberdeen_grid.addWidget(car, 0, 0)
        aberdeen_grid.addWidget(taxi, 1, 0)
        aberdeen_grid.addWidget(bus, 2, 0)
        aberdeen_grid.addWidget(walk, 3, 0)
        aberdeen_grid.addWidget(self.aberdeen_car_box, 0, 1)
        aberdeen_grid.addWidget(self.aberdeen_taxi_box, 1, 1)
        aberdeen_grid.addWidget(self.aberdeen_bus_box, 2, 1)
        aberdeen_grid.addWidget(self.aberdeen_walk_box, 3, 1)

        # Label to show selected percentatges
        self.aberdeen_select = 0
        self.percent_aberdeen_label = QLabel(f"Selected: {self.aberdeen_select}%")
        self.percent_aberdeen_label.setStyleSheet("font-size: 14px; color: #2d3436; font: bold")
        aberdeen_grid.addWidget(self.percent_aberdeen_label, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        # Create a group box for the grid layout
        aberdeen_group = QGroupBox("Journey from home to university.")
        aberdeen_group.setStyleSheet("font-size: 14px")
        aberdeen_group.setLayout(aberdeen_grid)

        # Adjust the sizes of the grids and group boxes to fit the window
        aberdeen_group.setFixedSize(300, 200)

        # Put the group boxes next to each other
        lay1 = QHBoxLayout()
        lay1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        lay1.addWidget(aberdeen_group)

        # Create a page indicator
        page_label = QLabel("1/5")
        page_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2d3436;")
        page_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(city)
        layout.addLayout(lay1)
        layout.addWidget(page_label)
        layout.addStretch(1)

        self.stack1.setLayout(layout)
    
    def scotlandUI(self):
        """UI for Scotland""" 
        layout = QVBoxLayout()
        lay1 = QHBoxLayout()
        country = QLabel("Scotland")
        country.setStyleSheet("font-weight: bold; font-size: 18px; color: #2d3436; margin-bottom: 10px; border-radius: 5px; background-color: #dfe6e9; padding: 5px;")
        scot_grid = QGridLayout()
        # Reduce space between labels and combo box columns
        scot_grid.setHorizontalSpacing(20)
        scot_grid.setVerticalSpacing(6)
        scot_grid.setRowStretch(0, 1)
        # Align the labels to the right
        scot_grid.setAlignment(Qt.AlignmentFlag.AlignCenter)


        car = QLabel("Car %")
        car.setStyleSheet("font-size: 14px; color: #2d3436")
        taxi = QLabel("Taxi %")
        taxi.setStyleSheet("font-size: 14px; color: #2d3436")
        bus = QLabel("Bus %")
        bus.setStyleSheet("font-size: 14px; color: #2d3436")
        walk = QLabel("Walk %")
        walk.setStyleSheet("font-size: 14px; color: #2d3436")
      
        # Combo boxes
        self.scot_car_box = QComboBox()
        self.scot_taxi_box = QComboBox()
        self.scot_bus_box = QComboBox()
        self.scot_walk_box = QComboBox()
        
        self.scot_combos = {'car': self.scot_car_box, 'taxi': self.scot_taxi_box, 'bus': self.scot_bus_box, 'walk': self.scot_walk_box}


        # Values for combo boxes
        values = [str(i) for i in range(101)]
        # Add % string to the end of each value
        for key, combo_box in self.scot_combos.items():
            combo_box.addItems(values)
            # Set fixed width
            combo_box.setFixedSize(QSize(50, 20))

        scot_grid.addWidget(car, 0, 0)
        scot_grid.addWidget(taxi, 1, 0)
        scot_grid.addWidget(bus, 2, 0)
        scot_grid.addWidget(walk, 3, 0)
        scot_grid.addWidget(self.scot_car_box, 0, 1)
        scot_grid.addWidget(self.scot_taxi_box, 1, 1)
        scot_grid.addWidget(self.scot_bus_box, 2, 1)
        scot_grid.addWidget(self.scot_walk_box, 3, 1)

        # Label to show selected percentatges
        self.scot_select = 0
        self.percent_scot_label = QLabel(f"Selected: {self.scot_select}%")
        self.percent_scot_label.setStyleSheet("font-size: 14px; color: #2d3436; font: bold")
        scot_grid.addWidget(self.percent_scot_label, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        # Create a group box for the grid layout
        scotland_group = QGroupBox("Journey from bus/rail station to university.")
        scotland_group.setStyleSheet("font-size: 14px")
        scotland_group.setLayout(scot_grid)

        # Adjust the sizes of the grids and group boxes to fit the window
        scotland_group.setFixedSize(300, 200)

        # Put the group boxes next to each other
        lay1 = QHBoxLayout()
        lay1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        lay1.addWidget(scotland_group)

        # Create a page indicator
        page_label = QLabel("2/5")
        page_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2d3436;")
        page_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(country)
        layout.addLayout(lay1)
        layout.addWidget(page_label)
        layout.addStretch(1)

        self.stack2.setLayout(layout)
		
    def englandUI(self):
        """UI for England""" 
        layout = QVBoxLayout()
        country = QLabel("England")
        country.setStyleSheet("font-weight: bold; font-size: 18px; color: #2d3436; margin-bottom: 10px; border-radius: 5px; background-color: #dfe6e9; padding: 5px;")
        eng_grid_top = QGridLayout()
        # Reduce space between labels and combo box columns
        eng_grid_top.setHorizontalSpacing(20)
        eng_grid_top.setVerticalSpacing(6)
        eng_grid_top.setRowStretch(0, 1)
        # Align the labels to the right
        eng_grid_top.setAlignment(Qt.AlignmentFlag.AlignCenter)

        eng_grid_bottom = QGridLayout()
        # Reduce space between labels and combo box columns
        eng_grid_bottom.setHorizontalSpacing(20)
        eng_grid_bottom.setVerticalSpacing(6)
        eng_grid_bottom.setRowStretch(0, 1)
        # Align the labels to the right
        eng_grid_bottom.setAlignment(Qt.AlignmentFlag.AlignCenter)


        car_top = QLabel("Car %")
        car_top.setStyleSheet("font-size: 14px; color: #2d3436")
        taxi_top = QLabel("Taxi %")
        taxi_top.setStyleSheet("font-size: 14px; color: #2d3436")
        bus_top = QLabel("Bus %")
        bus_top.setStyleSheet("font-size: 14px; color: #2d3436")
        walk_top = QLabel("Walk %")
        walk_top.setStyleSheet("font-size: 14px; color: #2d3436")

        car_bottom = QLabel("Car %")
        car_bottom.setStyleSheet("font-size: 14px; color: #2d3436")
        taxi_bottom = QLabel("Taxi %")
        taxi_bottom.setStyleSheet("font-size: 14px; color: #2d3436")
        bus_bottom = QLabel("Bus %")
        bus_bottom.setStyleSheet("font-size: 14px; color: #2d3436")
        walk_bottom = QLabel("Walk %")
        walk_bottom.setStyleSheet("font-size: 14px; color: #2d3436")
      
        # Combo boxes for left side
        self.eng_car_box_top = QComboBox()
        self.eng_taxi_box_top = QComboBox()
        self.eng_bus_box_top = QComboBox()
        self.eng_walk_box_top = QComboBox()

        # Combo boxes for right side
        self.eng_car_box_bottom = QComboBox()
        self.eng_taxi_box_bottom = QComboBox()
        self.eng_bus_box_bottom = QComboBox()
        self.eng_walk_box_bottom = QComboBox()
        
        self.eng_combos = {'car_land': self.eng_car_box_top, 'taxi_land': self.eng_taxi_box_top, 'bus_land': self.eng_bus_box_top, 
                           'walk_land': self.eng_walk_box_top, 'car_air': self.eng_car_box_bottom, 'taxi_air': self.eng_taxi_box_bottom, 
                           'bus_air': self.eng_bus_box_bottom, 'walk_air': self.eng_walk_box_bottom}
        
        # Dictionary to be used for percentage counters
        self.eng_combos1 = {'car_land': self.eng_car_box_top, 'taxi_land': self.eng_taxi_box_top, 'bus_land': self.eng_bus_box_top, 'walk_land': self.eng_walk_box_top}
        self.eng_combos2 = {'car_air': self.eng_car_box_bottom, 'taxi_air': self.eng_taxi_box_bottom, 'bus_air': self.eng_bus_box_bottom, 'walk_air': self.eng_walk_box_bottom}
     

        # Values for combo boxes
        values = [str(i) for i in range(101)]
        # Add % string to the end of each value
        for key, combo_box in self.eng_combos.items():
            combo_box.addItems(values)
            # Set fixed width
            combo_box.setFixedSize(QSize(50, 20))

        # Left side
        eng_grid_top.addWidget(car_top, 0, 0)
        eng_grid_top.addWidget(taxi_top, 1, 0)
        eng_grid_top.addWidget(bus_top, 2, 0)
        eng_grid_top.addWidget(walk_top, 3, 0)
        eng_grid_top.addWidget(self.eng_car_box_top, 0, 1)
        eng_grid_top.addWidget(self.eng_taxi_box_top, 1, 1)
        eng_grid_top.addWidget(self.eng_bus_box_top, 2, 1)
        eng_grid_top.addWidget(self.eng_walk_box_top, 3, 1)

        # Label to show selected percentatges for left side
        self.eng_select1 = 0
        self.percent_eng_label1 = QLabel(f"Selected: {self.eng_select1}%")
        self.percent_eng_label1.setStyleSheet("font-size: 14px; color: #2d3436; font: bold")
        eng_grid_top.addWidget(self.percent_eng_label1, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        # Right side
        eng_grid_bottom.addWidget(car_bottom, 0, 0)
        eng_grid_bottom.addWidget(taxi_bottom, 1, 0)
        eng_grid_bottom.addWidget(bus_bottom, 2, 0)
        eng_grid_bottom.addWidget(walk_bottom, 3, 0)
        eng_grid_bottom.addWidget(self.eng_car_box_bottom, 0, 1)
        eng_grid_bottom.addWidget(self.eng_taxi_box_bottom, 1, 1)
        eng_grid_bottom.addWidget(self.eng_bus_box_bottom, 2, 1)
        eng_grid_bottom.addWidget(self.eng_walk_box_bottom, 3, 1)

        # Label to show selected percentatges for right side
        self.eng_select2 = 0
        self.percent_eng_label2 = QLabel(f"Selected: {self.eng_select2}%")
        self.percent_eng_label2.setStyleSheet("font-size: 14px; color: #2d3436; font: bold")
        eng_grid_bottom.addWidget(self.percent_eng_label2, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)



        # Create a group box for the grid layout
        england_group_top = QGroupBox("Journey from bus/rail station to university.")
        england_group_top.setStyleSheet("font-size: 14px")
        england_group_top.setLayout(eng_grid_top)

        # Create a group box for the grid layout
        england_group_bottom = QGroupBox("Journey from airport to university.")
        england_group_bottom.setStyleSheet("font-size: 14px")
        england_group_bottom.setLayout(eng_grid_bottom)

        # Adjust the sizes of the grids and group boxes to fit the window
        england_group_top.setFixedSize(300, 200)
        england_group_bottom.setFixedSize(300, 200)

        # Put the group boxes next to each other
        lay1 = QHBoxLayout()
        lay1.addWidget(england_group_top)
        lay1.addWidget(england_group_bottom)

        # Create a page indicator
        page_label = QLabel("3/5")
        page_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2d3436;")
        page_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(country)
        layout.addLayout(lay1)
        layout.addWidget(page_label)
        layout.addStretch(1)
            
        self.stack3.setLayout(layout)
		
    def walesUI(self):
        """UI for Wales""" 
        layout = QVBoxLayout()
        country = QLabel("Wales")
        country.setStyleSheet("font-weight: bold; font-size: 18px; color: #2d3436; margin-bottom: 10px; border-radius: 5px; background-color: #dfe6e9; padding: 5px;")
        wales_grid_top = QGridLayout()
        # Reduce space between labels and combo box columns
        wales_grid_top.setHorizontalSpacing(20)
        wales_grid_top.setVerticalSpacing(6)
        wales_grid_top.setRowStretch(0, 1)
        # Align the labels to the right
        wales_grid_top.setAlignment(Qt.AlignmentFlag.AlignCenter)

        wales_grid_bottom = QGridLayout()
        # Reduce space between labels and combo box columns
        wales_grid_bottom.setHorizontalSpacing(20)
        wales_grid_bottom.setVerticalSpacing(6)
        wales_grid_bottom.setRowStretch(0, 1)
        # Align the labels to the right
        wales_grid_bottom.setAlignment(Qt.AlignmentFlag.AlignCenter)


        car_top = QLabel("Car %")
        car_top.setStyleSheet("font-size: 14px; color: #2d3436")
        taxi_top = QLabel("Taxi %")
        taxi_top.setStyleSheet("font-size: 14px; color: #2d3436")
        bus_top = QLabel("Bus %")
        bus_top.setStyleSheet("font-size: 14px; color: #2d3436")
        walk_top = QLabel("Walk %")
        walk_top.setStyleSheet("font-size: 14px; color: #2d3436")

        car_bottom = QLabel("Car %")
        car_bottom.setStyleSheet("font-size: 14px; color: #2d3436")
        taxi_bottom = QLabel("Taxi %")
        taxi_bottom.setStyleSheet("font-size: 14px; color: #2d3436")
        bus_bottom = QLabel("Bus %")
        bus_bottom.setStyleSheet("font-size: 14px; color: #2d3436")
        walk_bottom = QLabel("Walk %")
        walk_bottom.setStyleSheet("font-size: 14px; color: #2d3436")
      
        # Combo boxes for left side
        self.wales_car_box_top = QComboBox()
        self.wales_taxi_box_top = QComboBox()
        self.wales_bus_box_top = QComboBox()
        self.wales_walk_box_top = QComboBox()

        # Combo boxes for right side
        self.wales_car_box_bottom = QComboBox()
        self.wales_taxi_box_bottom = QComboBox()
        self.wales_bus_box_bottom = QComboBox()
        self.wales_walk_box_bottom = QComboBox()
        
        # Dictionary to store the combo boxes
        self.wales_combos = {'car_land': self.wales_car_box_top, 'taxi_land': self.wales_taxi_box_top, 'bus_land': self.wales_bus_box_top,
                                'walk_land': self.wales_walk_box_top, 'car_air': self.wales_car_box_bottom, 'taxi_air': self.wales_taxi_box_bottom,
                                'bus_air': self.wales_bus_box_bottom, 'walk_air': self.wales_walk_box_bottom}
        
        # Dictionary to be used for percentage counters
        self.wales_combos1 = {'car_land': self.wales_car_box_top, 'taxi_land': self.wales_taxi_box_top, 'bus_land': self.wales_bus_box_top, 'walk_land': self.wales_walk_box_top}
        self.wales_combos2 = {'car_air': self.wales_car_box_bottom, 'taxi_air': self.wales_taxi_box_bottom, 'bus_air': self.wales_bus_box_bottom, 'walk_air': self.wales_walk_box_bottom}


        # Values for combo boxes
        values = [str(i) for i in range(101)]
        # Add % string to the end of each value
        for key, combo_box in self.wales_combos.items():
            combo_box.addItems(values)
            # Set fixed width
            combo_box.setFixedSize(QSize(50, 20))

        # Left side
        wales_grid_top.addWidget(car_top, 0, 0)
        wales_grid_top.addWidget(taxi_top, 1, 0)
        wales_grid_top.addWidget(bus_top, 2, 0)
        wales_grid_top.addWidget(walk_top, 3, 0)
        wales_grid_top.addWidget(self.wales_car_box_top, 0, 1)
        wales_grid_top.addWidget(self.wales_taxi_box_top, 1, 1)
        wales_grid_top.addWidget(self.wales_bus_box_top, 2, 1)
        wales_grid_top.addWidget(self.wales_walk_box_top, 3, 1)

        # Label to show selected percentatges for left side
        self.wales_select1 = 0
        self.percent_wales_label1 = QLabel(f"Selected: {self.wales_select1}%")
        self.percent_wales_label1.setStyleSheet("font-size: 14px; color: #2d3436; font: bold")
        wales_grid_top.addWidget(self.percent_wales_label1, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        # Right side
        wales_grid_bottom.addWidget(car_bottom, 0, 0)
        wales_grid_bottom.addWidget(taxi_bottom, 1, 0)
        wales_grid_bottom.addWidget(bus_bottom, 2, 0)
        wales_grid_bottom.addWidget(walk_bottom, 3, 0)
        wales_grid_bottom.addWidget(self.wales_car_box_bottom, 0, 1)
        wales_grid_bottom.addWidget(self.wales_taxi_box_bottom, 1, 1)
        wales_grid_bottom.addWidget(self.wales_bus_box_bottom, 2, 1)
        wales_grid_bottom.addWidget(self.wales_walk_box_bottom, 3, 1)

        # Label to show selected percentatges for right side
        self.wales_select2 = 0
        self.percent_wales_label2 = QLabel(f"Selected: {self.wales_select2}%")
        self.percent_wales_label2.setStyleSheet("font-size: 14px; color: #2d3436; font: bold")
        wales_grid_bottom.addWidget(self.percent_wales_label2, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)



        # Create a group box for the grid layout
        wales_group_top = QGroupBox("Journey from bus/rail station to university.")
        wales_group_top.setStyleSheet("font-size: 14px")
        wales_group_top.setLayout(wales_grid_top)

        # Create a group box for the grid layout
        wales_group_bottom = QGroupBox("Journey from airport to university.")
        wales_group_bottom.setStyleSheet("font-size: 14px")
        wales_group_bottom.setLayout(wales_grid_bottom)

        # Adjust the sizes of the grids and group boxes to fit the window
        wales_group_top.setFixedSize(300, 200)	
        wales_group_bottom.setFixedSize(300, 200)

        # Put the group boxes next to each other
        lay1 = QHBoxLayout()
        lay1.addWidget(wales_group_top)
        lay1.addWidget(wales_group_bottom)

        # Create a page indicator
        page_label = QLabel("4/5")
        page_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2d3436;")
        page_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(country)
        layout.addLayout(lay1)
        layout.addWidget(page_label)
        layout.addStretch(1)
    
        self.stack4.setLayout(layout)

    def niUI(self):
        """UI for Northern Ireland""" 
        layout = QVBoxLayout()
        country = QLabel("Northern Ireland")
        country.setStyleSheet("font-weight: bold; font-size: 18px; color: #2d3436; margin-bottom: 10px; border-radius: 5px; background-color: #dfe6e9; padding: 5px;")
        ni_grid_top = QGridLayout()
        # Reduce space between labels and combo box columns
        ni_grid_top.setHorizontalSpacing(20)
        ni_grid_top.setVerticalSpacing(6)
        ni_grid_top.setRowStretch(0, 1)
        # Align the labels to the right
        ni_grid_top.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ni_grid_bottom = QGridLayout()
        # Reduce space between labels and combo box columns
        ni_grid_bottom.setHorizontalSpacing(20)
        ni_grid_bottom.setVerticalSpacing(6)
        ni_grid_bottom.setRowStretch(0, 1)
        # Align the labels to the right
        ni_grid_bottom.setAlignment(Qt.AlignmentFlag.AlignCenter)


        car_top = QLabel("Car %")
        car_top.setStyleSheet("font-size: 14px; color: #2d3436")
        taxi_top = QLabel("Taxi %")
        taxi_top.setStyleSheet("font-size: 14px; color: #2d3436")
        bus_top = QLabel("Bus %")
        bus_top.setStyleSheet("font-size: 14px; color: #2d3436")
        walk_top = QLabel("Walk %")
        walk_top.setStyleSheet("font-size: 14px; color: #2d3436")

        car_bottom = QLabel("Car %")
        car_bottom.setStyleSheet("font-size: 14px; color: #2d3436")
        taxi_bottom = QLabel("Taxi %")
        taxi_bottom.setStyleSheet("font-size: 14px; color: #2d3436")
        bus_bottom = QLabel("Bus %")
        bus_bottom.setStyleSheet("font-size: 14px; color: #2d3436")
        walk_bottom = QLabel("Walk %")
        walk_bottom.setStyleSheet("font-size: 14px; color: #2d3436")
      
        # Combo boxes for left side
        self.ni_car_box_top = QComboBox()
        self.ni_taxi_box_top = QComboBox()
        self.ni_bus_box_top = QComboBox()
        self.ni_walk_box_top = QComboBox()

        # Combo boxes for right side
        self.ni_car_box_bottom = QComboBox()
        self.ni_taxi_box_bottom = QComboBox()
        self.ni_bus_box_bottom = QComboBox()
        self.ni_walk_box_bottom = QComboBox()
        
        self.ni_combos = {'car_land': self.ni_car_box_top, 'taxi_land': self.ni_taxi_box_top, 'bus_land': self.ni_bus_box_top,
                                'walk_land': self.ni_walk_box_top, 'car_air': self.ni_car_box_bottom, 'taxi_air': self.ni_taxi_box_bottom,
                                'bus_air': self.ni_bus_box_bottom, 'walk_air': self.ni_walk_box_bottom}
        
        # Dictionary to be used for percentage counters
        self.ni_combos1 = {'car_land': self.ni_car_box_top, 'taxi_land': self.ni_taxi_box_top, 'bus_land': self.ni_bus_box_top, 'walk_land': self.ni_walk_box_top}
        self.ni_combos2 = {'car_air': self.ni_car_box_bottom, 'taxi_air': self.ni_taxi_box_bottom, 'bus_air': self.ni_bus_box_bottom, 'walk_air': self.ni_walk_box_bottom}


        # Values for combo boxes
        values = [str(i) for i in range(101)]
        # Add % string to the end of each value
        for key, combo_box in self.ni_combos.items():
            combo_box.addItems(values)
            # Set fixed width
            combo_box.setFixedSize(QSize(50, 20))

        # Left side
        ni_grid_top.addWidget(car_top, 0, 0)
        ni_grid_top.addWidget(taxi_top, 1, 0)
        ni_grid_top.addWidget(bus_top, 2, 0)
        ni_grid_top.addWidget(walk_top, 3, 0)
        ni_grid_top.addWidget(self.ni_car_box_top, 0, 1)
        ni_grid_top.addWidget(self.ni_taxi_box_top, 1, 1)
        ni_grid_top.addWidget(self.ni_bus_box_top, 2, 1)
        ni_grid_top.addWidget(self.ni_walk_box_top, 3, 1)

        # Label to show selected percentatges for left side
        self.ni_select1 = 0
        self.percent_ni_label1 = QLabel(f"Selected: {self.ni_select1}%")
        self.percent_ni_label1.setStyleSheet("font-size: 14px; color: #2d3436; font: bold")
        ni_grid_top.addWidget(self.percent_ni_label1, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        # Right side
        ni_grid_bottom.addWidget(car_bottom, 0, 0)
        ni_grid_bottom.addWidget(taxi_bottom, 1, 0)
        ni_grid_bottom.addWidget(bus_bottom, 2, 0)
        ni_grid_bottom.addWidget(walk_bottom, 3, 0)
        ni_grid_bottom.addWidget(self.ni_car_box_bottom, 0, 1)
        ni_grid_bottom.addWidget(self.ni_taxi_box_bottom, 1, 1)
        ni_grid_bottom.addWidget(self.ni_bus_box_bottom, 2, 1)
        ni_grid_bottom.addWidget(self.ni_walk_box_bottom, 3, 1)

        # Label to show selected percentatges for right side
        self.ni_select2 = 0
        self.percent_ni_label2 = QLabel(f"Selected: {self.ni_select2}%")
        self.percent_ni_label2.setStyleSheet("font-size: 14px; color: #2d3436; font: bold")
        ni_grid_bottom.addWidget(self.percent_ni_label2, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        # Create a group box for the grid layout
        ni_group_top = QGroupBox("Journey from bus/rail station to university.")
        ni_group_top.setStyleSheet("font-size: 14px")
        ni_group_top.setLayout(ni_grid_top)

        # Create a group box for the grid layout
        ni_group_bottom = QGroupBox("Journey from airport to university.")
        ni_group_bottom.setStyleSheet("font-size: 14px")
        ni_group_bottom.setLayout(ni_grid_bottom)

        # Adjust the sizes of the grids and group boxes to fit the window
        ni_group_top.setFixedSize(300, 200)
        ni_group_bottom.setFixedSize(300, 200)

        # Put the group boxes next to each other
        lay1 = QHBoxLayout()
        lay1.addWidget(ni_group_top)
        lay1.addWidget(ni_group_bottom)

        # Create a page indicator
        page_label = QLabel("5/5")
        page_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2d3436;")
        page_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(country)
        layout.addLayout(lay1)
        layout.addWidget(page_label)
        layout.addStretch(1)
        self.stack5.setLayout(layout)

    def display(self, i):
        self.Stack.setCurrentIndex(i)

    def extract_percentages(self):
        """Extract the percentages from the combo boxes and put them in a dictionary"""
        scot = {key: int(combo_box.currentText()) for key, combo_box in self.scot_combos.items()}
        eng = {key: int(combo_box.currentText()) for key, combo_box in self.eng_combos.items()}
        wales = {key: int(combo_box.currentText()) for key, combo_box in self.wales_combos.items()}
        ni = {key: int(combo_box.currentText()) for key, combo_box in self.ni_combos.items()}
        abe = {key: int(combo_box.currentText()) for key, combo_box in self.aberdeen_combos.items()}
        return scot, eng, wales, ni, abe
    
    def enable_page3(self, hundred_percent_page3):
        """Enable the result button if you get signal on page3"""
        if hundred_percent_page3:
            self.calculate_button.setEnabled(True)
        else:
            self.calculate_button.setEnabled(False)

    def get_combo_values(self, combo_dict: dict, country_select, country_label):
        """Get the changed index of the combo boxes and call method to update the selected percentage label"""
        for key, combo_box in combo_dict.items():
            # Connect each combo box to the update_percent_label function
            combo_box.currentIndexChanged.connect(lambda: self.update_percent_label(combo_dict, country_select, country_label))     


    def update_percent_label(self, combo_dict: dict, country_select, country_label):
        """Sum percentages of combo boxes and update the label accordingly"""
        sum_percent = 0
        for combo_box in combo_dict.values():
            # Get the current value of a combo box
            country = int(combo_box.currentText())
            # Add it to the total sum of the combo boxes in that dict
            sum_percent += country
            
        # Country select variable = sum_percent
        country_select = sum_percent
        if sum_percent > 100:
            country_label.setStyleSheet("font-size: 14px; color: red; font: bold")
        elif sum_percent == 100:
            country_label.setStyleSheet("font-size: 14px; color: green; font: bold")
        else:
            country_label.setStyleSheet("font-size: 14px; color: #2d3436; font: bold")

        # Set the country 'Selected' label represent the sum of percentages among combo boxes
        country_label.setText(f"Selected: {country_select}%")