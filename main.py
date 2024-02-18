from aiogram import executor

from config import admin_id
from loader import bot, dp
from handlers import register_handlers
from database import CreateDB


async def on_startup(dp):
    print('Bot is starting')
    try:
        await bot.send_message(admin_id, '[ADMIN] Bot is starting')
    except Exception as e:
        print('Error with sending notifications to admin: ', e)
        print('Check out connection with bot or admin id in settings')


if __name__ == '__main__':
    CreateDB.create_tables()
    CreateDB.insert_catalog_data()

    register_handlers(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
