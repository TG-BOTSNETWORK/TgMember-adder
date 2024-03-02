#Developed by: santhu
#Telegram: @my_name_is_nobitha

from pyrogram import Client as adder
from config.config import Config

addboy = adder(
       "adder_boy",
       api_id=Config.API_ID,
       api_hash=Config.API_HASH,
       bot_token=Config.BOT_TOKEN,
       plugins=dict(root="adder.modules")
)
