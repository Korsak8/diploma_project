from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QTableWidget, QTableWidgetItem,QPushButton,
    QMessageBox
)
from db.database import get_database_connection
from db.models import UserHistory
from db.queries import delete_activity, add_activity_description
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import os

class HistoryWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Solution History')

        self.setMinimumSize(640,480)

        main_layout = QVBoxLayout(self)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderLabels([
            "#",  "Description", "Task Type", "Matrix", "Alpha Value", "C Value", "Timestamp", ""
        ])

        self.table_widget.verticalHeader().setVisible(False)

        activities = self.fetch_user_activities()

        self.table_widget.setRowCount(len(activities))

        for row_index, activity_data in enumerate(activities):
            activity = activity_data['user_history']

            self.table_widget.setItem(row_index, 0, QTableWidgetItem(str(row_index+1)))
            self.table_widget.setItem(row_index, 1, QTableWidgetItem(activity.description))
            self.table_widget.setItem(row_index, 2, QTableWidgetItem(activity.task_type))
            self.table_widget.setItem(row_index, 3, QTableWidgetItem(activity.matrix))
            self.table_widget.setItem(row_index, 4, QTableWidgetItem(str(activity.alpha_value)))
            self.table_widget.setItem(row_index, 5, QTableWidgetItem(str(activity.c_value)))
            self.table_widget.setItem(row_index, 6, QTableWidgetItem(activity_data['timestamp']))

            self.table_widget.setRowHeight(row_index, 40)

            self.table_widget.item(row_index, 1).setFlags(Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled)

            delete_button = QPushButton()
            delete_icon_path = os.path.join(os.getcwd(), "src", "icons", "delete_icon.svg")
            delete_button.setIcon(QIcon(delete_icon_path))
            delete_button.setObjectName('delete_button')
            delete_button.clicked.connect(self.delete_activity_and_row)
            self.table_widget.setCellWidget(row_index,7,delete_button)

        scroll_area.setWidget(self.table_widget)
        main_layout.addWidget(scroll_area)

        self.table_widget.cellChanged.connect(lambda row, _: self.handle_description_changed(row,1))

    def fetch_user_activities(self):
        with get_database_connection() as con:
            cursor = con.cursor()
            cursor.execute('SELECT id, description, task_type, matrix, alpha_value, c_value, timestamp FROM user_history')
            rows = cursor.fetchall()

            activities = [
            {
                'id': row[0],
                'user_history': UserHistory(
                    description=row[1],
                    task_type=row[2],
                    matrix=row[3],
                    alpha_value=row[4],
                    c_value=row[5],
                ),
                'timestamp': row[6]  
            } for row in rows
            ]
            return activities
        
    def delete_activity_and_row(self):
        currentRow = self.table_widget.currentRow()
        activity_id = self.fetch_user_activities()[currentRow]['id']
        if delete_activity(activity_id) > 0:
            self.table_widget.removeRow(currentRow)
            self.update_row_numbers()
        else:
            print(f'Failed to delete the record with id: {activity_id}')

    def update_row_numbers(self):
        for row in range(self.table_widget.rowCount()):
            self.table_widget.item(row, 0).setText(str(row + 1))

    def handle_description_changed(self, row, column):
        activity_id = self.fetch_user_activities()[row]['id']
        new_description = self.table_widget.item(row,column).text()
        add_activity_description(new_description, activity_id)