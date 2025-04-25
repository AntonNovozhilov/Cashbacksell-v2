from aiogram import types, Router
from aiogram.filters import Command, CommandStart

from texts.command_text import FAQ, START

command = Router()

@command.message(CommandStart())
async def start(message: types.Message):
    await message.answer(START)

@command.message(Command('faq'))
async def faq(message: types.Message):
    await message.answer(FAQ)