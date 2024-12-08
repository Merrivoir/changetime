from telethon import TelegramClient, events
import os
from datetime import datetime
from utils import sandjob

api_hash = os.getenv("TTWO")
api_id = os.getenv("TONE")

allowed_chats = [
    #123456789,
]
me = sandjob.sender.my
print(f"ID client: {me}")

# Создаем директорию для логов и загрузок
os.makedirs("data", exist_ok=True)
os.makedirs("data/private", exist_ok=True)
os.makedirs("data/groups", exist_ok=True)
os.makedirs("data/channels", exist_ok=True)

# Инициализация клиента
client = TelegramClient('session_name', api_id, api_hash)

#------------------------------------------------------------------------------------------------------------------
# Функция для логирования сообщений

def log_message(log, sender, message, file_path=None):
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}]  {sender}: {message}\n"

    if file_path:  # Если есть медиафайл
        log_entry += f"Медиафайл: {file_path}\n"

    # Сохраняем лог в файл
    with open(log, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

#------------------------------------------------------------------------------------------------------------------
# Обработчик новых сообщений
@client.on(events.NewMessage)
async def handle_new_message(event):
    
    msgSender = event.sender_id # Сохраняем ID отправителя
    msgText = event.message.text or "<Без текста>" # Текст сообщения
    msgChat = event.chat_id
    isGroup = event.is_group
    isChannel = True if msgChat < 0 and isGroup == False else False
     
    #Логируем ID, направление и текст
    
    if (msgChat != msgSender and msgSender == me) or msgChat == msgSender:
        dir = f"data/private"
        down = f"data/private/{msgChat}/"
        log = f"data/private/{msgChat}.log"

    elif isChannel:
        dir = f"data/channels"
        down = f"data/channels/{msgChat}/"
        log = f"data/channels/{msgChat}.log"

    elif isGroup:
        dir = f"data/groups"
        down = f"data/groups/{msgChat}/"
        log = f"data/groups/{msgChat}.log"


    print(f"""
        Group: {isGroup}
        Channel: {isChannel}
        Chat: {msgChat}
        Sender: {msgSender}
        My ID: {me}
        Text: {msgText}
        Directory: {dir}
        Log: {log}
        Downloads: {down}
    """)

    if event.media:  # Если сообщение содержит медиа
        file_path = await event.download_media(file=down)
        log_message(log, msgSender, msgText, file_path)
    else:  # Если это текстовое сообщение
        log_message(log, msgSender, msgText)

#------------------------------------------------------------------------------------------------------------------
# Запускаем клиент
with client:
    print("Запуск клиента...")
    client.run_until_disconnected()