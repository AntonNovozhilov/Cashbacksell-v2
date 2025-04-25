from aiogram import Dispatcher, types, Bot, Router, F
from aiogram.filters import CommandStart, Command
import asyncio
import os
from dotenv import load_dotenv

from hendlers.command import command

load_dotenv()

bot = Bot(os.getenv('BOT'))
dp = Dispatcher()
dp.include_router(command)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())