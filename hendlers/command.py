from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart

from texts.command_text import FAQ, START
from keyboards.kb_user import user_kb
from database.requests import add_user
from config import home

command = Router()

@command.message(CommandStart())
async def start(message: types.Message):
    await add_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        )
    await message.answer(START, reply_markup=user_kb(message.from_user.id))

@command.message(Command('faq'))
async def faq(message: types.Message):
    await message.answer(FAQ)