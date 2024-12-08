from telethon import TelegramClient, events
import os
from datetime import datetime

api_hash = os.getenv("TTWO")
api_id = os.getenv("TONE")

#print(f"{api_hash}:{api_id}")

allowed_chats = [
    #123456789,
]

# Инициализация клиента
client = TelegramClient('session_name', api_id, api_hash)

async def list_chats():
    async for dialog in client.iter_dialogs():
        print(f"{dialog.name}: {dialog.id}")

with client:
    client.loop.run_until_complete(list_chats())