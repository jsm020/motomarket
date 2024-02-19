from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
            types.BotCommand('my_orders', "Buyurtmalar tarixi"),
            types.BotCommand("add_product", "Mahsulot qo'shish"),
        ]
    )
