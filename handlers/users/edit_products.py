from aiogram import types
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters import Command
from data.config import ADMINS
from keyboards.default.back_menu import back_menu_keyboard
from keyboards.default.categories_list import categories_keyboard
from keyboards.inline.nested_product_keyboard import edit_delete_callback_data, edit_or_cancel_markup, edit_or_cancel
from loader import dp, bot, db
from states.product_states import Product, EditProduct
from utils.photograph import photo_link


@dp.callback_query_handler(edit_delete_callback_data.filter(act='edit'), user_id=ADMINS)
async def exact_part(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    product_id = callback_data.get('product_id')
    text = "Quyidagilardan qaysini o'zgartirmoqchisiz?"
    text += "\nMahsulot nomi: /edit_name"
    text += "\nMahsulot kategoriyasi: /edit_category"
    text += "\nMahsulot rasmi: /edit_photo"
    text += "\nMahsulot narxi: /edit_price"
    text += "\nMahsulot haqida qisqacha ma'lumot: /edit_description"
    text += "\nO'zgartirmoqchi bo'lganingizning ustiga bosing"
    await EditProduct.base.set()
    await state.update_data(
        {
            'product_id': product_id
        }
    )
    await call.message.answer(text=text)


# for edit name
@dp.message_handler(Command('edit_name'), state=EditProduct.base)
async def run_state_name(message: types.Message, state: FSMContext):
    text = "Mahsulot uchun yangi nomni kiriting"
    await message.answer(text=text)
    await EditProduct.name.set()


@dp.message_handler(state=EditProduct.name)
async def edit_product_name(message: types.Message, state: FSMContext):
    product_name = message.text
    await state.update_data(
        {
            'name': product_name,
        }
    )
    text = "Yana o'zgartirasizmi?"
    text += "\nMahsulot nomi: /edit_name"
    text += "\nMahsulot kategoriyasi: /edit_category"
    text += "\nMahsulot rasmi: /edit_photo"
    text += "\nMahsulot narxi: /edit_price"
    text += "\nMahsulot haqida qisqacha ma'lumot: /edit_description"
    text += "\nO'zgartirmoqchi bo'lganingizning ustiga bosing"
    data = await state.get_data()
    product_id = int(data.get('product_id'))
    markup = await edit_or_cancel_markup(product_id=product_id)
    await message.answer(
        text=text,
        reply_markup=markup
    )
    await EditProduct.base.set()


# for edit category
@dp.message_handler(Command('edit_category'), state=EditProduct.base)
async def run_state_category(message: types.Message):
    text = "Mahsulot uchun kategory kiriting"
    await message.answer(text=text, reply_markup=await categories_keyboard())
    await EditProduct.category.set()


@dp.message_handler(state=EditProduct.category)
async def edit_product_category(message: types.Message, state: FSMContext):
    category = message.text
    await state.update_data(
        {
            'category': category,
        }
    )
    text = "Yana o'zgartirasizmi?"
    text += "\nMahsulot nomi: /edit_name"
    text += "\nMahsulot kategoriyasi: /edit_category"
    text += "\nMahsulot rasmi: /edit_photo"
    text += "\nMahsulot narxi: /edit_price"
    text += "\nMahsulot haqida qisqacha ma'lumot: /edit_description"
    text += "\nO'zgartirmoqchi bo'lganingizning ustiga bosing"
    data = await state.get_data()
    product_id = int(data.get('product_id'))
    markup = await edit_or_cancel_markup(product_id=product_id)
    await message.answer(
        text=text,
        reply_markup=markup
    )
    await EditProduct.base.set()


# for edit photo
@dp.message_handler(Command('edit_photo'), state=EditProduct.base)
async def run_state_photo(message: types.Message):
    text = "Mahsulot uchun yangi rasm kiriting"
    await message.answer(text=text)
    await EditProduct.photo.set()


@dp.message_handler(state=EditProduct.photo, content_types=types.ContentType.PHOTO)
async def edit_product_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    link = await photo_link(photo)
    await state.update_data(
        {
            'photo': link
        }
    )

    text = "Yana o'zgartirasizmi?"
    text += "\nMahsulot nomi: /edit_name"
    text += "\nMahsulot kategoriyasi: /edit_category"
    text += "\nMahsulot rasmi: /edit_photo"
    text += "\nMahsulot narxi: /edit_price"
    text += "\nMahsulot haqida qisqacha ma'lumot: /edit_description"
    text += "\nO'zgartirmoqchi bo'lganingizning ustiga bosing"
    data = await state.get_data()
    product_id = int(data.get('product_id'))
    markup = await edit_or_cancel_markup(product_id=product_id)
    await message.answer(
        text=text,
        reply_markup=markup
    )
    await EditProduct.base.set()


# for edit price
@dp.message_handler(Command('edit_price'), state=EditProduct.base)
async def run_state_price(message: types.Message):
    text = "Mahsulot uchun yangi narx kiriting, \n" \
           "Yangi narx 12000 dan kichik bo'lmasligi kerak"
    await message.answer(text=text)
    await EditProduct.price.set()


@dp.message_handler(state=EditProduct.price)
async def edit_product_price(message: types.Message, state: FSMContext):
    price = int(message.text)
    if price >= 12000:
        await state.update_data(
            {
                'price': price,
            }
        )
        text = "Yana o'zgartirasizmi?"
        text += "\nMahsulot nomi: /edit_name"
        text += "\nMahsulot kategoriyasi: /edit_category"
        text += "\nMahsulot rasmi: /edit_photo"
        text += "\nMahsulot narxi: /edit_price"
        text += "\nMahsulot haqida qisqacha ma'lumot: /edit_description"
        text += "\nO'zgartirmoqchi bo'lganingizning ustiga bosing"
        data = await state.get_data()
        product_id = int(data.get('product_id'))
        markup = await edit_or_cancel_markup(product_id=product_id)
        await message.answer(
            text=text,
            reply_markup=markup
        )
        await EditProduct.base.set()
    else:
        text = "Mahsulot uchun yangi narx kiriting, \n" \
               "Yangi narx 12000 dan kichik bo'lmasligi kerak"
        await message.answer(text=text)
        await EditProduct.price.set()


# for edit description
@dp.message_handler(Command('edit_description'), state=EditProduct.base)
async def run_state_description(message: types.Message):
    text = "Mahsulot uchun yangi qisqacha ma'lumot kiriting"
    await message.answer(text=text)
    await EditProduct.description.set()


@dp.message_handler(state=EditProduct.description)
async def edit_product_description(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(
        {
            'description': description,
        }
    )
    text = "Yana o'zgartirasizmi?"
    text += "\nMahsulot nomi: /edit_name"
    text += "\nMahsulot kategoriyasi: /edit_category"
    text += "\nMahsulot rasmi: /edit_photo"
    text += "\nMahsulot narxi: /edit_price"
    text += "\nMahsulot haqida qisqacha ma'lumot: /edit_description"
    text += "\nO'zgartirmoqchi bo'lganingizning ustiga bosing"
    data = await state.get_data()
    product_id = int(data.get('product_id'))
    markup = await edit_or_cancel_markup(product_id=product_id)
    await message.answer(
        text=text,
        reply_markup=markup
    )
    await EditProduct.base.set()


@dp.callback_query_handler(edit_or_cancel.filter(), state=EditProduct.base)
async def edit_or_cancel(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    edit_cancel = callback_data.get("edit_cancel")
    if edit_cancel == 'edit':
        product_id = int(callback_data.get('product_id'))
        product = await db.select_products(id=product_id)
        product = product[0]
        print('product', product)
        data = await state.get_data()
        name = data.get('name', product['name'])
        category_data = data.get('category', None)
        category = await db.select_categories(title=category_data)
        if category:
            category_id = category[0]['id']
        else:
            category_id = product['category_id']
        price = int(data.get('price', product['price']))
        photo = data.get('photo', product['photo'])
        description = data.get('description', product['description'])
        updated_product = await db.update_product(id=product_id, name=name, category_id=category_id, price=price,
                                                  photo=photo, description=description)
        print('updated_product', updated_product)
        await state.finish()
        await call.message.answer(
            text="Mahsulot muvaffaqiyatli o'zgartirildi",
            reply_markup=back_menu_keyboard
        )
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    else:
        await state.finish()
        await call.message.answer(
            text="Amaliyot bekor qilindi",
            reply_markup=back_menu_keyboard
        )
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
