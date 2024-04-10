from typing import Optional

import smtplib
from email.mime.text import MIMEText
from email.header import Header

from settings import settings
from loader import bot
from logs import notification_logger as logger


class Notification:
    def __init__(self, text: str = None, **kwargs):
        self.message = text

    @staticmethod
    def _build_message(**kwargs):
        """Build message depends on notification type"""
        pass

    def send(self):
        """Send message depends on notification type"""
        pass


class AdminBotNotification:
    @staticmethod
    async def send_startup_notification():
        try:
            await bot.send_message(settings.TELEGRAM_ADMIN_ID, 'Bot is started')
        except Exception as e:
            logger.warning(f'Some problem with start notification: {e}')

    @staticmethod
    async def send_shutdown_notification():
        try:
            await bot.send_message(settings.TELEGRAM_ADMIN_ID, 'Bot is stopped')
        except Exception as e:
            logger.warning(f'Some problem with stop notification: {e}')


class OrderNotification(Notification):
    def __init__(
            self,
            telegram_username: Optional[str],
            telegram_name: str,
            name: str,
            phone: int,
            address: str,
            order: list[list]
    ):
        super().__init__()
        self.message = self._build_message(telegram_username, telegram_name, name, phone, address, order)

    @staticmethod
    def _build_message(
            telegram_username: Optional[str],
            telegram_name: str,
            name: str,
            phone: int,
            address: str,
            order: list[list]
    ):
        message = (f'Новый заказ из Telegram-бота!\n\n'
                   f'Логин в Telegram: {telegram_username if telegram_username else "не указано"}\n'
                   f'Имя в Telegram: {telegram_name}\n'
                   f'Имя: {name}\n'
                   f'Телефон: {phone}\n'
                   f'Адрес: {address}')

        message += f'\n\nДанные заказа:\n'
        for product in order:
            message += (f'Товар: {product[1]}\n'
                        f'Цена: {product[2]} руб.\n'
                        f'Количество: {product[3]} шт.\n\n')
        return message


class EmailNotification(Notification):
    def send(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        try:
            server.login(settings.EMAIL_NOTIFICATION_FROM_LOGIN, settings.EMAIL_NOTIFICATION_FROM_PASSWORD)
        except Exception as e:
            logger.warning(f'Some problem with email sending: {e}\nLogin: {settings.EMAIL_NOTIFICATION_FROM_LOGIN}')
            return

        mime = MIMEText(self.message, 'plain', 'utf-8')
        mime['Subject'] = Header('Уведомление из Telegram-бота', 'utf-8')

        try:
            server.sendmail(settings.EMAIL_NOTIFICATION_FROM_LOGIN, settings.EMAIL_NOTIFICATION_TO, mime.as_string())
        except Exception as e:
            logger.warning(f'Some problem with email sending: {e}\nLogin: {settings.EMAIL_FROM_LOGIN}\nMessage: {self.message}')


class OrderEmailNotification(OrderNotification, EmailNotification):
    pass


class OrderTelegramNotification(OrderNotification):
    async def send(self):
        try:
            await bot.send_message(chat_id=settings.TELEGRAM_ADMIN_ID, text=self.message)
        except Exception as e:
            logger.warning(f'Some problem with telegram notification: {e}')
