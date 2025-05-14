import requests
import time

# Боттың токені
TOKEN = '7302516914:AAFf7O9szcJD5GZGSsSs3TuyHdyvKhF8zN8'

# Топтың ID-і (осы жерге нақты топтың ID-ін жазыңыз)
chat_id = '<Топтың ID-і>'

# Музыка файлының жолы (осы жерге нақты музыканың файлын жазыңыз)
file_path = 'path_to_music_file.mp3'

# Боттың жаңартуларын алу URL
url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'

# Қайдадан бастау керек екенін сақтау үшін offset мәні
offset = None

while True:
    # Жаңартуларды алу (offset қолданамыз)
    params = {'offset': offset}
    response = requests.get(url, params=params)
    updates = response.json()
    
    # Хабарламаларға жауап беру
    for update in updates['result']:
        if 'message' in update:
            message = update['message']
            text = message.get('text', '')
            print(f"Received message: {text}")
            
            # Егер хабарлама музыканы сұраса
            if text.lower() == 'music':
                # Файлды жіберу
                send_url = f'https://api.telegram.org/bot{TOKEN}/sendAudio?chat_id={chat_id}'
                with open(file_path, 'rb') as file:
                    requests.post(send_url, files={'audio': file})
            
            # Алдағы хабарламаларға жауап беруге мүмкіндік беру үшін offset мәнін жаңарту
            offset = update['update_id'] + 1
    
    # Әр 2 секунд сайын жаңартуларды тексеру
    time.sleep(2)