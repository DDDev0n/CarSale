from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidget, QPushButton, QHBoxLayout, QLineEdit, QScrollArea, QSizePolicy, QMessageBox
from PyQt6.QtCore import Qt, QTimer
from ui.account_window import AccountWindow

class CustomerWindow(QMainWindow):
    def __init__(self, db, parent=None, user_id=None):
        super().__init__(parent)
        self.setWindowTitle("Автосалон")
        self.db = db
        self.user_id = user_id
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Черно-красная тема
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

    def setup_ui(self):
        self.layout = QVBoxLayout(self.central_widget)

        # --- Верхняя панель поиска/фильтров ---
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Поиск автомобиля...")
        self.search_button = QPushButton("Поиск")
        self.account_button = QPushButton("Личный кабинет")
        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(self.search_bar)
        self.search_layout.addWidget(self.search_button)
        self.search_layout.addWidget(self.account_button)

        self.layout.addLayout(self.search_layout)

        # --- Scroll Area ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        # --- Список марок автомобилей ---
        self.makes_list = QListWidget()
        self.makes_list.itemClicked.connect(self.filter_by_make)  # Connect item click event
        self.scroll_layout.addWidget(QLabel("Марки автомобилей"))
        self.scroll_layout.addWidget(self.makes_list)
        self.load_makes()

        # --- Список объявлений ---
        self.car_list = QListWidget()
        self.car_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.scroll_layout.addWidget(QLabel("Объявления"))
        self.scroll_layout.addWidget(self.car_list)

        # --- Кнопка заказа ---
        self.order_button = QPushButton("Заказать")
        self.scroll_layout.addWidget(self.order_button)

        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

        # Подключение кнопок
        self.search_button.clicked.connect(self.perform_search)
        self.order_button.clicked.connect(self.place_order)
        self.account_button.clicked.connect(self.show_account)

        self.load_cars()

        # Set up a timer to check car orders every 5 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_car_orders)
        self.timer.start(5000)  # 5000 milliseconds = 5 seconds

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

    def place_order(self):
        selected_car = self.car_list.currentItem()
        if selected_car:
            car_info = selected_car.text().split(" - ")
            car_id = car_info[0].split()[0]  # Assuming the car ID is the first part of the item text
            user_id = self.user_id
            try:
                if self.is_car_in_order(int(car_id)):
                    QMessageBox.critical(self, "Ошибка", "Этот автомобиль уже находится в заказе.")
                else:
                    self.db.place_order(user_id, int(car_id))
                    QMessageBox.information(self, "Успешно!", "Заказ оформлен успешно! Его статус можно посмотреть в личном кабинете")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при оформлении заказа: {e}")
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста выберите машину для заказа.")

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