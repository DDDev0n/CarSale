from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt6.QtCore import Qt

from ui.car_list_window import CarListWindow
from ui.user_list_window import UserListWindow
from ui.manager_list_window import ManagerListWindow
from ui.reports_window import ReportsWindow

class AdminWindow(QMainWindow):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Панель администратора")
        self.db = db
        self.showMaximized()
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #222222;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
            }
            QListWidget, QTableWidget {
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

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        header = QLabel("Панель администратора")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        self.users_button = QPushButton("Список пользователей")
        self.users_button.clicked.connect(self.manage_users)
        layout.addWidget(self.users_button)

        self.managers_button = QPushButton("Управление менеджерами")
        self.managers_button.clicked.connect(self.manage_managers)
        layout.addWidget(self.managers_button)

        self.cars_button = QPushButton("Управление автомобилями")
        self.cars_button.clicked.connect(self.manage_cars)
        layout.addWidget(self.cars_button)

        self.reports_button = QPushButton("Отчёты")
        self.reports_button.clicked.connect(self.view_reports)
        layout.addWidget(self.reports_button)

    def manage_users(self):
        self.user_list_window = UserListWindow(self.db, self)
        self.user_list_window.show()
        self.hide()

    def manage_managers(self):
        self.manager_list_window = ManagerListWindow(self.db, self)
        self.manager_list_window.show()
        self.hide()

    def manage_cars(self):
        self.car_list_window_ = CarListWindow(self.db, self)
        self.car_list_window_.show()
        self.hide()

    def view_reports(self):
        self.reports_window = ReportsWindow(self.db, self)
        self.reports_window.show()