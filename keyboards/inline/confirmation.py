from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=" 🎁 Yaratish", callback_data="ok"),
            InlineKeyboardButton(text="❌ Cancel", callback_data='cancel')
        ]
    ]
)
