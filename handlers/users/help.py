from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from typing import Union
from loader import dp, bot


@dp.callback_query_handler(text='help')
@dp.message_handler(CommandHelp())
async def bot_help(message: Union[types.CallbackQuery, types.Message]):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam",
            "/my_orders - Buyurtmalar tarixi",
            "/add_product - Mahsulot qo'shish, Ushbu buyruq faqat adminlar uchun"
            )
    if isinstance(message, types.Message):
        await message.answer("\n".join(text))
    else:
        call = message
        await call.message.answer("\n".join(text))
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
