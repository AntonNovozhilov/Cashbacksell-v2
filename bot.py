from aiogram import Dispatcher, types, Bot, Router, F
from aiogram.filters import CommandStart, Command
import asyncio
import os
from dotenv import load_dotenv

from hendlers.kb_command import kb_com
from hendlers.command import command
from hendlers.private_caht import private
from fsm.post_cash import cachbackpost
from database.models import async_main

load_dotenv()

bot = Bot(os.getenv('BOT'))
dp = Dispatcher()
dp.include_router(cachbackpost)
dp.include_router(command)
dp.include_router(kb_com)
dp.include_router(private)




async def main():
    await async_main()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())