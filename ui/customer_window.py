from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidget, QPushButton, QHBoxLayout, QLineEdit, QScrollArea, QSizePolicy, QMessageBox, QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from ui.car_details_window import CarDetailsWindow
from ui.account_window import AccountWindow
from PyQt6.QtCore import QTimer


class CustomerWindow(QMainWindow):
    def __init__(self, db, parent=None, user_id=None):
        super().__init__(parent)
        self.setWindowTitle("Автосалон")
        self.db = db
        self.user_id = user_id
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
            QListWidget {
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

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_cars)
        self.timer.start(5000)

    def setup_ui(self):
        self.layout = QVBoxLayout(self.central_widget)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Поиск автомобиля...")
        self.search_button = QPushButton("Поиск")
        self.account_button = QPushButton("Личный кабинет")
        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(self.search_bar)
        self.search_layout.addWidget(self.search_button)
        self.search_layout.addWidget(self.account_button)

        self.layout.addLayout(self.search_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        self.makes_list = QListWidget()
        self.makes_list.itemClicked.connect(self.filter_by_make)
        self.scroll_layout.addWidget(QLabel("Марки автомобилей"))
        self.scroll_layout.addWidget(self.makes_list)
        self.load_makes()

        self.car_list = QListWidget()
        self.car_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.scroll_layout.addWidget(QLabel("Объявления"))
        self.scroll_layout.addWidget(self.car_list)

        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

        self.search_button.clicked.connect(self.perform_search)
        self.account_button.clicked.connect(self.show_account)

        self.view_button = QPushButton("Посмотреть")
        self.view_button.clicked.connect(self.show_car_details)
        self.layout.addWidget(self.view_button)

        self.load_cars()

    def load_makes(self):
        makes = self.db.get_makes()
        self.makes_list.clear()
        for make in makes:
            self.makes_list.addItem(make['name'])

    def load_cars(self):
        cars = self.db.get_all_cars()
        self.car_list.clear()
        for car in cars:
            if not self.is_car_in_order(car['id']):
                self.car_list.addItem(f"{car['id']} {car['make']} {car['model']} ({car['year']}) - {car['price']}")

    def filter_by_make(self, item):
        make = item.text()
        cars = self.db.get_cars_by_make(make)
        self.car_list.clear()
        for car in cars:
            if not self.is_car_in_order(car['id']):
                self.car_list.addItem(f"{car['id']} {car['make']} {car['model']} ({car['year']}) - {car['price']}")

    def perform_search(self):
        search_term = self.search_bar.text()
        cars = self.db.search_cars(search_term)
        self.car_list.clear()
        for car in cars:
            if not self.is_car_in_order(car['id']):
                self.car_list.addItem(f"{car['id']} {car['make']} {car['model']} ({car['year']}) - {car['price']}")

    def show_car_details(self):
        selected_item = self.car_list.currentItem()
        if selected_item:
            car_id = int(selected_item.text().split()[0])
            car_details = self.db.get_car_details(car_id)
            if car_details:
                self.car_details_window = CarDetailsWindow(car_details, self.db, self)
                self.car_details_window.show()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось получить детали автомобиля.")
        else:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите автомобиль из списка.")

    def show_account(self):
        user_id = self.user_id
        self.account_window = AccountWindow(self.db, user_id, self)
        self.account_window.show()
        self.hide()

    def is_car_in_order(self, car_id):
        orders = self.db.get_orders_by_car_id(car_id)
        for order in orders:
            if order['order_status'] != 'Отменён':
                return True
        return False

    def check_car_orders(self):
        for index in range(self.car_list.count()):
            car_item = self.car_list.item(index)
            if car_item is not None:
                car_text = car_item.text().split(" - ")[0]
                car_id = car_text.split()[0]
                if car_id.isdigit():
                    car_id = int(car_id)
                    if self.is_car_in_order(car_id):
                        self.car_list.takeItem(index)