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

# Приветственные сообщения
welcome_messages = [
    "Мы часто делаем выбор, основываясь на прошлом опыте и шагаем по одним и тем же дорожкам.\nДобавь в день немного магии 😉\n\nНазначь опции или просто брось кубик — освободи время для важных решений.",
    "Сколько времени мы тратим, чтобы решить простое: звонить или не звонить, чай или прогулка?\nДоверься удаче, пусть кубик подскажет.\n\nНазначь опции или просто брось кубик — освободи время для важных решений.",
    "Если всё время выбирать одно и то же — жизнь становится предсказуемой.\nПопробуй довериться случаю 🎲\n\nНазначь опции или просто брось кубик — освободи время для важных решений.",
    "Иногда лучшая интуиция — это кубик. Просто доверься.\n\nНазначь опции или просто брось кубик — освободи время для важных решений."
]

# Стартовое сообщение с кнопкой запуска
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get("started"):
        return
    context.user_data["started"] = True

    keyboard = [[InlineKeyboardButton("🚀 Запустить бота", callback_data="run_bot")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Нажми кнопку, чтобы сделать свою жизнь чуточку легче✨",
        reply_markup=reply_markup
    )

# Кнопка "Запустить бота"
async def run_bot_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    greeting = random.choice(welcome_messages)
    await query.message.reply_text(greeting)

    keyboard = [
        [InlineKeyboardButton("🎲 Бросить кубик", callback_data="roll")],
        [InlineKeyboardButton("📆 Назначить выбор", callback_data="set_choices")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Готово! Что будем делать?", reply_markup=reply_markup)

# Назначить варианты
async def set_choices(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "Напиши 6 вариантов, каждый с новой строки. Например: Смотреть сериал; Читать книгу; Позвонить близкому; Выполнить асаны; Выпить кофе; Пойти на массаж."
    )

# Обработка пользовательских опций (в виде текста)
async def handle_custom_choices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global choices
    text = update.message.text
    choices = [line.strip() for line in text.split('\n') if line.strip()]
    
    keyboard = [[InlineKeyboardButton("🎲 Бросить кубик", callback_data="roll")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Отлично! Теперь воля случая 🎲", reply_markup=reply_markup)

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

# Запуск бота (async)
if __name__ == "__main__":
    import asyncio

    async def main():
        BOT_TOKEN = os.getenv("BOT_TOKEN")
        app = ApplicationBuilder().token(BOT_TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(run_bot_button, pattern="^run_bot$"))
        app.add_handler(CallbackQueryHandler(roll_dice, pattern="^roll$"))
        app.add_handler(CallbackQueryHandler(set_choices, pattern="^set_choices$"))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_choices))

        await app.run_polling()

    # Это безопасный способ запустить event loop без ошибки
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "already running" in str(e):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        else:
            raise

