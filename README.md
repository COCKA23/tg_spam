# tg_spam  
Простой Telegram-спамер на pyrogram.

## Описание
Проэкт был полностью переделан на другую бибилиотеку, Это связонно с тем что
преведущая веррсия была не стабильной, могла переключиться на другое окно если 
поментять местро курсора.

Так же в новом скрипте появилась функция спам .gif и photo спам ими происходит 
атоматичекси вместе с спамом сообщений.  

## Особенности
- ✅ Стабильная работа (не теряет фокус окна)
- ✅ Автоматическая отправка GIF-файлов
- ✅ Отпрака фоток(рандомный выбор)

## Обновление
Самым главным новвоведение стало отправка радномных фотографий 
```python
    while RUN.get(msg.chat.id):
        ch = random.random()

        if GIF_IDS and ch < 0.33: #вероятнось 33%
            await client.send_animation(msg.chat.id, random.choice(GIF_IDS))
        elif ch < 0.66: #вероятнось 33%
            #собирает файлы в одну переменную
            photos = sorted(os.listdir("photo/"))
            
            #Выбирает андомное фото
            random_photo = random.choice(photos)
            #Собирает путь
            photo_path = os.path.join("photo/", random_photo)
            #Отправка
            await client.send_photo(msg.chat.id, photo_path, caption= text)#Коментарий "caption= text"
        else: #вероятнось 34%
            await client.send_message(msg.chat.id, text)
        
        await asyncio.sleep(random.uniform(0.8, 2.2))
```
C помощью данной библиотеки мы можем начать отправлять фото а также делать коментарий.
Мини обновление но оно полезное.

## Установка
```bash
git clone https://github.com/COCKA23/tg_spam.git
cd spammer
python -m venv venv
venv\Scripts\activate          # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Применение
Основные команды "/spam текст" это команда начинает спам вместе с gif. 
"/stop" останавливает спам 

НУ для начала нужно зайти на офицыальный [Telegram API](https://my.telegram.org) теперь нужно перейти в раздел "API development tools", от туда нам нужно будет
взять "App api_id" и "App api_hash" и втсавить их в config.py и сохранить
файл. Теперь можно запутить код, при первом запуски создасться файл 
gif.txt там будут id gif для отправки, перед начлом спама нужно просто по
отпровлять несколько gif, тогда в консоле будет сообщение "[+] GIF добавлена".
Также библиотека создаст два файла и будет просить войти в акаунт.




