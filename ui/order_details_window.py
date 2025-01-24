from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QMessageBox, QPushButton

class OrderDetailsWindow(QDialog):
    def __init__(self, order_details, customer_info, db, manager_panel=None, parent=None, manager_id=None):
        super().__init__(parent)
        self.setWindowTitle("Детали заказа")
        self.order_details = order_details
        self.manager_id = manager_id
        self.customer_info = customer_info
        self.db = db
        self.manager_panel = manager_panel
        self.setStyleSheet("""
            QDialog {
                background-color: #222222;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel(f"Заказ ID: {self.order_details['id']}"))
        self.layout.addWidget(QLabel(f"Автомобиль: {self.order_details['car']}"))
        self.layout.addWidget(QLabel(f"Статус: {self.order_details['status']}"))
        self.layout.addWidget(QLabel(f"ФИО: {self.customer_info['first_name']} {self.customer_info['last_name']}"))
        self.layout.addWidget(QLabel(f"Телефон: {self.customer_info['phone_number']}"))

        if self.order_details['status'] not in ['Отменён', 'Готов']:
            self.accept_button = QPushButton("Принять")
            self.accept_button.clicked.connect(self.accept_order)
            self.layout.addWidget(self.accept_button)

            self.cancel_button = QPushButton("Отменить")
            self.cancel_button.clicked.connect(self.cancel_order)
            self.layout.addWidget(self.cancel_button)

            self.update_buttons()

    def update_buttons(self):
        status = self.order_details['status']
        self.accept_button.setEnabled(status not in ['Принят', 'Отменён'])
        self.cancel_button.setEnabled(status not in ['Принят', 'Отменён'])

    def accept_order(self):
        if self.order_details['status'] not in ['Принят', 'Отменён']:
            self.db.accept_order(self.order_details['id'], manager_id=self.manager_id)
            QMessageBox.information(self, "Успешно", "Заказ принят.")
            if self.manager_panel:
                self.manager_panel.load_orders()
            self.close()

    def cancel_order(self):
        if self.order_details['status'] not in ['Принят', 'Отменён']:
            self.db.cancel_order(self.order_details['id'])
            QMessageBox.information(self, "Успешно", "Заказ отменён.")
            if self.manager_panel:
                self.manager_panel.load_orders()
            self.close()