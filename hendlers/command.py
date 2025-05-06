from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart

from config import (CHANNEL_ID_BARTER, CHANNEL_ID_CASH, CHANNEL_INFO_MESSAGE,
                    CHAT_ID, PRICE_MESSAGE_ID_BARTER, PRICE_MESSAGE_ID_CASH,
                    count_price_in_admin, count_users_in_admin, home,
                    kb_admin_pannel_text, kb_admin_text, kb_cannals_text,
                    kb_create_post_text, kb_faq_text, kb_price_text,
                    kb_requis_text)
from database.requests import (ChatPrivatUser, add_user, async_session,
                               count_price_barter, count_price_barter_month,
                               count_price_barter_today,
                               count_price_barter_week, count_price_cashback,
                               count_price_cashback_month,
                               count_price_cashback_today,
                               count_price_cashback_week, count_users,
                               count_users_today, count_users_week,
                               price_barter_add, price_cashback_add, select)
from keyboards.inline_kb import inline_create_post, inline_price
from keyboards.kb_user import kb_admin, user_kb
from texts.command_text import FAQ, START, TEXT_REQ

kb_com = Router()

@kb_com.message(CommandStart())
async def start(message: types.Message):
    '''Старт бота и добавление пользователя в базу данных.'''
    await add_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        )
    await message.answer(START, reply_markup=user_kb(message.from_user.id), parse_mode='MarkdownV2')

@kb_com.message(F.text==kb_create_post_text)
async def inline_create_posts(message: types.Message):
    '''Вызов 2 инлайн книпки при нажатии на меню Составить пост.'''
    await message.answer('Выберите в какой канал составить пост', reply_markup=inline_create_post())

@kb_com.message(F.text==kb_price_text)
async def price(message: types.Message):
    '''Вызов 2 инлайн книпки при нажатии на меню Прайс.'''
    await message.answer('Выберите канал 👇',
                         reply_markup=inline_price())
    
@kb_com.message(F.text == kb_faq_text)
async def faq(message: types.Message):
    '''Вызов поста с FAQом.'''
    photo_path = 'images/faq.jpg'
    photo = types.FSInputFile(photo_path)
    await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=FAQ, parse_mode='MarkdownV2')

@kb_com.message(F.text == kb_cannals_text)
async def list_channals(message: types.Message):
    '''Вызов поста с списком каналов.'''
    await message.bot.forward_message(
        chat_id=message.chat.id,
        from_chat_id=CHANNEL_ID_BARTER,
        message_id=CHANNEL_INFO_MESSAGE
    )

@kb_com.message(F.text == kb_requis_text)
async def reqwuis(message: types.Message):
    '''Вызов поста с реквизитами для оплаты.'''
    await message.answer(text=TEXT_REQ)

@kb_com.message(F.text == kb_admin_text)
async def link_admin(message: types.Message):
    '''Вызов поста с сылкой на админа.'''
    await message.answer(text='[Администратор Юлия](https://t.me/@Juli_Novozhilova)', parse_mode='MarkdownV2')

@kb_com.message(F.text == kb_admin_pannel_text)
async def panel_admin(message: types.Message):
    '''Вызов меню админа.'''
    await message.answer('Вы вошли в админку', reply_markup=kb_admin(message.from_user.id))

@kb_com.message(F.text == home)
async def panel_admin(message: types.Message):
    '''Выйти из меню админа.'''
    await message.answer('Вы вышли из меню админа', reply_markup=user_kb(message.from_user.id))


@kb_com.message(F.text == count_users_in_admin)
async def count_us(message: types.Message):
    '''Подсчет пользователей.'''
    users = await count_users()
    today_users = await count_users_today()
    week_users = await count_users_week()
    count = len(list(users))
    count_today_users = len(list(today_users))
    count_week_users = len(list(week_users))
    await message.answer(f'Количество подписчиков в боте {count}\nСегодня подписалось {count_today_users}\nЗа неделю подписалось {count_week_users}')

