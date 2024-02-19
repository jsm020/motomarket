from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🛍️ Mahsulotlar", callback_data='products'),
        ],
        [
            InlineKeyboardButton(text='📦 Mening buyurtmalarim', callback_data='my_orders'),
        ],
        [
            InlineKeyboardButton(text='❓ Help', callback_data='help'),
            InlineKeyboardButton(text='🤝 Support', callback_data='support'),
        ]
    ]
)
