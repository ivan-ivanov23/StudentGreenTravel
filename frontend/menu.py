import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QTableView
from PyQt6.QtCore import QSize



class WelcomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: rgb(193, 225, 193);")

        self.title_label = QLabel("Welcome to StudentCarbon", self)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2d3436;")

        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(QPushButton("Page 1", clicked=lambda: self.show_page(Page1())))
        self.button_layout.addWidget(QPushButton("Page 2", clicked=lambda: self.show_page(Page2())))
        self.button_layout.addWidget(QPushButton("Page 3", clicked=lambda: self.show_page(Page3())))

        self.main_layout = QVBoxLayout()
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
        self.label = QLabel("This is Page 1", self)
        self.back_button = QPushButton("Back to Menu", clicked=self.back_to_menu)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.back_button)



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
        self.setMinimumSize(QSize(600, 400))
        # Max size is size of screen, so no need to set

        self.central_widget = WelcomePage()
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
