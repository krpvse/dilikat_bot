import psycopg2
from config import host, user, password, dbname, port


def add_user(tg_user_id, tg_username, tg_first_name, tg_last_name):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        dbname=dbname,
        port=port,
    )

    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO users (tg_user_id, tg_username, tg_first_name, tg_last_name) VALUES 
            ({tg_user_id}, '{tg_username}', '{tg_first_name}', '{tg_last_name}')
            ON CONFLICT DO NOTHING;"""
        )

    connection.close()


def get_user_info(tg_user_id):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        dbname=dbname,
        port=port,
    )

    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT first_name, last_name, phone_number, delivery_address FROM users
            WHERE tg_user_id = {tg_user_id};"""
        )
        user_info = cursor.fetchall()[0]

    connection.close()
    return user_info


