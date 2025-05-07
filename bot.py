import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import yt_dlp

# Telegram ботыңның токенін осында жаз
TOKEN = '7302516914:AAFf7O9szcJD5GZGSsSs3TuyHdyvKhF8zN8'
# MP3 файлдар сақталатын папка
DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Сәлем! Маған /song командасымен әннің атын жаз:\nМысалы: /song sagyndym seni")

def song(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Әннің атын жазыңыз. Мысалы: /song sagyndym seni")
        return

    song_name = ' '.join(context.args)
    update.message.reply_text(f"Іздеп жатырмын: {song_name}...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{song_name}", download=True)
            entry = info['entries'][0]
            title = entry.get('title', 'song')
            filename = os.path.join(DOWNLOAD_DIR, f"{title}.mp3")

        # Файл жіберу
        with open(filename, 'rb') as audio_file:
            context.bot.send_audio(chat_id=update.message.chat_id, audio=audio_file, title=title)

        # Қаласаң, файлды жүктеп болған соң өшіріп тастауға болады:
        # os.remove(filename)

    except Exception as e:
        update.message.reply_text(f"Қате болды: {e}")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("song", song))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()