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

from config import CHAT_ID, admin
from database.requests import chat_privat
from keyboards.inline_kb import finish_kb
from keyboards.kb_user import user_kb

cachbackpost = Router()

media_group_buffer = defaultdict(list)

def contains_emoji(text: str):
    emoji_pattern = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)
    return bool(emoji_pattern.search(text))

class PostCachback(StatesGroup):
    """Класс для составления поста в кешбеке."""

    title = State()
    market = State()
    price_before = State()
    price_after = State()
    discount = State()
    seller = State()
    photo = State()

@cachbackpost.callback_query(F.data == 'create_cash')
async def start_post(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(PostCachback.title)
    await callback.message.answer('Введите название товара', reply_markup=types.ReplyKeyboardRemove())
    await callback.answer()

@cachbackpost.message(PostCachback.title)
async def post_market(message: types.Message, state: FSMContext):
    if contains_emoji(message.text):
        await message.answer('Пожалуйста, не используйте смайлики, только текст.')
        return
    await state.update_data(title=message.text)
    await state.set_state(PostCachback.market)
    await message.answer('На какой площадке продается товар?')

@cachbackpost.message(PostCachback.market)
async def post_price(message: types.Message, state: FSMContext):
    if contains_emoji(message.text):
        await message.answer('Пожалуйста, не используйте смайлики, только текст.')
        return
    await state.update_data(market=message.text)
    await state.set_state(PostCachback.price_before)
    await message.answer('Введите стоимость на маркетплейсе в рублях:')

@cachbackpost.message(PostCachback.price_before)
async def post_price_before(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Пожалуйста, введите цену числом без пробелов и символов (например, 1490):')
        return
    if contains_emoji(message.text):
        await message.answer('Пожалуйста, не используйте смайлики, только текст.')
        return
    
    await state.update_data(price_before=message.text)
    await state.set_state(PostCachback.price_after)
    await message.answer('Введите стоимость на маркетплейсе с учетом кешбека:')

@cachbackpost.message(PostCachback.price_after)
async def post_price_after(message: types.Message, state: FSMContext):
    if contains_emoji(message.text):
        await message.answer('Пожалуйста, не используйте смайлики, только текст.')
        return
    data = await state.get_data()
    if not message.text.isdigit():
        await message.answer('Пожалуйста, введите цену числом без пробелов и символов (например, 1000):')
        return
    new_price = int(message.text)
    old_price = int(data.get('price_before', 0))
    if new_price >= old_price:
        await message.answer('Стоимость после кешбека не может быть больше или равна стоимости до кешбека.')
        return
    await state.update_data(price_after=message.text)
    await state.set_state(PostCachback.discount)
    await message.answer('Какая скидка в процентах?')

@cachbackpost.message(PostCachback.discount)
async def post_cashback(message: types.Message, state: FSMContext):
    if contains_emoji(message.text):
        await message.answer('Пожалуйста, не используйте смайлики, только текст.')
        return
    if not message.text.isdigit():
            await message.answer("Пожалуйста, введите кешбэк числом (например, 300 или 10):")
            return
    cashback_value = int(message.text)
    cashback_type = "₽" if cashback_value > 100 else "%"
    await state.update_data(discount=cashback_value, cashback_type=cashback_type)
    await message.answer("Укажите контакт для связи:")
    await state.set_state(PostCachback.seller)

@cachbackpost.message(PostCachback.seller)
async def post_seller(message: types.Message, state: FSMContext):
    if contains_emoji(message.text):
        await message.answer('Пожалуйста, не используйте смайлики, только текст.')
        return
    await state.update_data(seller=message.text)
    await message.answer("Теперь прикрепите фото к посту:")
    await state.set_state(PostCachback.photo)

@cachbackpost.message(PostCachback.photo, ~F.photo)
async def wrong_input_in_photo(message: types.Message):
    await message.answer("❗️Пожалуйста, прикрепите *фотографию* товара.\n"
                         "Это можно сделать, используя 📎 и выбрав *Фото*.\n")


@cachbackpost.message(PostCachback.photo, F.photo)
async def post_photo(message: types.Message, state: FSMContext):
    if message.media_group_id:
        media_group_buffer[message.media_group_id].append(message.photo[-1].file_id)

        if len(media_group_buffer[message.media_group_id]) == 1:
            await asyncio.sleep(1.5)
            photo_ids = media_group_buffer.pop(message.media_group_id)
            data = await state.get_data()
            photos = data.get("photos", [])
            photos.extend(photo_ids)
            await state.update_data(photos=photos)

            await message.answer(
                "🖼 Фото добавлены. Далее: отправьте ещё или нажмите кнопку ниже для завершения.",
                reply_markup=finish_kb()
            )

    else:
        data = await state.get_data()
        photos = data.get("photos", [])
        photos.append(message.photo[-1].file_id)
        await state.update_data(photos=photos)

        await message.answer(
            "🖼 Фото добавлены. Далее: отправьте ещё или нажмите кнопку ниже для завершения.",
            reply_markup=finish_kb()
        )

@cachbackpost.callback_query(F.data == "finish_post")
async def handle_finish(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    photos = data.get("photos", [])

    if not photos:
        await callback.message.answer("Сначала добавьте хотя бы одно фото.")
        return

    price = int(data["price_before"])
    cashback = data["discount"]

    text = (
        f"<i><b>{data['title']}</b></i> \n"
        f"<i>{data['market']}</i> \n\n"
        f"<b>Цена на маркетплейсе:</b> {data['price_before']}₽ ❌ \n"
        f"<b>Цена для Вас:</b> {data['price_after']}₽ ✅ \n"
        f"<i>(Кешбек - {data['discount']}{data['cashback_type']}🔥)</i> \n\n"
        f"🖊️ <b>Для получения инструкции по выкупу пиши</b> <i>{data['seller']}</i>"
    )
    user_id = callback.from_user.id
    username = callback.from_user.username or ''
    first_name = callback.from_user.first_name or ''
    user_id = callback.from_user.id
    chat = await chat_privat(user_id)
    if user_id not in chat:
        topic_title = f'{username}|{first_name}'
        new_topic = await callback.bot.create_forum_topic(chat_id=CHAT_ID, name=topic_title)
        thread_id = new_topic.message_thread_id
        await callback.bot.send_message(chat_id=CHAT_ID, text=f"Новый пользователь: @{username} (id: {user_id})", message_thread_id=thread_id)

    async with async_session() as session:
            chat_user = await session.scalar(select(ChatPrivatUser).where(ChatPrivatUser.user_id == user_id))
            thread_id = chat_user.thread_id if chat_user else None
    media_group = [types.InputMediaPhoto(media=file_id) for file_id in photos]
    await callback.bot.send_media_group(chat_id=CHAT_ID, media=media_group, message_thread_id=thread_id)

    buttons = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="✅ Пост принят", callback_data=f"approve_{user_id}")],
        [types.InlineKeyboardButton(text="❌ Пост отклонён", callback_data=f"reject_{user_id}")]
    ])
    await callback.bot.send_message(chat_id=CHAT_ID, text=text, message_thread_id=thread_id, reply_markup=buttons, parse_mode='HTML')
    await state.clear()
    await callback.message.answer("Готово! Пост отправлен на модерацию.", reply_markup=user_kb(callback.from_user.id))


@cachbackpost.callback_query(F.data.startswith("approve_"))
async def approve_post(callback: types.CallbackQuery):
    if callback.from_user.id not in admin:
        return
    user_id = int(callback.data.split("_")[1])
    try:
        await callback.bot.send_message(chat_id=user_id, text="✅ Ваш пост принят! Ожидайте размещения. Если остались вопросы можете задать их здесь.")
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception as e:
        print(f"Ошибка при отправке принятия пользователю {user_id}: {e}")
        await callback.answer("Не удалось отправить сообщение пользователю.")

@cachbackpost.callback_query(F.data.startswith("reject_"))
async def reject_post(callback: types.CallbackQuery):
    if callback.from_user.id not in admin:
        return
    user_id = int(callback.data.split("_")[1])
    try:
        await callback.bot.send_message(chat_id=user_id, text="❌ Ваш пост был отклонен. Попробуйте подать его заново или напишите администратору.")
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer("Пользователю отправлено сообщение об отклонении.")
    except Exception as e:
        print(f"Ошибка при отправке отказа пользователю {user_id}: {e}")
        await callback.answer("Не удалось отправить сообщение пользователю.")