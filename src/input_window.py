import sys
import numpy as np
import pandas as pd
from PyQt6.QtWidgets import (
    QLabel, QPushButton, QWidget, QMessageBox, QVBoxLayout, QHBoxLayout,
    QSpinBox, QTableWidget, QDoubleSpinBox, QFileDialog, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from  solution_window import SolutionWindow
from pathlib import Path
from db.models import UserHistory
from db.queries import insert_user_activity

class InputWindow(QWidget):
    def __init__(self, task):
        super().__init__()

        self.task = task

        self.setWindowTitle('Input')

        main_layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()

        self.label = QLabel('Choose payoff matrix  dimension:', self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        header_layout.addWidget(self.label)

        self.row_input = QSpinBox(self)
        self.row_input.setMinimum(1)
        self.row_input.setMaximum(15)
        self.row_input.valueChanged.connect(self.update_matrix)
        header_layout.addWidget(self.row_input)

        self.multiplier_label = QLabel('x', self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.multiplier_label)

        self.col_input = QSpinBox(self)
        self.col_input.setMinimum(1)
        self.col_input.setMaximum(15)
        self.col_input.valueChanged.connect(self.update_matrix)
        header_layout.addWidget(self.col_input)

        self.upload_button = QPushButton('Upload file', self)
        self.upload_button.clicked.connect(self.load_file)
        header_layout.addWidget(self.upload_button) 
        
        main_layout.addLayout(header_layout)

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

        self.table_payoff_matrix = QTableWidget(self)
        main_layout.addWidget(self.table_payoff_matrix)

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
            self.table_payoff_matrix.setRowCount(rows + 1)
            self.table_payoff_matrix.setVerticalHeaderLabels(['Probabilities'] + [f'Row {i+1}' for i in range(rows)])
        else:
            self.table_payoff_matrix.setRowCount(rows)
            self.table_payoff_matrix.setVerticalHeaderLabels([f'Row {i+1}' for i in range(rows)])
        
        self.table_payoff_matrix.setColumnCount(cols)
        self.table_payoff_matrix.setHorizontalHeaderLabels([f'Column {i+1}' for i in range(cols)])

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self,"Open file", "", "CSV Files (*.csv);;Excel Files (*.xlsx *.xls);;TSV Files (*.tsv)")

        if not file_name:
            return

        if file_name:
            file_extension = Path(file_name).suffix

            if file_extension == '.csv':
                matrix = pd.read_csv(file_name, header=None).to_numpy()
            elif file_extension in ['.xlsx','.xls']:
                matrix = pd.read_excel(file_name, header=None).to_numpy()
            elif file_extension == '.tsv':
                matrix = pd.read_csv(file_name, sep="\t", header=None).to_numpy()
            else:
                QMessageBox.warning(self,"Unsupported File", "File format is not supported.")
        
        rows, cols = matrix.shape

        self.row_input.setValue(rows)
        self.col_input.setValue(cols)
        
        self.table_payoff_matrix.setRowCount(rows)
        self.table_payoff_matrix.setColumnCount(cols)

        for row in range(rows):
            for col in range(cols):
                item = QTableWidgetItem(str(matrix[row, col]))
                self.table_payoff_matrix.setItem(row, col, item)


    def on_button_click_previous(self):
        from main_window import MainWindow
        self.previous_window = MainWindow()
        self.previous_window.show()

    def on_button_click_next(self):
        data = []
        for row in range(self.table_payoff_matrix.rowCount()):
            row_data = []
            for col in range(self.table_payoff_matrix.columnCount()):
                item = self.table_payoff_matrix.item(row, col)
                text = item.text() if item is not None else ""
                row_data.append(text)
            data.append(row_data)
        
        try:
            num_array = np.array(data, dtype=float)
        except ValueError:
            QMessageBox.warning(self, "Error", "The matrix is empty or contains invalid entries.")
            return
        
        matrix_str = '\n'.join([','.join(map(str, row)) for row in num_array])
    
        activity = UserHistory(
            description='',
            task_type=self.task,
            matrix=matrix_str,
            alpha_value=self.alpha_input.value(),
            c_value=self.c_input.value() if self.task == "Decision making under risk" else None
        )

        insert_user_activity(activity)

        if self.task == 'Decision making under risk':
            self.new_window = SolutionWindow(num_array, self.alpha_input.value(), self.task, self.c_input.value())
        else:
            self.new_window = SolutionWindow (num_array, self.alpha_input.value(), self.task)

        self.new_window.show()
        self.close()