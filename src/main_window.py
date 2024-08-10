import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QRadioButton,
    QPushButton, QWidget, QMessageBox, QVBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from dimension_window import DimensionWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('GameDecideApp')
        self.setWindowTitle("My App")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.label = QLabel('Choose the kind of problem', self.central_widget)
        self.label.setFont(QFont('Arial', 20))
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.label)


        self.radio_uncertainty = QRadioButton('Decision making under uncertainty', self.central_widget)
        self.radio_risk = QRadioButton('Decision making under risk',self.central_widget)

        layout_radio = QVBoxLayout()
        layout_radio.addWidget(self.radio_uncertainty)
        layout_radio.addWidget(self.radio_risk)

        layout_radio.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addLayout(layout_radio)
        self.button_next = QPushButton('Next', self.central_widget)
        self.button_next.clicked.connect(self.on_button_click)
        layout.addWidget(self.button_next)

    def on_button_click(self):
        if self.radio_uncertainty.isChecked():
            task = 'Decision making under uncertainty'
        elif self.radio_risk.isChecked():
            task = 'Decision making under risk'
        else:
            QMessageBox.warning(self, 'Choosing the task', 'Choose the kind of problem')
            return
        
        self.new_window = DimensionWindow(task)
        self.new_window.show()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
