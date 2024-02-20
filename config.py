import os

from dotenv import load_dotenv


load_dotenv('.env')


# Bot
bot_token = os.getenv('BOT_TOKEN')
admin_id = int(os.getenv('ADMIN_ID'))
order_notification_id = int(os.getenv('ORDER_NOTIFICATION_ID'))


# Database
host = os.getenv('POSTGRES_HOST')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
dbname = os.getenv('POSTGRES_DB')
port = os.getenv('POSTGRES_PORT')


# Email
email_from = os.getenv('EMAIL_FROM')
email_from_password = os.getenv('EMAIL_FROM_PASSWORD')
email_to = os.getenv('EMAIL_TO')
