import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import yt_dlp

# Боттың токенін осында қой
TOKEN = 'ТВОЙ_ТОКЕН_ОСЫНДА'

# Жүктелетін файлдардың сақталатын папкасы
DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Сәлем! Музыка алу үшін /song командасын және ән атын жаз:\nМысалы: /song Qara kyz")

def song(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Әннің атын жазыңыз. Мысалы: /song sagyndym seni")
        return

    song_name = ' '.join(context.args)
    update.message.reply_text(f"Іздеп жатырмын: {song_name}...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
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

        with open(filename, 'rb') as audio_file:
            context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio_file, title=title)

        # Файлды өшіріп тастау (қаласаң)
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