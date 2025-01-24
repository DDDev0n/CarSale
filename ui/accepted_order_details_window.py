from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox

class AcceptedOrderDetailsWindow(QDialog):
    def __init__(self, order_details, customer_info, db, manager_panel, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Детали принятого заказа")
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

        self.ready_button = QPushButton("Готов")
        self.ready_button.clicked.connect(self.mark_as_ready)
        self.layout.addWidget(self.ready_button)

        self.cancel_button = QPushButton("Отменить")
        self.cancel_button.clicked.connect(self.cancel_order)
        self.layout.addWidget(self.cancel_button)

        self.update_buttons()

    def update_buttons(self):
        status = self.order_details['status']
        self.ready_button.setEnabled(status not in ['Готов', 'Отменён'])
        self.cancel_button.setEnabled(status not in ['Готов', 'Отменён'])

    def mark_as_ready(self):
        if self.order_details['status'] not in ['Готов', 'Отменён']:
            self.db.update_order_status(self.order_details['id'], 'Готов')
            QMessageBox.information(self, "Успешно", "Заказ готов.")
            self.manager_panel.load_orders()
            self.close()

    def cancel_order(self):
        if self.order_details['status'] not in ['Готов', 'Отменён']:
            self.db.cancel_order(self.order_details['id'])
            QMessageBox.information(self, "Успешно", "Заказ отменён.")
            self.manager_panel.load_orders()
            self.close()

    def closeEvent(self, event):
        if self.parent_window is not None:
            self.parent_window.show()
        event.accept()