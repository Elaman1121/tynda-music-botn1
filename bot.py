import os
import yt_dlp
from yt_dlp.utils import DownloadError
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Сіздің бот токеніңіз
TOKEN = "7302516914:AAFf7O9szcJD5GZGSsSs3TuyHdyvKhF8zN8"

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Сәлем! Мен Tyn’daMusicBot.\n"
        "Маған әннің атын жазсаңыз, YouTube-тен MP3 (320 kbps) форматында жүктеп беруге тырысамын."
    )

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
        # Әдетте конвертациядан кейін файл 'song.mp3' болады
        return "song.mp3"

def handle_message(update: Update, context: CallbackContext):
    query = update.message.text.strip()
    update.message.reply_text(f"Іздеймін: «{query}»…")
    try:
        file_path = download_audio(query)
        with open(file_path, 'rb') as f:
            update.message.reply_audio(audio=f)
        os.remove(file_path)
    except DownloadError as e:
        # YouTube-тың кіргізуді талап ететін видеолары үшін
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
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Тек polling (getUpdates) әдісін қолданамыз
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
