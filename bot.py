import os
import yt_dlp
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = "7302516914:AAFf7O9szcJD5GZGSsSs3TuyHdyvKhF8zN8"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Сәлем! Әннің атын жазыңыз, мен MP3 жіберемін.")

def download_audio(query):
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
    query = update.message.text.strip()
    update.message.reply_text(f"Іздеймін: {query}…")
    try:
        file_path = download_audio(query)
        with open(file_path, 'rb') as f:
            update.message.reply_audio(audio=f)
        os.remove(file_path)
    except Exception as e:
        update.message.reply_text(f"Қате: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # МҰНДА ТЕК polling керек:
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()