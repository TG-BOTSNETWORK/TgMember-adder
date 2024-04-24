#Developed by: santhu
#Telegram: @my_name_is_nobitha

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from config.config import Config 
from adder import addboy 
from adder.modules.login import get_user

start_keyboard = InlineKeyboardMarkup([[
      InlineKeyboardButton("🪪 Login", callback_data="login"),
      ],[
      InlineKeyboardButton("🛡️ Help Section 🛡️", callback_data="help")
]])
start_keyboard_with_settings = InlineKeyboardMarkup([[
        InlineKeyboardButton("Settings ⚙️", callback_data="settings"),
        InlineKeyboardButton("Adder 🎁", callback_data="adder"),
        ],[
        InlineKeyboardButton("🛡️ Help Section 🛡️", callback_data="help"),
]])
help_keyboard = InlineKeyboardMarkup([[
     InlineKeyboardButton("🪪 Login", callback_data="login_txt"),
     InlineKeyboardButton("Adder 🎁", callback_data="adder_txt"),
],[
     InlineKeyboardButton("🔙 Back", callback_data="start_cq")

]])

@addboy.on_message(filters.command("start") & filters.private)
async def start(app: Client, message):
    chat_id = message.chat.id
    user = await get_user(chat_id)
    if user:
        await message.reply_text(
            text=f"Hello {message.from_user.mention()}\n\nWelcome back! You are already logged in.",
            reply_markup=start_keyboard_with_settings,
        )
    else:
        await message.reply_text(
            text=f"Hello {message.from_user.mention()}\n\nMy name is **{Config.BOT_NAME}**. I am a member adder bot. To use my features, please log in first.",
            reply_markup=start_keyboard,
        )

@addboy.on_callback_query(filters.regex("start_cq"))
async def start(app: Client, CallbackQuery):
    chat_id = CallbackQuery.message.chat.id
    user = await get_user(chat_id)
    if user:
        await CallbackQuery.edit_message_text(
            text=f"Hello {CallbackQuery.from_user.mention()}\n\nWelcome back! You are already logged in.",
            reply_markup=start_keyboard_with_settings,
        )
    else:
        await CallbackQuery.edit_message_text(
            text=f"Hello {CallbackQuery.from_user.mention()}\n\nMy name is **{Config.BOT_NAME}**. I am a member adder bot. To use my features, please log in first.",
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