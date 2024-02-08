import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QTableView 
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QLineEdit
from PyQt6.QtCore import Qt
from main import main



class WelcomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: rgb(193, 225, 193);")

        self.title_label = QLabel("Welcome to StudentCarbon", self)
        self.title_label.setStyleSheet("font-size: 34px; font-weight: bold; color: #2d3436;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(QPushButton("Emission Calculator", clicked=lambda: self.show_page(Page1())))
        self.button_layout.addWidget(QPushButton("Display Routes", clicked=lambda: self.show_page(Page2())))
        self.button_layout.addWidget(QPushButton("Statistics", clicked=lambda: self.show_page(Page3())))
        # Make the buttons fixed size
        for i in range(self.button_layout.count()):
            self.button_layout.itemAt(i).widget().setFixedHeight(60)
            self. button_layout.itemAt(i).widget().setFixedWidth(300)

        # Center the buttons
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout = QVBoxLayout()
        # Add margins to the layout
        self.main_layout.setContentsMargins(100, 150, 100, 150)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)


        # Set the stylesheet for the welcome page buttons
        self.setStyleSheet("""
            QPushButton {
                background-color: #0984e3;
                color: #ffffff;
                font-weight: bold;
                height: 40px;
                border: none;
                border-radius: 5px;
                margin: 5px 0;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #74b9ff;
            }
        """)

    def show_page(self, page):
        self.parent().setCentralWidget(page)


class Page1(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Emissions Calculator")
        self.setGeometry(100, 100, 800, 600)
        self.back_button = QPushButton("Back to Menu", clicked=self.back_to_menu)
        # create clear button that will clear the table
        self.clear_button = QPushButton("Clear", clicked=self.clear_table)
        # Add search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search for a postcode")
        self.search_bar.setFixedHeight(40)
        self.search_bar.setFixedWidth(200)
        self.search_bar.setStyleSheet("border: 1px solid black; border-radius: 5px; padding: 5px;")
        self.search_bar.textChanged.connect(self.search_table)


        self.setLayout(QVBoxLayout())
        

        self.button = QPushButton("Calculate Emissions")
        self.button.clicked.connect(self.calculate_emissions)
        self.layout().addWidget(self.button)
        self.layout().addWidget(self.search_bar)

        self.table = QTableWidget()
        # Make it non-editable 
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # Set the table to stretch to the size of the window
        self.table.horizontalHeader().setStretchLastSection(True)
        # Pad the table with some space
        self.table.setContentsMargins(10, 10, 10, 10)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Postcode", "Emissions"])
        # Set the headers to stretch to the size of the window and be bold
        self.table.horizontalHeader().setStyleSheet("font-weight: bold;")
        # Add borders to the table
        self.table.setStyleSheet("border: 1px solid black;")
        # make the index column a bit wider
        self.table.verticalHeader().setMinimumWidth(50)
        self.layout().addWidget(self.table)
        self.layout().addWidget(self.back_button)
        # Add the clear button to the layout next to the back button
        self.layout().addWidget(self.clear_button)
        # Make the back button and clear button be smaller and be next to each other
        self.back_button.setFixedWidth(100)
        self.clear_button.setFixedWidth(100)
        self.back_button.setFixedHeight(40)
        self.clear_button.setFixedHeight(40)


        # Style the buttons
        self.setStyleSheet("""
            QPushButton {
                background-color: #0984e3;
                color: #ffffff;
                font-weight: bold;
                height: 40px;
                border: none;
                border-radius: 5px;
                margin: 5px 0;
            }
            QPushButton:hover {
                background-color: #74b9ff;
            }
        """)

    def search_table(self):
        # Get the text from the search bar
        text = self.search_bar.text()
        # If the text is empty, then show all the rows
        if text == "":
            for i in range(self.table.rowCount()):
                self.table.setRowHidden(i, False)
        else:
            # If the text is not empty, then hide all the rows that don't contain the text
            for i in range(self.table.rowCount()):
                if text.lower() in self.table.item(i, 0).text().lower():
                    self.table.setRowHidden(i, False)
                else:
                    self.table.setRowHidden(i, True)


    def clear_table(self):
        self.table.clearContents()
        # reset the table to have no rows
        self.table.setRowCount(0)

    def calculate_emissions(self):
        bus, plane = main()
        total_rows = len(bus) + len(plane)
        self.table.setRowCount(total_rows)
        
        for i, (postcode, emissions) in enumerate(bus.values):
            self.table.setItem(i, 0, QTableWidgetItem(postcode))
            self.table.setItem(i, 1, QTableWidgetItem(str(emissions)))

        for i, (postcode, emissions) in enumerate(plane.values):
            self.table.setItem(i + len(bus), 0, QTableWidgetItem(postcode))
            self.table.setItem(i + len(bus), 1, QTableWidgetItem(str(emissions)))

        self.table.sortItems(1, Qt.SortOrder.DescendingOrder)



    def back_to_menu(self):
        self.parent().setCentralWidget(WelcomePage())


class Page2(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("This is Page 2", self)
        self.back_button = QPushButton("Back to Menu", clicked=self.back_to_menu)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.back_button)

    def back_to_menu(self):
        self.parent().setCentralWidget(WelcomePage())


class Page3(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("This is Page 3", self)
        self.back_button = QPushButton("Back to Menu", clicked=self.back_to_menu)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.back_button)

    def back_to_menu(self):
        self.parent().setCentralWidget(WelcomePage())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StudentCarbon: Domestic Relocation Emissions Estimator")
        self.setMinimumSize(QSize(800, 600))
        # Max size is size of screen, so no need to set

        self.central_widget = WelcomePage()
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
