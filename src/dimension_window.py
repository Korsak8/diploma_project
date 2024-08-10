import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QRadioButton,
    QPushButton, QWidget, QMessageBox, QVBoxLayout, QHBoxLayout,
    QSpinBox, QTableWidget,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class DimensionWindow(QWidget):
    def __init__(self, task):
        super().__init__()

        self.setWindowTitle('Choosing dimension')

        main_layout = QVBoxLayout(self)

        head_layout = QHBoxLayout()

        self.label = QLabel('Choose payoff matrix  dimension:', self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        head_layout.addWidget(self.label)

        self.row_input = QSpinBox(self)
        self.row_input.setMinimum(1)
        self.row_input.setMaximum(7)
        self.row_input.valueChanged.connect(self.update_matrix)
        head_layout.addWidget(self.row_input)

        self.multiplier_label = QLabel('x', self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        head_layout.addWidget(self.multiplier_label)

        self.col_input = QSpinBox(self)
        self.col_input.setMinimum(1)
        self.col_input.setMaximum(7)
        self.col_input.valueChanged.connect(self.update_matrix)
        head_layout.addWidget(self.col_input)
        
        main_layout.addLayout(head_layout)

        self.payoff_matrix = QTableWidget(self)
        main_layout.addWidget(self.payoff_matrix)

        bottom_layout = QHBoxLayout()

        self.button_previous = QPushButton("Previous", self)
        self.button_previous.clicked.connect(self.on_button_click_previous)
        bottom_layout.addWidget(self.button_previous)

        self.button_next = QPushButton("Next", self)
        self.button_next.clicked.connect(self.on_button_click_next)
        bottom_layout.addWidget(self.button_next)

        main_layout.addLayout(bottom_layout)

        self.update_matrix()

    def update_matrix(self):
        rows = self.row_input.value()
        cols = self.col_input.value()
        self.payoff_matrix.setRowCount(rows)
        self.payoff_matrix.setColumnCount(cols)
        self.payoff_matrix.setHorizontalHeaderLabels([f'Column {i+1}' for i in range(cols)])
        self.payoff_matrix.setVerticalHeaderLabels([f'Row {i+1}' for i in range(rows)])

    def on_button_click_previous(self):
        from main_window import MainWindow
        self.previous_window = MainWindow()
        self.previous_window.show()

    def on_button_click_next(self):
        pass
        # self.next_window = Solution()
        # self.next_window.show()