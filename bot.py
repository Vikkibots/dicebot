import os
import logging
import random
from telegram.ext import ApplicationBuilder

BOT_TOKEN = os.getenv("BOT_TOKEN")

application = ApplicationBuilder().token(BOT_TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(run_bot, pattern="^run_bot$"))
application.add_handler(CallbackQueryHandler(roll_dice, pattern="^roll$"))
application.add_handler(CallbackQueryHandler(set_choices, pattern="^set_choices$"))

application.run_polling()

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Приветственные сообщения
welcome_messages = [
    "Мы часто делаем выбор, основываясь на прошлом опыте и шагаем по одним и тем же дорожкам.\nДобавь в день немного магии 😉\n\nНазначь опции или просто брось кубик — освободи время для важных решений.",
    "Сколько времени мы тратим, чтобы решить простое: звонить или не звонить, чай или прогулка?\nДоверься удаче, пусть кубик подскажет.\n\nНазначь опции или просто брось кубик — освободи время для важных решений.",
    "Если всё время выбирать одно и то же — жизнь становится предсказуемой.\nПопробуй довериться случаю 🎲\n\nНазначь опции или просто брось кубик — освободи время для важных решений.",
    "Иногда лучшая интуиция — это кубик. Правда-правда!\n\nНазначь опции или просто брось кубик — освободи время для важных решений."
]

choices = []

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("🚀 Запустить бота", callback_data="run_bot")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Нажми кнопку, чтобы сделать свою жизнь чуточку легче ✨", reply_markup=reply_markup)

# Обработка кнопки запуска
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

# Обработка броска кубика
async def roll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    result = random.randint(1, 6)
    if choices:
        response = f"🎲 Выпало число: {result}\n👉 {choices[result - 1]}"
    else:
        response = f"🎲 Выпало число: {result}"

    await query.edit_message_text(text=response)

# Обработка назначения опций
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

# Запуск приложения
if __name__ == '__main__':
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(run_bot, pattern="^run_bot$"))
    app.add_handler(CallbackQueryHandler(roll_dice, pattern="^roll$"))
    app.add_handler(CallbackQueryHandler(set_choices, pattern="^set_choices$"))

    app.run_polling()

