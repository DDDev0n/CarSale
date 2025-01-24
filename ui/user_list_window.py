from PyQt6.QtWidgets import QDialog,QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel

class UserListWindow(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список пользователей")
        self.db = db
        self.showMaximized()
        self.setup_ui()
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #222222;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
            }
            QTableWidget {
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

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.back_button_layout = QHBoxLayout()
        self.back_button_layout.addStretch()
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)
        self.back_button_layout.addWidget(self.back_button)
        self.layout.addLayout(self.back_button_layout)

        self.user_list = QListWidget()
        self.layout.addWidget(self.user_list)

        self.load_users()

    def load_users(self):
        users = self.db.get_all_users()
        for user in users:
            self.user_list.addItem(f"{user['first_name']} {user['last_name']} - {user['email']}")

    def go_back(self):
        if self.parent() is not None:
            self.parent().show()
        self.close()

    def closeEvent(self, event):
        if event.spontaneous():
            QApplication.instance().quit()
        event.accept()