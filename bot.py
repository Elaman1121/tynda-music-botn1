import telegram
from telegram.ext import Updater, CommandHandler
import yt_dlp

TOKEN = '7302516914:AAFf7O9szcJD5GZGSsSs3TuyHdyvKhF8zN8'  # Сіздің токеніңіз

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    update.message.reply_text("Сәлем! Әннің атын /song командасынан кейін жаз.")

def song(update, context):
    song_name = ' '.join(context.args)
    if song_name:
        # Әнді іздеу және MP3 файлы ретінде қайта жіберу
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'quiet': True,
            'extractaudio': True,  # аудио алу
            'audioquality': 1,     # жоғары сапа
            'postprocessors': [{
                'key': 'FFmpegAudioConvertor',
                'preferredcodec': 'mp3',  # MP3 форматы
                'preferredquality': '320',  # 320 kbps
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{song_name}", download=False)
            url = info['entries'][0]['url']  # бірінші нәтижені алу
            song_file = ydl.prepare_filename(info['entries'][0])
            
            # Жүктеу
            ydl.download([f"ytsearch:{song_name}"])
            
            # Файлды Telegram арқылы жіберу
            context.bot.send_audio(chat_id=update.message.chat_id, audio=open(song_file, 'rb'))

    else:
        update.message.reply_text("Әннің атын жазыңыз!")

start_handler = CommandHandler('start', start)
song_handler = CommandHandler('song', song)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(song_handler)

updater.start_polling()
import yt_dlp

def search_song(song_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'extractaudio': True,  # аудио алу
        'audioquality': 1,     # жоғары сапа
        'postprocessors': [{
            'key': 'FFmpegAudioConvertor',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch:{song_name}", download=False)
        if 'entries' in result:
            return result['entries'][0]['url']
        return None
    
# Тест функциясы
print(search_song('sagyndym'))  # Бұл жерде 'sagyndym' әнін іздеңіз
