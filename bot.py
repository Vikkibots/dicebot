import os
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(

    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',

    level=logging.INFO

)

# Глобальная переменная для хранения вариантов выбора пользователя

choices = []

# Приветственные сообщения для команды /start

welcome_messages = [

    "Мы часто делаем выбор, основываясь на прошлом опыте и шагаем… [и далее текст приветствия].",

    # остальные варианты…

]

# Обработчик команды /start

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # Проверяем, был ли уже запущен бот для этого пользователя

    if context.user_data.get("started"):

        return

    context.user_data["started"] = True

    # Выбираем случайное приветствие

    greeting = random.choice(welcome_messages)

    await update.message.reply_text(greeting)

    # Создаем кнопки для выбора действия

    keyboard = [

        [InlineKeyboardButton("🎲 Бросить кубик", callback_data="roll")],

        [InlineKeyboardButton("📆 Назначить выбор", callback_data="set_choices")]

    ]

    await update.message.reply_text("Готово! Что будем делать?", reply_markup=InlineKeyboardMarkup(keyboard))

# Обработчик нажатия кнопки "Бросить кубик"

async def roll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    query = update.callback_query

    await query.answer()

    # Если пользователь не задал варианты выбора, бросаем обычный кубик (1-6)

    if not choices:

        result = random.randint(1, 6)

        await query.edit_message_text(f"🎲 Выпало число: {result}")

    # Если варианты выбора заданы, выбираем случайный вариант из списка

    else:

        result = random.randint(1, len(choices))

        await query.edit_message_text(f"🎲 Выпало число: {result}\n👉 {choices[result - 1]}")

# Обработчик нажатия кнопки "Назначить выбор"

async def set_choices(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(

        "Напиши варианты, каждый с новой строки. Например: Смотреть сериал; Читать книгу; Позвонить близкому; Выполнить асаны; Выпить кофе; Пойти на массаж."

    )

# Обработчик текстовых сообщений, содержащих варианты выбора

async def handle_custom_choices(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global choices

    text = update.message.text

    choices = [line.strip() for line in text.split('\n') if line.strip()]

    keyboard = [[InlineKeyboardButton("🎲 Бросить кубик", callback_data="roll")]]

    await update.message.reply_text("Отлично! Теперь воля случая 🎲",

                              reply_markup=InlineKeyboardMarkup(keyboard))

# Основная функция запуска бота

if __name__ == "__main__":

    BOT_TOKEN = os.getenv("BOT_TOKEN")  # Получаем токен из переменной окружения

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Регистрируем обработчики команд и сообщений

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CallbackQueryHandler(roll_dice, pattern="^roll$"))

    app.add_handler(CallbackQueryHandler(set_choices, pattern="^set_choices$"))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_choices))

    # Запускаем бота

    app.run_polling()
