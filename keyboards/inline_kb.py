from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from  database.requests import count_users

def inline_create_post():
    inline_kb = [
        [InlineKeyboardButton(text='Для канала с кешбеком', callback_data='create_cash')],
        [InlineKeyboardButton(text='Для канала с блогерами', callback_data='create_barter')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)


def inline_price():
    inline_kb = [
        [InlineKeyboardButton(text='Для канала с кешбеком', callback_data='price_cash')],
        [InlineKeyboardButton(text='Для канала с блогерами', callback_data='price_barter')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)

def finish_kb():
    finish_kb = [[InlineKeyboardButton(text="✅ Завершить загрузку", callback_data="finish_post")]]
    return InlineKeyboardMarkup(inline_keyboard=finish_kb)

def finish_kb2():
    finish_kb = [[InlineKeyboardButton(text="✅ Завершить загрузку", callback_data="finish_post2")]]
    return InlineKeyboardMarkup(inline_keyboard=finish_kb)