from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def inline_create_post():
    '''Кнопки для создания поста.'''
    inline_kb = [
        [InlineKeyboardButton(text='Для канала с кешбеком', callback_data='create_cash')],
        [InlineKeyboardButton(text='Для канала с блогерами', callback_data='create_barter')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)


def inline_price():
    '''Кнопки для запроса прайса.'''
    inline_kb = [
        [InlineKeyboardButton(text='Для канала с кешбеком', callback_data='price_cash')],
        [InlineKeyboardButton(text='Для канала с блогерами', callback_data='price_barter')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)

def finish_kb():
    '''Кнопка завершить загрузку фото.'''
    finish_kb = [[InlineKeyboardButton(text='✅ Завершить загрузку', callback_data='finish_post')]]
    return InlineKeyboardMarkup(inline_keyboard=finish_kb)

def finish_kb2():
    '''Кнопка завершить загрузку фото два.'''
    finish_kb = [[InlineKeyboardButton(text='✅ Завершить загрузку', callback_data='confirm_post2')]]
    return InlineKeyboardMarkup(inline_keyboard=finish_kb)