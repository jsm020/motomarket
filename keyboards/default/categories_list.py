from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db


async def categories_keyboard():
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    categories = await db.get_categories()
    for category in categories:
        text_button = f"{category['title']}".capitalize()
        markup.insert(
            KeyboardButton(
                text=text_button
            )
        )

    return markup
