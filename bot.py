import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from yt_dlp.utils import DownloadError
import yt_dlp

# Сіздің бот токеніңіз
TOKEN = "7302516914:AAFf7O9szcJD5GZGSsSs3TuyHdyvKhF8zN8"

# Қарсы алу хабарламасы және тіл таңдау
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Қазақша 🇰🇿", callback_data='kazakh')],
        [InlineKeyboardButton("Русский 🇷🇺", callback_data='russian')],
        [InlineKeyboardButton("English 🇺🇸", callback_data='english')],
        [InlineKeyboardButton("O‘zbekcha 🇺🇿", callback_data='uzbek')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Tyn’da Music Bot-қа қош келдің! Саған қай тілде сөйлескен ыңғайлы?", reply_markup=reply_markup)

# Тілді таңдау және жауап беру
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    language = query.data

    if language == 'kazakh':
        query.edit_message_text(text="Сәлем! Қалай көмек көрсете аламын?")
    elif language == 'russian':
        query.edit_message_text(text="Привет! Чем могу помочь?")
    elif language == 'english':
        query.edit_message_text(text="Hello! How can I help you?")
    elif language == 'uzbek':
        query.edit_message_text(text="Salom! Yordam bera olishim mumkinmi?")
    
    query.message.reply_text("Енді маған әннің атын жазыңыз, мен оны іздеп тауып беремін.")

# Ән жүктеу логикасы
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

# Ән сұрауы және аудио жіберу
def handle_message(update: Update, context: CallbackContext):
    query = update.message.text.strip()
    update.message.reply_text(f"Іздеймін: «{query}»…")
    try:
        file_path = download_audio(query)
        with open(file_path, 'rb') as f:
            update.message.reply_audio(audio=f)
        os.remove(file_path)
    except DownloadError as e:
        if 'Sign in to confirm you’re not a bot' in str(e):
            update.message.reply_text(
                "Кешіріңіз, бұл ән шектеулі немесе авторландырылған контент болғандықтан жүктелмейді.\n"
                "Өтінемін, басқа әннің атын жазыңыз."
            )
        else:
            update.message.reply_text(f"Таңғадамалы қате шықты: {e}")
    except Exception as e:
        update.message.reply_text(f"Өзге қате: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()