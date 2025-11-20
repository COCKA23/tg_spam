from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio, random
import os
import logging


from config import *


'''Дополнитедьные функции'''


# Логирование
logging.basicConfig(
    filename= 'spam.txt',
    level= logging.INFO,
    encoding = 'utf-8',
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)



# Файл с гифками
def load_gif():
    try:
        with open("object/gif.txt", "r") as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        return [] 

# Файл с стикером
def load_sticker():
    try:
        with open("object/sticker.txt", "r") as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        return[]


'''Код спамера'''



# Данные для подключения к акаунту
app = Client(SESSION, API_ID, API_HASH)
RUN = {}
GIF_IDS = load_gif()
STICKER_IDS = load_sticker()

print("\nСтарт успешный💚\n")

# Авто-сбор гифок
@app.on_message(filters.animation)
async def collect_gif(_, msg: Message):
    gif_id = msg.animation.file_id
    if gif_id not in GIF_IDS:
        GIF_IDS.append(gif_id)
        print("[+] GIF добавлена:", gif_id)
        
        with open("object/gif.txt", "a") as f:
            f.write(gif_id + "\n")

# Авто-сбор стикеров
@app.on_message(filters.sticker)
async def collect_sticker(_, msg: Message):
    sticker_id = msg.sticker.file_id
    if sticker_id not in STICKER_IDS:
        STICKER_IDS.append(sticker_id)
        print("[+] STICKER добавлен:", sticker_id)
        
        with open("object/sticker.txt", "a") as f:
            f.write(sticker_id + "\n")

# Спам
@app.on_message(filters.command("spam", "/") & filters.me)
async def start_spam(client: Client, msg: Message):
    await msg.delete()
    RUN[msg.chat.id] = True
    text = msg.text.split(maxsplit=1)[1]

    while RUN.get(msg.chat.id):
        ch = random.random()
        
        try:
            if GIF_IDS and ch < 0.25:
                await client.send_animation(msg.chat.id, random.choice(GIF_IDS))
                
                logger.info("Успешная отправка GIF")
            elif ch < 0.50:
                photos = sorted(os.listdir("photo/"))
                random_photo = random.choice(photos)
                photo_path = os.path.join("photo/", random_photo)
                await client.send_photo(msg.chat.id, photo_path, caption= text)

                logger.info("Успешная отправка ФОТО")
            elif ch < 0.75:
                await client.send_sticker(msg.chat.id, random.choice(STICKER_IDS))

                logger.info("Успешная отправка STICKER")
            else:
                await client.send_message(msg.chat.id, text)

                logger.info("Успешная отправка СООБЩЕНИЯ")
                
            await asyncio.sleep(random.uniform(0.8, 1.3))

        except Exception as e:
           logger.error(f"Ошибка: {e}") 

# Cтоп
@app.on_message(filters.command("stop", "/") & filters.me)
async def stop_spam(client: Client, msg: Message):
    await msg.delete()
    RUN[msg.chat.id] = False

app.run()