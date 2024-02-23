import os

from dotenv import load_dotenv


load_dotenv('.env')


# Telegram Bot
bot_token = os.getenv('BOT_TOKEN')
admin_id = int(os.getenv('ADMIN_ID'))
order_notification_id = int(os.getenv('ORDER_NOTIFICATION_ID'))


# PostgreSQL
db_host = os.getenv('POSTGRES_HOST')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_name = os.getenv('POSTGRES_DB')
db_port = os.getenv('POSTGRES_PORT')

catalog_updating_interval = 3600  # 3600 sec = 1 hour


# Redis
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')

catalog_redis_expire_time = 600000  # 600 000 ms = 10 min


# Email
email_from = os.getenv('EMAIL_FROM')
email_from_password = os.getenv('EMAIL_FROM_PASSWORD')
email_to = os.getenv('EMAIL_TO')
