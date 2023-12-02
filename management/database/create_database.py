import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../'))

import psycopg2
import csv

from config import host, user, password, dbname, port


def create_telegram_user_table(connection):
    with connection as connection, connection.cursor() as cursor:
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS telegram_user(
                tg_user_id bigint PRIMARY KEY,
                tg_username varchar(32),
                tg_first_name varchar(64),
                tg_last_name varchar(64)
                )"""
        )


def create_customer_table(connection):
    with connection as connection, connection.cursor() as cursor:
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS customer(
                fk_tg_user_id bigint REFERENCES telegram_user(tg_user_id) NOT NULL,
                first_name varchar(64),
                last_name varchar(64),
                phone_number bigint,
                delivery_address text,
                PRIMARY KEY (fk_tg_user_id)
                )"""
        )


def create_product_category_table(connection):
    with connection as connection, connection.cursor() as cursor:
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS product_category(
                id serial PRIMARY KEY,
                category_name varchar(64) UNIQUE
                )"""
        )


def create_product_table(connection):
    with connection as connection, connection.cursor() as cursor:
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS product(
                product_id int PRIMARY KEY,
                title text UNIQUE NOT NULL,
                description text,
                image_url text,
                price decimal,
                site_url text,
                fk_category_id smallint REFERENCES product_category(id) NOT NULL
                )"""
        )


def create_basket_table(connection):
    with connection as connection, connection.cursor() as cursor:
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS basket(
                fk_product_id int REFERENCES product(product_id),
                quantity smallint DEFAULT 1 CHECK (quantity > 0),
                fk_tg_user_id bigint REFERENCES telegram_user(tg_user_id),
                PRIMARY KEY (fk_product_id, fk_tg_user_id)
                )"""
        )


def create_order_table(connection):
    with connection as connection, connection.cursor() as cursor:
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS customer_order(
                id serial PRIMARY KEY,
                fk_product_id int REFERENCES product(product_id),
                quantity smallint DEFAULT 1 CHECK (quantity > 0),
                fk_tg_user_id bigint REFERENCES telegram_user(tg_user_id),
                order_date date NOT NULL DEFAULT CURRENT_DATE
                )"""
        )


def create_bot_management_table(connection):
    with connection as connection, connection.cursor() as cursor:
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS bot_management(
                tg_user_id bigint PRIMARY KEY,
                main_message_id bigint NOT NULL
                )"""
        )


def add_product_categories(connection):
    with connection as connection, connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO product_category (category_name) VALUES 
            ('3D принтеры'), ('3D сканеры'),
            ('Фрезерные станки'), ('Печи'),
            ('Фотополимеры'), ('CAD CAM блоки'),
            ('Фрезы')
            ON CONFLICT DO NOTHING"""
        )


def add_products_from_csv(connection):
    with open('management/database/products.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        products = [product for product in reader if product][1:]

    for product in products:
        with connection as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO product
                (product_id, title, description, image_url, 
                price, site_url, fk_category_id)
                VALUES ({product[0]}, '{product[1]}', '{product[2]}', '{product[3]}', 
                        {product[4]}, '{product[5]}', {product[6]})
                ON CONFLICT DO NOTHING"""
            )


def create_database():
    connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=dbname,
            port=port,
        )

    create_telegram_user_table(connection)
    create_customer_table(connection)
    create_product_category_table(connection)
    create_product_table(connection)
    create_basket_table(connection)
    create_order_table(connection)
    create_bot_management_table(connection)
    
    add_product_categories(connection)
    add_products_from_csv(connection)


if __name__ == '__main__':
    create_database()
