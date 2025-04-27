from aiogram import types, Router, F

from keyboards.inline_kb import inline_create_post, inline_price

from config import (
    CHANNEL_ID_CASH,
    PRICE_MESSAGE_ID_CASH,
    CHANNEL_ID_BARTER,
    PRICE_MESSAGE_ID_BARTER,
    admin,
    kb_price_text,
    kb_create_post_text,
    kb_cannals_text,
    kb_faq_text,
    kb_requis_text,
    kb_admin_text,
    kb_admin_pannel_text
)


kb_com = Router()



@kb_com.message(F.text==kb_create_post_text)
async def inline_create_posts(message: types.Message):
    await message.answer('Выберите в какой канал составить пост', reply_markup=inline_create_post())

@kb_com.message(F.text==kb_price_text)
async def price(message: types.Message):
    await message.answer('Выберите канал 👇',
                         reply_markup=inline_price())

@kb_com.callback_query(F.data=='price_cash')
async def price_cashback(callback: types.CallbackQuery):
    await callback.message.bot.forward_message(
        chat_id=callback.message.chat.id,
        from_chat_id=CHANNEL_ID_CASH,
        message_id=PRICE_MESSAGE_ID_CASH
    )

@kb_com.callback_query(F.data=='price_barter')
async def price_barter(callback: types.CallbackQuery):
    await callback.message.bot.forward_message(
        chat_id=callback.message.chat.id,
        from_chat_id=CHANNEL_ID_BARTER,
        message_id=PRICE_MESSAGE_ID_BARTER
    )

# @kb_com.message(F.text==kb_price_text)
# async def price(message: types.Message):
#     await message.bot.forward_message(
#         chat_id=message.chat.id,
#         from_chat_id=CHANNEL_ID_CASH,
#         message_id=PRICE_MESSAGE_ID_CASH
#     )
#     await message.bot.forward_message(
#         chat_id=message.chat.id,
#         from_chat_id=CHANNEL_ID_BARTER,
#         message_id=PRICE_MESSAGE_ID_BARTER
#     )

# Обработчки чтобы получить id канала и сообщения
# @kb_com.message()
# async def catch_forwarded(message: types.Message):
#     if message.forward_from_chat:
#         chat_id = message.forward_from_chat.id
#         post_id = message.forward_from_message_id
#         await message.answer(f"Канал ID: {chat_id}\nПост ID: {post_id}")