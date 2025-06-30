import os
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

choices = []

welcome_messages = [
    "Мы часто делаем выбор, основываясь на прошлом опыте и шагаем по одним и тем же дорожкам.\nДобавь в день немного магии 😉\n\nНазначь опции или просто брось кубик — освободи время для важных решений.",
    "Сколько времени мы тратим, чтобы решить простое: звонить или не звонить, чай или прогулка?\nДоверься удаче, пусть кубик подскажет.\n\nНазначь опции или просто брось кубик — освободи время для важных решений.",
    "Если всё время выбирать одно и то же — жизнь становится предсказуемой.\nПопробуй довериться случаю 🎲\n\nНазначь опции или просто брось кубик — освободи время для важных решений.",
    "Иногда лучшая интуиция — это кубик. Просто доверься.\n\nНазначь опции или просто брось кубик — освободи время для важных решений."
]

# Старт
def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if context.user_data.get("started"):
        return
    context.user_data["started"] = True

    greeting = random.choice(welcome_messages)
    update.message.reply_text(greeting)

    keyboard = [
        [InlineKeyboardButton("🎲 Бросить кубик", callback_data="roll")],
        [InlineKeyboardButton("📆 Назначить выбор", callback_data="set_choices")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Готово! Что будем делать?", reply_markup=reply_markup)

# Кнопка «Бросить кубик»
def roll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    query.answer()
    if not choices:
        result = random.randint(1, 6)
        query.edit_message_text(text=f"🎲 Выпало число: {result}")
    else:
        result = random.randint(1, len(choices))
        query.edit_message_text(text=f"🎲 Выпало число: {result}\n👉 {choices[result - 1]}")

# Кнопка «Назначить выбор»
def set_choices(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        "Напиши 6 вариантов, каждый с новой строки. Например: Смотреть сериал; Читать книгу; Позвонить близкому; Выполнить асаны; Выпить кофе; Пойти на массаж."
    )

# Пользователь вводит свои опции
def handle_custom_choices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global choices
    text = update.message.text
    choices = [line.strip() for line in text.split('\n') if line.strip()]

    keyboard = [[InlineKeyboardButton("🎲 Бросить кубик", callback_data="roll")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Отлично! Теперь воля случая 🎲", reply_markup=reply_markup)

# Запуск приложения
if __name__ == "__main__":
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(roll_dice, pattern="^roll$"))
    app.add_handler(CallbackQueryHandler(set_choices, pattern="^set_choices$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_choices))

    app.run_polling()

