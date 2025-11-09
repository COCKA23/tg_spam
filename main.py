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
        with open("gif.txt", "r") as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        return [] 


# Данные для подключения к акаунту
app = Client(SESSION, API_ID, API_HASH)
RUN = {}
GIF_IDS = load_gif()



'''Код спамера'''



print("\nСтарт успешный💚\n")

# Авто-сбор гифок
@app.on_message(filters.animation)
async def collect_gif(_, msg: Message):
    gif_id = msg.animation.file_id
    if gif_id not in GIF_IDS:
        GIF_IDS.append(gif_id)
        print("[+] GIF добавлена:", gif_id)
        
        with open("gif.txt", "a") as f:
            f.write(gif_id + "\n")

# Спам
@app.on_message(filters.command("spam", "/") & filters.me)
async def start_spam(client: Client, msg: Message):
    await msg.delete()
    RUN[msg.chat.id] = True
    text = msg.text.split(maxsplit=1)[1]

    while RUN.get(msg.chat.id):
        ch = random.random()
        
        try:
            if GIF_IDS and ch < 0.33:
                await client.send_animation(msg.chat.id, random.choice(GIF_IDS))
                
                logger.info("Успешная отправка GIF")
            elif ch < 0.66:
                photos = sorted(os.listdir("photo/"))
                random_photo = random.choice(photos)
                photo_path = os.path.join("photo/", random_photo)
                await client.send_photo(msg.chat.id, photo_path, caption= text)

                logger.info("Успешная отправка ФОТО")
            else:
                await client.send_message(msg.chat.id, text)

                logger.info("Успешная отправка СООБЩЕНИЯ")
                
            await asyncio.sleep(random.uniform(0.8, 2.2))

        except Exception as e:
           logger.error(f"Ошибка: {e}") 

# Cтоп
@app.on_message(filters.command("stop", "/") & filters.me)
async def stop_spam(client: Client, msg: Message):
    await msg.delete()
    RUN[msg.chat.id] = False

app.run()
