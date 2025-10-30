from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio, random
import os


from config import *


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

        if GIF_IDS and ch < 0.33:
            await client.send_animation(msg.chat.id, random.choice(GIF_IDS))
        elif ch < 0.66:
            photos = sorted(os.listdir("photo/"))
            
            random_photo = random.choice(photos)
            photo_path = os.path.join("photo/", random_photo)
            await client.send_photo(msg.chat.id, photo_path, caption= text)
        else:
            await client.send_message(msg.chat.id, text)
            
        await asyncio.sleep(random.uniform(0.8, 2.2))

# Cтоп
@app.on_message(filters.command("stop", "/") & filters.me)
async def stop_spam(client: Client, msg: Message):
    await msg.delete()
    RUN[msg.chat.id] = False

app.run()
