from config import admin_id, order_notification_id
from loader import bot
from .messages import create_telegram_order_msgs


async def send_startup_notification():
    try:
        await bot.send_message(admin_id, '[ADMIN] Bot is started')
    except Exception as e:
        print('Error with sending notifications to admin: ', e)
        print('Check out your Telegram accounts')


async def send_shutdown_notification():
    try:
        await bot.send_message(admin_id, '[ADMIN] Bot is stopped')
    except Exception as e:
        print('Error with sending notifications to admin: ', e)
        print('Check out your Telegram accounts')


async def send_order_notification_to_telegram(order, customer):
    msg1, msg2 = await create_telegram_order_msgs(order, customer)
    try:
        await bot.send_message(chat_id=order_notification_id, text=msg1)
        await bot.send_message(chat_id=order_notification_id, text=msg2)
    except Exception as e:
        print('Error with sending order notifications: ', e)
        print('Check out your Telegram accounts')