@kb_com.message(F.text == count_price_in_admin)
async def count_us_price(message: types.Message):
    '''Подсчет запроса прайсов.'''
    count_pricebarter = await count_price_barter()
    today_pricebarter  = await count_price_barter_today()
    week_pricebarter  = await count_price_barter_week()
    month_pricebarter  = await count_price_barter_month()
    count_price_bart = len(list(count_pricebarter))
    count_today_pricebarter  = len(list(today_pricebarter))
    count_week_pricebarter  = len(list(week_pricebarter))
    count_month_pricebarter  = len(list(month_pricebarter))
    count_pricecashback = await count_price_cashback()
    today_pricecashback  = await count_price_cashback_today()
    week_pricecashback  = await count_price_cashback_week()
    month_pricecashback  = await count_price_cashback_month()
    count_pricec = len(list(count_pricecashback))
    count_today_pricec = len(list(today_pricecashback))
    count_week_pricec = len(list(week_pricecashback))
    count_month_pricec = len(list(month_pricecashback))
    await message.answer(f'''
<b>Статистика запросов прайса</b>

🔁 <b>Бартер:</b>
— Всего: <b>{count_price_bart}</b>
— За месяц: <b>{count_month_pricebarter}</b>
— За неделю: <b>{count_week_pricebarter}</b>
— Сегодня: <b>{count_today_pricebarter}</b>

💰 <b>Кэшбек:</b>
— Всего: <b>{count_pricec}</b>
— За месяц: <b>{count_month_pricec}</b>
— За неделю: <b>{count_week_pricec}</b>
— Сегодня: <b>{count_today_pricec}</b>
''', parse_mode='HTML')

@kb_com.callback_query(F.data=='price_cash')
async def price_cashback(callback: types.CallbackQuery):
    '''При нажатии на кнопку 1 пересылает сообщение из канала с прайсом кешбека.'''
    await price_cashback_add(callback.from_user.id)  
    await callback.message.bot.forward_message(
        chat_id=callback.message.chat.id,
        from_chat_id=CHANNEL_ID_CASH,
        message_id=PRICE_MESSAGE_ID_CASH
    )

@kb_com.callback_query(F.data=='price_barter')
async def price_barter(callback: types.CallbackQuery):
    '''При нажатии на кнопку 2 пересылает сообщение из канала с прайсом бартера.'''
    await price_barter_add(callback.from_user.id)
    await callback.message.bot.forward_message(
        chat_id=callback.message.chat.id,
        from_chat_id=CHANNEL_ID_BARTER,
        message_id=PRICE_MESSAGE_ID_BARTER
    )

@kb_com.message(F.chat.id == CHAT_ID, F.message_thread_id, Command('pc'))
async def from_admin_to_user_cashbak(message: types.Message):
    '''Администратор может отправить прайс кешбека пользователю командой.'''
    thread_id = message.message_thread_id
    async with async_session() as session:
        chat_user = await session.scalar(
            select(ChatPrivatUser).where(ChatPrivatUser.thread_id == thread_id)
        )
        if chat_user:
            try:
                await message.bot.forward_message(
                    chat_id=chat_user.user_id,
                    from_chat_id=CHANNEL_ID_CASH,
                    message_id=PRICE_MESSAGE_ID_CASH
                )
            except Exception as e:
                await message.reply(f'Не удалось переслать сообщение: {e}')

@kb_com.message(F.chat.id == CHAT_ID, F.message_thread_id, Command('pb'))
async def from_admin_to_user_barter(message: types.Message):
    '''Администратор может отправить прайс бартера пользователю командой.'''
    thread_id = message.message_thread_id
    async with async_session() as session:
        chat_user = await session.scalar(
            select(ChatPrivatUser).where(ChatPrivatUser.thread_id == thread_id)
        )
        if chat_user:
            try:
                await message.bot.forward_message(
                    chat_id=chat_user.user_id,
                    from_chat_id=CHANNEL_ID_BARTER,
                    message_id=PRICE_MESSAGE_ID_BARTER
                )
            except Exception as e:
                await message.reply(f'Не удалось переслать сообщение: {e}')

@kb_com.message(F.chat.id == CHAT_ID, F.message_thread_id, Command('r'))
async def from_admin_to_user_req(message: types.Message):
    '''Администратор может отправить реквизиты пользователю командой.'''
    thread_id = message.message_thread_id
    async with async_session() as session:
        chat_user = await session.scalar(
            select(ChatPrivatUser).where(ChatPrivatUser.thread_id == thread_id)
        )
        if chat_user:
            try:
                await message.bot.send_message(
                    chat_id=chat_user.user_id,
                    text=TEXT_REQ
                )
            except Exception as e:
                await message.reply(f'Не удалось переслать сообщение: {e}')


# Обработчки чтобы получить id канала и сообщения
# @kb_com.message()
# async def catch_forwarded(message: types.Message):
#     if message.forward_from_chat:
#         chat_id = message.forward_from_chat.id
#         post_id = message.forward_from_message_id
#         await message.answer(f'Канал ID: {chat_id}\nПост ID: {post_id}')