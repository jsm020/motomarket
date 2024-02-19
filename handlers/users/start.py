import asyncpg
from aiogram import types
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import filters, FSMContext
from keyboards.inline.menu_keyboard import menu
from loader import dp, db


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    try:
        user = await db.create_user(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username,
        )
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)

    text = f"Salom, {message.from_user.full_name}!\n"
    text += "Botimizga xush kelibsiz"
    await message.answer(text, reply_markup=menu)
    await state.finish()
