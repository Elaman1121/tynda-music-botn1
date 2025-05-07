from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# /start командасына жауап
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Сәлем! Бұл Tyn’da Music Bot. Музыка іздеу үшін әннің атын жазыңыз.")

def main():
    # Telegram bot token
    updater = Updater("7302516914:AAFf7O9szcJD5GZGSsSs3TuyHdyvKhF8zN8", use_context=True)

    dispatcher = updater.dispatcher

    # /start командасы
    dispatcher.add_handler(CommandHandler("start", start))

    # Ботты іске қосу
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()