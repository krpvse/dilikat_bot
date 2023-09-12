import os
from dotenv import load_dotenv

load_dotenv('.env')

# Bot
bot_token = os.getenv('BOT_TOKEN')

# Database
host = os.getenv('HOST')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
dbname = os.getenv('DBNAME')
port = os.getenv('PORT')