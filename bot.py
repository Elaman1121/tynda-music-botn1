import os
import telebot
from flask import Flask, request

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# Музыка файлы (осы файлды repo-ңа салып қой)
AUDIO_FILE = 'music.mp3'

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Сәлем! Музыка алу үшін 'music' деп жаз!")

@bot.message_handler(func=lambda message: message.text and 'music' in message.text.lower())
def send_music(message):
    with open(AUDIO_FILE, 'rb') as audio:
        bot.send_audio(message.chat.id, audio)

@server.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

@server.route("/")
def index():
    return "Bot is working", 200

# Heroku портын алу
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://tynda-music-botn1.herokuapp.com/{TOKEN}")
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))