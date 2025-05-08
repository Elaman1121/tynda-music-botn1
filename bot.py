import os
import yt_dlp
from yt_dlp.utils import DownloadError
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters,
    CallbackContext, ConversationHandler
)

# Боттың токені (өзіңдікі)
TOKEN = "7302516914:AAFf7O9szcJD5GZGSsSs3TuyHdyvKhF8zN8"

# Conversation этаптары
LANGUAGE, SEARCH = range(2)

# Әр қолданушының тілі сақталады
user_languages = {}

# Көптілді хабарламалар
MESSAGES = {
    'kz': {
        'start': "Сәлем! Мен Tyn’daMusicBot.\nТілді таңдаңыз:",
        'choose': "Қандай ән жүктейін?",
        'downloading': "Іздеп жатырмын: «{}»…",
        'error': "Қате шықты: {}",
        'limit': "Бұл әнді жүктеу мүмкін емес. Басқа ән жазып көріңіз.",
    },
    'ru': {
        'start': "Привет! Я Tyn’daMusicBot.\nВыберите язык:",
        'choose': "Какую песню хотите скачать?",
        'downloading': "Ищу: «{}»…",
        'error': "Произошла ошибка: {}",
        'limit': "Невозможно скачать эту песню. Попробуйте другую.",
    },
    'en': {
        'start': "Hi! I'm Tyn’daMusicBot.\nChoose your language:",
        'choose': "What song do you want?",
        'downloading': "Searching: «{}»…",
        'error': "An error occurred: {}",
        'limit': "Can't download this song. Try another one.",
    }
}


def start(update: Update, context: CallbackContext):
    reply_keyboard = [['🇰🇿 Қазақша', '🇷🇺 Русский', '🇬🇧 English']]
    update.message.reply_text(
        "Сәлем! Hello!\nТілді таңдаңыз / Выберите язык / Choose your language:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return LANGUAGE


def choose_language(update: Update, context: CallbackContext):
    lang_text = update.message.text
    if 'Қазақша' in lang_text:
        user_languages[update.effective_user.id] = 'kz'
    elif 'Русский' in lang_text:
        user_languages[update.effective_user.id] = 'ru'
    else:
        user_languages[update.effective_user.id] = 'en'

    lang = user_languages[update.effective_user.id]
    update.message.reply_text(MESSAGES[lang]['choose'], reply_markup=ReplyKeyboardRemove())
    return SEARCH


def download_audio(query: str) -> str:
    """YouTube-тан аудио жүктеп, 'song.mp3' атымен қайтарады."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)
        return "song.mp3"


def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    lang = user_languages.get(user_id, 'kz')  # Егер жоқ болса, қазақша бола береді
    query = update.message.text.strip()

    update.message.reply_text(MESSAGES[lang]['downloading'].format(query))
    try:
        file_path = download_audio(query)
        with open(file_path, 'rb') as f:
            update.message.reply_audio(audio=f)
        os.remove(file_path)
    except DownloadError as e:
        if 'Sign in to confirm you’re not a bot' in str(e):
            update.message.reply_text(MESSAGES[lang]['limit'])
        else:
            update.message.reply_text(MESSAGES[lang]['error'].format(e))
    except Exception as e:
        update.message.reply_text(MESSAGES[lang]['error'].format(e))


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [MessageHandler(Filters.text & ~Filters.command, choose_language)],
            SEARCH: [MessageHandler(Filters.text & ~Filters.command, handle_message)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()