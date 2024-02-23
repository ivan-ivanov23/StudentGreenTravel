from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QSize
import sys
from old_app.welcomepage import WelcomePage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StudentGreenTravel: Domestic Relocation Emissions Estimator")
        self.setMinimumSize(QSize(800, 600))
        # Max size is size of screen, so no need to set

        self.central_widget = WelcomePage()
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
