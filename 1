import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

# Хранилище пользовательских вариантов
user_choices = {}

# Опции по умолчанию для простого броска
default_options = [
    "Почитать",
    "Прокрастинировать дальше",
    "Забронировать поездку",
    "Прогуляться",
    "Позвонить близкому",
    "Выпить чай"
]

# Приветственные сообщения
welcome_messages = [
    "Каждый день мы делаем выбор, опираясь на привычки и старый опыт.\n"
    "Так мозг экономит энергию — и мы снова идём по протоптанной дорожке.\n\n"
    "Хочешь выйти из петли?\nДобавь немного случайности. Немного магии. 🎲\n\n"
    "Назначь опции или просто брось кубик — освободи время для важных решений.",

    "Мы часто выбираем не то, что хотим, а то, что уже делали.\n"
    "Мозг любит повторять. Привычки сильнее желаний.\n\n"
    "Этот бот создан, чтобы сломать петлю.\nБрось кубик — пусть Вселенная подскажет. ✨\n\n"
    "Назначь опции или просто брось кубик — освободи время для важных решений.",

    "Мы ходим по кругу: выбор → привычка → автомат.\n\n"
    "А что, если добавить элемент неожиданности? 🎲\n"
    "Вдруг сегодня всё пойдёт по-другому.\n\n"
    "Назначь опции или просто брось кубик — освободи время для важных решений.",

    "Наши выборы — это след прошлого.\n"
    "Хочешь шагнуть в новое — доверься случаю.\n\n"
    "Кубик знает больше, чем кажется 😉\n\n"
    "Назначь опции или просто брось кубик — освободи время для важных решений."
]

# Кнопки
def main_menu():
    keyboard = [
        [InlineKeyboardButton("  🎲 БРОСИТЬ КУБИК  ", callback_data="simple_roll")],
        [InlineKeyboardButton("  🗳 НАЗНАЧИТЬ ВЫБОРЫ  ", callback_data="start_choices")]
    ]
    return InlineKeyboardMarkup(keyboard)

def roll_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("  🎲 БРОСИТЬ КУБИК  ", callback_data="choice_roll")]
    ])

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = random.choice(welcome_messages)
    await update.message.reply_text(welcome)
    await update.message.reply_text("Выбери, что сделать:", reply_markup=main_menu())

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "simple_roll":
        number = random.randint(1, 6)
        choice = default_options[number - 1]
        await query.message.reply_text(f"🎲 Выпало число: {number}\n👉 {choice}", reply_markup=main_menu())

    elif query.data == "start_choices":
        await query.message.reply_text(
            "Напиши 6 новых вариантов, каждый с новой строки. Например:\n\nпочитать\nпрогуляться\nвыпить чай"
        )

    elif query.data == "choice_roll":
        if user_id not in user_choices or len(user_choices[user_id]) != 6:
            await query.message.reply_text("Ты ещё не прислал 6 вариантов. Напиши их сначала.")
            return
        number = random.randint(1, 6)
        choice = user_choices[user_id][number - 1]
        await query.message.reply_text(f"🎲 Выпало число: {number}\n👉 {choice}", reply_markup=main_menu())

# Сообщения с 6 вариантами
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if len(lines) != 6:
        await update.message.reply_text("Пожалуйста, пришли ровно 6 строк.")
        return

    user_choices[user_id] = lines
    await update.message.reply_text("Принято! Теперь нажми кнопку ниже, чтобы бросить кубик:", reply_markup=roll_button())

# Запуск
app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

app.run_polling()
