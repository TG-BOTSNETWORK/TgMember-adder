#Developed by: santhu
#Telegram: @my_name_is_nobitha

import os 
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(getenv("API_ID", "22363963"))
    API_HASH = getenv("API_HASH", "5c096f7e8fd4c38c035d53dc5a85d768")
    BOT_TOKEN = getenv("BOT_TOKEN", "6885430381:AAHjzM8P6Zk2eCyLQlv4mF5qbsaBRYhnV4U")
    BOT_NAME = getenv("BOT_NAME", "Tg Member Adder")
    BOT_USERNAME = getenv("BOT_USERNAME", "")
    DB_MAN = getenv("DB_MAN", "mongodb+srv://santhoshpodili874:SANTHU7981@cluster0.rz2dqev.mongodb.net/Cluster0?retryWrites=true&w=majority")
