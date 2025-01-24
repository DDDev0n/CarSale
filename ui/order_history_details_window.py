from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox

class HistoryOrderDetailsWindow(QDialog):
    def __init__(self, order_details, customer_info, db, manager_panel, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Детали завершённого заказа")
        self.order_details = order_details
        self.customer_info = customer_info
        self.db = db
        self.parent_window = parent
        self.manager_panel = manager_panel
        self.setStyleSheet("""
            QDialog {
                background-color: #222222;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #FF3333;
                color: #FFFFFF;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #CC0000;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel(f"Заказ ID: {self.order_details['id']}"))
        self.layout.addWidget(QLabel(f"Автомобиль: {self.order_details['car']}"))
        self.layout.addWidget(QLabel(f"Модель: {self.order_details['model']}"))
        self.layout.addWidget(QLabel(f"Год выпуска: {self.order_details['year']}"))
        self.layout.addWidget(QLabel(f"Цвет: {self.order_details['color']}"))
        self.layout.addWidget(QLabel(f"Статус: {self.order_details['status']}"))
        self.layout.addWidget(QLabel(f"ФИО: {self.customer_info['first_name']} {self.customer_info['last_name']}"))
        self.layout.addWidget(QLabel(f"Телефон: {self.customer_info['phone_number']}"))

    def closeEvent(self, event):
        if self.parent_window is not None:
            self.parent_window.show()
        event.accept()