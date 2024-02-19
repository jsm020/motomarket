from aiogram.dispatcher.filters.state import State, StatesGroup


class Product(StatesGroup):
    name = State()
    new_category = State()
    category = State()
    photo = State()
    price = State()
    description = State()


class EditProduct(StatesGroup):
    base = State()
    name = State()
    new_category = State()
    category = State()
    photo = State()
    price = State()
    description = State()
