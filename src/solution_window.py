import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QRadioButton,
    QPushButton, QWidget, QMessageBox, QVBoxLayout, QHBoxLayout,
    QSpinBox, QTableWidget,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from decision_making_under_risk import DecisionMakingUnderRisk
from decision_making_under_uncertainty import DecisionMakingUnderUncertainty

class SolutionWindow(QWidget):
    def __init__(self,num_array, alpha_value, task, c_value = None):
        super().__init__()

        self.num_array = num_array
        self.alpha_value = alpha_value
        self.task = task
        self.c_value = c_value

        self.setWindowTitle('Solution')

        main_layout =  QVBoxLayout(self)

        task_label  = QLabel(f"Task: {self.task}",self)
        main_layout.addWidget(task_label)

        if task == "Decision making under risk":
            methods = {
                "Bayes-Laplace Criterio":  DecisionMakingUnderRisk.bayes_laplace_criterio,
                "Germeyer Criterio": lambda pm:DecisionMakingUnderRisk.germeyer_criterio(pm, c_value=self.c_value),
                "Hodge-Lehmann Criterio": lambda pm: DecisionMakingUnderRisk.hodge_lehmann_criterio(pm,alpha=self.alpha_value)
            }
        else:
            methods = {
                "Wald Criterion": DecisionMakingUnderUncertainty.wald_criterion,
                "Laplace Criterion": DecisionMakingUnderUncertainty.laplace_criterion,
                "Maximax Criterion": DecisionMakingUnderUncertainty.maximax_criterion,
                "Hurwitz Criterion": lambda pm: DecisionMakingUnderUncertainty.hurwitz_criterion(pm,alpha=self.alpha_value)
            }
        
        for method_name, method in methods.items():
            result = method(self.num_array)
            dynamic_layout = QHBoxLayout()  
            
            method_label = QLabel(f"Method: {method_name}", self)
            result_label = QLabel(f"Result: {result}", self)
            
            dynamic_layout.addWidget(method_label)
            dynamic_layout.addWidget(result_label)
            
            main_layout.addLayout(dynamic_layout) 
        

        buttom_layout = QHBoxLayout()

        self.button_previous = QPushButton("Previous", self)
        self.button_previous.clicked.connect(self.on_button_click_previous)
        buttom_layout.addWidget(self.button_previous)

        self.button_close = QPushButton("Close", self)
        self.button_close.clicked.connect(self.close)
        buttom_layout.addWidget(self.button_close)

        main_layout.addLayout(buttom_layout)


    def on_button_click_previous(self):
        from input_window import InputWindow
        self.previous_window = InputWindow(self.task)
        self.previous_window.show()
        self.close()