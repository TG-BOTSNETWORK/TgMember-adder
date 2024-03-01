import os
import asyncio
import importlib
from adder import addboy
from adder.modules import ALL_MODULES
from pyrogram import idle

PLUGINS = {}
plugs = PLUGINS 

async def main():
    for all_modules in ALL_MODULES:
        try:
            imported_plugin = importlib.import_module("adder.modules." + all_modules)
            if hasattr(imported_plugin, "__MODNAME__") and imported_plugin.__MODNAME__:
                imported_plugin.__MODNAME__ = imported_plugin.__MODNAME__
                if hasattr(imported_plugin, "__MODHELP__") and imported_plugin.__MODHELP__:
                    plugs[imported_plugin.__MODNAME__.lower()] = imported_plugin
            print(f"Successfully imported plugin: {imported_plugin.__MODNAME__}")
        except ImportError as e:
            print(f"Failed to import plugin {all_modules}: {e}")


async def run_bot():
    await main()
    await idle()
    await addboy.run()
    await addboy.send_message("@my_name_is_nobitha", "hello started!")
    print("Bot started!")

if __name__ == "__main__":
    asyncio.run(run_bot())
