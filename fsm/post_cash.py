from aiogram import Router, F, types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup

cachbackpost = Router()

class PostCachback(StatesGroup):
    """Класс для составления поста в кешбеке."""

    title = State()
    market = State()
    price_before = State()
    price_after = State()
    discount = State()

@cachbackpost.callback_query(F.data == 'price_cash')
async def start_post(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(PostCachback.title)
    await callback.message.answer('Введите название товара', reply_markup=types.ReplyKeyboardRemove())
    await callback.answer()

@cachbackpost.message(PostCachback.title)
async def post_market(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(PostCachback.market)
    await message.answer('На какой площадке продается товар?')

@cachbackpost.message(PostCachback.market)
async def post_price(message: types.Message, state: FSMContext):
    await state.update_data(market=message.text)
    await state.set_state(PostCachback.price_before)
    await message.answer('Введите стоимость на маркетплейсе в рублях:')

@cachbackpost.message(PostCachback.price_before)
async def post_price_before(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Пожалуйста, введите цену числом без пробелов и символов (например, 1490):')
        return
    
    await state.update_data(price_before=message.text)
    await state.set_state(PostCachback.price_after)
    await message.answer('Введите стоимость на маркетплейсе с учетом кешбека:')

@cachbackpost.message(PostCachback.price_after)
async def post_price_after(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Пожалуйста, введите цену числом без пробелов и символов (например, 1000):')
        return
    
    await state.update_data(price_after=message.text)
    await state.set_state(PostCachback.discount)
    await message.answer('Какая скидка в процентах?')

@cachbackpost.message(PostCachback.discount)
async def post_discount(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Пожалуйста, введите процент числом (например, 15):')
        return
    
    await state.update_data(discount=message.text)
    
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Завершить"))
    await message.answer(
        "Все данные получены! Нажмите 'Завершить' для публикации.",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

@cachbackpost.message(PostCachback.discount, F.text == "Завершить")
async def finish_post(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    post_text = (
        f"🏷 {data['title']}\n"
        f"🛒 Площадка: {data['market']}\n"
        f"💵 Цена: {data['price_before']} → {data['price_after']}\n"
        f"🔥 Скидка: {data['discount']}%\n"
    )
    
    await message.answer(post_text, reply_markup=types.ReplyKeyboardRemove())
    await state.clear()