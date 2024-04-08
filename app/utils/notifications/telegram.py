from logs import notification_logger as logger
from settings import settings
from loader import bot
from utils.notifications.messages import create_telegram_order_msgs


async def send_startup_notification():
    try:
        await bot.send_message(settings.TELEGRAM_ADMIN_ID, '[ADMIN] Bot is started')
    except Exception as e:
        logger.warning('Some problems with start bot notification: ', e)


async def send_shutdown_notification():
    try:
        await bot.send_message(settings.TELEGRAM_ADMIN_ID, '[ADMIN] Bot is stopped')
    except Exception as e:
        logger.warning('Some problems with stop bot notification: ', e)


async def send_order_notification_to_telegram(order, customer):
    msg1, msg2 = create_telegram_order_msgs(order, customer)
    try:
        await bot.send_message(chat_id=settings.TELEGRAM_NOTIFICATION_ID, text=msg1)
        await bot.send_message(chat_id=settings.TELEGRAM_NOTIFICATION_ID, text=msg2)
        logger.info(f'Order telegram notification is sent to customer {customer}')
    except Exception as e:
        logger.warning('Some problems with telegram order notification: ', e)
