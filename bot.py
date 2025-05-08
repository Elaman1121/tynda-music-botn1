from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = "7302516914:AAFf7O9szcJD5GZGSsSs3TuyHdyvKhF8zN8"  # Сіздің токеніңіз

# Тілдер мен олардың флагтары
languages = [
    ('Қазақша', '🇰🇿'),
    ('Русский', '🇷🇺'),
    ('English', '🇬🇧')
]

# Сәлемдесу хабарламасы
def start(update: Update, context: CallbackContext):
    user_name = update.message.from_user.first_name
    # Тек тілді таңдау экранын көрсету
    update.message.reply_text(
        f"Сәлем, {user_name}! 👋\n"
        "Мен — Tyn’da Music Bot. Сізді көргеніме қуаныштымын! ☺️\n"
        "Музыка әлемінде бірге сапар шегейік 🎶 — қалаған әніңізді айтыңыз, мен лезде тауып беремін! 🔍\n"
        "Сізбен жұмыс істеуге дайынмын, қай тілде сөйлескіңіз келеді? 🎧"
    )
    # Тіл таңдауды сұрау
    keyboard = [[f"{flag} {language}" for language, flag in languages]]
    reply_markup = {'keyboard': keyboard, 'one_time_keyboard': True, 'resize_keyboard': True}
    update.message.reply_text("Тілді таңдаңыз:", reply_markup=reply_markup)

# Тіл таңдау
def handle_message(update: Update, context: CallbackContext):
    query = update.message.text.strip()
    for language, flag in languages:
        if f"{flag} {language}" == query:
            # Тілді сақтап, оның ішінен жауап қайтарамыз
            context.user_data['language'] = language
            language_responses = {
                'Қазақша': "Сіз тіл ретінде Қазақшаны таңдадыңыз!",
                'Русский': "Вы выбрали русский язык!",
                'English': "You selected English language!"
            }
            update.message.reply_text(language_responses.get(language, "Тіл таңдалмады"))
            break
    else:
        update.message.reply_text("Таңдауды дұрыс енгізіңіз!")

# Музыка сұрау
def music_request(update: Update, context: CallbackContext):
    # Тілді таңдаған соң, әнді іздеу мүмкіндігі беріледі
    if 'language' in context.user_data:
        language = context.user_data['language']
        
        # Тіл бойынша хабарламалар
        music_messages = {
            'Қазақша': "Қалаған әніңіздің атын жазыңыз! 🎶",
            'Русский': "Напишите название песни! 🎶",
            'English': "Write the name of the song! 🎶"
        }
        update.message.reply_text(music_messages.get(language, "Тіл таңдалмады"))
    else:
        update.message.reply_text("Тіл таңдауды ұмытпаңыз! Тілді таңдап алғаннан кейін мен сізге ән іздеуге көмектесемін.")

# Ән тапқан соңғы хабарлама
def song_found(update: Update, context: CallbackContext):
    if 'language' in context.user_data:
        language = context.user_data['language']
        
        song_messages = {
            'Қазақша': "Сіз таңдаған әуен дайын! 🎧✨ Тыңдаңыз да, ләззат алыңыз! Мен әрқашан сіздің музыкалық серігіңізбін! 🫶🎶",
            'Русский': "Выбранная вами песня готова! 🎧✨ Слушайте и наслаждайтесь! Я всегда ваш музыкальный спутник! 🫶🎶",
            'English': "The song you selected is ready! 🎧✨ Listen and enjoy! I’m always your musical companion! 🫶🎶"
        }
        update.message.reply_text(song_messages.get(language, "Тіл таңдалмады"))
    else:
        update.message.reply_text("Тіл таңдауды ұмытпаңыз!")

# Қорытынды хабарлама
def thank_you(update: Update, context: CallbackContext):
    if 'language' in context.user_data:
        language = context.user_data['language']
        
        thank_you_messages = {
            'Қазақша': "Сізге әрқашан көмектесу маған ләззат береді 🖤",
            'Русский': "Помогать вам — это всегда удовольствие для меня 🖤",
            'English': "Helping you is always a pleasure for me 🖤"
        }
        update.message.reply_text(thank_you_messages.get(language, "Тіл таңдалмады"))

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, music_request))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, song_found))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, thank_you))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()