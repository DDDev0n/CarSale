from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem, QLabel, QApplication
from PyQt6.QtCore import Qt

from ui.add_car_window import AddCarWindow
from ui.admin_car_details_window import AdminCarDetailsWindow


class CarListWindow(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список машин")
        self.db = db
        self.showMaximized()
        self.setup_ui()
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
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

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.back_button_layout = QHBoxLayout()
        self.back_button_layout.addStretch()
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)
        self.back_button_layout.addWidget(self.back_button)
        self.layout.addLayout(self.back_button_layout)

        self.car_list = QListWidget()
        self.car_list.itemClicked.connect(self.edit_car)
        self.layout.addWidget(self.car_list)

        self.button_layout = QHBoxLayout()
        self.add_car_button = QPushButton("Добавить машину")
        self.add_car_button.clicked.connect(self.add_car)
        self.button_layout.addWidget(self.add_car_button)

        self.layout.addLayout(self.button_layout)

        self.load_cars()

    def load_cars(self):
        self.car_list.clear()
        cars = self.db.admin_get_all_cars()
        for car in cars:
            make = car.get('make', 'Unknown')
            model = car.get('model', 'Unknown')
            year = car.get('year', 'Unknown')
            price = car.get('price', 'Unknown')
            mileage = car.get('mileage', 'Unknown')
            color = car.get('color', 'Unknown')
            category = car.get('category', 'Unknown')
            item_text = f"{make} {model} - {year} - {price} - {mileage} - {color} - {category}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, car)
            self.car_list.addItem(item)

    def edit_car(self, item):
        car = item.data(Qt.ItemDataRole.UserRole)
        if car is not None:
            self.car_details_window = AdminCarDetailsWindow(car, self.db, self)
            self.car_details_window.car_updated.connect(self.load_cars)
            self.car_details_window.show()

    def add_car(self):
        self.add_car_window = AddCarWindow(self.db, self)
        self.add_car_window.show()


    def go_back(self):
        if self.parent() is not None:
            self.parent().show()
        self.close()

    def closeEvent(self, event):
        if event.spontaneous():
            QApplication.instance().quit()
        event.accept()