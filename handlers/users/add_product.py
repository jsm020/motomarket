from aiogram import types
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup

from data.config import ADMINS
from keyboards.default import categories_list
from keyboards.default.back_menu import back_menu_keyboard
from keyboards.default.categories_list import categories_keyboard
from keyboards.inline.confirmation import confirm_keyboard
from keyboards.inline.menu_keyboard import menu
from loader import dp, db
from states.product_states import Product
from utils.photograph import photo_link


@dp.message_handler(Command('add_product'), user_id=ADMINS)
async def begin_creating(message: types.Message):
    text = "Mahsulot nomini kiriting"
    await message.answer(text=text)
    await Product.name.set()


@dp.message_handler(Command('add_product'))
async def disallowance_to_create_product(message: types.Message):
    await message.answer(
        text="❌ Sizda ruhsat mavjud emas!"
    )


@dp.message_handler(state=Product.name)
async def enter_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'name': name,
        }
    )
    markup = await categories_keyboard()
    await message.answer(text="Mahsulot uchun kategoriyalardan birini tanlang, \n"
                              "Agar siz kiritmoqchi bo'lgan kategoriya mavjud bo'lmasa /yaratish ni bosing",
                         reply_markup=markup
                         )
    await Product.category.set()


@dp.message_handler(Command('yaratish'), state=Product.category)
async def create_category(message: types.Message):
    text = "Yaratmoqchi bo'lgan kategoriyangiz nomini kiriting"
    await message.answer(text=text)
    await Product.new_category.set()


@dp.message_handler(state=Product.new_category)
async def create_category(message: types.Message, state: FSMContext):
    new_category = message.text.capitalize()
    await db.create_category(title=new_category)

    title = new_category.lower()
    category = await db.select_categories(title=title)
    if category:
        category = category[0]
        await state.update_data(
            {
                'category_id': category['id']
            }
        )

    text = "Kategoriya yaratildi"
    text += "\nMahsulot uchun rasm yuboring"
    await message.answer(text=text)
    await Product.photo.set()


@dp.message_handler(state=Product.category)
async def choose_category(message: types.Message, state: FSMContext):
    title = message.text
    category = await db.select_categories(title=title)
    print('category', category)
    if category:
        category = category[0]
        await state.update_data(
            {
                'category_id': category['id']
            }
        )
        await message.answer(text="Mahsulot uchun rasm yuboring")
        await Product.photo.set()
    else:
        markup = await categories_keyboard()
        await message.answer(text="Mahsulot uchun kategoriyalardan birini tanlang\n"
                                  "Agar siz kiritmoqchi bo'lgan kategoriya mavjud bo'lmasa /yaratish ni bosing",
                             reply_markup=markup
                             )
        await Product.category.set()


@dp.message_handler(state=Product.photo, content_types=types.ContentTypes.PHOTO)
async def enter_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    link = await photo_link(photo)
    await state.update_data(
        {
            'photo': link
        }
    )
    await message.answer(
        text="Mahsulot narxini kiriting\n"
             "U 12000 dan katta bo'lishi kerak."
    )
    await Product.price.set()


@dp.message_handler(state=Product.price)
async def enter_price(message: types.Message, state: FSMContext):
    price = message.text
    try:
        price = int(price)
        if price < 12000:
            await message.answer(text="Mahsulot narxi 12000 dan yuqori bo'lishi kerak")
            await Product.price.set()
        else:
            await state.update_data(
                {
                    'price': price
                }
            )
            await message.answer(text="Mahsulot haqida qisqacha ma'lumot kiriting")
            await Product.description.set()
    except:
        await message.answer(text="Mahsulot narxi son bo'lishi kerak")
        await Product.price.set()


@dp.callback_query_handler(state=Product.description, text="ok")
async def confirm_product(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    category_id = data.get("category_id")
    price = data.get("price")
    photo = data.get("photo")
    description = data.get("description")

    product = await db.create_product(
        name=name,
        category_id=category_id,
        photo_url=photo,
        price=price,
        description=description
    )

    text = "Ushbu mahsulot muvaffaqiyatli yaratildi"
    await call.message.answer(text=text, reply_markup=back_menu_keyboard)
    await state.finish()


@dp.callback_query_handler(state=Product.description, text="cancel")
async def confirm_product(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Siz mahsulni muvaffaqiyatli rad etdingiz", reply_markup=back_menu_keyboard)
    await state.finish()


@dp.message_handler(state=Product.description)
async def enter_description(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(
        {
            'description': description
        }
    )
    data = await state.get_data()
    name = data.get("name")
    category = data.get("category_id")
    price = data.get("price")
    photo = data.get("photo")
    description = data.get("description")

    if photo:
        text = f"<a href=\"{photo}\">{name}</a>\n\n"
    else:
        text = ""
    text += f"{name}\n"
    text += f"\nNarxi: {price} so'm\n"
    text += f"\n  {description}"

    text += "\n\n\nMahsulot quyidagicha bo'ladi\nUni davom etamizmi?"

    await message.answer(text=text, reply_markup=confirm_keyboard)


@dp.message_handler(filters.Text(equals="◀ Bosh Menyuga qaytish"))
async def back_to_menu(message: types.Message):
    text = "Quyidagi bo'limlardan birini tanlang"
    await message.answer(text=text, reply_markup=menu)
