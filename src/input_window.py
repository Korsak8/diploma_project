import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QRadioButton,
    QPushButton, QWidget, QMessageBox, QVBoxLayout, QHBoxLayout,
    QSpinBox, QTableWidget, QDoubleSpinBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from  solution_window import SolutionWindow

class InputWindow(QWidget):
    def __init__(self, task):
        super().__init__()

        self.task = task

        self.setWindowTitle('Input')

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

        parameter_layout = QHBoxLayout()

        self.alpha_label = QLabel('Choose alpha value:')
        parameter_layout.addWidget(self.alpha_label)

        self.alpha_input = QDoubleSpinBox()
        self.alpha_input.setMinimum(0)
        self.alpha_input.setMaximum(1)
        self.alpha_input.setSingleStep(0.001)
        self.alpha_input.setDecimals(3)
        parameter_layout.addWidget(self.alpha_input)

        if self.task == 'Decision making under risk':
            self.c_value_label = QLabel('Choose c value:')
            parameter_layout.addWidget(self.c_value_label)

            self.c_input = QDoubleSpinBox()
            self.c_input.setMinimum(1)
            self.c_input.setMaximum(5)
            self.c_input.setSingleStep(0.001)
            self.c_input.setDecimals(3)
            parameter_layout.addWidget(self.c_input)

        main_layout.addLayout(parameter_layout)

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
        if self.task == "Decision making under risk":
            self.payoff_matrix.setRowCount(rows + 1)
            self.payoff_matrix.setVerticalHeaderLabels(['Probabilities'] + [f'Row {i+1}' for i in range(rows)])
        else:
            self.payoff_matrix.setRowCount(rows)
            self.payoff_matrix.setVerticalHeaderLabels([f'Row {i+1}' for i in range(rows)])
        
        self.payoff_matrix.setColumnCount(cols)
        self.payoff_matrix.setHorizontalHeaderLabels([f'Column {i+1}' for i in range(cols)])

    def on_button_click_previous(self):
        from main_window import MainWindow
        self.previous_window = MainWindow()
        self.previous_window.show()

    def on_button_click_next(self):
        data = []
        for row in range(self.payoff_matrix.rowCount()):
            row_data = []
            for col in range(self.payoff_matrix.columnCount()):
                item = self.payoff_matrix.item(row, col)
                text = item.text() if item is not None else ""
                row_data.append(text)
            data.append(row_data)
        num_array = np.array(data, dtype=float)

        if self.task == 'Decision making under risk':
            self.new_window = SolutionWindow(num_array, self.alpha_input.value(), self.task, self.c_input.value())
        else:
            self.new_window = SolutionWindow (num_array, self.alpha_input.value(), self.task)

        self.new_window.show()
        self.close()