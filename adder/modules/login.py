from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    PhoneCodeExpired,
    PhoneCodeInvalid,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
import pymongo
from config.config import Config

mongo_client = pymongo.MongoClient(Config.DB_MAN)
db = mongo_client["telegramusers"]
collection = db["users"]

login_sessions = {}

async def handle_login(app: Client, chat_id):
    await app.send_message(
        chat_id,
        text="Please provide your API ID:"
    )
    api_id_message = await app.listen(chat_id)
    api_id = api_id_message.text.strip()

    await app.send_message(
        chat_id,
        text="Please provide your API hash:"
    )
    api_hash_message = await app.listen(chat_id)
    api_hash = api_hash_message.text.strip()

    await app.send_message(
        chat_id,
        text="Please send your contact information with the button below:",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Send Contact", request_contact=True)]]
        )
    )
    contact_message = await app.listen(chat_id)
    phone_number = contact_message.contact.phone_number
    
    try:
        result = await app.send_code(
            phone_number,
            api_id=api_id,
            api_hash=api_hash
        )
        if result.phone_registered:
            await app.send_message(chat_id, "Please enter the OTP code sent to your phone number:")
            otp_message = await app.listen(chat_id)
            otp = otp_message.text.strip()
            
            sign_in_result = await app.sign_in(
                phone_number,
                result.phone_code_hash,
                otp
            )
            await app.send_message(chat_id, f"Login successful. ID: {sign_in_result.user.id}")
            await save_user(chat_id, sign_in_result.user.id)
        else:
            await app.send_message(chat_id, "Phone number not registered.")
    except PhoneCodeExpired:
        await app.send_message(chat_id, "The OTP code has expired. Please try again.")
    except PhoneCodeInvalid:
        await app.send_message(chat_id, "The OTP code you entered is invalid. Please try again.")
    except SessionPasswordNeeded:
        await app.send_message(chat_id, "Your account has two-step verification enabled. Please enter your password:")
        password_message = await app.listen(chat_id)
        password = password_message.text.strip()
        try:
            sign_in_result = await app.check_password(password)
            await app.send_message(chat_id, f"Login successful. ID: {sign_in_result.user.id}")
            await save_user(chat_id, sign_in_result.user.id)
        except PasswordHashInvalid:
            await app.send_message(chat_id, "The password you entered is incorrect. Please try again.")

async def save_user(chat_id, user_id):
    user = {"chat_id": chat_id, "user_id": user_id}
    collection.insert_one(user)
    print("User saved to database.")

@Client.on_message(filters.private & filters.me)
async def handle_user_input(app: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in login_sessions:
        await login_sessions[chat_id](app, chat_id)
        del login_sessions[chat_id]

@Client.on_callback_query(filters.regex("login"))
async def login_callback(app: Client, callback_query):
    chat_id = callback_query.message.chat.id
    if chat_id not in login_sessions:
        login_sessions[chat_id] = handle_login
        await handle_login(app, chat_id)
    else:
        await app.send_message(chat_id, "You're already in a login session.")