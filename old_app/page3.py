# from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget
# from welcomepage import WelcomePage

# class Page3(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.label = QLabel("This is Page 3", self)
#         self.back_button = QPushButton("Back to Menu", clicked=self.back_to_menu)
#         self.setLayout(QVBoxLayout())
#         self.layout().addWidget(self.label)
#         self.layout().addWidget(self.back_button)

#     def back_to_menu(self):
#         self.parent().setCentralWidget(WelcomePage())