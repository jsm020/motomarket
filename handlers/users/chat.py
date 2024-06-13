import json
from aiogram import types
import websockets
from aiogram import types
from keyboards.inline.menu_keyboard import menu
from loader import dp, db,bot
from datetime import datetime

# WebSocket URL manzili

async def send_message_to_ws(message):
    WS_URI = f"ws://localhost:8000/ws/chat/chat_with_{message['sender_id']}/"

    try:
        async with websockets.connect(WS_URI) as websocket:
            await websocket.send(json.dumps(message))
            print(f"Yuborilgan xabar: {message}")

            while True:
                response = await websocket.recv()
                data = json.loads(response)
                if data["sender_id"] != message["sender_id"]:
                    print(f"Olingan xabar: {response}")
                    await bot.send_message(chat_id=message["sender_id"], text=f'{data["message"]}')
    except Exception as e:
        print(f"WebSocket connection error: {e}")

@dp.message_handler()
async def echo(message: types.Message):
    # WebSocket orqali xabar yuborish
    ws_message = {
        "message": message.text,
        "sender_id": str(message.from_user.id),
        "time": datetime.now().strftime("%h-%d %H:%M")  # Telegram chat ID ni qo'shamiz
    }
    await send_message_to_ws(ws_message)