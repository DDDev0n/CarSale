from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QLabel, QPushButton
from ui.order_details_window import OrderDetailsWindow
from ui.manager_account_window import ManagerAccountWindow
from ui.order_history_window import OrderHistoryWindow
from ui.add_car_window import AddCarWindow

class ManagerWindow(QMainWindow):
    def __init__(self, db, parent=None, manager_id=None):
        super().__init__(parent)
        self.setWindowTitle("Панель менеджера")
        self.db = db
        self.manager_id = manager_id
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.showMaximized()
        self.setStyleSheet("""
            QMainWindow {
                background-color: #222222;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
            }
            QListWidget, QTableWidget {
                background-color: #333333;
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
        self.layout = QVBoxLayout(self.central_widget)
        self.order_table = QTableWidget()
        self.order_table.setColumnCount(3)
        self.order_table.setHorizontalHeaderLabels(["Order ID", "Car", "Status"])
        self.order_table.cellClicked.connect(self.show_order_details)
        self.layout.addWidget(QLabel("Оплаченные заказы"))
        self.layout.addWidget(self.order_table)
        self.load_orders()

        self.account_button = QPushButton("Активные заказы")
        self.account_button.clicked.connect(self.open_account_window)
        self.layout.addWidget(self.account_button)

        self.history_button = QPushButton("История заказов")
        self.history_button.clicked.connect(self.show_order_history)
        self.layout.addWidget(self.history_button)

        self.add_car_button = QPushButton("Добавить машину")
        self.add_car_button.clicked.connect(self.open_add_car_window)
        self.layout.addWidget(self.add_car_button)

    def load_orders(self):
        orders = self.db.get_paid_orders()
        self.order_table.setRowCount(len(orders))
        for row, order in enumerate(orders):
            self.order_table.setItem(row, 0, QTableWidgetItem(str(order['id'])))
            self.order_table.setItem(row, 1, QTableWidgetItem(order['car']))
            self.order_table.setItem(row, 2, QTableWidgetItem(order['status']))

    def show_order_details(self, row, column):
        order_id = int(self.order_table.item(row, 0).text())
        order_details = self.db.get_order_details(order_id)
        customer_info = self.db.get_customer_info_by_order(order_id)
        self.details_window = OrderDetailsWindow(order_details, customer_info, self.db, manager_panel=self, parent=self,
                                                 manager_id=self.manager_id)
        self.details_window.show()

    def open_account_window(self):
        self.account_window = ManagerAccountWindow(self.db, self.manager_id, parent=self)
        self.account_window.show()
        self.hide()

    def show_order_history(self):
        self.history_window = OrderHistoryWindow(self.db, self.manager_id, self)
        self.history_window.show()
        self.hide()

    def open_add_car_window(self):
        self.add_car_window = AddCarWindow(self.db, self)
        self.add_car_window.show()
        self.hide()

    def closeEvent(self, event):
        self.close()
        event.accept()