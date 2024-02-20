from aiogram import executor

from loader import dp
from handlers import register_handlers
from database import CreateDB
from utils.notifications import send_startup_notification, send_shutdown_notification


async def on_startup(dp):
    print('Bot is started')
    await send_startup_notification()


async def on_shutdown(dp):
    print('Bot is stopped')
    await send_shutdown_notification()


if __name__ == '__main__':
    CreateDB.create_tables()
    CreateDB.insert_catalog_data()

    register_handlers(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
