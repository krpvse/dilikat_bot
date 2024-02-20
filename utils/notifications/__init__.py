from .telegram import send_order_notification_to_telegram, send_startup_notification, send_shutdown_notification
from .email import send_order_notification_to_email


async def send_order_notification(order, customer, to_telegram=True, to_email=True):
    if to_telegram:
        await send_order_notification_to_telegram(order, customer)
    if to_email:
        await send_order_notification_to_email(order, customer)
