from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart

from texts.command_text import FAQ, START
from keyboards.kb_user import user_kb
from database.requests import add_user, caht_add, chat_privat
from config import CHAT_ID, home

command = Router()

@command.message(CommandStart())
async def start(message: types.Message):
    await add_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        )
    user_id = message.from_user.id
    username = message.from_user.username or ''
    first_name = message.from_user.first_name or ''
    user_id = message.from_user.id
    chat = await chat_privat(user_id)
    if user_id not in chat:
        topic_title = f'{username}|{first_name}'
        new_topic = await message.bot.create_forum_topic(chat_id=CHAT_ID, name=topic_title)
        thread_id = new_topic.message_thread_id
        await caht_add(tg_id=message.from_user.id, thread_id=thread_id)
    await message.answer(START, reply_markup=user_kb(message.from_user.id))

@command.message(Command('faq'))
async def faq(message: types.Message):
    await message.answer(FAQ)