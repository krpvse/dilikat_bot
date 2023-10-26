from datetime import datetime
import psycopg2

from config import host, user, password, dbname, port


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=dbname,
            port=port,
        )

    def get_user_basket(self, tg_user_id):
        with self.connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT product_title, quantity FROM orders
                WHERE is_ordered = FALSE AND fk_tg_user_id = {tg_user_id}"""
            )
            user_basket = cursor.fetchall()
        return user_basket

    def add_user(self, tg_user_id, tg_username, tg_first_name, tg_last_name):
        with self.connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO customers (tg_user_id, tg_username, tg_first_name, tg_last_name, last_activity)
                VALUES ({tg_user_id}, '{tg_username}', '{tg_first_name}', '{tg_last_name}', 
                '{datetime.now().strftime('%Y-%m-%d')}')
                ON CONFLICT DO NOTHING"""
            )

    def get_user_info(self, tg_user_id):
        with self.connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT first_name, last_name, phone_number, delivery_address FROM customers
                    WHERE first_name IS NOT NULL AND tg_user_id = {tg_user_id}"""
            )
            user_info = cursor.fetchall()
        return user_info

    def add_basket_product(self, tg_user_id, product_id, product_title):
        with self.connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""UPDATE orders SET quantity = quantity + 1
                WHERE fk_tg_user_id = {tg_user_id} AND product_id = {product_id} and product_title = '{product_title}'
                AND is_ordered = FALSE
                ON CONFLICT DO INSERT INTO orders (fk_tg_user_id, product_id, product_title, order_date)
                VALUES ({tg_user_id}, {product_id}, '{product_title}')"""
            )

    def remove_basket_product(self, tg_user_id, product_id, product_title):
        with self.connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""UPDATE orders SET quantity = quantity - 1
                WHERE fk_tg_user_id = {tg_user_id} AND product_id = {product_id} and product_title = '{product_title}'
                AND is_ordered = FALSE
                ON CONFLICT DO DELETE FROM orders 
                WHERE fk_tg_user_id = {tg_user_id} AND product_id = {product_id} and product_title = '{product_title}'
                AND is_ordered = FALSE"""
            )

    def change_user_info(self, tg_user_id, first_name, last_name, phone_number, delivery_address):
        with self.connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""UPDATE customers SET (first_name, last_name, phone_number, delivery_address) = 
                ('{first_name}', '{last_name}', {phone_number}, '{delivery_address}')
                WHERE tg_user_id = {tg_user_id}"""
            )
