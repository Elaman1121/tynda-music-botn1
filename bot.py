from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp
import os
import logging

TOKEN = "7302516914:AAFf7O9szcJD5GZGSsSs3TuyHdyvKhF8zN8"
bot = Bot(TOKEN)

app = Flask(__name__)

dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

LANGUAGES = {
    '🇰🇿 Қазақша': 'kk',
    '🇷🇺 Русский': 'ru',
    '🇬🇧 English': 'en'
}

GREETINGS = {
    'kk': "Сәлем, {name}! Мен — Tyn’da Music Bot...",
    'ru': "Привет, {name}! Я — Tyn’da Music Bot...",
    'en': "Hello, {name}! I’m Tyn’da Music Bot..."
}

FOUND_MESSAGES = {
    'kk': "Сіз таңдаған әуен дайын! 🎧",
    'ru': "Ваша песня готова! 🎧",
    'en': "Your song is ready! 🎧"
}

NOT_FOUND_MESSAGES = {
    'kk': "Өкінішке орай, бұл әнді таба алмадым.",
    'ru': "Извините, не удалось найти эту песню.",
    'en': "Sorry, I couldn't find this song."
}

SEARCHING_MESSAGES = {
    'kk': "Ән ізделіп жатыр...",
    'ru': "Песня ищется...",
    'en': "Searching for the song..."
}

user_lang = {}

def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_lang.pop(user_id, None)
    keyboard = [[key for key in LANGUAGES]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text("1. Тілді таңдаңыз / Выберите язык / Select language:", reply_markup=reply_markup)

def handle_language_selection(update: Update, context: CallbackContext):
    lang_key = update.message.text
    user_id = update.message.from_user.id
    name = update.message.from_user.first_name

    if lang_key in LANGUAGES:
        lang_code = LANGUAGES[lang_key]
        user_lang[user_id] = lang_code
        update.message.reply_text(GREETINGS[lang_code].format(name=name), reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text("Тілді дұрыс таңдаңыз / Выберите язык правильно / Choose a valid language")

def download_audio(query: str, file_name: str = "song.mp3") -> str or None:
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': file_name,
        'noplaylist': True,
        'quiet': False,
        'default_search': 'ytsearch5',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'cookiefile': 'cookies.txt'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
            first = info['entries'][0]
            ydl.download([first['webpage_url']])
            if os.path.exists(file_name):
                return file_name
        except:
            pass
    return None

def handle_music_request(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    lang_code = user_lang.get(user_id)

    if not lang_code:
        keyboard = [[key for key in LANGUAGES]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
        update.message.reply_text("2. Алдымен тілді таңдаңыз!", reply_markup=reply_markup)
        return

    if update.message.audio or update.message.photo:
        update.message.reply_text("Мен тек мәтіндермен жұмыс істей аламын! 🚫")
        return

    song_name = update.message.text.strip()
    update.message.reply_text(SEARCHING_MESSAGES[lang_code])
    audio_file = download_audio(song_name)

    if audio_file:
        update.message.reply_audio(audio=open(audio_file, 'rb'))
        update.message.reply_text(FOUND_MESSAGES[lang_code])
        os.remove(audio_file)
    else:
        update.message.reply_text(NOT_FOUND_MESSAGES[lang_code])

# Тіркеу
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex('^(🇰🇿 Қазақша|🇷🇺 Русский|🇬🇧 English)$'), handle_language_selection))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_music_request))

# Telegram webhook қабылдайтын маршрут
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok", 200

# Heroku тіркеу кезінде жұмыс істеу үшін басты бет
@app.route("/")
def index():
    return "Bot is running!"

# Port Heroku автоматты түрде орнатады
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)