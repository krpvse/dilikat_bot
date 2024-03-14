import smtplib
from email.mime.text import MIMEText
from email.header import Header

from logs import notification_logger as logger
from config import email_from, email_from_password, email_to
from utils.notifications.messages import create_email_order_msg


async def create_server_connection():
    login = email_from
    password = email_from_password

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
    subject, text = await create_email_order_msg(order, customer)

    mime = MIMEText(text, 'plain', 'utf-8')
    mime['Subject'] = Header(subject, 'utf-8')

    try:
        server = await create_server_connection()
        server.sendmail(email_from, email_to, mime.as_string())
        logger.info(f'Order email notification is sent to customer {customer}')
    except Exception as e:
        logger.warning('Some problems with email sending: ', e)
