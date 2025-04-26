from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
# Вытащить админа или админов, это надо реализовать в конфиге и передавать список id. 

def user_kb(user_telegram_id: int):
    kb = [
        [KeyboardButton(text='Создать пост')],
        [KeyboardButton(text='Прайс'), KeyboardButton(text='Реквизиты')],
        [KeyboardButton(text='Наши каналы'), KeyboardButton(text='Контакты для связи')],
        [KeyboardButton(text='FAQ')]
    ]
    # if user_telegram_id in admins:
    #     kb.append([KeyboardButton('Админка')])
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder='Воспользуйтесь меню или напишите админу сюда в чат')
    return keyboard