import asyncio
from .queries import CreateDB


async def start_catalog_update_loop(interval: int):
    while True:
        CreateDB.update_catalog_data()
        await asyncio.sleep(interval)
