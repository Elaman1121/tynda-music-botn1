import os
import yt_dlp
from yt_dlp.utils import DownloadError
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, RegexHandler

# Сіздің бот токеніңіз
TOKEN = "YOUR_BOT_TOKEN"  # Токенді дұрыс енгізіңіз

LANGUAGE, MUSIC_QUERY = range(2)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Сәлем! Қай тілде сөйлескіңіз келеді?\n"
        "1. Қазақша\n"
        "2. Русский"
    )
    return LANGUAGE

def choose_language(update: Update, context: CallbackContext):
    user_choice = update.message.text.strip()
    
    if user_choice == "1":
        context.user_data['language'] = 'kazakh'
        update.message.reply_text(
            "Қайырлы күн! Менімен қазақ тілінде сөйлесіңіз.\n"
            "Маған әннің атын жазыңыз."
        )
    elif user_choice == "2":
        context.user_data['language'] = 'russian'
        update.message.reply_text(
            "Здравствуйте! Пожалуйста, напишите название песни."
        )
    else:
        update.message.reply_text("Қате таңдаңыз! Қазақша немесе орысша таңдаңыз.")
        return LANGUAGE

    return MUSIC_QUERY

def download_audio(query: str) -> str:
    """YouTube-тан аудио жүктеп, 'song.mp3' атымен қайтарады."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.%(ext)s',
        'noplaylist': True,
        'quiet': False,  # Қате туралы толық ақпарат алу үшін 'False' қою
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)
            return "song.mp3"
    except DownloadError as e:
        print(f"Жүктеу қатесі: {e}")
        raise
    except Exception as e:
        print(f"Басқа қате: {e}")
        raise

def handle_message(update: Update, context: CallbackContext):
    query = update.message.text.strip()
    user_language = context.user_data.get('language', 'kazakh')  # Әдепкі тіл - қазақша

    if user_language == 'kazakh':
        update.message.reply_text(f"Іздеймін: «{query}»…")
    else:
        update.message.reply_text(f"Ищу: «{query}»…")
    
    try:
        file_path = download_audio(query)
        with open(file_path, 'rb') as f:
            update.message.reply_audio(audio=f)
        os.remove(file_path)
    except DownloadError as e:
        # Қате туралы хабарлама шығару
        if user_language == 'kazakh':
            update.message.reply_text("Кешіріңіз, бұл ән жүктелмеді. Басқа әннің атын жазыңыз.")
        else:
            update.message.reply_text("Извините, эта песня не может быть загружена. Пожалуйста, напишите другое название.")
    except Exception as e:
        if user_language == 'kazakh':
            update.message.reply_text(f"Қате шықты: {e}")
        else:
            update.message.reply_text(f"Ошибка: {e}")

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Процесс завершен.")
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # ConversationHandler-ді анықтау
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANGUAGE: [MessageHandler(Filters.text & ~Filters.command, choose_language)],
            MUSIC_QUERY: [MessageHandler(Filters.text & ~Filters.command, handle_message)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conversation_handler)
    
    # Тек polling (getUpdates) әдісін қолданамыз
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()