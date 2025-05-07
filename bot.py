from telegram import Update
from telegram.ext import Updater, CommandHandler
import yt_dlp as youtube_dl
from PIL import Image  # Pillow кітапханасын қосамыз
import os

TOKEN = "7302516914:AAFf7O9szcJD5GZGSsSs3TuyHdyvKhF8zN8"

def start(update: Update, context):
    update.message.reply_text("Сәлем! Әннің атын /song командасынан кейін жаз.")

def download(update: Update, context):
    query = " ".join(context.args)
    if not query:
        return update.message.reply_text("Әуелі әннің атын жаз!")
    update.message.reply_text(f"Іздеп жатырмын: {query}")
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': 'song.%(ext)s',
        'quiet': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
    filename = f"{info['title']}.mp3"
    os.rename("song.mp3", filename)
    
    # Музыка файлды жіберу
    update.message.reply_audio(open(filename, 'rb'))
    os.remove(filename)

if __name__ == "__main__":
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("song", download))
    updater.start_polling()
    updater.idle()