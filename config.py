import os

from dotenv import load_dotenv


load_dotenv('.env')

# Bot
bot_token = os.getenv('BOT_TOKEN')
admin_id = os.getenv('ADMIN_ID')


# Database
host = os.getenv('POSTGRES_HOST')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
dbname = os.getenv('POSTGRES_DB')
port = os.getenv('POSTGRES_PORT')
