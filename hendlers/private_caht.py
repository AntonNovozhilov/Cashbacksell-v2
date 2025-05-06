from aiogram import F, Router, types
from sqlalchemy import select

from config import CHAT_ID
from database.models import ChatPrivatUser, async_session
from database.requests import add_user, caht_add, chat_privat

private = Router()

@private.message(F.chat.type == 'private')
async def private_chat_message(message: types.Message):
    '''Обработка всех сообщений и инициализация теммы в группе.'''
    user_id = message.from_user.id
    username = message.from_user.username or ''
    first_name = message.from_user.first_name or ''
    await add_user(user_id, username=username, first_name=first_name)
    chat = await chat_privat(user_id)
    if user_id not in chat:
        topic_title = f'{username}|{first_name}'
        new_topic = await message.bot.create_forum_topic(chat_id=CHAT_ID, name=topic_title)
        thread_id = new_topic.message_thread_id
        await caht_add(tg_id=user_id, thread_id=thread_id)
        await message.bot.send_message(chat_id=CHAT_ID, text='Клиент пишет', message_thread_id=thread_id)
    else:
        async with async_session() as session:
            chat_user = await session.scalar(select(ChatPrivatUser).where(ChatPrivatUser.user_id == user_id))
            thread_id = chat_user.thread_id if chat_user else None
    if thread_id:
        await message.bot.forward_message(
            chat_id=CHAT_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            message_thread_id=thread_id
        )

@private.message(F.chat.id == CHAT_ID, F.message_thread_id)
async def from_admin_to_user(message: types.Message):
    '''Ответ клиенту через бота и тему.'''
    thread_id = message.message_thread_id
    async with async_session() as session:
        chat_user = await session.scalar(
            select(ChatPrivatUser).where(ChatPrivatUser.thread_id == thread_id)
        )
        if chat_user:
            try:
                await message.bot.copy_message(
                    chat_id=chat_user.user_id,
                    from_chat_id=message.chat.id,
                    message_id=message.message_id
                )
            except Exception as e:
                await message.reply(f'Не удалось переслать сообщение: {e}')
