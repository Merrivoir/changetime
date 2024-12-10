from telethon import TelegramClient, events
from datetime import datetime
import os

allowed_chats = [
    6785296508,
]

# Укажите ваши данные API
api_hash = os.getenv("TFOUR")
api_id = os.getenv("TTHREE")

chat_identifier = allowed_chats[0]
log_file = 'tour/cpl.txt'  # Имя файла для сохранения логов
attachments_folder = 'tour'  # Папка для вложений

# Создаем папку для вложений, если ее нет
os.makedirs(attachments_folder, exist_ok=True)

# Инициализируем клиента
client = TelegramClient('tremolo', api_id, api_hash)

# Обработчик новых сообщений
@client.on(events.NewMessage(chats=chat_identifier))
async def handle_new_message(event):
    message = event.message
    with open(log_file, 'a', encoding='utf-8') as log:
        # Форматирование текста сообщения
        timestamp = message.date.strftime('%Y-%m-%d %H:%M:%S')
        sender = "1" if message.out else "2"
        text = message.text or "<none text>"
        log_line = f"[{timestamp}] {sender}: {text}\n"
        log.write(log_line)
        print(log_line.strip())
        
        # Проверка наличия вложений
        if message.media:
            # Сохраняем вложение
            file_path = await client.download_media(
                message.media,
                file=attachments_folder
            )
            if file_path:
                log_line = f"  Вложение сохранено: {file_path}\n"
                log.write(log_line)
                print(log_line.strip())

# Запуск клиента
print("Скрипт запущен. Ожидание новых сообщений...")
client.start()
client.run_until_disconnected()
