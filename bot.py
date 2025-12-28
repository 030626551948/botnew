import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TOKEN, ADMIN_ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}

# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я бот для приёма заявок.\nВведите своё имя:")

# Обработка сообщений
@dp.message()
async def get_info(message: types.Message):
    chat_id = message.from_user.id

    if chat_id not in user_data:
        user_data[chat_id] = {"name": message.text}
        await message.answer("Отлично! Теперь введите телефон:")
    else:
        user_data[chat_id]["phone"] = message.text

        # Сохраняем в файл
        with open("data.txt", "a", encoding="utf-8") as f:
            f.write(f"{user_data[chat_id]['name']} - {user_data[chat_id]['phone']}\n")

        # Отправка админу
        await bot.send_message(
            ADMIN_ID,
            f"Новая заявка:\nИмя: {user_data[chat_id]['name']}\nТелефон: {user_data[chat_id]['phone']}"
        )

        await message.answer("Спасибо! Ваша заявка отправлена.")
        del user_data[chat_id]

# Запуск бота
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))

