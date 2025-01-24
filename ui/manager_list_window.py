from PyQt6.QtWidgets import QDialog,QApplication, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton
from PyQt6.QtCore import Qt
from ui.add_manager_window import AddManagerWindow
from ui.manager_details_window import ManagerDetailsWindow

class ManagerListWindow(QDialog,):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список менеджеров")
        self.db = db
        self.setup_ui()
        self.showMaximized()
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

        self.manager_list = QListWidget()
        self.manager_list.itemClicked.connect(self.open_manager_details)
        self.layout.addWidget(self.manager_list)

        self.add_manager_button = QPushButton("Добавить менеджера")
        self.add_manager_button.clicked.connect(self.add_manager)
        self.layout.addWidget(self.add_manager_button)

        self.load_managers()

    def load_managers(self):
        self.manager_list.clear()
        managers = self.db.get_all_managers()
        for manager in managers:
            item = QListWidgetItem(f"{manager['first_name']} {manager['last_name']} - {manager['phone_number']} - {manager['email']}")
            item.setData(Qt.ItemDataRole.UserRole, manager)
            self.manager_list.addItem(item)

    def open_manager_details(self, item):
        manager = item.data(Qt.ItemDataRole.UserRole)
        if manager is not None:
            self.manager_details_window = ManagerDetailsWindow(manager, self.db, self)
            self.manager_details_window.manager_updated.connect(self.load_managers)
            self.manager_details_window.show()

    def add_manager(self):
        self.add_manager_window = AddManagerWindow(self.db, self)
        self.add_manager_window.manager_added.connect(self.load_managers)
        self.add_manager_window.show()

    def go_back(self):
        if self.parent() is not None:
            self.parent().show()
        self.close()

    def closeEvent(self, event):
        if event.spontaneous():
            QApplication.instance().quit()
        event.accept()