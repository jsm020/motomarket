from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

products_callback_data = CallbackData('products', 'level', 'category_id', 'product_id')
buy_product_callback_data = CallbackData('buy', 'product_id', "cart")
edit_delete_callback_data = CallbackData('edit', 'act', 'product_id')
are_you_sure_callback_data = CallbackData('sure', 'product_id', 'yes_no')
edit_or_cancel = CallbackData('edit_or_cancel', 'product_id', 'edit_cancel')


async def edit_or_cancel_markup(product_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="O'zgartirish",
                                     callback_data=edit_or_cancel.new(product_id=product_id, edit_cancel='edit')),
                InlineKeyboardButton(text="Bekor qilish",
                                     callback_data=edit_or_cancel.new(product_id=product_id, edit_cancel='cancel')),
            ]
        ]
    )
    return markup


async def create_sureness_button(product_id):
    sureness_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Yes",
                                     callback_data=are_you_sure_callback_data.new(product_id=product_id, yes_no="yes")),
                InlineKeyboardButton(text="No",
                                     callback_data=are_you_sure_callback_data.new(product_id=product_id, yes_no="no"))
            ]
        ]
    )
    return sureness_markup


def create_callback_data(level, category_id='0', product_id='0'):
    return products_callback_data.new(
        level=level,
        category_id=category_id,
        product_id=product_id
    )


async def categories_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    categories = await db.get_categories()
    for category in categories:
        text_button = f"{category['title']}".capitalize()
        callback_data = create_callback_data(level=1, category_id=category['id'])
        markup.insert(
            InlineKeyboardButton(
                text=text_button,
                callback_data=callback_data,
            )
        )
    markup.insert(
        InlineKeyboardButton(
            text="⏪ Orqaga",
            callback_data='menu'
        )
    )

    return markup


async def products_keyboard(category_id):
    markup = InlineKeyboardMarkup(row_width=1)
    products = await db.select_products(category_id=category_id)
    for product in products:
        text_button = f"{product['name']}".capitalize()
        callback_data = create_callback_data(level=2, category_id=category_id, product_id=product['id'])
        markup.insert(
            InlineKeyboardButton(
                text=text_button,
                callback_data=callback_data
            )
        )
    markup.insert(
        InlineKeyboardButton(
            text='⏪ Orqaga',
            callback_data=create_callback_data(
                level=0
            )
        )
    )
    return markup


async def product_keyboard(category_id, product_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💸 Xarid qilish",
                                     callback_data=buy_product_callback_data.new(product_id=product_id, cart="basic")),
                InlineKeyboardButton(
                    text='⏪ Orqaga',
                    callback_data=create_callback_data(
                        level=1,
                        category_id=category_id
                    )
                )
            ]
        ]
    )

    return markup


async def product_keyboard_for_admin(category_id, product_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✏️ Taxrirlash", callback_data=edit_delete_callback_data.new(
                    act='edit', product_id=product_id
                )),
                InlineKeyboardButton(text="🗑️ O'chirish", callback_data=edit_delete_callback_data.new(
                    act='delete', product_id=product_id
                ))
            ],
            [
                InlineKeyboardButton(text="💸 Xarid qilish",
                                     callback_data=buy_product_callback_data.new(product_id=product_id, cart="basic")),
                InlineKeyboardButton(
                    text='⏪ Orqaga',
                    callback_data=create_callback_data(
                        level=1,
                        category_id=category_id
                    )
                )
            ]
        ]
    )

    return markup


def get_payment_option(product_id, category_id):
    payment_options = InlineKeyboardMarkup()
    payment_options.insert(
        InlineKeyboardButton(text="Payme",
                             callback_data=buy_product_callback_data.new(product_id=product_id, cart='payme'))
    )
    payment_options.insert(
        InlineKeyboardButton(text="Click",
                             callback_data=buy_product_callback_data.new(product_id=product_id, cart='click'))
    )
    payment_options.insert(
        InlineKeyboardButton(text="Tranzo",
                             callback_data=buy_product_callback_data.new(product_id=product_id, cart='tranzo'))
    )

    payment_options.insert(
        InlineKeyboardButton(
            text="⏪ Orqaga",
            callback_data=create_callback_data(level=2, category_id=category_id, product_id=product_id)
        )
    )
    return payment_options
