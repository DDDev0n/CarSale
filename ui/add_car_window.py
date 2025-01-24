from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class AddCarWindow(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить машину")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.db = db
        self.car_photo_path = None
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.layout.addWidget(QLabel("Марка:"))
        self.make_input = QComboBox()
        self.load_makes()
        self.layout.addWidget(self.make_input)

        self.layout.addWidget(QLabel("Модель:"))
        self.model_input = QLineEdit()
        self.layout.addWidget(self.model_input)

        self.layout.addWidget(QLabel("Год выпуска:"))
        self.year_input = QLineEdit()
        self.layout.addWidget(self.year_input)

        self.layout.addWidget(QLabel("Цвет:"))
        self.color_input = QLineEdit()
        self.layout.addWidget(self.color_input)

        self.layout.addWidget(QLabel("Тип:"))
        self.type_input = QComboBox()
        self.load_types()
        self.layout.addWidget(self.type_input)

        self.layout.addWidget(QLabel("Цена:"))
        self.price_input = QLineEdit()
        self.layout.addWidget(self.price_input)

        self.layout.addWidget(QLabel("Пробег:"))
        self.mileage_input = QLineEdit()
        self.layout.addWidget(self.mileage_input)

        self.layout.addWidget(QLabel("Фотография:"))
        self.photo_button = QPushButton("Загрузить фотографию")
        self.photo_button.clicked.connect(self.upload_photo)
        self.layout.addWidget(self.photo_button)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_car)
        self.layout.addWidget(self.add_button)

    def load_makes(self):
        makes = self.db.get_makes()
        for make in makes:
            self.make_input.addItem(make['name'])

    def load_types(self):
        types = self.db.get_car_types()
        for car_type in types:
            self.type_input.addItem(car_type['name'])

    def upload_photo(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg)")
        if file_dialog.exec():
            self.car_photo_path = file_dialog.selectedFiles()[0]
            QMessageBox.information(self, "Успех", "Фото успешно загружено!")

    def add_car(self):
        make = self.make_input.currentText()
        model = self.model_input.text()
        year = self.year_input.text()
        color = self.color_input.text()
        category = self.type_input.currentText()
        price = self.price_input.text()
        mileage = self.mileage_input.text()

        if self.car_photo_path:
            with open(self.car_photo_path, 'rb') as file:
                photo = file.read()
        else:
            photo = None

        try:
            self.db.add_car(make, model, year, color, category, price, mileage, photo)
            QMessageBox.information(self, "Успех", "Машина успешно добавлена!")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить машину: {e}")