import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget

# class Test(QWidget):

#     def __init__(self):
#         super().__init__()
#         self.initializeUI()


#     def initializeUI(self):
#         """Set up application GUI"""
#         self.setFixedSize(800, 600)
#         self.setWindowTitle("StudentGreenTravel")

#         # Button
#         self.button = QPushButton("Click me")

#         self.stack1 = QWidget()
#         #self.stack2 = QHBoxLayout()
            
#         self.stack1UI()
#         #self.stack2UI()

#         self.Stack = QStackedWidget(self)
#         self.Stack.addWidget(self.stack1)
#         #self.Stack.addWidget(self.stack2)

#         hbox = QHBoxLayout(self)
#         hbox.addWidget(self.button)
#         hbox.addWidget(self.Stack)

#         self.setLayout(hbox)
#         self.button.clicked.connect(self.display)

#         self.show()

#     def stack1UI(self):
#         #button1 = QPushButton("Bip")
#         layout = QHBoxLayout()
#         #layout.addWidget(button1)
#         self.stack1.setLayout(layout)

#     def display(self, i):
#         self.Stack.setCurrentIndex(i)

# app = QApplication(sys.argv)
# window = Test()
# app.exec()

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QStackedWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Two Pages Example")
        self.setGeometry(100, 100, 400, 300)

        # Create stacked widget and its pages
        self.stacked_widget = QStackedWidget()
        self.page1 = QWidget()
        self.page2 = QWidget()
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)

        # Create layouts for pages
        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        self.page1.setLayout(self.layout1)
        self.page2.setLayout(self.layout2)

        # Create buttons for each page
        self.button1 = QPushButton("Go to Page 2")
        self.button2 = QPushButton("Go to Page 1")

        # Add buttons to layouts
        self.layout1.addWidget(self.button1)
        self.layout2.addWidget(self.button2)

        # Connect button signals to page switching functions
        self.button1.clicked.connect(self.switch_to_page2)
        self.button2.clicked.connect(self.switch_to_page1)

        # Set central widget as stacked widget
        self.setCentralWidget(self.stacked_widget)

    def switch_to_page1(self):
        self.stacked_widget.setCurrentIndex(0)

    def switch_to_page2(self):
        self.stacked_widget.setCurrentIndex(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
