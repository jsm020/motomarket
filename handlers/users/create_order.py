from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message, LabeledPrice

from data import config
from data.config import ADMINS
from data.shipping import FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING
from keyboards.default.back_menu import back_menu_keyboard
from keyboards.inline.nested_product_keyboard import buy_product_callback_data, get_payment_option

from loader import dp, bot, db
from utils.misc.product import Product
from typing import Union


@dp.message_handler(Command('my_orders'))
@dp.callback_query_handler(text="my_orders")
async def my_orders(message: Union[CallbackQuery, Message]):
    if isinstance(message, CallbackQuery):
        call = message
        user = await db.select_users(telegram_id=call.from_user.id)
        orders = await db.select_orders(user_id=user[0]['id'])
        if orders:
            text = ""
            count_ = 0
            for order in orders:
                product_order = await db.select_order_product(order_id=order['id'])
                product_id = product_order[0]['product_id']
                products = await db.select_products(id=product_id)
                product = products[0]
                count_ += 1
                text += f"{count_}.\n"
                text += f"Product: {product['name'].capitalize()}\n"
                text += f"Currency: {order['currency']}\n"
                text += f"Total amount: {order['total_amount']}\n"
                text += f"Date: {order['created_time']}\n\n\n"

            await call.message.answer(text=text, reply_markup=back_menu_keyboard)
        else:
            await call.message.answer(
                text="Siz hali hech narsa sotib olmadingiz",
                reply_markup=back_menu_keyboard
            )
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


    else:
        user = await db.select_users(telegram_id=message.from_user.id)
        orders = await db.select_orders(user_id=user[0]['id'])
        if orders:
            text = ""
            count_ = 0
            for order in orders:
                product_order = await db.select_order_product(order_id=order['id'])
                product_id = product_order[0]['product_id']
                products = await db.select_products(id=product_id)
                product = products[0]
                count_ += 1
                text += f"{count_}.\n"
                text += f"Product: {product['name'].capitalize()}\n"
                text += f"Currency: {order['currency']}\n"
                text += f"Total amount: {order['total_amount']}\n"
                text += f"Date: {order['created_time']}\n\n\n"

            await message.answer(text=text, reply_markup=back_menu_keyboard)
        else:
            await message.answer(
                text="Siz hali hech narsa sotib olmadingiz",
                reply_markup=back_menu_keyboard
            )


@dp.callback_query_handler(buy_product_callback_data.filter(cart="basic"))
async def choose_cart(call: CallbackQuery, callback_data: dict):
    product_id = int(callback_data.get('product_id'))
    products = await db.select_products(id=product_id)
    product = products[0]
    text = "To'lovni qaysi yo'l bilan amalga oshirmoqchisi? "
    markup = get_payment_option(product_id=product_id, category_id=product['category_id'])

    await call.message.answer(text=text, reply_markup=markup)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(buy_product_callback_data.filter())
async def book_invoice(call: CallbackQuery, callback_data: dict):
    print(callback_data)
    product_id = int(callback_data.get('product_id'))
    cart = callback_data.get('cart')
    products = await db.select_products(id=product_id)
    product = products[0]
    price = int(product['price'])

    if cart == "click":
        provider = config.PROVIDER_TOKEN_CLICK
        currency = "UZS"
    elif cart == "tranzo":
        provider = config.PROVIDER_TOKEN_TRANZO
        currency = "USD"
        price = price / 12500
    else:
        provider = config.PROVIDER_TOKEN_PAYME
        currency = "UZS"
    price *= 100
    price = int(price)

    order = Product(
        title=product['name'],
        description=product['description'],
        currency=currency,
        prices=[
            LabeledPrice(
                label='Mahsulot',
                amount=price
            ),
        ],
        start_parameter="create_invoice_ds_praktikum",
        photo_url=product['photo'],
        photo_width=1280,
        photo_height=564,
        # photo_size=600,
        # need_email=True,
        need_shipping_address=True,  # foydalanuvchi manzilini kiritishi shart
        need_name=True,
        need_phone_number=True,
        provider_token=provider
    )
    await bot.send_invoice(chat_id=call.from_user.id,
                           **order.generate_invoice(),
                           payload=str(product['id']))

    await call.answer()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.shipping_query_handler()
async def choose_shipping(query: types.ShippingQuery):
    if query.shipping_address.country_code != "UZ":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        ok=False,
                                        error_message="Chet elga yetkazib bera olmaymiz")
    elif query.shipping_address.city.lower() == "tashkent":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING],
                                        ok=True)
    else:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[REGULAR_SHIPPING],
                                        ok=True)


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)
    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text="Xaridingiz uchun rahmat!", reply_markup=back_menu_keyboard)
    await bot.send_message(chat_id=ADMINS[0],
                           text=f"Quyidagi mahsulot sotildi: {pre_checkout_query.invoice_payload}\n"
                                f"ID: {pre_checkout_query.id}\n"
                                f"Telegram user: {pre_checkout_query.from_user.first_name}\n"
                                f"Xaridor: {pre_checkout_query.order_info.name}, tel: {pre_checkout_query.order_info.phone_number}",
                           reply_markup=back_menu_keyboard
                           )


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print(message.successful_payment)
    user = await db.select_users(telegram_id=message.from_user.id)
    user_id = user[0]['id']
    currency = message.successful_payment.currency
    total_amount = message.successful_payment.total_amount
    invoice_payload = message.successful_payment.invoice_payload

    # order info
    order_info = message.successful_payment.order_info
    user_name = order_info.name
    phone_number = order_info.phone_number
    email = order_info.email

    # location
    state = order_info.shipping_address.state
    city = order_info.shipping_address.city

    order = await db.create_order(
        user_id=user_id,
        currency=currency,
        total_amount=total_amount,
        invoice_payload=invoice_payload,
        state=state,
        city=city,
        user_name=user_name,
        phone_number=phone_number,
        email=email
    )

    order_product = await db.create_order_product(
        order_id=order["id"],
        product_id=int(invoice_payload)
    )
