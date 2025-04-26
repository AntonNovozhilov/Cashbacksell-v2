from aiogram import types, Router
from aiogram.filters import Command, CommandStart

from texts.command_text import FAQ, START
from keyboards.kb_user import user_kb

command = Router()

@command.message(CommandStart())
async def start(message: types.Message):
    await message.answer(START, reply_markup=user_kb(message.from_user.id))

@command.message(Command('faq'))
async def faq(message: types.Message):
    await message.answer(FAQ)