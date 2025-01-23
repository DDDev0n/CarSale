from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidget, QPushButton, QLineEdit

class AdminWindow(QMainWindow):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Панель администратора")
        self.db = db
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self.central_widget)
        self.user_list = QListWidget()
        self.order_stats_label = QLabel()
        self.manager_sales_label = QLabel()
        self.create_manager_button = QPushButton("Создать аккаунт менеджера")
        self.add_category_button = QPushButton("Добавить категорию")
        self.add_car_button = QPushButton("Добавить автомобиль")

        self.layout.addWidget(QLabel("Пользователи"))
        self.layout.addWidget(self.user_list)
        self.layout.addWidget(QLabel("Статистика заказов"))
        self.layout.addWidget(self.order_stats_label)
        self.layout.addWidget(QLabel("Продажи менеджеров"))
        self.layout.addWidget(self.manager_sales_label)
        self.layout.addWidget(self.create_manager_button)
        self.layout.addWidget(self.add_category_button)
        self.layout.addWidget(self.add_car_button)

        self.load_users()
        self.load_order_stats()
        self.load_manager_sales()
        self.create_manager_button.clicked.connect(self.create_manager)
        self.add_category_button.clicked.connect(self.add_category)
        self.add_car_button.clicked.connect(self.add_car)

    def load_users(self):
        users = self.db.get_users()
        for user in users:
            self.user_list.addItem(f"{user['email']} - {user['role']}")

    def load_order_stats(self):
        stats = self.db.get_order_stats()
        self.order_stats_label.setText(f"Всего заказов: {stats['total']}\nВыполнено: {stats['completed']}\nВ процессе: {stats['in_progress']}")

    def load_manager_sales(self):
        sales = self.db.get_manager_sales()
        sales_text = "\n".join([f"{manager['name']}: {manager['sales']} машин" for manager in sales])
        self.manager_sales_label.setText(sales_text)

    def create_manager(self):
        # Логика создания аккаунта менеджера
        pass

    def add_category(self):
        # Логика добавления категории
        pass

    def add_car(self):
        # Логика добавления автомобиля
        pass