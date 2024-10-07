import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QRadioButton,
    QPushButton, QWidget, QMessageBox, QVBoxLayout,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
from input_window import InputWindow
from history_window import HistoryWindow
from db.database import create_user_history_table
from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('GameDecideApp')

        self.setMinimumSize(640,480)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout(self.central_widget)

        # Add activity history icon
        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join(script_dir, 'icons', 'user_history.svg')

        icon_container = QWidget(self.central_widget)
        header_layout = QVBoxLayout(icon_container)

        self.history_icon = QPushButton(self.central_widget)
        self.history_icon.setIcon(QIcon(icon_path))
        self.history_icon.setIconSize(QSize(24,24))
        self.history_icon.setFixedSize(32,32)
        self.history_icon.setObjectName('history_icon')
        self.history_icon.clicked.connect(self.show_history)
        header_layout.addWidget(self.history_icon, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        main_layout.addWidget(icon_container)

        radio_container = QWidget(self.central_widget)
        layout_radio = QVBoxLayout(radio_container)

        self.label = QLabel('Choose the kind of problem', radio_container)
        self.label.setObjectName('problem_label')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_radio.addWidget(self.label)

        self.radio_uncertainty = QRadioButton('Decision making under uncertainty', self.central_widget)
        layout_radio.addWidget(self.radio_uncertainty)

        self.radio_risk = QRadioButton('Decision making under risk',self.central_widget)
        layout_radio.addWidget(self.radio_risk)
        
        layout_radio.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        main_layout.addWidget(radio_container, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()

        self.button_next = QPushButton('Next', self.central_widget)
        self.button_next.clicked.connect(self.on_button_click)
        main_layout.addWidget(self.button_next)

    def show_history(self):
        create_user_history_table()
        self.new_window = HistoryWindow()
        self.new_window.show()

    def on_button_click(self):
        if self.radio_uncertainty.isChecked():
            task = 'Decision making under uncertainty'
        elif self.radio_risk.isChecked():
            task = 'Decision making under risk'
        else:
            QMessageBox.warning(self, 'Choosing the task', 'Choose the kind of problem')
            return
        
        self.new_window = InputWindow(task)
        self.new_window.show()
        self.close()

def load_stylesheet(app, qss_path):
    qss_file = Path(qss_path)
    if qss_file.exists():
        with open(qss_file, "r", encoding="utf-8") as file:
            app.setStyleSheet(file.read())


app = QApplication(sys.argv)

qss_path = os.path.join(os.path.dirname(__file__), 'styles', 'light.qss')

load_stylesheet(app, qss_path)

window = MainWindow()
window.show()

app.exec()