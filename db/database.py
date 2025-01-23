import mysql.connector
from mysql.connector import Error
from datetime import datetime

class Database:
    def __init__(self, host, name, user, password, port):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.name,
                user=self.user,
                password=self.password,
                port=self.port
            )
            if self.connection.is_connected():
                print("Successfully connected to the database")
                return self.connection
        except Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor
        except Error as e:
            print(f"Error executing query: {e}")
            return None

    def get_makes(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT id, name FROM Makes")
            makes = cursor.fetchall()
            cursor.close()
            return makes
        except Error as e:
            print(f"Error: {e}")
            return []

    def get_user(self, email):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
            result = cursor.fetchone()
            if result:
                return result
            return None
        except Error as e:
            print(f"Error: {e}")
            return None

    def insert_user(self, first_name, last_name, patronymic, phone_number, email, birthdate, password):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO Users (first_name, last_name, patronymic, phone_number, email, birthdate, password, role_id) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, 3)",
                (first_name, last_name, patronymic, phone_number, email, birthdate, password)
            )
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error: {e}")
            return False

    def validate_user(self, email, password):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT role_id, id FROM Users WHERE email = %s AND password = %s", (email, password))
            result = cursor.fetchone()
            if result:
                return result
            return None
        except Error as e:
            print(f"Error: {e}")
            return None

    def get_categories(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Categories")
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(f"Error: {e}")
            return []

    def get_all_cars(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT
                    c.id,
                    m.name AS make,
                    c.model,
                    c.year,
                    c.price,
                    c.mileage
                FROM Cars c
                JOIN Makes m ON c.make_id = m.id;
            """)
            cars = cursor.fetchall()
            cursor.close()
            return cars
        except Error as e:
            print(f"Error: {e}")
            return []

    def search_cars(self, search_term):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT
                    c.id,
                    m.name AS make,
                    c.model,
                    c.year,
                    c.price,
                    c.mileage
                FROM Cars c
                JOIN Makes m ON c.make_id = m.id
                WHERE m.name LIKE %s OR c.model LIKE %s;
            """, (f'%{search_term}%', f'%{search_term}%'))
            cars = cursor.fetchall()
            cursor.close()
            return cars
        except Error as e:
            print(f"Error: {e}")
            return []

    def get_cars_by_make(self, make):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT
                    c.id,
                    m.name AS make,
                    c.model,
                    c.year,
                    c.price,
                    c.mileage
                FROM Cars c
                JOIN Makes m ON c.make_id = m.id
                WHERE m.name = %s;
            """, (make,))
            cars = cursor.fetchall()
            cursor.close()
            return cars
        except Error as e:
            print(f"Error: {e}")
            return []

    def get_user_orders(self, user_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT
                    o.id,
                    o.order_date,
                    c.model,
                    m.name AS make,
                    (SELECT os.title FROM OrderStatuses os
                     JOIN OrderStatusHistory osh ON os.id = osh.status_id
                     WHERE osh.order_id = o.id
                     ORDER BY osh.status_date DESC LIMIT 1) AS order_status
                FROM Orders o
                JOIN Cars c ON o.car_id = c.id
                JOIN Makes m ON c.make_id = m.id
                WHERE o.user_id = %s;
            """, (user_id,))
            orders = cursor.fetchall()
            cursor.close()
            return orders
        except Error as e:
            print(f"Error: {e}")
            return []

    def update_order_status(self, order_id, status_title):
        try:
            cursor = self.connection.cursor()
            status_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""
                INSERT INTO OrderStatusHistory (order_id, status_id, status_date)
                VALUES (%s, (SELECT id FROM OrderStatuses WHERE title = %s), %s);
            """, (order_id, status_title, status_date))
            self.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"Error updating order status: {e}")

    def get_user_info(self, user_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT first_name, last_name, email
                FROM Users
                WHERE id = %s;
            """, (user_id,))
            user_info = cursor.fetchone()
            cursor.close()
            return user_info
        except Error as e:
            print(f"Error: {e}")
            return {}

    def place_order(self, user_id, car_id, manager_id=None):
        try:
            cursor = self.connection.cursor()
            order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""
                INSERT INTO Orders (user_id, car_id, order_date, manager_id)
                VALUES (%s, %s, %s, %s);
            """, (user_id, car_id, order_date, manager_id))
            order_id = cursor.lastrowid
            cursor.execute("""
                INSERT INTO OrderStatusHistory (order_id, status_id, status_date)
                VALUES (%s, (SELECT id FROM OrderStatuses WHERE title = 'в обработке'), %s);
            """, (order_id, order_date))
            self.connection.commit()
            cursor.close()
            print("Order placed successfully")
        except Exception as e:
            print(f"Error placing order: {e}")

    def get_orders_by_car_id(self, car_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT o.*, 
                       (SELECT os.title 
                        FROM OrderStatuses os 
                        JOIN OrderStatusHistory osh ON os.id = osh.status_id 
                        WHERE osh.order_id = o.id 
                        ORDER BY osh.status_date DESC 
                        LIMIT 1) AS order_status
                FROM Orders o 
                WHERE o.car_id = %s
            """
            cursor.execute(query, (car_id,))
            orders = cursor.fetchall()
            cursor.close()
            return orders
        except Error as e:
            print(f"Error: {e}")
            return []