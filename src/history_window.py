from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QTableWidget, QTableWidgetItem
)
from db.database import get_database_connection
from db.models import UserHistory

class HistoryWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Solution History')

        main_layout = QVBoxLayout(self)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels([
            "№",  "Description", "Task Type", "Matrix", "Alpha Value", "C Value", "Timestamp"
        ])

        self.table_widget.verticalHeader().setVisible(False)

        activities = self.fetch_user_activities()

        self.table_widget.setRowCount(len(activities))

        for row_index, activity_data in enumerate(activities):
            activity = activity_data['user_history']

            self.table_widget.setItem(row_index, 0, QTableWidgetItem(str(activity_data['id'])))
            self.table_widget.setItem(row_index, 1, QTableWidgetItem(activity.description))
            self.table_widget.setItem(row_index, 2, QTableWidgetItem(activity.task_type))
            self.table_widget.setItem(row_index, 3, QTableWidgetItem(activity.matrix))
            self.table_widget.setItem(row_index, 4, QTableWidgetItem(str(activity.alpha_value)))
            self.table_widget.setItem(row_index, 5, QTableWidgetItem(str(activity.c_value)))
            self.table_widget.setItem(row_index, 6, QTableWidgetItem(activity_data['timestamp']))

        scroll_area.setWidget(self.table_widget)
        main_layout.addWidget(scroll_area)



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