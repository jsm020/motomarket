from data import config
from keyboards.inline.nested_product_keyboard import categories_keyboard, products_keyboard, product_keyboard, \
    products_callback_data, product_keyboard_for_admin
from loader import db, dp, bot
from aiogram.types import CallbackQuery
from keyboards.inline.menu_keyboard import menu


@dp.callback_query_handler(text="menu")
async def main_menu(call: CallbackQuery):
    await call.message.edit_text(text="Quyidagi bo'limlardan birini tanlang", reply_markup=menu)


@dp.callback_query_handler(text='products')
async def products(call: CallbackQuery):
    await open_categories_list(call)


async def open_categories_list(call: CallbackQuery, **kwargs):
    text = "Ushbu kategoriyalardan birini tanlang"
    markup = await categories_keyboard()
    await call.message.edit_text(text=text, reply_markup=markup)


async def open_products_list(call: CallbackQuery, category_id, **kwargs):
    text = "Mahsulotlar ro'yxati"
    markup = await products_keyboard(category_id=category_id)
    await call.message.edit_text(text=text, reply_markup=markup)


async def show_product(call: CallbackQuery, category_id, product_id, **kwargs):
    product = await db.select_products(id=product_id)
    product = product[0]
    if product["photo"]:
        text = f"<a href=\"{product['photo']}\">{product['name']}</a>\n\n"
    else:
        text = ""
    text += f"{product['name']}\n"
    text += f"\nNarxi: {product['price']} so'm\n"
    text += f"\n  {product['description']}"
    if str(call.message.chat.id) in config.ADMINS:
        markup = await product_keyboard_for_admin(category_id=category_id, product_id=product_id)
        await call.message.edit_text(text=text, reply_markup=markup)
    else:
        markup = await product_keyboard(category_id=category_id, product_id=product_id)
        await call.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query_handler(products_callback_data.filter())
async def navigate_all(call: CallbackQuery, callback_data: dict):
    current_level = callback_data.get('level')
    category_id = int(callback_data.get('category_id'))
    product_id = int(callback_data.get('product_id'))

    levels = {
        "0": open_categories_list,
        "1": open_products_list,
        "2": show_product,
    }
    current_level_function = levels[current_level]
    await current_level_function(
        call, category_id=category_id, product_id=product_id
    )
