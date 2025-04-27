from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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