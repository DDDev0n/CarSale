from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidget, QPushButton, QLineEdit

class ManagerWindow(QMainWindow):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Панель менеджера")
        self.db = db
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self.central_widget)
        self.order_list = QListWidget()
        self.order_status_edit = QLineEdit()
        self.update_status_button = QPushButton("Обновить статус")
        self.customer_info_label = QLabel()

        self.layout.addWidget(QLabel("Заказы"))
        self.layout.addWidget(self.order_list)
        self.layout.addWidget(QLabel("Новый статус"))
        self.layout.addWidget(self.order_status_edit)
        self.layout.addWidget(self.update_status_button)
        self.layout.addWidget(QLabel("Информация о клиенте"))
        self.layout.addWidget(self.customer_info_label)

        self.load_orders()
        self.order_list.itemClicked.connect(self.load_customer_info)
        self.update_status_button.clicked.connect(self.update_order_status)

    def load_orders(self):
        orders = self.db.get_orders()
        for order in orders:
            self.order_list.addItem(f"Заказ {order['id']} - {order['order_status']}")

    def load_customer_info(self, item):
        order_info = item.text()
        order_id = int(order_info.split()[1])
        customer_info = self.db.get_customer_info_by_order(order_id)
        self.customer_info_label.setText(f"ФИО: {customer_info['first_name']} {customer_info['last_name']}\nТелефон: {customer_info['phone_number']}")

    def update_order_status(self):
        selected_order = self.order_list.currentItem()
        if selected_order:
            order_info = selected_order.text()
            order_id = int(order_info.split()[1])
            new_status = self.order_status_edit.text()
            self.db.update_order_status(order_id, new_status)
            self.load_orders()