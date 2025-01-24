from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem

class UserDetailsWindow(QDialog):
    def __init__(self, user, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Details")
        self.user = user
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.first_name_label = QLabel("First Name:")
        self.layout.addWidget(self.first_name_label)
        self.first_name_edit = QLineEdit(self.user['first_name'])
        self.layout.addWidget(self.first_name_edit)

        self.last_name_label = QLabel("Last Name:")
        self.layout.addWidget(self.last_name_label)
        self.last_name_edit = QLineEdit(self.user['last_name'])
        self.layout.addWidget(self.last_name_edit)

        self.email_label = QLabel("Email:")
        self.layout.addWidget(self.email_label)
        self.email_edit = QLineEdit(self.user['email'])
        self.layout.addWidget(self.email_edit)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_user_details)
        self.layout.addWidget(self.save_button)

        self.order_history_label = QLabel("Order History:")
        self.layout.addWidget(self.order_history_label)
        self.order_history_table = QTableWidget()
        self.order_history_table.setColumnCount(3)
        self.order_history_table.setHorizontalHeaderLabels(["Order ID", "Car", "Status"])
        self.layout.addWidget(self.order_history_table)
        self.load_order_history()

    def load_order_history(self):
        orders = self.db.get_orders_by_user_id(self.user['id'])
        self.order_history_table.setRowCount(len(orders))
        for row, order in enumerate(orders):
            self.order_history_table.setItem(row, 0, QTableWidgetItem(str(order['id'])))
            self.order_history_table.setItem(row, 1, QTableWidgetItem(order['car']))
            self.order_history_table.setItem(row, 2, QTableWidgetItem(order['status']))

    def save_user_details(self):
        self.user['first_name'] = self.first_name_edit.text()
        self.user['last_name'] = self.last_name_edit.text()
        self.user['email'] = self.email_edit.text()
        self.db.update_user_details(self.user)
        self.close()