import asyncio

from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert

from logs import db_logger as logger
from loader import db_engine
from database.models import telegram_user_table, product_table, product_category_table, basket_table, customer_info_table
from database.cache.catalog_cache import save_products_in_cache, get_product_from_cache, get_catalog_from_cache


class DB:
    @staticmethod
    async def get_products():
        logger.debug('Someone requested products')
        products_from_cache = await get_catalog_from_cache()

        if not products_from_cache:
            logger.debug('Products in cache is not found')

            async with db_engine.connect() as connection:
                query = select(product_table, product_category_table).join_from(product_table, product_category_table)

                try:
                    result = await connection.execute(query)
                    products = result.all()
                    logger.debug('Get products from database')
                except Exception as e:
                    logger.warning(f'Some problems with database queries: {e}')

                asyncio.create_task(save_products_in_cache(products))
                return products
        else:
            logger.debug('Get products from cache')
            return products_from_cache

    @staticmethod
    async def get_product(product_id: int):
        logger.debug(f'Someone requested product {product_id}')
        product_from_cache = await get_product_from_cache(product_id)

        if not product_from_cache:
            logger.debug(f'Product {product_id} in cache is not found')
            async with db_engine.connect() as connection:
                query = select(product_table, product_category_table).join_from(product_table, product_category_table)
                filtered_query = query.where(product_table.c.id == product_id)

                try:
                    result = await connection.execute(filtered_query)
                    product = result.one()
                    logger.debug(f'Get product {product_id} from database')
                except Exception as e:
                    logger.warning(f'Some problems with database queries: {e}')

                return product
        else:
            logger.debug(f'Get product {product_id} from cache')
            return product_from_cache

    @staticmethod
    async def add_user(user_id: int, username: str, full_name: str):
        async with db_engine.connect() as connection:
            stmt = insert(telegram_user_table).values(user_id=user_id, username=username, full_name=full_name)
            on_conflict_do_nothing_stmt = stmt.on_conflict_do_nothing(index_elements=['user_id'])
            await connection.execute(on_conflict_do_nothing_stmt)
            await connection.commit()

    @staticmethod
    async def get_customer_info(user_id: int):
        async with db_engine.connect() as connection:
            query = select(telegram_user_table, customer_info_table).join_from(telegram_user_table, customer_info_table)
            filtered_query = query.where(customer_info_table.c.user_id == user_id)
            result = await connection.execute(filtered_query)
            customer_info = result.one_or_none()
            return customer_info

    @staticmethod
    async def change_customer_info(user_id: int, first_name: str, last_name: str, phone_number: str, delivery_address: str):
        async with db_engine.connect() as connection:
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
        async with (db_engine.connect() as connection):
            query = select(basket_table.c.product_id, product_table.c.title, product_table.c.price, basket_table.c.quantity)
            join_query = query.join_from(basket_table, product_table).where(basket_table.c.user_id == user_id)
            result = await connection.execute(join_query)
            basket = result.fetchall()
            return basket

    @staticmethod
    async def add_to_basket(product_id: int, user_id: int):
        async with db_engine.connect() as connection:
            stmt = insert(basket_table).values(product_id=product_id, user_id=user_id)
            on_conflict_do_update_stmt = stmt.on_conflict_do_update(index_elements=['product_id', 'user_id'], set_={
                'quantity': basket_table.c.quantity + 1,
            })
            await connection.execute(on_conflict_do_update_stmt)
            await connection.commit()

    @staticmethod
    async def remove_from_basket(product_id: int, user_id: int):
        async with db_engine.connect() as connection:
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
        async with db_engine.connect() as connection:
            stmt = delete(basket_table).where(basket_table.c.user_id == user_id)
            await connection.execute(stmt)
            await connection.commit()
