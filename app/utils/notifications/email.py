import smtplib
from email.mime.text import MIMEText
from email.header import Header

from logs import notification_logger as logger
from settings import settings
from utils.notifications.messages import create_email_order_msg


def create_server_connection():
    login = settings.EMAIL_NOTIFICATION_FROM_LOGIN
    password = settings.EMAIL_NOTIFICATION_FROM_PASSWORD

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(login, password)
        login = True
    except Exception as e:
        logger.warning('Some problems with smtp connection: ', e)
        login = False

    return server if login else None


async def send_order_notification_to_email(order, customer):
    subject, text = create_email_order_msg(order, customer)

    mime = MIMEText(text, 'plain', 'utf-8')
    mime['Subject'] = Header(subject, 'utf-8')

    try:
        server = create_server_connection()
        server.sendmail(settings.EMAIL_NOTIFICATION_FROM_LOGIN, settings.EMAIL_NOTIFICATION_TO, mime.as_string())
        logger.info(f'Order email notification is sent to customer {customer}')
    except Exception as e:
        logger.warning('Some problems with email sending: ', e)
