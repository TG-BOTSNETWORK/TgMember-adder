#Developed by: santhu
#Telegram: @my_name_is_nobitha

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from config.config import Config 
from adder import addboy 

start_keyboard = InlineKeyboardMarkup([[
      InlineKeyboardButton("🪪 Login", callback_data="login"),
      InlineKeyboardButton("Adder 🎁", callback_data="adder"),
      ],[
      InlineKeyboardButton("🛡️ Help Section 🛡️", callback_data="help")
]])

@addboy.on_message(filters.command("start") & filters.private)
async def start(addboy, message):
    await message.reply_text(
        text="Hello {}\n\nIam a member adder bot i can add members in your group simply and smoothly for more information click below **Help Section** button or /help command to see information.".format(message.from_user.mention()),
        reply_markup=start_keyboard,
    )
