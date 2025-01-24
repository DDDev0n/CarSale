from PyQt6.QtWidgets import QDialog, QApplication, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton
from ui.order_details_window import OrderDetailsWindow
from ui.order_history_details_window import HistoryOrderDetailsWindow

class OrderHistoryWindow(QDialog):
    def __init__(self, db, manager_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("История заказов")
        self.db = db
        self.manager_id = manager_id
        self.setStyleSheet("""
            QDialog {
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
        self.layout = QVBoxLayout(self)

        self.back_button_layout = QHBoxLayout()
        self.back_button_layout.addStretch()
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)
        self.back_button_layout.addWidget(self.back_button)
        self.layout.addLayout(self.back_button_layout)

        self.canceled_table = QTableWidget()
        self.canceled_table.setColumnCount(3)
        self.canceled_table.setHorizontalHeaderLabels(["Order ID", "Car", "Status"])
        self.canceled_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.canceled_table.cellClicked.connect(self.show_order_details)
        self.layout.addWidget(QLabel("Отменённые заказы"))
        self.layout.addWidget(self.canceled_table)

        self.completed_table = QTableWidget()
        self.completed_table.setColumnCount(3)
        self.completed_table.setHorizontalHeaderLabels(["Order ID", "Car", "Status"])
        self.completed_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.completed_table.cellClicked.connect(self.show_order_details)
        self.layout.addWidget(QLabel("Готовые заказы"))
        self.layout.addWidget(self.completed_table)

        self.load_order_history()

    def load_order_history(self):
        orders = self.db.get_orders_by_manager(self.manager_id)
        canceled_orders = [order for order in orders if order['status'] == 'Отменён']
        completed_orders = [order for order in orders if order['status'] == 'Готов']

        self.canceled_table.setRowCount(len(canceled_orders))
        for row, order in enumerate(canceled_orders):
            self.canceled_table.setItem(row, 0, QTableWidgetItem(str(order['id'])))
            self.canceled_table.setItem(row, 1, QTableWidgetItem(order['car']))
            self.canceled_table.setItem(row, 2, QTableWidgetItem(order['status']))

        self.completed_table.setRowCount(len(completed_orders))
        for row, order in enumerate(completed_orders):
            self.completed_table.setItem(row, 0, QTableWidgetItem(str(order['id'])))
            self.completed_table.setItem(row, 1, QTableWidgetItem(order['car']))
            self.completed_table.setItem(row, 2, QTableWidgetItem(order['status']))

    def show_order_details(self, row, column):
        table = self.sender()
        order_id = int(table.item(row, 0).text())
        order_details = self.db.get_accepted_order_details(order_id)
        customer_info = self.db.get_customer_info_by_order(order_id)
        self.details_window = HistoryOrderDetailsWindow(order_details, customer_info, self.db, manager_panel=self, parent=self)
        self.details_window.show()

    def go_back(self):
        if self.parent() is not None:
            self.parent().show()
        self.close()

    def closeEvent(self, event):
        if event.spontaneous():
            QApplication.instance().quit()
        event.accept()