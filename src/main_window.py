import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QRadioButton,
    QPushButton, QWidget, QMessageBox, QSpinBox, QLineEdit, QTableWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout
)
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('GameDecideApp')
        self.setWindowTitle("My App")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        layout.addStretch(1)


        self.label = QLabel('Choose the kind of problem', self.central_widget)
        self.label.setFont(QFont('Arial', 20))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        layout.addStretch(1)


        self.radio_uncertainty = QRadioButton('Decision making under uncertainty', self.central_widget)
        self.radio_risk = QRadioButton('Decision making under risk',self.central_widget)

        layout_radio = QVBoxLayout()
        layout_radio.addWidget(self.radio_uncertainty)
        layout_radio.addWidget(self.radio_risk)
        layout.addLayout(layout_radio)

        self.button_next = QPushButton('Next', self.central_widget)
        layout.addWidget(self.button_next)





app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
