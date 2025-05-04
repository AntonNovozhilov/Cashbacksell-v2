import asyncio
import re
from collections import defaultdict
from aiogram import Router, F, types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select
from database.models import async_session, ChatPrivatUser

from config import CHAT_ID, admin, news
from database.requests import chat_privat
from keyboards.inline_kb import finish_kb
from keyboards.kb_user import user_kb

newses = Router()


class NewsPost(StatesGroup):
    text = State()


@newses.message(F.text == news)
async def news_to_subsriber(message: types.Message, state: FSMContext):
    await state.set_state(NewsPost.text)
    await message.answer('Введите текст рассылки')

@newses.message(NewsPost.text)
async def news_post(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    async with async_session() as session:
            chats_user = await session.scalars(select(ChatPrivatUser))
            for chat in tuple(chats_user):
                 thread_id = chat.thread_id if chat else None
                 await message.bot.send_message(chat_id=CHAT_ID, text=data['text'], message_thread_id=thread_id)
