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

choices = []

welcome_messages = [
    "Мы часто делаем выбор, основываясь на прошлом опыте и шагаем… [и далее текст приветствия].",
    # остальные варианты…
]

def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get("started"):
        return
    context.user_data["started"] = True
    greeting = random.choice(welcome_messages)
    update.message.reply_text(greeting)
    keyboard = [
        [InlineKeyboardButton("🎲 Бросить кубик", callback_data="roll")],
        [InlineKeyboardButton("📆 Назначить выбор", callback_data="set_choices")]
    ]
    update.message.reply_text("Готово! Что будем делать?", reply_markup=InlineKeyboardMarkup(keyboard))

def roll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    query.answer()
    if not choices:
        result = random.randint(1, 6)
        query.edit_message_text(f"🎲 Выпало число: {result}")
    else:
        result = random.randint(1, len(choices))
        query.edit_message_text(f"🎲 Выпало число: {result}\n👉 {choices[result - 1]}")

def set_choices(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        "Напиши 6 вариантов, каждый с новой строки. Например: Смотреть сериал; Читать книгу; Позвонить близкому; Выполнить асаны; Выпить кофе; Пойти на массаж."
    )

def handle_custom_choices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global choices
    text = update.message.text
    choices = [line.strip() for line in text.split('\n') if line.strip()]
    keyboard = [[InlineKeyboardButton("🎲 Бросить кубик", callback_data="roll")]]
    update.message.reply_text("Отлично! Теперь воля случая 🎲", 
                              reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == "__main__":
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(roll_dice, pattern="^roll$"))
    app.add_handler(CallbackQueryHandler(set_choices, pattern="^set_choices$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_choices))
    app.run_polling()  # ✅ Всё, без `await`, без webhooks, без конфликтов
