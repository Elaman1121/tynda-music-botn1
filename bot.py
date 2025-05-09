from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp
import os

TOKEN = "7302516914:AAFf7O9szcJD5GZGSsSs3TuyHdyvKhF8zN8"

LANGUAGES = {
    '🇰🇿 Қазақша': 'kk',
    '🇷🇺 Русский': 'ru',
    '🇬🇧 English': 'en'
}

GREETINGS = {
    'kk': "Сәлем, {name}! 👋\nМен — Tyn’da Music Bot. Сізді көргеніме қуаныштымын! ☺️\nМузыка әлемінде бірге сапар шегейік 🎶 — қалаған әніңізді жазыңыз, мен бірден тауып беремін! 🔍",
    'ru': "Привет, {name}! 👋\nЯ — Tyn’da Music Bot. Рад вас видеть! ☺️\nОтправьте название песни, и я сразу найду её для вас! 🎶",
    'en': "Hello, {name}! 👋\nI’m Tyn’da Music Bot. Happy to see you! ☺️\nTell me the name of the song and I’ll find it for you instantly! 🎶"
}

FOUND_MESSAGES = {
    'kk': "Сіз таңдаған әуен дайын! 🎧✨ Тыңдаңыз да, ләззат алыңыз! Мен әрқашан сіздің музыкалық серігіңізбін! 🫶🎶",
    'ru': "Ваша песня готова! 🎧✨ Слушайте и наслаждайтесь! Я всегда ваш музыкальный спутник! 🫶🎶",
    'en': "Your song is ready! 🎧✨ Listen and enjoy! I'm always your music companion! 🫶🎶"
}

NOT_FOUND_MESSAGES = {
    'kk': "Өкінішке орай, бұл әнді таба алмадым.🥲\nАвторлық құқықтар мен басқа да шектеулер себепті, немесе басқа әуен іздеп көріңіз! Әр қашан сізге көмектесуге дайынмын 🎶✨🫂",
    'ru': "Извините, не удалось найти эту песню.🥲\nВозможно, из-за авторских прав или других ограничений. Попробуйте найти другую песню! Я всегда готов помочь! 🎶✨🫂",
    'en': "Sorry, I couldn't find this song.🥲\nIt might be due to copyright restrictions or other limitations. Try finding another song! I'm always here to help! 🎶✨🫂"
}

SEARCHING_MESSAGES = {
    'kk': "Ән ізделіп жатыр... Күте тұрыңыз.",
    'ru': "Поиск песни... Пожалуйста, подождите.",
    'en': "Song is being searched... Please wait."
}

user_lang = {}  # user_id: 'kk' or 'ru' or 'en'

def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_lang.pop(user_id, None)  # reset previous language
    keyboard = [[key for key in LANGUAGES]]  # Keyboard in first row
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
        'quiet': True,  # керек болса False қойып лог қарауға болады
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)
            return file_name if os.path.exists(file_name) else None
        except Exception as e:
            print("Қате:", e)
            return None

def handle_music_request(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    lang_code = user_lang.get(user_id)

    if not lang_code:
        keyboard = [[key for key in LANGUAGES]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
        update.message.reply_text("2. Алдымен тілді таңдаңыз! / Сначала выберите язык! / Please select a language first!", reply_markup=reply_markup)
        return

    if update.message.audio or update.message.photo:
        update.message.reply_text("Мен тек мәтіндермен жұмыс істей аламын! 🚫🎶")
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