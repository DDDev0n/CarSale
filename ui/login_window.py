from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QMessageBox
from ui.customer_window import CustomerWindow
from ui.admin_window import AdminWindow
from ui.manager_window import ManagerWindow
from ui.register_window import RegisterWindow

class LoginWindow(QMainWindow):
    login_successful = pyqtSignal(int)

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Вход")
        self.db = db
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self.central_widget)
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Email")
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Пароль")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton("Войти")
        self.register_button = QPushButton("Зарегистрироваться")

        self.layout.addWidget(self.email_edit)
        self.layout.addWidget(self.password_edit)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.register_button)

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self):
        email = self.email_edit.text().strip()
        password = self.password_edit.text().strip()

        if not email or "@" not in email or "." not in email:
            QMessageBox.critical(self, "Ошибка входа", "Пожалуйста, введите корректный email.")
            return
        if not password or len(password) < 6:
            QMessageBox.critical(self, "Ошибка входа", "Пароль должен содержать не менее 6 символов.")
            return

        role_id, user_id = self.db.validate_user(email, password)
        if role_id == 1:
            self.admin_window = AdminWindow(self.db)
            self.admin_window.show()
            self.login_successful.emit(role_id)
        elif role_id == 2:
            self.manager_window = ManagerWindow(self.db)
            self.manager_window.show()
            self.login_successful.emit(role_id)
        elif role_id == 3:
            self.customer_window = CustomerWindow(self.db, user_id=user_id)
            self.customer_window.show()
            self.login_successful.emit(role_id)
        else:
            QMessageBox.critical(self, "Ошибка входа", "Неверный email или пароль.")

        self.hide()  # Hide the login window after showing the respective window

    def register(self):
        self.register_window = RegisterWindow(self.db)
        self.register_window.show()