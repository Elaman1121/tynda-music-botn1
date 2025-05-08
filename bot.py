import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp
import uuid

TOKEN = os.getenv("TOKEN", "7302516914:AAFf7O9szcJD5GZGSsSs3TuyHdyvKhF8zN8")

LANGUAGES = {
    '🇰🇿 Қазақша': 'kk',
    '🇷🇺 Русский': 'ru',
    '🇬🇧 English': 'en'
}

GREETINGS = {
    'kk': "Сәлем, {name}! 👋\nМен — Tyn’da Music Bot. Музыка әлемінде бірге сапар шегейік 🎶",
    'ru': "Привет, {name}! 👋\nЯ — Tyn’da Music Bot. Отправьте название песни, и я её найду 🎶",
    'en': "Hello, {name}! 👋\nI’m Tyn’da Music Bot. Tell me the name of the song and I’ll find it 🎶"
}

FOUND_MESSAGES = {
    'kk': "Сіз таңдаған әуен дайын! 🎧",
    'ru': "Ваша песня готова! 🎧",
    'en': "Your song is ready! 🎧"
}

NOT_FOUND_MESSAGES = {
    'kk': "Кешіріңіз, бұл әнді таба алмадым.",
    'ru': "Извините, не удалось найти эту песню.",
    'en': "Sorry, I couldn't find this song."
}

user_lang = {}

def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_lang.pop(user_id, None)
    keyboard = [[key for key in LANGUAGES]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("1. Тілді таңдаңыз / Select language / Выберите язык:", reply_markup=markup)

def handle_language_selection(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    name = update.message.from_user.first_name
    lang_key = update.message.text

    if lang_key in LANGUAGES:
        lang_code = LANGUAGES[lang_key]
        user_lang[user_id] = lang_code
        update.message.reply_text(GREETINGS[lang_code].format(name=name), reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text("Дұрыс тілді таңдаңыз!")

def download_song(song_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': f'{uuid.uuid4().hex}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{song_name}", download=True)['entries'][0]
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
            return filename, info.get('title')
        except Exception as e:
            print(f"Error: {e}")
            return None, None

def handle_music_request(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    lang_code = user_lang.get(user_id, 'en')

    if not lang_code:
        update.message.reply_text("Алдымен тілді таңдаңыз!")
        return

    if update.message.audio or update.message.photo:
        update.message.reply_text("Мен тек мәтінмен жұмыс істей аламын!")
        return

    song_name = update.message.text.strip()
    update.message.reply_text("Іздеп жатырмын... ⏳")

    filepath, title = download_song(song_name)

    if filepath and os.path.exists(filepath):
        with open(filepath, 'rb') as audio_file:
            update.message.reply_audio(audio_file, title=title)
        os.remove(filepath)
        update.message.reply_text(FOUND_MESSAGES[lang_code])
    else:
        update.message.reply_text(NOT_FOUND_MESSAGES[lang_code])

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex('^(🇰🇿 Қазақша|🇷🇺 Русский|🇬🇧 English)$'), handle_language_selection))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_music_request))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()