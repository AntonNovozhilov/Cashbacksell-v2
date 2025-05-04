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
from keyboards.inline_kb import finish_kb, finish_kb2
from keyboards.kb_user import user_kb

barterpost = Router()

media_group_bufferbarter = defaultdict(list)

class PostBarter(StatesGroup):
    """Класс для составления поста в бартере."""

    title = State()
    money = State()
    web = State()
    ohwats = State()
    tematic = State()
    descriptions = State()
    seller = State()
    photo = State()

def barter_money_kb():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="С доплатой", callback_data="money_yes")],
        [types.InlineKeyboardButton(text="Без доплаты", callback_data="money_no")]
    ])

@barterpost.callback_query(F.data == 'create_barter')
async def start_post(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(PostBarter.title)
    await callback.message.answer('Введите название товара', reply_markup=types.ReplyKeyboardRemove())
    await callback.answer()

@barterpost.message(PostBarter.title)
async def start_post2(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(PostBarter.money)
    await message.answer("Рассматриваете бартер с доплатой или без?", reply_markup=barter_money_kb())

@barterpost.callback_query(F.data.startswith("money_"))
async def set_money(callback: types.CallbackQuery, state: FSMContext):
    money_value = "С доплатой" if callback.data == "money_yes" else "Без доплаты"
    await state.update_data(money=money_value)
    await callback.message.answer("Укажите нужные соцсети (можно перечислить через запятую):")
    await state.set_state(PostBarter.web)

@barterpost.message(PostBarter.web)
async def set_web(message: types.Message, state: FSMContext):
    await state.update_data(web=message.text)
    await message.answer("Какие охваты?")
    await state.set_state(PostBarter.ohwats)

@barterpost.message(PostBarter.ohwats)
async def set_ohwats(message: types.Message, state: FSMContext):
    await state.update_data(ohwats=message.text)
    await message.answer("Тематика блога?")
    await state.set_state(PostBarter.tematic)

@barterpost.message(PostBarter.tematic)
async def set_thematic(message: types.Message, state: FSMContext):
    await state.update_data(tematic=message.text)
    await message.answer("Опишите задание:")
    await state.set_state(PostBarter.descriptions)

@barterpost.message(PostBarter.descriptions)
async def set_description(message: types.Message, state: FSMContext):
    await state.update_data(descriptions=message.text)
    await message.answer("Контакт для связи:")
    await state.set_state(PostBarter.seller)

@barterpost.message(PostBarter.seller)
async def set_seller(message: types.Message, state: FSMContext):
    await state.update_data(seller=message.text)
    await message.answer("Теперь прикрепите фото к посту:")
    await state.set_state(PostBarter.photo)

@barterpost.message(PostBarter.photo, ~F.photo)
async def wrong_input_in_photobarter(message: types.Message):
    await message.answer("❗️Пожалуйста, прикрепите *фотографию* товара.\n"
                         "Это можно сделать, используя 📎 и выбрав *Фото*.\n")


@barterpost.message(PostBarter.photo, F.photo)
async def post_photo(message: types.Message, state: FSMContext):
    if message.media_group_id:
        media_group_bufferbarter[message.media_group_id].append(message.photo[-1].file_id)

        if len(media_group_bufferbarter[message.media_group_id]) == 1:
            await asyncio.sleep(1.5)
            photo_ids = media_group_bufferbarter.pop(message.media_group_id)
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
            reply_markup=finish_kb2()
        )

@barterpost.callback_query(F.data == "finish_post2")
async def handle_finish2(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    photos = data.get("photos", [])
    if not photos:
        await callback.message.answer("Сначала добавьте хотя бы одно фото.")
        return
    text = (
    f"<i><b>{data['title']}</b></i> \n"
    f"Готовы работать с блогерами по бартеру {data['money']}, отправляйте данные на свой блог и статистику! \n\n"
    f"<b>❗️ВАЖНО:</b>\n"
    f"<b><i>▫️ Соц. сеть. Охват и аудитория: </i></b>\n"
    f"-{data['web']}\n"
    f"- Охваты сториз и рилз от {data['ohwats']}\n"
    f"-{data['descriptions']}\n"
    f"🖊️ <b>Для сотрудничества отправляйте отклик</b> <i>{data['seller']}</i>"
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


@barterpost.callback_query(F.data.startswith("approve_"))
async def approve_post2(callback: types.CallbackQuery):
    if callback.from_user.id not in admin:
        return
    user_id = int(callback.data.split("_")[1])
    try:
        await callback.bot.send_message(chat_id=user_id, text="✅ Ваш пост принят! Ожидайте размещения. Если остались вопросы можете задать их здесь.")
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception as e:
        print(f"Ошибка при отправке принятия пользователю {user_id}: {e}")
        await callback.answer("Не удалось отправить сообщение пользователю.")

@barterpost.callback_query(F.data.startswith("reject_"))
async def reject_post2(callback: types.CallbackQuery):
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