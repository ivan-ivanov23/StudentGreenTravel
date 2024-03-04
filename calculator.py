import sys
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QStackedLayout, QMessageBox, QHBoxLayout, QProgressDialog, QProgressBar
from PyQt6.QtCore import pyqtSignal
from PyQt6 import QtCore
from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon
from tkinter.filedialog import askopenfile
import pandas as pd
from preprocess_data import determine_postcode, divide_scot_addresses, divide_uk_addresses
from final_leg import assign_scotland, assign_uk
from page1 import MainPage
from page2 import Page2
from page3 import Page3
from results_page import ResultPage
from main import main
import plotly.express as px
from council_areas import get_district, group_district, find_percentage

"""
Info:

- main page is the menu that is first shown (page1)
- page2 is the second page where the user selects the percentages of students travelling by each transport method
  for Scotland and the rest of the UK
- page3 is the third page where the user selects the travel assumptions for the final leg of the journey 
  from Aberdeen transport hub to the University of Aberdeen
- page4 is the final page where the user can see the results of the calculations in the form of heatmaps and pie charts

"""

class Calculator(QWidget):

    file_selected = pyqtSignal(bool)
    hundred_percent = pyqtSignal(bool)
    hundred_percent_page3 = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.initializeUI()
        self.scotland = None
        self.wales = None
        self.north_ireland = None
        self.england = None

    def initializeUI(self):
        """Set up application GUI"""
        self.setMinimumSize(1000, 600)
        self.setWindowTitle("StudentGreenTravel")
        main_icon = QIcon('icons/eco.svg')
        self.setWindowIcon(main_icon)


        # Layouts for pages
        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        self.layout3 = QVBoxLayout()
        self.layout4 = QHBoxLayout()

        # Stacked layout to hold the pages
        # Source: https://www.tutorialspoint.com/pyqt/pyqt_qstackedwidget.htm 
        self.stackedLayout = QStackedLayout()

        # Create the pages
        self.page1 = MainPage()
        self.page2 = Page2()
        self.page3 = Page3()
        self.page4 = ResultPage()

        # Add the pages to the stacked layout and set the stacked layout as the main layout
        self.stackedLayout.addWidget(self.page1)
        self.stackedLayout.addWidget(self.page2)
        self.stackedLayout.addWidget(self.page3)
        self.stackedLayout.addWidget(self.page4)

        self.setLayout(self.stackedLayout)

        # Connect signals for page1
        self.page1.button1.clicked.connect(self.go_to_page2)
        self.page1.button2.clicked.connect(self.open_file)
        self.file_selected.connect(self.page1.enable_buttons1)

        # Connect signals for page2
        self.page2.next_button2.clicked.connect(self.go_to_page3)
        self.page2.submit.clicked.connect(self.check_combo_page2)
        self.page2.back.clicked.connect(self.go_to_page1)
        self.hundred_percent.connect(self.page2.enable_page2)

        # Connect signals for page3
        self.page3.back.clicked.connect(self.go_to_page2)
        self.page3.calculate_button.clicked.connect(self.go_to_results)
        self.hundred_percent_page3.connect(self.page3.enable_page3)
        self.page3.submit.clicked.connect(self.check_combo_page3)

        # Connect signals for page4
        self.page4.button1.clicked.connect(self.go_to_page3)
        self.page4.button2.clicked.connect(self.go_to_page1)
        self.page4.radio1.clicked.connect(self.click_radio1)
        self.page4.radio2.clicked.connect(self.click_radio2)
        self.page4.radio3.clicked.connect(self.click_radio3)
        self.page4.radio4.clicked.connect(self.click_radio4)
        self.page4.radio5.clicked.connect(self.click_radio5)
        self.page4.radio6.clicked.connect(self.click_radio6)
        self.page4.radio7.clicked.connect(self.click_radio7)
        self.page4.radio8.clicked.connect(self.click_radio8)
    

        # Set style for the widgets in the application
        self.setStyleSheet("font-size: 12px; font-weight: bold; color: #2d3436;")

        # Set style for all QButtons in the application so that they are bigger and have a greenish color
        self.setStyleSheet(
            "QPushButton {"
            "background-color: #A1FA80;"
            "border: none;"
            "color: #2d3436;"
            "padding: 10px 10px;"
            "text-align: center;"
            "text-decoration: none;"
            "font-size: 16px;"
            "margin: 4px 2px;"
            "border-radius: 12px;"
            "}"

            "QPushButton:hover {"
            "background-color: #00b894;"
            "}"

            "QPushButton:disabled {"
            "background-color: #dfe6e9;"
            "}"

            "QComboBox {"
            "font-size: 12px;"
            "color: #2d3436;"
            "}"

            "QLineEdit {"
            "font-size: 12px;"
            "color: #2d3436;"
            "}"

            "QGroupBox {"
            "font-size: 12px;"
            "font-weight: bold;"
            "color: #2d3436;"
            "border-radius: 5px;"
            "background-color: #dfe6e9;"
            "padding: 5px;"
            "margin-bottom: 10px;"
            "margin-top: 15px;"
            "}"

            "QGroupBox::title {"
            "subcontrol-origin: margin;"
            "padding: 0 3px;"
            "}"

            "QRadioButton {"
            "font-size: 12px;"
            "color: #2d3436;"
            "}"

            "QRadioButton::indicator:checked {"
            "background-color: #64C540;"
            "border: 1px solid #64C540;"
            "border-radius: 6px;"
            "}"

            "QWebEngineView {"
            "background-color: #dfe6e9;"
            "}"
            """

        """)

        # Get icons from StandardPixmap
        # Source: https://www.svgrepo.com/
        calculate_icon = QIcon('icons/calculator.svg')
        back = QIcon('icons/back.svg')
        submit = QIcon('icons/submit.svg')
        next_button = QIcon('icons/next.svg')
        file_button = QIcon('icons/file.svg')
        dash = QIcon('icons/dash.svg')
        menu = QIcon('icons/menu.svg')

        # Set the icon for all the back buttons
        self.page1.button1.setIcon(dash)
        self.page1.button2.setIcon(file_button)
        self.page2.back.setIcon(back)
        self.page3.back.setIcon(back)
        self.page4.button1.setIcon(back)
        self.page4.button2.setIcon(menu)
        # Set the icon for the calculate button from images/calculator.png
        
        self.page3.calculate_button.setIcon(calculate_icon)
        # Set the icon for the submit button
        self.page2.submit.setIcon(submit)
        self.page3.submit.setIcon(submit)
        # Set the icon for the next button
        self.page2.next_button2.setIcon(next_button)


        # Show the application
        self.show()

    """==============================================Methods for pages=============================================="""
    def open_file(self):
        file = askopenfile(filetypes=[("Excel files", "*.xlsx")])
        # If the user selected a file, then read it using pandas
        if file:
        # Read address file
            addresses = pd.read_excel(file.name, engine='openpyxl')
            addresses.iloc[:, 1] = addresses.iloc[:, 1].str.replace(' ', '')
            # Add the file name to the label text with the file name withouth the path
            self.page1.file_label.setText(f"File: {file.name.split('/')[-1]}")
            self.scotland, self.wales, self.north_ireland, self.england = determine_postcode(addresses.iloc[:, 1])
            # Style the label
            #self.file_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #2d3436;")
            # Emit signal that a file has been selected
            self.file_selected.emit(True)
        else:
            self.page1.file_label.setText("No file was selected.")
            # Emit a signal that a file has not been selected
            self.file_selected.emit(False)


    def go_to_page1(self):
        self.stackedLayout.setCurrentIndex(0)
    
    def go_to_page2(self):
        self.stackedLayout.setCurrentIndex(1)

    def go_to_page3(self):
        self.stackedLayout.setCurrentIndex(2)

    def go_to_page4(self):
        self.stackedLayout.setCurrentIndex(3)


    def check_combo_page2(self):
        """Check if the sum of the percentages for each country is 100. 
        If it is, then call the menu function. 
        If not, show a message box with an error.""" 
        # Get the percentages for each country
        scot_car = int(self.page2.combo_car_scot.currentText())
        scot_bus = int(self.page2.combo_bus_scot.currentText())
        scot_rail = int(self.page2.combo_rail_scot.currentText())
        uk_plane = int(self.page2.plane_uk.currentText())
        uk_car = int(self.page2.car_uk.currentText())
        uk_rail = int(self.page2.rail_uk.currentText())

        # Sum the percentages for each country
        scot_sum = sum([scot_car, scot_bus, scot_rail])
        uk_sum = sum([uk_plane, uk_car, uk_rail])

        if scot_sum == 100 and uk_sum == 100:
            # Show a message that the data has been submitted
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            success = QIcon('icons/success.svg')
            msg.setWindowIcon(success)
            msg.setText("The data has been submitted!")
            # Add a success icon to the message box
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
            # take the returns from the file explorer function without running it again
            scotland, wales, north_ireland, england = self.get_country_data()
            self.hundred_percent.emit(True)
            # call the divide_address functions for each country
            self.travel_scotland = divide_scot_addresses(scotland, scot_bus, scot_car, scot_rail)
            self.travel_england = divide_uk_addresses(england, uk_plane, uk_car, uk_rail)
            self.travel_wales = divide_uk_addresses(wales, uk_plane, uk_car, uk_rail)
            self.travel_ni = divide_uk_addresses(north_ireland, uk_plane, uk_car, uk_rail)

        else:
            self.hundred_percent.emit(False)
            # Show a message box with the error
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            warning = QIcon('icons/warning.svg')
            msg.setWindowIcon(warning)
            msg.setText("The sum of the percentages for each country must be 100!\nPlease try again.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()

    def get_country_data(self):
        """Return the data from the file explorer function"""
        return self.scotland, self.wales, self.north_ireland, self.england
    
    
    def check_combo_page3(self):
        """Check if the sum of the percentages for each country is 100. If it is, then call the menu function. If not, show a message box with an error.""" 
        # call extract function from page3 to get the percentages for each country
        scot, eng, wales, ni = self.page3.extract_percentages()
        # Divide the percentages into lists for each country
        scot = [int(i) for key, i in scot.items()]
        # [:4] for land and [4:] for air transport
        eng_land = [int(i) for key, i in eng.items()][:4]
        eng_air = [int(i) for key, i in eng.items()][4:]
        wales_land = [int(i) for key, i in wales.items()][:4]
        wales_air = [int(i) for key, i in wales.items()][4:]
        ni_land = [int(i) for key, i in ni.items()][:4]
        ni_air = [int(i) for key, i in ni.items()][4:]

        # Sum of all
        sum_all = sum(scot) + sum(eng_land) + sum(eng_air) + sum(wales_land) + sum(wales_air) + sum(ni_land) + sum(ni_air)

        # If the sum of the percentages for each country is 700 (7 elements * 100), then call the menu function.
        if sum_all == 700:
            # Show a message that the data has been submitted
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            success = QIcon('icons/success.svg')
            msg.setWindowIcon(success)
            msg.setText("The data has been submitted!")
            # Add a success icon to the message box
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
            self.hundred_percent_page3.emit(True)
            # Combine the bus and rail postcodes for Scotland in a list to be used in the final leg function
            scot_bus_rail = self.travel_scotland[0] + self.travel_scotland[2]
            # Call the select_country function
            # Scotland
            self.scot_fleg = assign_scotland(scot_bus_rail, scot[0], scot[1], scot[2], scot[3])

            # England
            eng_rail = self.travel_england[2]
            eng_plane = self.travel_england[0]
            self.eng_fleg_bus_rail, self.eng_fleg_plane = assign_uk(eng_rail, eng_plane, eng_land[0], eng_land[1], eng_land[2], eng_land[3], eng_air[0], eng_air[1], eng_air[2], eng_air[3])
            # Wales
            wales_rail = self.travel_wales[2]
            wales_plane = self.travel_wales[0]
            self.wales_fleg_bus_rail, self.wales_fleg_plane = assign_uk(wales_rail, wales_plane, wales_land[0], wales_land[1], wales_land[2], wales_land[3], wales_air[0], wales_air[1], wales_air[2], wales_air[3])

            # Northern Ireland
            ni_rail = self.travel_ni[2]
            ni_plane = self.travel_ni[0]
            self.ni_fleg_bus_rail, self.ni_fleg_plane = assign_uk(ni_rail, ni_plane, ni_land[0], ni_land[1], ni_land[2], ni_land[3], ni_air[0], ni_air[1], ni_air[2], ni_air[3])

        else:
            self.hundred_percent_page3.emit(False)
            # Show a message box with the error
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            warning = QIcon('icons/warning.svg')
            msg.setWindowIcon(warning)
            msg.setText("The sum of the percentages for each country must be 100!\nPlease try again.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()


    def go_to_results(self):
        """Extract the final leg of the journey for each country"""
        # Crate a progress dialog
        pdg = QProgressDialog()
        pdg.setWindowTitle("Calculating")
        pdg.setLabelText("Please wait while distances and emissions are processed...")
        loading_icon = QIcon('icons/loading.svg')
        pdg.setWindowIcon(loading_icon)
        self.pbar = QProgressBar()
        pdg.setBar(self.pbar)
        pdg.setMinimum(0)
        pdg.setMaximum(100)
        pdg.show()

        self.pbar.setValue(0)
        QtWidgets.QApplication.processEvents()

        self.stackedLayout.setCurrentIndex(3)
        # Scotland
        scot_car_fleg = self.scot_fleg[0]
        scot_taxi_fleg = self.scot_fleg[1]
        scot_bus_fleg = self.scot_fleg[2]
        scot_walk_fleg = self.scot_fleg[3]

        # England
        eng_car_fleg = self.eng_fleg_bus_rail[0] + self.eng_fleg_plane[0]
        eng_taxi_fleg = self.eng_fleg_bus_rail[1] + self.eng_fleg_plane[1]
        eng_bus_fleg = self.eng_fleg_bus_rail[2] + self.eng_fleg_plane[2]
        eng_walk_fleg = self.eng_fleg_bus_rail[3] + self.eng_fleg_plane[3]

        # Wales
        wales_car_fleg = self.wales_fleg_bus_rail[0] + self.wales_fleg_plane[0]
        wales_taxi_fleg = self.wales_fleg_bus_rail[1] + self.wales_fleg_plane[1]
        wales_bus_fleg = self.wales_fleg_bus_rail[2] + self.wales_fleg_plane[2]
        wales_walk_fleg = self.wales_fleg_bus_rail[3] + self.wales_fleg_plane[3]

        # Northern Ireland
        ni_car_fleg = self.ni_fleg_bus_rail[0] + self.ni_fleg_plane[0]
        ni_taxi_fleg = self.ni_fleg_bus_rail[1] + self.ni_fleg_plane[1]
        ni_bus_fleg = self.ni_fleg_bus_rail[2] + self.ni_fleg_plane[2]
        ni_walk_fleg = self.ni_fleg_bus_rail[3] + self.ni_fleg_plane[3]

        # Update the progress bar
        self.pbar.setValue(25)
        # This is necessary for showing and updating the progress bar
        # Source: https://stackoverflow.com/questions/30823863/pyqt-progress-bar-not-updating-or-appearing-until-100
        QtWidgets.QApplication.processEvents()

        # Call the main function
        self.emissions, self.distances, self.total_emissions, self.total_distance_dict = main(self.travel_scotland, self.travel_england, self.travel_wales, self.travel_ni, scot_car_fleg, scot_taxi_fleg, scot_bus_fleg, scot_walk_fleg, eng_car_fleg, eng_taxi_fleg, eng_bus_fleg, eng_walk_fleg, wales_car_fleg, wales_taxi_fleg, wales_bus_fleg, wales_walk_fleg, ni_car_fleg, ni_taxi_fleg, ni_bus_fleg, ni_walk_fleg)
        # Update the progress bar
        self.pbar.setValue(50)
        QtWidgets.QApplication.processEvents()


        # Create piechart for council areas
        scot_dict = self.create_council_areas()

        # # Create a dataframe with the distances for each mode of transport for Scotland
        df = pd.DataFrame(scot_dict)
        df = df.round(1)
        areas = df.columns
        car_values = df.loc['Car', :]
        bus_values = df.loc['Bus', :]
        rail_values = df.loc['Rail', :]
        taxi_values = df.loc['Taxi', :]

        labels = {'x': 'Council Area', 'y': 'Distance (km)'}
        



        # # Bar chart for the car distances by council area
        self.scot_car = px.bar(df, x=areas, y=car_values, title='Car Distance by Council Area (in km)', labels=labels)
        # # Show distance values on the bars
        # # self.scot_car.update_traces(texttemplate='%{y}', textposition='outside')

        # # do this for bus, rail and taxi
        self.scot_bus = px.bar(df, x=areas, y=bus_values, title='Bus Distance by Council Area (in km)', labels=labels)


        self.scot_rail = px.bar(df, x=areas, y=rail_values, title='Rail Distance by Council Area (in km)', labels=labels)

        self.scot_taxi = px.bar(df, x=areas, y=taxi_values, title='Taxi Distance by Council Area (in km)', labels=labels)

        #self.scot_car = px.bar(scot_dict, x=scot_dict.keys(), y=[i['Car'] for i in scot_dict.values()], title='Car Distance by Council Area (in km)', labels=dict(x="Council Area", y="Distance (km)"))

        #Update the progress bar
        self.pbar.setValue(100)
        QtWidgets.QApplication.processEvents()
        pdg.close()
        
    def click_radio1(self):
        """Set the webview to show the first heatmap with the emissions data"""
        # Create the heatmaps
        df = self.emissions
        # Exclude the Walk values
        df = df.drop('Walk', axis=0)
        # Round the values to 2 decimal places
        df = df.round(0)
        # Source: https://plotly.com/python/heatmaps/
        # Figure to store the heatmap with the emissions
        self.fig1 = px.imshow(df, text_auto=True, aspect='auto', title='Total Emissions (kgCO2e) by Country and Mode of Transport',
                        labels=dict(x="Country", y="Transport", color="Emissions (kgCO2e)"),
                        color_continuous_scale='bupu')

        # Edit the font size and color of the values
        self.fig1.update_traces(textfont_size=16)
        # Source: https://zetcode.com/pyqt/qwebengineview/
        self.page4.webview.setHtml(self.fig1.to_html(include_plotlyjs='cdn'))

    def click_radio2(self):
        """Set the webview to show the second heatmap with the distances data"""
        # Do the same for the distances
        df = self.distances
        df = df.round(0)
        # Figure to store the heatmap with the distances
        self.fig2 = px.imshow(df, text_auto=True, aspect='auto', title='Total Distance (km) by Country and Mode of Transport',
                        labels=dict(x="Country", y="Transport", color="Distance (km)"),
                        color_continuous_scale='bugn')
        
        self.fig2.update_traces(textfont_size=16)
        # Source: https://zetcode.com/pyqt/qwebengineview/
        self.page4.webview.setHtml(self.fig2.to_html(include_plotlyjs='cdn'))

    def click_radio3(self):
        """Set the webview to show the pie chart with the total emissions data"""
         # Pie chart for the total emissions
        # Source: https://plotly.com/python/pie-charts/
        df = self.total_emissions
        df = df.round(0)
        # take names from columns
        names = df.columns
        # Values are the second row
        values = df.iloc[0, :]
        # Figure to store the pie chart with the total emissions
        self.fig3 = px.pie(df, values=values, names=names, title='Total Emissions by Country (in kgCO2e)', labels=dict(names="Country", values="Emissions (kgCO2e)"))
        # Edit the font size and color of the values
        self.fig3.update_traces(textfont_size=16)
        # Source: https://zetcode.com/pyqt/qwebengineview/
        self.page4.webview.setHtml(self.fig3.to_html(include_plotlyjs='cdn'))

    def click_radio4(self):
        """Set the webview to show the pie chart with the emissions per student data"""
        # Pie chart for emissions per student by country
        df = self.total_emissions
        # Divide the total emissions by the number of students for each country
        scot_emissions = df.iloc[0, 0] / len(self.scotland)
        eng_emissions = df.iloc[0, 1] / len(self.england)
        wales_emissions = df.iloc[0, 2] / len(self.wales)
        ni_emissions = df.iloc[0, 3] / len(self.north_ireland)

        # Create a pie chart
        # Source: https://plotly.com/python/pie-charts/
        labels = ['Scotland', 'England', 'Wales', 'Northern Ireland']
        values = [scot_emissions, eng_emissions, wales_emissions, ni_emissions]
        # Round the values to 0 decimal places
        values = [round(i, 0) for i in values]
        # Figure to store the pie chart with the emissions per student
        self.fig4 = px.pie(values=values, names=labels, title='Emissions per Student by Country (in kgCO2e)', labels=dict(names="Country", values="Emissions (kgCO2e)"), color_discrete_sequence=px.colors.sequential.RdBu)
        # Edit the font size and color of the values
        self.fig4.update_traces(textfont_size=16)
        # Source: https://zetcode.com/pyqt/qwebengineview/
        self.page4.webview.setHtml(self.fig4.to_html(include_plotlyjs='cdn'))

    def click_radio5(self):
        """Set the webview to show the heatmap with the council areas data"""
        # Source: https://zetcode.com/pyqt/qwebengineview/
        self.page4.webview.setHtml(self.scot_car.to_html(include_plotlyjs='cdn'))

    def click_radio6(self):
        """Set the webview to show the heatmap with the bus distances data"""
        # Source: https://zetcode.com/pyqt/qwebengineview/
        self.page4.webview.setHtml(self.scot_bus.to_html(include_plotlyjs='cdn'))

    def click_radio7(self):
        """Set the webview to show the heatmap with the rail distances data"""
        # Source: https://zetcode.com/pyqt/qwebengineview/
        self.page4.webview.setHtml(self.scot_rail.to_html(include_plotlyjs='cdn'))

    def click_radio8(self):
        """Set the webview to show the heatmap with the taxi distances data"""
        # Source: https://zetcode.com/pyqt/qwebengineview/
        self.page4.webview.setHtml(self.scot_taxi.to_html(include_plotlyjs='cdn'))


    def create_council_areas(self):
        # Scotland
        self.scotland = self.scotland.to_list()
        scot_districts = get_district(self.scotland)
        #print(scot_districts)
        scot_grouped = group_district(scot_districts)
        scot_percent = find_percentage(scot_grouped, self.scotland)
        #print(scot_percent)


        # From self.total_distance_dict get the distances for Scotland
        scot_distances = self.total_distance_dict['Scotland']

        # Extract the distances for each mode of transport
        scot_car = scot_distances[3]
        scot_bus = scot_distances[2]
        scot_rail = scot_distances[0]
        scot_walk = scot_distances[5]
        scot_taxi = scot_distances[4]

        # Create a dict with the distances for each mode of transport for Scotland according to the admin district percentage
        scot_dict = {}
        for key, value in scot_percent.items():
            scot_dict[key] = {'Car': scot_car * value / 100, 'Bus': scot_bus * value / 100, 'Rail': scot_rail * value / 100, 'Taxi': scot_taxi * value / 100, 'Walk': scot_walk * value / 100}

        # Update the progress bar
        self.pbar.setValue(65)
        QtWidgets.QApplication.processEvents()

        # # England
        # eng_districts = get_district(self.england)
        # eng_grouped = group_district(eng_districts)
        # eng_percent = find_percentage(eng_grouped, self.england)

        # # From self.total_distance_dict get the distances for England
        # eng_distances = self.total_distance_dict['England']
        # # Extract the distances for each mode of transport
        # eng_car = eng_distances[3]
        # eng_bus = eng_distances[2]
        # eng_rail = eng_distances[0]
        # eng_walk = eng_distances[5]
        # eng_taxi = eng_distances[4]
        # eng_plane = eng_distances[1]

        # # Create a dict with the distances for each mode of transport for England according to the admin district percentage
        # eng_dict = {}
        # for key, value in eng_percent.items():
        #     eng_dict[key] = {'Car': eng_car * value, 'Bus': eng_bus * value, 'Rail': eng_rail * value, 'Taxi': eng_taxi * value, 'Walk': eng_walk * value, 'Plane': eng_plane * value}

        # self.pbar.setValue(75)
        # QtWidgets.QApplication.processEvents()

        # # Wales
        # wales_districts = get_district(self.wales)
        # wales_grouped = group_district(wales_districts)
        # wales_percent = find_percentage(wales_grouped, self.wales)

        # # From self.total_distance_dict get the distances for Wales
        # wales_distances = self.total_distance_dict['Wales']
        # # Extract the distances for each mode of transport
        # wales_car = wales_distances[3]
        # wales_bus = wales_distances[2]
        # wales_rail = wales_distances[0]
        # wales_walk = wales_distances[5]
        # wales_taxi = wales_distances[4]
        # wales_plane = wales_distances[1]

        # # Create a dict with the distances for each mode of transport for Wales according to the admin district percentage
        # wales_dict = {}
        # for key, value in wales_percent.items():
        #     wales_dict[key] = {'Car': wales_car * value, 'Bus': wales_bus * value, 'Rail': wales_rail * value, 'Taxi': wales_taxi * value, 'Walk': wales_walk * value, 'Plane': wales_plane * value}

        # self.pbar.setValue(85)
        # QtWidgets.QApplication.processEvents()

        # # Northern Ireland
        # ni_districts = get_district(self.north_ireland)
        # ni_grouped = group_district(ni_districts)
        # ni_percent = find_percentage(ni_grouped, self.north_ireland)

        # # From self.total_distance_dict get the distances for Northern Ireland
        # ni_distances = self.total_distance_dict['Northern Ireland']
        # # Extract the distances for each mode of transport
        # ni_car = ni_distances[3]
        # ni_bus = ni_distances[2]
        # ni_rail = ni_distances[0]
        # ni_walk = ni_distances[5]
        # ni_taxi = ni_distances[4]
        # ni_plane = ni_distances[1]

        # # Create a dict with the distances for each mode of transport for Northern Ireland according to the admin district percentage
        # ni_dict = {}
        # for key, value in ni_percent.items():
        #     ni_dict[key] = {'Car': ni_car * value, 'Bus': ni_bus * value, 'Rail': ni_rail * value, 'Taxi': ni_taxi * value, 'Walk': ni_walk * value, 'Plane': ni_plane * value}

        # self.pbar.setValue(90)
        # QtWidgets.QApplication.processEvents()

        return scot_dict#, eng_dict, wales_dict, ni_dict

        

"""==============================================Run the app=============================================="""
app = QApplication(sys.argv)
window = Calculator()
sys.exit(app.exec())
