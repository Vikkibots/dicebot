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

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Глобальные переменные
choices = []

# Стартовое сообщение с кнопкой запуска
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if context.user_data.get("started"):
        return
    context.user_data["started"] = True

    keyboard = [[InlineKeyboardButton("🚀 Запустить бота", callback_data="run_bot")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Нажми кнопку, чтобы сделать свою жизнь чуточку легче✨",
        reply_markup=reply_markup
    )

# Приветственные сообщения
welcome_messages = [
    "Мы часто делаем выбор, основываясь на прошлом опыте и шагаем по одним и тем же дорожкам.\nДобавь в день немного магии 😉\n\nНазначь опции или просто брось кубик — освободи время для важных решений.",
    "Сколько времени мы тратим, чтобы решить простое: звонить или не звонить, чай или прогулка?\nДоверься удаче, пусть кубик подскажет.\n\nНазначь опции или просто брось кубик — освободи время для важных решений.",
    "Если всё время выбирать одно и то же — жизнь становится предсказуемой.\nПопробуй довериться случаю 🎲\n\nНазначь опции или просто брось кубик — освободи время для важных решений.",
    "Иногда лучшая интуиция — это кубик. Просто доверься.\n\nНазначь опции или просто брось кубик — освободи время для важных решений."
]

# Кнопка "Запустить бота"
async def run_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    greeting = random.choice(welcome_messages)
    keyboard = [
        [InlineKeyboardButton("🎲 Бросить кубик", callback_data="roll")],
        [InlineKeyboardButton("📆 Назначить выбор", callback_data="set_choices")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(greeting, reply_markup=reply_markup)

# Бросить кубик
async def roll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if not choices:
        result = random.randint(1, 6)
        await query.edit_message_text(text=f"🎲 Выпало число: {result}")
    else:
        result = random.randint(1, len(choices))
        response = f"🎲 Выпало число: {result}\n👉 {choices[result - 1]}"
        await query.edit_message_text(text=response)

# Назначить варианты (по умолчанию)
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

# Обработка пользовательских опций (в виде текста)
async def handle_custom_choices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global choices
    text = update.message.text
    choices = [line.strip() for line in text.split('\n') if line.strip()]
    await update.message.reply_text("Выбор сохранён! Теперь нажми 🎲 Бросить кубик")

# Запуск приложения
if __name__ == '__main__':
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(run_bot, pattern="^run_bot$"))
    app.add_handler(CallbackQueryHandler(roll_dice, pattern="^roll$"))
    app.add_handler(CallbackQueryHandler(set_choices, pattern="^set_choices$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_choices))

    app.run_polling()

