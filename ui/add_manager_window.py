from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit
from PyQt6.QtCore import QDate, pyqtSignal
from PyQt6.QtCore import Qt

class AddManagerWindow(QDialog):
    manager_added = pyqtSignal()

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить менеджера")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.first_name_label = QLabel("Имя:")
        self.layout.addWidget(self.first_name_label)
        self.first_name_edit = QLineEdit()
        self.layout.addWidget(self.first_name_edit)

        self.last_name_label = QLabel("Фамилия:")
        self.layout.addWidget(self.last_name_label)
        self.last_name_edit = QLineEdit()
        self.layout.addWidget(self.last_name_edit)

        self.patronymic_label = QLabel("Отчество:")
        self.layout.addWidget(self.patronymic_label)
        self.patronymic_edit = QLineEdit()
        self.layout.addWidget(self.patronymic_edit)

        self.email_label = QLabel("Email:")
        self.layout.addWidget(self.email_label)
        self.email_edit = QLineEdit()
        self.layout.addWidget(self.email_edit)

        self.phone_label = QLabel("Телефон:")
        self.layout.addWidget(self.phone_label)
        self.phone_edit = QLineEdit()
        self.layout.addWidget(self.phone_edit)

        self.birthdate_label = QLabel("День рождения:")
        self.layout.addWidget(self.birthdate_label)
        self.birthdate_edit = QDateEdit()
        self.birthdate_edit.setDisplayFormat("yyyy-MM-dd")
        self.layout.addWidget(self.birthdate_edit)

        self.password_label = QLabel("Пароль:")
        self.layout.addWidget(self.password_label)
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_edit)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_manager_details)
        self.layout.addWidget(self.save_button)

    def save_manager_details(self):
        first_name = self.first_name_edit.text()
        last_name = self.last_name_edit.text()
        patronymic = self.patronymic_edit.text()
        email = self.email_edit.text()
        phone_number = self.phone_edit.text()
        birthdate = self.birthdate_edit.date().toString("yyyy-MM-dd")
        password = self.password_edit.text()

        if self.db.insert_manager(first_name, last_name, patronymic, phone_number, email, birthdate, password):
            self.manager_added.emit()
            self.close()
        else:
            print("Error adding manager")