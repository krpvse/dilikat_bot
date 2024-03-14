import asyncio

from logs import db_logger as logger
from database.queries import DBManagement


async def start_catalog_update_loop(interval: int):
    logger.debug('Catalog update loop is started')
    while True:
        await DBManagement.update_catalog_data()
        await asyncio.sleep(interval)
