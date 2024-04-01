from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.raw import functions
import asyncio
import time
from adder import addboy  

login_sessions = {}

async def handle_login(chat_id):
    start_time = time.time()
    timeout = 300 
    await addboy.send_message(chat_id, "Please provide your API ID:")
    api_id_message = await get_user_input(chat_id, timeout)
    api_id = api_id_message.text.strip()
    
    await addboy.send_message(chat_id, "Please provide your API Hash:")
    api_hash_message = await get_user_input(chat_id, timeout)
    api_hash = api_hash_message.text.strip()
    
    await addboy.send_message(chat_id, "Please provide your phone number:")
    phone_number_message = await get_user_input(chat_id, timeout)
    phone_number = phone_number_message.text.strip()
    
    result = await addboy.send(
        functions.auth.SendCode(
            phone_number=phone_number,
            api_id=int(api_id),
            api_hash=api_hash
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

@addboy.on_message(filters.private)
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
