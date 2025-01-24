from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QLabel, QPushButton
from ui.accepted_order_details_window import AcceptedOrderDetailsWindow

class ManagerAccountWindow(QMainWindow):
    def __init__(self, db, manager_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Активные заказы")
        self.db = db
        self.parent_window = parent
        self.manager_id = manager_id
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #222222;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
            }
            QTableWidget {
                background-color: #333333;
                color: #FFFFFF;
            }
        """)
        self.setup_ui()
        self.showMaximized()

    def setup_ui(self):
        self.layout = QVBoxLayout(self.central_widget)

        self.back_button_layout = QHBoxLayout()
        self.back_button_layout.addStretch()
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)
        self.back_button_layout.addWidget(self.back_button)
        self.layout.addLayout(self.back_button_layout)

        self.order_table = QTableWidget()
        self.order_table.setColumnCount(3)
        self.order_table.setHorizontalHeaderLabels(["Order ID", "Car", "Status"])
        self.order_table.cellClicked.connect(self.show_order_details)
        self.layout.addWidget(QLabel("Принятые заказы"))
        self.layout.addWidget(self.order_table)
        self.load_orders()

    def load_orders(self):
        orders = self.db.get_orders_by_manager(self.manager_id)
        filtered_orders = [order for order in orders if order['status'] not in ['Готов', 'Отменён']]
        self.order_table.setRowCount(len(filtered_orders))
        for row, order in enumerate(filtered_orders):
            self.order_table.setItem(row, 0, QTableWidgetItem(str(order['id'])))
            self.order_table.setItem(row, 1, QTableWidgetItem(order['car']))
            self.order_table.setItem(row, 2, QTableWidgetItem(order['status']))

    def show_order_details(self, row, column):
        order_id = int(self.order_table.item(row, 0).text())
        order_details = self.db.get_accepted_order_details(order_id)
        customer_info = self.db.get_customer_info_by_order(order_id)
        self.details_window = AcceptedOrderDetailsWindow(order_details, customer_info, self.db, self, parent=self)
        self.details_window.show()

    def go_back(self):
        if self.parent_window is not None:
            self.parent_window.show()
        self.close()

    def closeEvent(self, event):
        if event.spontaneous():
            QApplication.instance().quit()
        event.accept()