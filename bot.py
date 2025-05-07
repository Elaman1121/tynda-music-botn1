import yt_dlp
import os
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# /start командасы
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Сәлем! Әннің атын /song командасынан кейін жаз. Мысалы: /song 'Shape of You'"
    )

# /song командасы
def song(update: Update, context: CallbackContext):
    song_name = ' '.join(context.args)  # Қолданушының команданың соңындағы мәтіні
    if song_name:
        update.message.reply_text(f"Әнді іздеп жатырмын: {song_name}")

        # YT-DLP кітапханасы арқылы әнді іздеу
        ydl_opts = {
            'format': 'bestaudio/best',  # Ең жақсы аудио форматын таңдаймыз
            'extractaudio': True,  # Тек аудио шығару
            'outtmpl': 'downloads/%(id)s.%(ext)s',  # Файлды сақтау жолы
            'quiet': True,  # Әрекеттер туралы көп ақпарат көрсетпеу
        }

        try:
            # yt-dlp арқылы әнді жүктеу
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{song_name}", download=True)
                
                # Егер нәтиже болса
                if 'entries' in info:
                    video_url = info['entries'][0]['url']
                    file_path = f"downloads/{info['entries'][0]['id']}.mp3"
                    update.message.reply_text(f"Әнді жүктеп жатырмыз: {video_url}")

                    # Файлды Telegram арқылы жіберу
                    if os.path.exists(file_path):
                        # Жіберу алдында 3 секунд күту
                        time.sleep(3)
                        update.message.reply_audio(open(file_path, 'rb'))
                        os.remove(file_path)  # Файлды жіберген соң жоямыз
                    else:
                        update.message.reply_text("Ән жүктелген жоқ.")
                else:
                    update.message.reply_text("Өкінішке орай, ән табылмады.")
        except Exception as e:
            update.message.reply_text(f"Қате орын алды: {str(e)}")
    else:
        update.message.reply_text("Әннің атын жазыңыз. Мысалы: /song 'Shape of You'")

# Боттың негізгі функциясы
def main():
    # Сіздің токеніңізді қосыңыз
    updater = Updater("7302516914:AAFf7O9szcJD5GZGSsSs3TuyHdyvKhF8zN8", use_context=True)
    dp = updater.dispatcher

    # /start командасына хендлер
    dp.add_handler(CommandHandler("start", start))

    # /song командасына хендлер
    dp.add_handler(CommandHandler("song", song))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()