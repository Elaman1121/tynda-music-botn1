import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from yt_dlp import YoutubeDL

# Лог орнату
logging.basicConfig(level=logging.INFO)

TOKEN = "7302516914:AAFf7O9szcJD5GZGSsSs3TuyHdyvKhF8zN8"
LANGUAGE, = range(1)

LANGUAGES = {
    "Қазақша": "kk",
    "Русский": "ru",
    "English": "en"
}

START_MESSAGES = {
    "kk": "Сәлем! Менен кез келген әнді сұра! Тек атын жазсаң жеткілікті.",
    "ru": "Привет! Напиши название песни — и я найду её для тебя.",
    "en": "Hi! Just type the name of any song — I'll find it for you!"
}

SEARCHING_MESSAGES = {
    "kk": "Ән ізделіп жатыр... Күте тұрыңыз.",
    "ru": "Ищу песню... Пожалуйста, подождите.",
    "en": "Searching for the song... Please wait."
}

NOT_FOUND_MESSAGES = {
    "kk": "Өкінішке орай, бұл әнді таба алмадым. Басқа әнді жазып көріңіз!",
    "ru": "К сожалению, не удалось найти эту песню. Попробуйте другую!",
    "en": "Sorry, I couldn't find this song. Try another one!"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Қазақша", "Русский", "English"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Тілді таңдаңыз / Choose language / Выберите язык:", reply_markup=reply_markup)
    return LANGUAGE

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.message.text
    context.user_data["lang"] = LANGUAGES.get(lang, "en")
    await update.message.reply_text(START_MESSAGES[context.user_data["lang"]])
    return ConversationHandler.END

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    query = update.message.text

    await update.message.reply_text(SEARCHING_MESSAGES[lang])

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
        logging.error(f"Error: {e}")
        await update.message.reply_text(NOT_FOUND_MESSAGES[lang])

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_language)]},
        fallbacks=[]
    )

    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()