from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QAbstractItemView
from PyQt6.QtCore import Qt

class AccountWindow(QMainWindow):
    def __init__(self, db, user_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Личный кабинет")
        self.db = db
        self.user_id = user_id
        self.parent_window = parent
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.apply_styles()
        self.setup_ui()
        self.showMaximized()

    def apply_styles(self):
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

    def setup_ui(self):
        self.layout = QVBoxLayout(self.central_widget)

        self.back_button_layout = QHBoxLayout()
        self.back_button_layout.addStretch()
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)
        self.back_button_layout.addWidget(self.back_button)
        self.layout.addLayout(self.back_button_layout)

        user_info = self.db.get_user_info(self.user_id)
        self.layout.addWidget(QLabel(f"Имя: {user_info['first_name']}"))
        self.layout.addWidget(QLabel(f"Фамилия: {user_info['last_name']}"))
        self.layout.addWidget(QLabel(f"Email: {user_info['email']}"))

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(4)
        self.orders_table.setHorizontalHeaderLabels(["ID", "Модель", "Марка", "Статус"])
        self.orders_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.layout.addWidget(self.orders_table)
        self.load_orders()

        self.pay_button = QPushButton("Оплатить")
        self.cancel_button = QPushButton("Отменить")
        self.pay_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        self.layout.addWidget(self.pay_button)
        self.layout.addWidget(self.cancel_button)

        self.orders_table.itemSelectionChanged.connect(self.on_order_selected)
        self.pay_button.clicked.connect(self.pay_order)
        self.cancel_button.clicked.connect(self.cancel_order)

    def load_orders(self):
        orders = self.db.get_user_orders(self.user_id)
        self.orders_table.setRowCount(0)
        for order in orders:
            row_position = self.orders_table.rowCount()
            self.orders_table.insertRow(row_position)
            id_item = QTableWidgetItem()
            id_item.setData(Qt.ItemDataRole.DisplayRole, order['id'])
            self.orders_table.setItem(row_position, 0, id_item)
            self.orders_table.setItem(row_position, 1, QTableWidgetItem(order['model']))
            self.orders_table.setItem(row_position, 2, QTableWidgetItem(order['make']))
            self.orders_table.setItem(row_position, 3, QTableWidgetItem(order['order_status']))
        self.orders_table.setSortingEnabled(True)
        self.orders_table.sortItems(0, Qt.SortOrder.AscendingOrder)

    def on_order_selected(self):
        selected_items = self.orders_table.selectedItems()
        if len(selected_items) >= 4:
            order_status = selected_items[3].text()
            self.pay_button.setEnabled(order_status not in ['Оплачен', 'Готов'])
            self.cancel_button.setEnabled(order_status != 'Отменён')
        else:
            self.pay_button.setEnabled(False)
            self.cancel_button.setEnabled(False)

    def get_selected_order_id(self):
        selected_row = self.orders_table.currentRow()
        if selected_row >= 0:
            return int(self.orders_table.item(selected_row, 0).text())
        return None

    def pay_order(self):
        order_id = self.get_selected_order_id()
        if order_id:
            self.update_order_status(order_id, 'Оплачен')

    def cancel_order(self):
        order_id = self.get_selected_order_id()
        if order_id:
            self.update_order_status(order_id, 'Отменён')

    def update_order_status(self, order_id, status):
        try:
            self.db.update_order_status(order_id, status)
            QMessageBox.information(self, "Успех", f"Статус заказа обновлён на {status}!")
            self.load_orders()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить статус заказа: {e}")

    def go_back(self):
        self.parent_window.show()
        self.close()

    def closeEvent(self, event):
        if event.spontaneous():
            QApplication.instance().quit()
        event.accept()