from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal

class AdminCarDetailsWindow(QDialog):
    car_updated = pyqtSignal()

    def __init__(self, car, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Детали автомобиля")
        self.car = car
        self.db = db
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setup_ui()
        self.load_car_details()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.make_label = QLabel("Марка:")
        self.make_combo = QComboBox()
        self.layout.addWidget(self.make_label)
        self.layout.addWidget(self.make_combo)

        self.model_label = QLabel("Модель:")
        self.model_edit = QLineEdit()
        self.layout.addWidget(self.model_label)
        self.layout.addWidget(self.model_edit)

        self.year_label = QLabel("Год:")
        self.year_edit = QLineEdit()
        self.layout.addWidget(self.year_label)
        self.layout.addWidget(self.year_edit)

        self.price_label = QLabel("Цена:")
        self.price_edit = QLineEdit()
        self.layout.addWidget(self.price_label)
        self.layout.addWidget(self.price_edit)

        self.mileage_label = QLabel("Пробег:")
        self.mileage_edit = QLineEdit()
        self.layout.addWidget(self.mileage_label)
        self.layout.addWidget(self.mileage_edit)

        self.color_label = QLabel("Цвет:")
        self.color_edit = QLineEdit()
        self.layout.addWidget(self.color_label)
        self.layout.addWidget(self.color_edit)

        self.category_label = QLabel("Категория:")
        self.category_combo = QComboBox()
        self.layout.addWidget(self.category_label)
        self.layout.addWidget(self.category_combo)

        self.button_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_car_details)
        self.button_layout.addWidget(self.save_button)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_car)
        self.button_layout.addWidget(self.delete_button)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_layout)

    def load_car_details(self):
        makes = self.db.get_all_makes()
        for make in makes:
            self.make_combo.addItem(make['name'], make['id'])

        categories = self.db.get_all_categories()
        for category in categories:
            self.category_combo.addItem(category['name'], category['id'])

        make_index = self.make_combo.findText(self.car.get('make', ''), Qt.MatchFlag.MatchFixedString)
        if make_index >= 0:
            self.make_combo.setCurrentIndex(make_index)

        self.model_edit.setText(self.car.get('model', ''))
        self.year_edit.setText(str(self.car.get('year', '')))
        self.price_edit.setText(str(self.car.get('price', '')))
        self.mileage_edit.setText(str(self.car.get('mileage', '')))
        self.color_edit.setText(self.car.get('color', ''))

        category_index = self.category_combo.findText(self.car.get('category', ''), Qt.MatchFlag.MatchFixedString)
        if category_index >= 0:
            self.category_combo.setCurrentIndex(category_index)

    def save_car_details(self):
        car_details = {
            'make_id': self.make_combo.currentData(),
            'model': self.model_edit.text(),
            'year': int(self.year_edit.text()),
            'price': float(self.price_edit.text()),
            'mileage': int(self.mileage_edit.text()),
            'color': self.color_edit.text(),
            'category_id': self.category_combo.currentData()
        }

        try:
            self.db.update_car(self.car['id'], car_details)
            QMessageBox.information(self, "Успех", "Детали автомобиля успешно сохранены.")
            self.car_updated.emit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить детали автомобиля: {e}")

    def delete_car(self):
        try:
            self.db.delete_car(self.car['id'])
            QMessageBox.information(self, "Успех", "Автомобиль успешно удален.")
            self.car_updated.emit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить автомобиль: {e}")