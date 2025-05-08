from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

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
    'kk': "Өкінішке орай, бұл әнді таба алмадым.🥲\nБасқа әуен іздеп көріңіз!",
    'ru': "Извините, не удалось найти эту песню.🥲\nПопробуйте найти другую песню!",
    'en': "Sorry, I couldn't find this song.🥲\nTry finding another song!"
}

user_lang = {}  # user_id: 'kk' or 'ru' or 'en'

def send_language_keyboard(update: Update, context: CallbackContext):
    keyboard = [[key for key in LANGUAGES]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text("Тілді таңдаңыз / Выберите язык / Select language:", reply_markup=reply_markup)

def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_lang.pop(user_id, None)  # reset previous language
    send_language_keyboard(update, context)

def handle_language_selection(update: Update, context: CallbackContext):
    lang_key = update.message.text
    user_id = update.message.from_user.id
    name = update.message.from_user.first_name

    if lang_key in LANGUAGES:
        lang_code = LANGUAGES[lang_key]
        user_lang[user_id] = lang_code
        update.message.reply_text(GREETINGS[lang_code].format(name=name), reply_markup=ReplyKeyboardRemove())
    else:
        send_language_keyboard(update, context)

def handle_music_request(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    lang_code = user_lang.get(user_id)

    if not lang_code:
        send_language_keyboard(update, context)
        return

    if update.message.audio or update.message.photo:
        update.message.reply_text("Мен тек мәтіндермен жұмыс істей аламын! 🚫🎶")
        return

    song_name = update.message.text.strip()

    # Мұнда ән іздеу логикасын жазуыңа болады
    song_found = False  # Тест үшін

    if song_found:
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