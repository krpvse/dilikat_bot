import asyncio
from aiogram import executor

from loader import dp
from handlers import register_handlers
from database import DBManagement
from database.utils import start_catalog_update_loop
from utils.notifications import AdminBotNotification
from settings import settings
from logs import init_logger, bot_logger as logger


async def on_startup(dp):
    logger.debug('Bot started')

    await DBManagement.create_tables()
    asyncio.create_task(start_catalog_update_loop(interval=settings.CATALOG_UPDATING_INTERVAL))

    await AdminBotNotification.send_startup_notification()


async def on_shutdown(dp):
    logger.debug('Bot stopped')
    await AdminBotNotification.send_shutdown_notification()


if __name__ == '__main__':
    init_logger('bot')

    register_handlers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
