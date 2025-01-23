from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QMessageBox, QDateEdit

class RegisterWindow(QMainWindow):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Регистрация")
        self.db = db
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self.central_widget)
        self.first_name_edit = QLineEdit()
        self.first_name_edit.setPlaceholderText("Имя")
        self.last_name_edit = QLineEdit()
        self.last_name_edit.setPlaceholderText("Фамилия")
        self.patronymic_edit = QLineEdit()
        self.patronymic_edit.setPlaceholderText("Отчество")
        self.phone_number_edit = QLineEdit()
        self.phone_number_edit.setPlaceholderText("Номер телефона")
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Email")
        self.birthdate_edit = QDateEdit()
        self.birthdate_edit.setCalendarPopup(True)
        self.birthdate_edit.setDisplayFormat("yyyy-MM-dd")
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Пароль")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_button = QPushButton("Зарегистрироваться")

        self.layout.addWidget(self.first_name_edit)
        self.layout.addWidget(self.last_name_edit)
        self.layout.addWidget(self.patronymic_edit)
        self.layout.addWidget(self.phone_number_edit)
        self.layout.addWidget(self.email_edit)
        self.layout.addWidget(self.birthdate_edit)
        self.layout.addWidget(self.password_edit)
        self.layout.addWidget(self.register_button)

        self.register_button.clicked.connect(self.register)

    def register(self):
        first_name = self.first_name_edit.text().strip()
        last_name = self.last_name_edit.text().strip()
        patronymic = self.patronymic_edit.text().strip()
        phone_number = self.phone_number_edit.text().strip()
        email = self.email_edit.text().strip()
        birthdate = self.birthdate_edit.date().toString("yyyy-MM-dd")
        password = self.password_edit.text().strip()

        if not first_name or not last_name or not patronymic:
            QMessageBox.critical(self, "Ошибка регистрации", "Пожалуйста, введите ФИО.")
            return
        if not phone_number.isdigit() or len(phone_number) < 10:
            QMessageBox.critical(self, "Ошибка регистрации", "Пожалуйста, введите корректный номер телефона.")
            return
        if "@" not in email or "." not in email:
            QMessageBox.critical(self, "Ошибка регистрации", "Пожалуйста, введите корректный email.")
            return
        if not password or len(password) < 6:
            QMessageBox.critical(self, "Ошибка регистрации", "Пароль должен содержать не менее 6 символов.")
            return

        if self.db.insert_user(first_name, last_name, patronymic, phone_number, email, birthdate, password):
            QMessageBox.information(self, "Регистрация", "Регистрация прошла успешно")
            self.close()
        else:
            QMessageBox.critical(self, "Ошибка регистрации", "Ошибка при сохранении данных.")