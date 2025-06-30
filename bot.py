import os
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
)

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Стартовое сообщение с кнопкой запуска
async def roll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    result = random.randint(1, 6)

    if choices:
        response = f"🎲 Выпало число: {result}\n👉 {choices[result - 1]}"
    else:
        response = f"🎲 Выпало число: {result}"

    await query.edit_message_text(text=response)

# Приветственные сообщения
welcome_messages = [
    "Мы часто делаем выбор, основываясь на прошлом опыте и шагаем по одними и тем же дорожкам.\nДобавь в день немного магии 😉\n\nНазначь опции или просто брось кубик — освободи время для важных решений.",
    "Сколько времени мы тратим, чтобы решить простое: звонить или не звонить, чай или прогулка?\nДоверься удаче, пусть кубик подскажет.\n\nНазначь опции или просто брось кубик — освободи время для важных решений.",
    "Если всё время выбирать одно и то же — жизнь становится предсказуемой.\nПопробуй довериться случаю 🎲\n\nНазначь опции или просто брось кубик — освободи время для важных решений.",
    "Иногда лучшая интуиция — это кубик. Правда-правда!\n\nНазначь опции или просто брось кубик — освободи время для важных решений."
]

# Кнопка "Запустить бота"
async def run_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    greeting = random.choice(welcome_messages)
    keyboard = [
        [InlineKeyboardButton("🎲 Бросить кубик", callback_data="roll")],
        [InlineKeyboardButton("📦 Назначить выбор", callback_data="set_choices")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(greeting, reply_markup=reply_markup)

# Бросить кубик
async def roll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    result = random.randint(1, len(choices))
    response = f"🎲 Выпало число: {result}\n👉 {choices[result - 1]}"
    await query.edit_message_text(text=response)

# Назначить варианты
async def set_choices(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    global choices
    choices = [
        "Почитать",
        "Прокрастинировать дальше",
        "Забронировать поездку",
        "Прогуляться",
        "Позвонить близкому",
        "Выпить чай"
    ]
    await query.edit_message_text("Выбор сохранён! Теперь нажми 🎲 Бросить кубик")

# Запуск
if __name__ == '__main__':
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    choices = []

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(run_bot, pattern="^run_bot$"))
    app.add_handler(CallbackQueryHandler(roll_dice, pattern="^roll$"))
    app.add_handler(CallbackQueryHandler(set_choices, pattern="^set_choices$"))

    app.run_polling()

