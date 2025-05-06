import asyncio

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import news
from database.requests import count_users_tg_id_list

newses = Router()

class NewsPost(StatesGroup):
    '''Пост для рассылки.'''

    text = State()


@newses.message(F.text == news)
async def news_to_subsriber(message: types.Message, state: FSMContext):
    '''Инициализация ввода текста.'''
    await state.set_state(NewsPost.text)
    await message.answer('Введите текст рассылки')

@newses.message(NewsPost.text)
async def news_post(message: types.Message, state: FSMContext):
    '''Сохранение текста, посчет успешных и не успешных отправлений.'''
    await state.update_data(text=message.text)
    data = await state.get_data()
    users_list = await count_users_tg_id_list()
    success = 0
    failed = 0
    for user in users_list:
        try:
            await message.bot.send_message(chat_id=user, text=data['text'])
            success += 1
        except Exception as e:
            failed += 1
            print(f'Не удалось отправить сообщение пользователю {user}: {e}')
        await asyncio.sleep(1)
    await message.answer(f'✅ Рассылка завершена.\nУспешно: {success}\nНе удалось: {failed}')
    await state.clear()
