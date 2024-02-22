from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert

from ..database import engine
from ..models import telegram_user_table, product_table, product_category_table, basket_table, customer_info_table


class DB:
    @staticmethod
    async def get_products():
        async with engine.connect() as connection:
            query = select(product_table, product_category_table).join_from(product_table, product_category_table)
            result = await connection.execute(query)
            products = result.all()
            return products

    @staticmethod
    async def get_product(product_id: int):
        async with engine.connect() as connection:
            query = select(product_table, product_category_table).join_from(product_table, product_category_table)
            filtered_query = query.where(product_table.c.id == product_id)
            result = await connection.execute(filtered_query)
            product = result.one()
            return product

    @staticmethod
    async def add_user(user_id: int, username: str, full_name: str):
        async with engine.connect() as connection:
            stmt = insert(telegram_user_table).values(user_id=user_id, username=username, full_name=full_name)
            on_conflict_do_nothing_stmt = stmt.on_conflict_do_nothing(index_elements=['user_id'])
            await connection.execute(on_conflict_do_nothing_stmt)
            await connection.commit()

    @staticmethod
    async def get_customer_info(user_id: int):
        async with engine.connect() as connection:
            query = select(telegram_user_table, customer_info_table).join_from(telegram_user_table, customer_info_table)
            filtered_query = query.where(customer_info_table.c.user_id == user_id)
            result = await connection.execute(filtered_query)
            customer_info = result.one_or_none()
            return customer_info

    @staticmethod
    async def change_customer_info(user_id: int, first_name: str, last_name: str, phone_number: str, delivery_address: str):
        async with engine.connect() as connection:
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

            await connection.execute(on_conflict_do_update_stmt)
            await connection.commit()

    @staticmethod
    async def get_basket(user_id: int):
        async with (engine.connect() as connection):
            query = select(basket_table.c.product_id, product_table.c.title, product_table.c.price, basket_table.c.quantity)
            join_query = query.join_from(basket_table, product_table).where(basket_table.c.user_id == user_id)
            result = await connection.execute(join_query)
            basket = result.fetchall()
            return basket

    @staticmethod
    async def add_to_basket(product_id: int, user_id: int):
        async with engine.connect() as connection:
            stmt = insert(basket_table).values(product_id=product_id, user_id=user_id)
            on_conflict_do_update_stmt = stmt.on_conflict_do_update(index_elements=['product_id', 'user_id'], set_={
                'quantity': basket_table.c.quantity + 1,
            })
            await connection.execute(on_conflict_do_update_stmt)
            await connection.commit()

    @staticmethod
    async def remove_from_basket(product_id: int, user_id: int):
        async with engine.connect() as connection:
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

            await connection.execute(delete_stmt)
            await connection.execute(update_stmt)
            await connection.commit()

    @staticmethod
    async def clear_basket(user_id: int):
        async with engine.connect() as connection:
            stmt = delete(basket_table).where(basket_table.c.user_id == user_id)
            await connection.execute(stmt)
            await connection.commit()
