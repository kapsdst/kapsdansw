import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties

# Токен и ID администратора
BOT_TOKEN = "7875811952:AAHDfz_-g6UaU48RU4ITCVx7jB9mkDhVH7M"
ADMIN_ID = 1006934033  # ← это ты

# Логгирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# 👉 Сначала хендлер для команды /reply
@dp.message(Command("reply"))
async def reply_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ У тебя нет прав на использование этой команды.")
        return

    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer("⚠️ Формат: /reply <user_id> <текст ответа>")
        return

    try:
        user_id = int(args[1])
        reply_text = args[2]
        await bot.send_message(chat_id=user_id, text=f"✉️ Ответ от администратора:\n\n{reply_text}")
        await message.answer("✅ Ответ отправлен.")
    except Exception as e:
        await message.answer(f"❌ Ошибка при отправке: {e}")

# 👉 Затем общий хендлер
@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "без username"
    text = message.text

    # Отправляем админу
    admin_message = (
        f"📩 Сообщение от @{username} (ID: <code>{user_id}</code>):\n\n"
        f"{text}\n\n"
        f"Ответ:\n<code>/reply {user_id} Твой ответ</code>"
    )
    await bot.send_message(chat_id=ADMIN_ID, text=admin_message)

    # Ответ пользователю
    await message.answer("Спасибо за сообщение! Мы скоро ответим.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
