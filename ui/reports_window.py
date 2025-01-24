from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
import pandas as pd
from PyQt6.QtCore import Qt

class ReportsWindow(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Экспорт данных")
        self.db = db
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.add_export_button("Экспорт пользователей", self.export_users)
        self.add_export_button("Экспорт машин", self.export_cars)
        self.add_export_button("Экспорт заказов", self.export_orders)
        self.add_export_button("Экспорт менеджеров", self.export_managers)
        self.add_export_button("Экспорт истории статусов", self.export_status_history)

    def add_export_button(self, label, function):
        button = QPushButton(label)
        button.clicked.connect(function)
        self.layout.addWidget(button)

    def export_users(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить пользователей", "", "Excel Files (*.xlsx);;All Files (*)")
        if file_path:
            data = self.db.fetch_users()
            self.export_to_excel(file_path, data, ["id", "email", "last_name", "phone_number", "birthdate"])

    def export_cars(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить машины", "", "Excel Files (*.xlsx);;All Files (*)")
        if file_path:
            data = self.db.fetch_cars()
            self.export_to_excel(file_path, data, ["id", "model", "year", "price", "mileage", "color"])

    def export_orders(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить заказы", "", "Excel Files (*.xlsx);;All Files (*)")
        if file_path:
            data = self.db.fetch_orders()
            self.export_to_excel(file_path, data, ["id", "user_id", "car_id", "order_date"])

    def export_managers(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить менеджеров", "", "Excel Files (*.xlsx);;All Files (*)")
        if file_path:
            data = self.db.fetch_managers()
            self.export_to_excel(file_path, data, ["id", "email", "last_name", "phone_number", "birthdate"])

    def export_status_history(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить историю статусов", "",
                                                   "Excel Files (*.xlsx);;All Files (*)")
        if file_path:
            data = self.db.fetch_status_history()
            if not data:
                QMessageBox.warning(self, "Нет данных", "Нет данных для экспорта.")
                return
            self.export_to_excel(file_path, data, ["id", "order_id", "status", "status_date"])

    def export_to_excel(self, file_path, data, columns):
        if not data:
            QMessageBox.warning(self, "Нет данных", "Нет данных для экспорта.")
            return

        df = pd.DataFrame(data, columns=columns)

        df.to_excel(file_path, index=False)

        from openpyxl import load_workbook
        wb = load_workbook(file_path)
        ws = wb.active

        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column].width = adjusted_width

        wb.save(file_path)
        QMessageBox.information(self, "Успех", f"Данные успешно экспортированы в {file_path}.")