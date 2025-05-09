import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    ConversationHandler, ContextTypes
)
from yt_dlp import YoutubeDL

# Лог
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Язык таңдау константалары
LANGUAGE, AWAITING_QUERY = range(2)

# Тіл таңдаулары
LANGUAGES = {
    'Қазақша': 'kk',
    'Русский': 'ru',
    'English': 'en'
}

# Тілдік хабарламалар
MESSAGES = {
    'start': {
        'kk': 'Қош келдіңіз! Тілді таңдаңыз:',
        'ru': 'Добро пожаловать! Пожалуйста, выберите язык:',
        'en': 'Welcome! Please select your language:'
    },
    'waiting': {
        'kk': 'Ән ізделіп жатыр... Күте тұрыңыз.',
        'ru': 'Ищем песню... Пожалуйста, подождите.',
        'en': 'Searching for the song... Please wait.'
    },
    'not_found': {
        'kk': 'Өкінішке орай, бұл әнді таба алмадым. Басқа әуен іздеп көріңіз!',
        'ru': 'К сожалению, я не смог найти эту песню. Попробуйте другую!',
        'en': 'Sorry, I couldn’t find this song. Try another one!'
    },
    'send_song': {
        'kk': 'Міне, сіз іздеген ән!',
        'ru': 'Вот ваша песня!',
        'en': 'Here is your song!'
    },
    'invalid_input': {
        'kk': 'Тек мәтін жазыңыз, аудио немесе сурет жібермеңіз.',
        'ru': 'Пожалуйста, отправьте только текст, без аудио или фото.',
        'en': 'Please send only text, no audio or photos.'
    }
}

# Пайдаланушылардың тілін сақтау
user_languages = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[key] for key in LANGUAGES.keys()]
    await update.message.reply_text(
        text=MESSAGES['start']['kk'],  # Қазақша қарсы алу
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return LANGUAGE

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    selected = update.message.text
    lang_code = LANGUAGES.get(selected)
    if not lang_code:
        return LANGUAGE

    user_languages[update.effective_user.id] = lang_code
    await update.message.reply_text(MESSAGES['waiting'][lang_code])
    return AWAITING_QUERY

async def handle_song_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = user_languages.get(user_id, 'en')
    query = update.message.text

    await update.message.reply_text(MESSAGES['waiting'][lang])

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.%(ext)s',
        'cookiefile': 'cookies.txt',
        'quiet': True,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
            audio_path = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")

        await update.message.reply_audio(audio=open(audio_path, 'rb'), caption=MESSAGES['send_song'][lang])
        os.remove(audio_path)

    except Exception as e:
        print("Қате:", e)
        await update.message.reply_text(MESSAGES['not_found'][lang])

    return AWAITING_QUERY

async def invalid_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = user_languages.get(update.effective_user.id, 'en')
    await update.message.reply_text(MESSAGES['invalid_input'][lang])

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_language)],
            AWAITING_QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_song_request)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(~filters.TEXT, invalid_input))

    print("Бот іске қосылды.")
    app.run_polling()

if __name__ == "__main__":
    main()