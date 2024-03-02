import os
import asyncio
from adder import addboy
from pyrogram import idle

async def main():
    try:
        await addboy.start()  
        print("Bot started!")  
    except Exception as e:
        print(f"Failed to start bot: {e}")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
