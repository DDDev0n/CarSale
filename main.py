import sys
import json
from PyQt6.QtWidgets import QApplication, QMessageBox
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from db.database import Database

def load_config(config_file="config.json"):
    """Loads database configuration from a JSON file."""
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        QMessageBox.critical(None, "Configuration Error", f"Configuration file '{config_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        QMessageBox.critical(None, "Configuration Error", f"Invalid JSON format in '{config_file}'.")
        sys.exit(1)

def main():
    app = QApplication(sys.argv)
    config = load_config()

    db = Database(config["db_host"], config["db_name"], config["db_user"], config["db_password"], config["db_port"])
    if db.connect() is None:
        QMessageBox.critical(None, "Database Error", "Failed to connect to the database. Please check your configuration.")
        sys.exit(1)

    login_window = LoginWindow(db)

    def show_main_window(role):
        main_window = MainWindow(role, db)
        main_window.show()

    login_window.login_successful.connect(show_main_window)
    login_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()