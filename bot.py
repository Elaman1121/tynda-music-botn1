import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO)

TOKEN = "7302516914:AAFf7O9szcJD5GZGSsSs3TuyHdyvKhF8zN8"
LANGUAGE = range(1)

LANGUAGES = {
    "Қазақша": "kk",
    "Русский": "ru",
    "English": "en"
}

MESSAGES = {
    "start": {
        "kk": "Сәлем! Маған ән атын жазсаң, мен оны тауып берем!",
        "ru": "Привет! Напиши название песни, и я её найду!",
        "en": "Hi! Send me a song name and I’ll find it!"
    },
    "searching": {
        "kk": "Ән ізделіп жатыр... Күте тұрыңыз.",
        "ru": "Ищу песню... Пожалуйста, подождите.",
        "en": "Searching for the song... Please wait."
    },
    "not_found": {
        "kk": "Кешір, бұл әнді таба алмадым. Басқасын көрейік.",
        "ru": "Не удалось найти песню. Попробуйте другую.",
        "en": "Couldn't find the song. Try another one."
    }
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Қазақша", "Русский", "English"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Тілді таңдаңыз / Choose language / Выберите язык:", reply_markup=reply_markup)
    return LANGUAGE


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.message.text
    context.user_data["lang"] = LANGUAGES.get(lang, "en")
    await update.message.reply_text(MESSAGES["start"][context.user_data["lang"]])
    return ConversationHandler.END


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    query = update.message.text

    await update.message.reply_text(MESSAGES["searching"][lang])

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'cookiefile': 'cookies.txt',
        'quiet': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")

        with open(filename, 'rb') as audio:
            await update.message.reply_audio(audio)
        os.remove(filename)
    except Exception as e:
        logging.error(f"Error while downloading: {e}")
        await update.message.reply_text(MESSAGES["not_found"][lang])


def main():
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_language)],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    application.run_polling()


if __name__ == '__main__':
    main()