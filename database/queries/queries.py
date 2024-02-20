from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert

from ..database import engine
from ..models import telegram_user_table, product_table, product_category_table, basket_table, customer_info_table


class DB:
    def __init__(self):
        pass

    @staticmethod
    def get_products():
        with engine.connect() as connection:
            query = select(product_table, product_category_table).join_from(product_table, product_category_table)
            products = connection.execute(query).all()
            return products

    @staticmethod
    def get_product(product_id: int):
        with engine.connect() as connection:
            query = select(product_table, product_category_table).join_from(product_table, product_category_table)
            filtered_query = query.where(product_table.c.id == product_id)
            product = connection.execute(filtered_query).one()
            return product

    @staticmethod
    def add_user(user_id: int, username: str, full_name: str):
        with engine.connect() as connection:
            stmt = insert(telegram_user_table).values(user_id=user_id, username=username, full_name=full_name)
            on_conflict_do_nothing_stmt = stmt.on_conflict_do_nothing(index_elements=['user_id'])
            connection.execute(on_conflict_do_nothing_stmt)
            connection.commit()

    @staticmethod
    def get_customer_info(user_id: int):
        with (engine.connect() as connection):
            query = select(telegram_user_table, customer_info_table).join_from(telegram_user_table, customer_info_table)
            filtered_query = query.where(customer_info_table.c.user_id == user_id)
            customer_info = connection.execute(filtered_query).one_or_none()
            return customer_info

    @staticmethod
    def change_customer_info(user_id: int, first_name: str, last_name: str, phone_number: int, delivery_address: str):
        with engine.connect() as connection:
            stmt = insert(customer_info_table).values(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                delivery_address=delivery_address,
            )
            on_conflict_do_update_stmt = stmt.on_conflict_do_update(index_elements=['user_id'], set_={
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone_number,
                'delivery_address': delivery_address,
            })

            connection.execute(on_conflict_do_update_stmt)
            connection.commit()

    @staticmethod
    def get_basket(user_id: int):
        with (engine.connect() as connection):
            query = select(basket_table.c.product_id, product_table.c.title, product_table.c.price, basket_table.c.quantity)
            join_query = query.join_from(basket_table, product_table).where(basket_table.c.user_id == user_id)
            basket = connection.execute(join_query).fetchall()
            return basket

    @staticmethod
    def add_to_basket(product_id: int, user_id: int):
        with engine.connect() as connection:
            stmt = insert(basket_table).values(product_id=product_id, user_id=user_id)
            on_conflict_do_update_stmt = stmt.on_conflict_do_update(index_elements=['product_id', 'user_id'], set_={
                'quantity': basket_table.c.quantity + 1,
            })
            connection.execute(on_conflict_do_update_stmt)
            connection.commit()

    @staticmethod
    def remove_from_basket(product_id: int, user_id: int):
        with engine.connect() as connection:
            delete_stmt = delete(basket_table).where(
                basket_table.c.quantity == 1,
                basket_table.c.product_id == product_id,
                basket_table.c.user_id == user_id,
            )
            update_stmt = update(basket_table).where(
                basket_table.c.quantity > 1,
                basket_table.c.product_id == product_id,
                basket_table.c.user_id == user_id,
            ).values(quantity=basket_table.c.quantity - 1)

            connection.execute(delete_stmt)
            connection.execute(update_stmt)
            connection.commit()

    @staticmethod
    def clear_basket(user_id: int):
        with engine.connect() as connection:
            stmt = delete(basket_table).where(basket_table.c.user_id == user_id)
            connection.execute(stmt)
            connection.commit()
