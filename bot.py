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

user_lang = {}  # user_id: 'kk' or 'ru' or 'en'

def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_lang.pop(user_id, None)  # reset previous language
    keyboard = [[key for key in LANGUAGES]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("Тілді таңдаңыз / Выберите язык / Select language:", reply_markup=reply_markup)

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

def get_song_response(song_found: bool, language: str) -> str:
    if song_found:
        messages = {
            'kk': (
                "Сіз таңдаған әуен дайын! 🎧✨ Тыңдаңыз да, ләззат алыңыз! "
                "Мен әрқашан сіздің музыкалық серігіңізбін! 🫶🎶\n"
                "Сізге әрқашан көмектесу маған ләззат береді 🖤"
            ),
            'ru': (
                "Ваша выбранная песня готова! 🎧✨ Наслаждайтесь каждой нотой! "
                "Я всегда ваш музыкальный спутник! 🫶🎶\n"
                "Помогать вам — это для меня удовольствие 🖤"
            ),
            'en': (
                "Your selected song is ready! 🎧✨ Enjoy every beat! "
                "I’m always your musical companion! 🫶🎶\n"
                "Helping you is always a pleasure for me 🖤"
            )
        }
    else:
        messages = {
            'kk': (
                "Кешіріңіз, бұл әнді таба алмадым. 👀\n"
                "Басқа атауын байқап көрсеңіз қалай болады?🥹 "
                "Немесе дұрыс жазылғанына көз жеткізіңіз.🥲"
            ),
            'ru': (
                "Извините, не удалось найти эту песню. 👀\n"
                "Попробуйте другое название или проверьте правильность написания.🥹🥲"
            ),
            'en': (
                "Sorry, I couldn't find this song. 👀\n"
                "Try a different name or make sure it's spelled correctly.🥹🥲"
            )
        }
    return messages.get(language, "Тіл анықталмады")

def handle_music_request(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    lang_code = user_lang.get(user_id)

    if not lang_code:
        update.message.reply_text("Алдымен тілді таңдаңыз! / Сначала выберите язык! / Please select a language first!")
        return

    # Мұнда нақты іздеу логикасы қосылады. Әзірше жай жауап:
    song_found = False  # Таппаған жағдайда, бұл айнымалыны өзгерту қажет
    update.message.reply_text(get_song_response(song_found, lang_code))

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