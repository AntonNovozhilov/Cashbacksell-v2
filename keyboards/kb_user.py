from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from config import (
    admin,
    kb_price_text,
    kb_create_post_text,
    kb_cannals_text,
    kb_faq_text,
    kb_requis_text,
    kb_admin_text,
    kb_admin_pannel_text
)
# Вытащить админа или админов, это надо реализовать в конфиге и передавать список id. 

def user_kb(user_telegram_id: int):
    kb = [
        [KeyboardButton(text=kb_create_post_text), KeyboardButton(text=kb_faq_text)],
        [KeyboardButton(text=kb_price_text), KeyboardButton(text=kb_requis_text)],
        [KeyboardButton(text=kb_cannals_text), KeyboardButton(text=kb_admin_text)],
    ]
    if user_telegram_id in admin:
        kb.append([KeyboardButton(text=kb_admin_pannel_text)])
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder='Воспользуйтесь меню или напишите админу сюда в чат')
    return keyboard