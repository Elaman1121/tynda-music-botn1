from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = "7302516914:AAFf7O9szcJD5GZGSsSs3TuyHdyvKhF8zN8"

LANGUAGES = {
    '🇰🇿 Қазақша': 'kk',
    '🇷🇺 Русский': 'ru',
    '🇬🇧 English': 'en'
}

user_lang = {}  # user_id: 'kk' or 'ru' or 'en'

def send_language_keyboard(update):
    # Тек тіл таңдау кнопкалары ғана шығарылады
    keyboard = [[key for key in LANGUAGES]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text("", reply_markup=reply_markup)

def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_lang.pop(user_id, None)  # reset previous language
    send_language_keyboard(update)

def handle_language_selection(update: Update, context: CallbackContext):
    lang_key = update.message.text
    user_id = update.message.from_user.id

    if lang_key in LANGUAGES:
        lang_code = LANGUAGES[lang_key]
        user_lang[user_id] = lang_code
        # Тіл таңдалғаннан кейін ғана жауап хабарламасын жібереміз
        update.message.reply_text("Тілді таңдадыңыз! Жазып, менің көмегіме жүгіне аласыз!", reply_markup=ReplyKeyboardRemove())
    else:
        send_language_keyboard(update)

def handle_music_request(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    lang_code = user_lang.get(user_id)

    if not lang_code:
        # Егер тіл таңдалмаған болса, тек тіл таңдау экранды көрсетеміз
        send_language_keyboard(update)
        return

    song_name = update.message.text.strip()

    # Мұнда ән іздеу логикасын жазуыңа болады
    song_found = False  # Тест үшін

    if song_found:
        update.message.reply_text("Ән табылды!")
    else:
        update.message.reply_text("Ән табылмады!")

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