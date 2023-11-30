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

    def get_customer_basket(self, tg_user_id):
        with self.connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT title, quantity FROM basket
                INNER JOIN product ON product.product_id = basket.fk_product_id
                WHERE fk_tg_user_id = {tg_user_id}"""
            )
            user_basket = cursor.fetchall()
        return user_basket

    def add_user(self, tg_user_id, tg_username, tg_first_name, tg_last_name):
        with self.connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO telegram_user (tg_user_id, tg_username, tg_first_name, tg_last_name)
                VALUES ({tg_user_id}, '{tg_username}', '{tg_first_name}', '{tg_last_name}')
                ON CONFLICT DO NOTHING"""
            )

    def get_customer_info(self, tg_user_id):
        with self.connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT first_name, last_name, phone_number, delivery_address FROM customer
                    WHERE fk_tg_user_id = {tg_user_id}"""
            )
            customer_info = cursor.fetchone()
        return customer_info

    def change_customer_info(self, tg_user_id, first_name, last_name, phone_number, delivery_address):
        with self.connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO customer (fk_tg_user_id, first_name, last_name, phone_number, delivery_address)
                VALUES ({tg_user_id}, '{first_name}', '{last_name}', {phone_number}, '{delivery_address}')
                ON CONFLICT (fk_tg_user_id) DO 
                UPDATE SET (first_name, last_name, phone_number, delivery_address) = 
                ('{first_name}', '{last_name}', {phone_number}, '{delivery_address}')
                WHERE customer.fk_tg_user_id = {tg_user_id}"""
            )

    def get_products(self):
        with self.connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM product
                INNER JOIN product_category ON product.fk_category_id = product_category.id"""
            )
            products = cursor.fetchall()
        return products

    def add_basket_product(self, tg_user_id, product_id):
        with self.connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO basket (fk_product_id, fk_tg_user_id)
                VALUES ({product_id}, {tg_user_id})
                ON CONFLICT (fk_product_id, fk_tg_user_id) DO
                UPDATE SET quantity = basket.quantity + 1
                WHERE basket.fk_tg_user_id = {tg_user_id} AND basket.fk_product_id = {product_id}"""
            )

    def remove_basket_product(self, tg_user_id, product_id):
        with self.connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""UPDATE basket SET quantity = quantity - 1
                WHERE fk_tg_user_id = {tg_user_id} AND fk_product_id = {product_id} AND quantity > 1;
                DELETE FROM basket
                WHERE fk_tg_user_id = {tg_user_id} AND fk_product_id = {product_id} AND quantity = 1;"""
            )

    def remove_customer_basket(self, tg_user_id):
        with self.connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""DELETE FROM basket WHERE fk_tg_user_id = {tg_user_id}"""
            )

    def create_order(self, tg_user_id):
        with self.connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO customer_order (fk_product_id, quantity, fk_tg_user_id)
                SELECT fk_product_id, quantity, fk_tg_user_id
                FROM basket WHERE fk_tg_user_id = {tg_user_id}"""
            )
