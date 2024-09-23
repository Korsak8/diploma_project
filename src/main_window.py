import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QRadioButton,
    QPushButton, QWidget, QMessageBox, QVBoxLayout,
    QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QSize
from input_window import InputWindow
from history_window import HistoryWindow
from db.database import create_user_history_table

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('GameDecideApp')

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout(self.central_widget)

        header_layout = QHBoxLayout()

        self.label = QLabel('Choose the kind of problem', self.central_widget)
        self.label.setFont(QFont('Arial', 20))
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        header_layout.addWidget(self.label)

        # Add activity history icon
        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join(script_dir, 'icons', 'user_history.svg')

        self.history_icon = QPushButton(self.central_widget)
        self.history_icon.setIcon(QIcon(icon_path))
        self.history_icon.setIconSize(QSize(24,24))
        self.history_icon.setFixedSize(32,32)
        self.history_icon.clicked.connect(self.show_history)
        header_layout.addWidget(self.history_icon)

        main_layout.addLayout(header_layout)

        # Add a spacer to ensure the header_layout remains at the top regardless of window resizing
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        main_layout.addItem(spacer)

        layout_radio = QVBoxLayout()

        self.radio_uncertainty = QRadioButton('Decision making under uncertainty', self.central_widget)
        layout_radio.addWidget(self.radio_uncertainty)

        self.radio_risk = QRadioButton('Decision making under risk',self.central_widget)
        layout_radio.addWidget(self.radio_risk)
        
        layout_radio.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        main_layout.addLayout(layout_radio)

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

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()