from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QListWidget, QLineEdit, QGridLayout
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, role, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Главное окно")
        self.role = role
        self.db = db
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self.central_widget)
        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        self.role_label = QLabel(f"Вы вошли как: {self.role}")
        self.role_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logout_button = QPushButton("Выйти")
        self.logout_button.clicked.connect(self.logout)

        if self.role == 'admin':
            self.admin_label = QLabel("Панель администратора")
            self.admin_layout = QGridLayout()
            self.admin_layout.addWidget(QLabel("Username:"), 0,0)
            self.username_edit = QLineEdit()
            self.admin_layout.addWidget(self.username_edit, 0, 1)

            self.user_list = QListWidget()
            self.admin_layout.addWidget(self.user_list, 1, 0, 1, 2)

        elif self.role == 'customer':
            self.customer_label = QLabel("Панель покупателя")

        else:
            self.role_label.setText(f"Неопознанная роль: {self.role}")

    def setup_layout(self):
        self.main_layout.addWidget(self.role_label)

        if self.role == 'admin':
            self.main_layout.addWidget(self.admin_label)
            self.main_layout.addLayout(self.admin_layout)

        elif self.role == 'customer':
            self.main_layout.addWidget(self.customer_label)


        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.logout_button)
        button_layout.addStretch(1)
        self.main_layout.addLayout(button_layout)
        self.main_layout.addStretch(1)

    def logout(self):
        self.close()
