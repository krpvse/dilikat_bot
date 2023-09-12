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
                f"""SELECT product, quantity FROM basket
                WHERE is_ordered <> TRUE AND fk_tg_user_id = {tg_user_id}"""
            )
            user_basket = cursor.fetchall()

        return user_basket if user_basket else None

    def add_user(self, tg_user_id, tg_username, tg_first_name, tg_last_name):
        with self.connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO users VALUES ({tg_user_id}, '{tg_username}', '{tg_first_name}', '{tg_last_name}')
                ON CONFLICT DO NOTHING"""
            )

    def get_user_info(self, tg_user_id):
        with self.connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT first_name, last_name, phone_number, delivery_address FROM users
                    WHERE first_name IS NOT NULL AND tg_user_id = {tg_user_id}"""
            )
            user_info = cursor.fetchall()

        return user_info[0] if user_info else None

    def add_basket_product(self, tg_user_id, product_id):
        with self.connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO basket VALUES (DEFAULT, '{product_id}', 1, FALSE, '{tg_user_id}')"""
            )

    def remove_basket_product(self, tg_user_id, product_id):
        with self.connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""DELETE FROM basket
                WHERE product = '{product_id}' AND fk_tg_user_id = {tg_user_id}"""
            )