from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from pyrogram.raw import functions
import asyncio
import time
import pymongo
from config.config import Config 
from adder import addboy 

mongo_client = pymongo.MongoClient(Config.DB_MAN)
db = mongo_client["telegramusers"]
collection = db["users"]

login_sessions = {}

async def handle_login(chat_id):
    start_time = time.time()
    timeout = 300 
    await addboy.send_message(
        chat_id,
        "Please send your contact information with the button below:",
         reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("Send Contact", request_contact=True)]],
                resize_keyboard=True
         )
    )
    contact_message = await get_user_input(chat_id, timeout)
    phone_number = contact_message.contact.phone_number
    
    result = await addboy.send(
        functions.auth.SendCode(
            phone_number=phone_number,
            api_id=22363963,
            api_hash='5c096f7e8fd4c38c035d53dc5a85d768'
        )
    )
    if result.phone_registered:
        await addboy.send_message(chat_id, "Please enter the OTP code sent to your phone number:")
        otp_message = await get_user_input(chat_id, timeout)
        otp = otp_message.text.strip()
        
        sign_in_result = await addboy.send(
            functions.auth.SignIn(
                phone_number=phone_number,
                phone_code_hash=result.phone_code_hash,
                phone_code=otp
            )
        )
        await addboy.send_message(chat_id, f"Login successful. ID: {sign_in_result.user.id}")
        save_user(chat_id, sign_in_result.user.id)
    else:
        await addboy.send_message(chat_id, "Phone number not registered.")

async def get_user_input(chat_id, timeout):
    try:
        while True:
            async for message in addboy.get_chat_history(chat_id, limit=1):
                if message.from_user.id == (await addboy.get_me()).id:
                    return message
    except asyncio.TimeoutError:
        raise asyncio.TimeoutError("No input received.")

async def save_user(chat_id, user_id):
    user = {"chat_id": chat_id, "user_id": user_id}
    collection.insert_one(user)
    print("User saved to database.")

@addboy.on_message(filters.private & filters.me)
async def handle_user_input(_, message):
    chat_id = message.chat.id
    if chat_id in login_sessions:
        await login_sessions[chat_id](chat_id, message)
        del login_sessions[chat_id]

@addboy.on_callback_query(filters.regex("login"))
async def login_callback(_, callback_query):
    chat_id = callback_query.message.chat.id
    if chat_id not in login_sessions:
        login_sessions[chat_id] = handle_login
        await handle_login(chat_id)
    else:
        await addboy.send_message(chat_id, "You're already in a login session.")
