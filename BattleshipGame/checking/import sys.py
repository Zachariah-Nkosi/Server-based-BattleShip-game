import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set the background image
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("battle.jpg")))
        self.setPalette(palette)

        # Add a button to change the color
        self.button = QPushButton("Change color", self)
        self.button.setGeometry(QRect(10, 10, 100, 30))
        self.button.setStyleSheet("background-color: #3C3C3C; color: #FFFFFF; border-radius: 5px;")
        self.button.clicked.connect(self.changeColor)

        self.show()

    def changeColor(self):
        # Generate a random color that doesn't hide the background image
        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 127)

        # Set the new color for the frame and button
        self.setStyleSheet(f"QMainWindow {{border: 10px solid {color.darker(150).name()};}}")
       

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
