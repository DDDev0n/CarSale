import mysql.connector
from mysql.connector import Error
from datetime import datetime
from PIL import Image
import io

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
            result = cursor.fetchall()
            cursor.close()
            self.connection.commit()
            return result
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

    def get_paid_orders(self):
        query = """
        SELECT Orders.id, Cars.model, OrderStatuses.title
        FROM Orders
        JOIN Cars ON Orders.car_id = Cars.id
        JOIN (
            SELECT order_id, MAX(status_date) AS latest_status_date
            FROM OrderStatusHistory
            GROUP BY order_id
        ) AS LatestStatus ON Orders.id = LatestStatus.order_id
        JOIN OrderStatusHistory ON Orders.id = OrderStatusHistory.order_id
            AND LatestStatus.latest_status_date = OrderStatusHistory.status_date
        JOIN OrderStatuses ON OrderStatusHistory.status_id = OrderStatuses.id
        WHERE OrderStatuses.title = 'Оплачен'
        """
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        orders = cursor.fetchall()
        cursor.close()
        return [{'id': row['id'], 'car': row['model'], 'status': row['title']} for row in orders]

    def get_order_details(self, order_id):
        query = """
        SELECT
            o.id,
            o.order_date,
            c.model AS car,
            m.name AS make,
            u.first_name,
            u.last_name,
            u.email,
            (SELECT os.title FROM OrderStatuses os
             JOIN OrderStatusHistory osh ON os.id = osh.status_id
             WHERE osh.order_id = o.id
             ORDER BY osh.status_date DESC LIMIT 1) AS status
        FROM Orders o
        JOIN Cars c ON o.car_id = c.id
        JOIN Makes m ON c.make_id = m.id
        JOIN Users u ON o.user_id = u.id
        WHERE o.id = %s;
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, (order_id,))
            order_details = cursor.fetchone()
            cursor.close()
            return order_details
        except Error as e:
            print(f"Error: {e}")
            return None

    def get_customer_info_by_order(self, order_id):
        query = """
        SELECT u.first_name, u.last_name, u.email, u.phone_number
        FROM Users u
        JOIN Orders o ON u.id = o.user_id
        WHERE o.id = %s;
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, (order_id,))
            customer_info = cursor.fetchone()
            cursor.close()
            return customer_info
        except Error as e:
            print(f"Error: {e}")
            return None

    def accept_order(self, order_id, manager_id):
        try:
            cursor = self.connection.cursor()
            status_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""
                UPDATE Orders
                SET manager_id = %s
                WHERE id = %s;
            """, (manager_id, order_id))
            cursor.execute("""
                INSERT INTO OrderStatusHistory (order_id, status_id, status_date)
                VALUES (%s, (SELECT id FROM OrderStatuses WHERE title = 'Принят'), %s);
            """, (order_id, status_date))
            self.connection.commit()
            cursor.close()
            print("Order accepted successfully")
        except Exception as e:
            print(f"Error accepting order: {e}")

    def cancel_order(self, order_id):
        try:
            cursor = self.connection.cursor()
            status_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""
                INSERT INTO OrderStatusHistory (order_id, status_id, status_date)
                VALUES (%s, (SELECT id FROM OrderStatuses WHERE title = 'Отменён'), %s);
            """, (order_id, status_date))
            self.connection.commit()
            cursor.close()
            print("Order cancelled successfully")
        except Exception as e:
            print(f"Error cancelling order: {e}")

    def get_orders_by_manager(self, manager_id):
        query = """
        SELECT o.id, c.model AS car, 
               (SELECT os.title FROM OrderStatuses os
                JOIN OrderStatusHistory osh ON os.id = osh.status_id
                WHERE osh.order_id = o.id
                ORDER BY osh.status_date DESC LIMIT 1) AS status
        FROM Orders o
        JOIN Cars c ON o.car_id = c.id
        WHERE o.manager_id = %s;
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, (manager_id,))
            orders = cursor.fetchall()
            cursor.close()
            return orders
        except Error as e:
            print(f"Error: {e}")
            return []

    def get_accepted_order_details(self, order_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT o.id, c.model, c.year, c.color, os.title as status
                FROM Orders o
                JOIN Cars c ON o.car_id = c.id
                JOIN OrderStatusHistory osh ON o.id = osh.order_id
                JOIN OrderStatuses os ON osh.status_id = os.id
                WHERE o.id = %s
                ORDER BY osh.status_date DESC
                LIMIT 1;
            """, (order_id,))
            order_details = cursor.fetchone()
            cursor.close()
            return {
                'id': order_details[0],
                'car': order_details[1],
                'model': order_details[1],
                'year': order_details[2],
                'color': order_details[3],
                'status': order_details[4]
            }
        except Exception as e:
            print(f"Error retrieving order details: {e}")
            return None

    def resize_photo(self, photo_data, max_width, max_height):
        image = Image.open(io.BytesIO(photo_data))
        image.thumbnail((max_width, max_height))
        byte_arr = io.BytesIO()
        image.save(byte_arr, format='JPEG')
        return byte_arr.getvalue()


    def get_car_details(self, car_id):
        query = "SELECT id, model, (select name from Makes where id = make_id) as make, year, color, price, photo FROM cars WHERE id = %s"
        result = self.execute_query(query, (car_id,))
        if result:
            car_details = result[0]
            if car_details['photo']:
                car_details['photo'] = self.resize_photo(car_details['photo'], 800, 600)
            else:
                car_details['photo'] = "\nНет доступных фотографий"
            return car_details
        return None

    def order_car(self, car_id, user_id):
        try:
            cursor = self.connection.cursor()
            order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""
                INSERT INTO Orders (user_id, car_id, order_date)
                VALUES (%s, %s, %s);
            """, (user_id, car_id, order_date))
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

    def get_car_types(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT name FROM Categories")
        return cursor.fetchall()

    def add_car(self, make, model, year, color, category, price, mileage, photo):
        cursor = self.connection.cursor(dictionary=True)

        cursor.execute("SELECT id FROM Makes WHERE name = %s", (make,))
        make_id = cursor.fetchone()['id']

        cursor.execute("SELECT id FROM Categories WHERE name = %s", (category,))
        category_id = cursor.fetchone()['id']

        if photo and len(photo) > 16 * 1024 * 1024:
            raise ValueError("Photo size exceeds the limit of 16MB")

        cursor.execute("""
            INSERT INTO Cars (make_id, model, year, color, category_id, price, mileage, photo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (make_id, model, year, color, category_id, price, mileage, photo))

        self.connection.commit()
        cursor.close()

    def get_all_users(self):
        query = "SELECT id, email, first_name, last_name, phone_number FROM Users WHERE role_id = 3"
        result = self.execute_query(query)
        if result:
            return [{'id': user['id'], 'email': user['email'], 'first_name': user['first_name'],
                     'last_name': user['last_name'], 'phone_number': user['phone_number']} for user in result]
        return []

    def get_all_managers(self):
        query = "SELECT id, email, first_name, last_name, patronymic, phone_number, birthdate FROM Users WHERE role_id = 2"
        result = self.execute_query(query)
        if result:
            return [{'id': manager['id'], 'email': manager['email'], 'first_name': manager['first_name'],
                     'last_name': manager['last_name'], 'patronymic': manager['patronymic'],
                     'phone_number': manager['phone_number'], 'birthdate': manager['birthdate']} for manager in result]
        return []

    def update_manager_details(self, manager):
        query = """
            UPDATE Users
            SET first_name = %s, last_name = %s, patronymic = %s, email = %s, phone_number = %s, birthdate = %s
            WHERE id = %s
        """
        self.execute_query(query, (manager['first_name'], manager['last_name'], manager['patronymic'],
                                   manager['email'], manager['phone_number'], manager['birthdate'], manager['id']))
        self.connection.commit()

    def insert_manager(self, first_name, last_name, patronymic, phone_number, email, birthdate, password):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO Users (first_name, last_name, patronymic, phone_number, email, birthdate, password, role_id) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, 2)",
                (first_name, last_name, patronymic, phone_number, email, birthdate, password)
            )
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error: {e}")
            return False

    def get_all_makes(self):
        query = "SELECT id, name FROM Makes"
        cursor = self.connection.cursor()
        cursor.execute(query)
        makes = cursor.fetchall()
        return [{'id': make[0], 'name': make[1]} for make in makes]

    def get_all_categories(self):
        query = "SELECT id, name FROM Categories"
        cursor = self.connection.cursor()
        cursor.execute(query)
        categories = cursor.fetchall()
        return [{'id': category[0], 'name': category[1]} for category in categories]

    def admin_get_all_cars(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT
                    c.id,
                    m.name AS make,
                    c.model,
                    c.year,
                    c.price,
                    c.mileage,
                    c.color,
                    cat.name AS category
                FROM Cars c
                JOIN Categories cat ON cat.id = c.category_id
                JOIN Makes m ON c.make_id = m.id;
            """)
            cars = cursor.fetchall()
            cursor.close()
            return cars
        except Error as e:
            print(f"Error: {e}")
            return []

    def update_car(self, car_id, car_details):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE Cars
                SET make_id = %s, model = %s, year = %s, price = %s, mileage = %s, color = %s, category_id = %s
                WHERE id = %s
            """, (
                car_details['make_id'],
                car_details['model'],
                car_details['year'],
                car_details['price'],
                car_details['mileage'],
                car_details['color'],
                car_details['category_id'],
                car_id
            ))
            self.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"Error: {e}")
            raise

    def delete_car(self, car_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM Orders WHERE car_id = %s", (car_id,))
            cursor.execute("DELETE FROM Cars WHERE id = %s", (car_id,))
            self.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"Error: {e}")
            raise