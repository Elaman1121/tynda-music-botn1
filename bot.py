import os
import yt_dlp
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = '7302516914:AAFf7O9szcJD5GZGSsSs3TuyHdyvKhF8zN8'  # Сенің токенің

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Сәлем! Музыка үшін /song командасын қолданыңыз.\nМысалы: /song sagyndym seni")

def song(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Ән атын жазыңыз. Мысалы: /song Qara kyz")
        return

    song_name = ' '.join(context.args)
    update.message.reply_text(f"Іздеп жатырмын: {song_name}...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': f'%(title)s.%(ext)s',
        'ffmpeg_location': '/app/.heroku/ffmpeg/bin/ffmpeg',  # Heroku үшін ffmpeg жолы
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{song_name}", download=True)  # Дұрыс жазылған параметр
            entry = info['entries'][0]
            title = entry.get('title', 'song')
            filename = f"{title}.mp3"

        with open(filename, 'rb') as audio_file:
            context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio_file, title=title)

        os.remove(filename)

    except Exception as e:
        update.message.reply_text(f"Қате болды: {str(e)}")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("song", song))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()