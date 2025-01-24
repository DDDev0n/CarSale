from PyQt6.QtWidgets import QLabel, QVBoxLayout, QPushButton,  QMessageBox, QDialog
from PyQt6.QtGui import QPixmap, QImage

class CarDetailsWindow(QDialog):
    def __init__(self, car_details, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Детали автомобиля")
        self.car_details = car_details
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.layout.addWidget(QLabel(f"Модель: {self.car_details['model']}"))
        self.layout.addWidget(QLabel(f"Марка: {self.car_details['make']}"))
        self.layout.addWidget(QLabel(f"Год выпуска: {self.car_details['year']}"))
        self.layout.addWidget(QLabel(f"Цвет: {self.car_details['color']}"))
        self.layout.addWidget(QLabel(f"Цена: {self.car_details['price']}"))

        self.car_photo = QLabel()
        if isinstance(self.car_details['photo'], bytes):
            image = QImage.fromData(self.car_details['photo'])
            pixmap = QPixmap.fromImage(image)
            self.car_photo.setPixmap(pixmap)
        else:
            self.car_photo.setText(self.car_details['photo'])
        self.layout.addWidget(self.car_photo)

        self.order_button = QPushButton("Заказать")
        self.order_button.clicked.connect(self.order_car)
        self.layout.addWidget(self.order_button)

    def order_car(self):
        try:
            if not self.is_car_in_order(self.car_details['id']):
                self.db.order_car(self.car_details['id'], self.parent().user_id)
                QMessageBox.information(self, "Успех", "Автомобиль успешно заказан, статус выполнения заказа можно посмотреть в личном кабинете!")
                self.close()
            else:
                QMessageBox.information(self, "Ошибка", "Этот автомобиль уже кто-то заказал")
                self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось заказать автомобиль: {e}")

    def is_car_in_order(self, car_id):
        orders = self.db.get_orders_by_car_id(car_id)
        for order in orders:
            if order['order_status'] != 'Отменён':
                return True
        return False