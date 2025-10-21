import pyautogui      # эмуляция клавиатуры/мыши
import pyperclip      # буфер обмена (Ctrl+V)
import time           
import random         

def generator_message(base_text):
    """Возвращает один из 5 случайных вариантов текста."""
    variants = [
        f"{base_text} {random.randint(1000, 9999)}",
        f"{base_text.upper()}",
        f"{base_text.lower()}",
        f"{base_text}{random.choice(['😎', '🤡', '💩', '🔥'])}",
        f"{random.choice(['😎', '🤡', '💩', '🔥'])}"
    ]
    return random.choice(variants)

def send_message(text):
    """Копирует text в буфер и отправляет Ctrl+V + Enter."""
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')

def spam_tg(message, amount):
    """Цикл отправки `amount` сообщений с паузой 0.5-3 с."""
    for i in range(1, amount + 1):
        msg = generator_message(message)
        send_message(msg)
        print(f"\r💚 Отправлено: {i}/{amount}", end=' ', flush=True)
        time.sleep(random.uniform(0.5, 3.0))

def get_user_input():
    """Запрашивает текст, кол-во и таймер. При ошибке возвращает (None,None,None)."""
    message = input("💬 Введи текст для отправки: ")
    try:
        amount      = int(input("🔢 Количество сообщений: "))
        start_time  = int(input("⏱️ Через сколько секунд начать спам?: "))
    except ValueError:
        print("❌ Ошибка ввода. Введи число!")
        return None, None, None
    return message, amount, start_time

def main():
    """Точка входа: собирает данные, ждёт, спамит."""
    print("😎 Запуск спам-скрипта ... ⚡")
    message, amount, start_time = get_user_input()
    if message is None:
        return

    print(f"⏳ Старт через {start_time} сек...")
    time.sleep(start_time)

    spam_tg(message, amount)
    print("\n✅ Готово. Не забудь удалить следы.")

if __name__ == '__main__':
    main()