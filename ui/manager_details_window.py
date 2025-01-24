from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit
from PyQt6.QtCore import QDate, pyqtSignal
from datetime import datetime

class ManagerDetailsWindow(QDialog):
    manager_updated = pyqtSignal()

    def __init__(self, manager, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Детали менеджера")
        self.manager = manager
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.first_name_label = QLabel("Имя:")
        self.layout.addWidget(self.first_name_label)
        self.first_name_edit = QLineEdit(self.manager['first_name'])
        self.layout.addWidget(self.first_name_edit)

        self.last_name_label = QLabel("Фамилия:")
        self.layout.addWidget(self.last_name_label)
        self.last_name_edit = QLineEdit(self.manager['last_name'])
        self.layout.addWidget(self.last_name_edit)

        self.patronymic_label = QLabel("Отчество:")
        self.layout.addWidget(self.patronymic_label)
        self.patronymic_edit = QLineEdit(self.manager['patronymic'])
        self.layout.addWidget(self.patronymic_edit)

        self.email_label = QLabel("Email:")
        self.layout.addWidget(self.email_label)
        self.email_edit = QLineEdit(self.manager['email'])
        self.layout.addWidget(self.email_edit)

        self.phone_label = QLabel("Телефон:")
        self.layout.addWidget(self.phone_label)
        self.phone_edit = QLineEdit(self.manager['phone_number'])
        self.layout.addWidget(self.phone_edit)

        self.birthdate_label = QLabel("День рождения:")
        self.layout.addWidget(self.birthdate_label)
        self.birthdate_edit = QDateEdit()
        self.birthdate_edit.setDisplayFormat("yyyy-MM-dd")
        birthdate_str = self.manager['birthdate'].strftime("%Y-%m-%d")
        self.birthdate_edit.setDate(QDate.fromString(birthdate_str, "yyyy-MM-dd"))
        self.layout.addWidget(self.birthdate_edit)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_manager_details)
        self.layout.addWidget(self.save_button)

    def save_manager_details(self):
        self.manager['first_name'] = self.first_name_edit.text()
        self.manager['last_name'] = self.last_name_edit.text()
        self.manager['patronymic'] = self.patronymic_edit.text()
        self.manager['email'] = self.email_edit.text()
        self.manager['phone_number'] = self.phone_edit.text()
        self.manager['birthdate'] = self.birthdate_edit.date().toString("yyyy-MM-dd")
        self.db.update_manager_details(self.manager)
        self.manager_updated.emit()
        self.close()