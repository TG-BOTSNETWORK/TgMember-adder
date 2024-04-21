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

help_keyboard = InlineKeyboardMarkup([[
     InlineKeyboardButton("🪪 Login", callback_data="login_txt"),
     InlineKeyboardButton("Adder 🎁", callback_data="adder_txt"),
],[
     InlineKeyboardButton("🔙 Back", callback_data="start_cq")

]])

@addboy.on_message(filters.command("start") & filters.private)
async def start(app: Client, message):
    await message.reply_text(
        text="Hello {}\n\nMy name is **{}** Iam a member adder bot i can add members in your group simply and smoothly for more information click below **Help Section** button or /help command to see information.".format(message.from_user.mention(), Config.BOT_NAME),
        reply_markup=start_keyboard,
    )

@addboy.on_callback_query(filters.regex("start_cq"))
async def start(app: Client, CallbackQuery):
    await CallbackQuery.edit_message_text(
        text="Hello {}\n\nMy name is **{}** Iam a member adder bot i can add members in your group simply and smoothly for more information click below **Help Section** button or /help command to see information.".format(CallbackQuery.from_user.mention(), Config.BOT_NAME),
        reply_markup=start_keyboard,
    )

@addboy.on_message(filters.command("help"))
async def help(app: Client, message):
    await message.reply_text(
        text="Welcome to help section iam a group member adder bot see more commands from below.",
        reply_markup=help_keyboard,
    )

@addboy.on_callback_query(filters.regex("help"))
async def help(app: Client, CallbackQuery):
    await CallbackQuery.edit_message_text(
        text="Welcome to help section iam a group member adder bot see more commands from below.",
        reply_markup=help_keyboard,
    )