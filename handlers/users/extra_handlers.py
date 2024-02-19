from aiogram import types

from keyboards.default.back_menu import back_menu_keyboard
from loader import dp, bot


@dp.callback_query_handler(text='support')
async def support(call: types.CallbackQuery):
    text = "Bot haqida to'liq ma'lumot olish uchun: \n\n" \
           "Tel: +998881778747\n" \
           "Command: /help\n" \
           "Telegram: https://t.me/HikmatullayevFarhod0205\n" \
           "Pochta manzili: farhodjonhikmatullayev@gmail.com\n" \
           "\n" \
           "Yuqoridagilardan biri orqali murojaat qiling"
    await call.message.answer(text=text, reply_markup=back_menu_keyboard)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
