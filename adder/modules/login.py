from pyrogram import Client, filters
from pyrogram.types import Message
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
    try:
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
            text="Please provide your phone number with the country code (e.g., +1234567890):"
        )
        phone_number_message = await app.listen(chat_id)
        client = Client("new adder", api_id=api_id, api_hash=api_hash, in_memory=True)
        await client.connect()
        if phone_number_message is not None and phone_number_message.text is not None:
            phone_number = phone_number_message.text.strip()
            if not phone_number.startswith('+'):
                await app.send_message(chat_id, "Phone number must start with a country code (e.g., +1234567890).")
                return
            try:
                result = await client.send_code(phone_number)
                await app.send_message(chat_id, "Please enter the OTP code sent to your phone number format `x x x x x`:")
                otp_message = await app.listen(chat_id)
                otp = otp_message.text.strip()
                sign_in_result = await client.sign_in(phone_number, result.phone_code_hash, otp)
                
                # Fetch more information about the logged-in user
                me = await app.get_me()
                user_info = f"Username: {me.username}\nPhone number: {me.phone_number}\nLast login: {me.status.date}"
                await app.send_message(chat_id, f"Login successful.\n{user_info}")
                
                # Save user to database
                await save_user(chat_id, me.id)
                
            except PhoneCodeExpired:
                await app.send_message(chat_id, "The OTP code has expired. Please try again.")
            except PhoneCodeInvalid:
                await app.send_message(chat_id, "The phone number is not registered.")
            except SessionPasswordNeeded:
                await app.send_message(chat_id, "Your account has two-step verification enabled. Please enter your password:")
                password_message = await app.listen(chat_id)
                password = password_message.text.strip()
                try:
                    sign_in_result = await client.check_password(password)
                    me = await app.get_me()
                    user_info = f"Username: {me.username}\nPhone number: {me.phone_number}\nLast login: {me.status.date}"
                    await app.send_message(chat_id, f"Login successful.\n{user_info}")
                    await save_user(chat_id, me.id)
                except PasswordHashInvalid:
                    await app.send_message(chat_id, "The password you entered is incorrect. Please try again.")
        else:
            await app.send_message(chat_id, "Invalid phone number format or no message received.")
    except Exception as e:
        print(f"Error handling login: {e}")

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
