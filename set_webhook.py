import requests

TOKEN = "7302516914:AAFf7O9szcJD5GZGSsSs3TuyHdyvKhF8zN8"
HEROKU_APP_NAME = "tynda-music-botn1"

URL = f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}"

response = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={URL}")

print("Webhook response:")
print(response.text)
