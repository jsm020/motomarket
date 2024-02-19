from aiogram import types

from data.config import ADMINS
from keyboards.inline.nested_product_keyboard import edit_delete_callback_data, create_sureness_button, \
    are_you_sure_callback_data
from loader import dp, bot, db


@dp.callback_query_handler(edit_delete_callback_data.filter(act='delete'), user_id=ADMINS)
async def sure_to_delete(call: types.CallbackQuery, callback_data: dict):
    product_id = callback_data.get('product_id')
    text = "Haqiqatdan ham bu mahsulotni o'chirmoqchimisiz?"
    markup = await create_sureness_button(product_id=product_id)
    await call.message.answer(
        text=text,
        reply_markup=markup
    )
    await call.message.delete()


@dp.callback_query_handler(are_you_sure_callback_data.filter())
async def delete_or_cancel(call: types.CallbackQuery, callback_data: dict):
    product_id = int(callback_data.get('product_id'))
    yes_no = callback_data.get('yes_no')
    if yes_no == "yes":
        await db.delete_product(id=product_id)
        text = "Mahsulot muvaffaqiyatli o'chirildi"
        await call.message.edit_text(text=text)
    else:
        text = "Amaliyot to'xtatildi"
        await call.message.edit_text(text=text)
