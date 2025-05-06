from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from config import (admin, count_price_in_admin, count_users_in_admin, home,
                    kb_admin_pannel_text, kb_admin_text, kb_cannals_text,
                    kb_create_post_text, kb_faq_text, kb_price_text,
                    kb_requis_text, news)


def user_kb(user_telegram_id: int):
    '''Главное меню.'''
    kb = [
        [KeyboardButton(text=kb_cannals_text)],
        [KeyboardButton(text=kb_price_text), KeyboardButton(text=kb_create_post_text)],
        [KeyboardButton(text=kb_requis_text)],
        [KeyboardButton(text=kb_faq_text), KeyboardButton(text=kb_admin_text)],
    ]
    if user_telegram_id in admin:
        kb.append([KeyboardButton(text=kb_admin_pannel_text)])
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder='Воспользуйтесь меню или напишите админу сюда в чат')
    return keyboard

def kb_admin(user_telegram_id: int):
    '''Меню в админке.'''
    kb = [
        [KeyboardButton(text=count_users_in_admin)],
        [KeyboardButton(text=count_price_in_admin)],
        [KeyboardButton(text=news)],
        [KeyboardButton(text=home)]

    ]
    return ReplyKeyboardMarkup(keyboard=kb)