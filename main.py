import requests
import json
from pprint import pprint
from datetime import datetime, timezone, timedelta
from translate import Translator

API_KEY = '#######################'

while True:
    city_name = input('Shahar nomini kiriting (yoki "stop" deb yozing): ').lower()
    if city_name == "stop":
        break

    try:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric&lang=uz'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            temp = int(data['main']['temp'])
            description = data['weather'][0]['description']
            time_zone = data['timezone']
            wind = data['wind']['speed']
            name = data['name']
            sunrise_timestamp = data['sys']['sunrise'] + time_zone
            sunset_timestamp = data['sys']['sunset'] + time_zone

            sunrise_utc = datetime.fromtimestamp(sunrise_timestamp, tz=timezone.utc).strftime('%H:%M:%S')
            sunset_utc = datetime.fromtimestamp(sunset_timestamp, tz=timezone.utc).strftime('%H:%M:%S')

            # Shahar vaqti hisoblash
            current_utc_time = datetime.utcnow()
            city_time = current_utc_time + timedelta(seconds=time_zone)
            city_time_str = city_time.strftime('%H:%M:%S')

            translator = Translator(to_lang='uz')
            translated_description = translator.translate(description)

            output_data = {
                'Shahar nomi': name,
                'Ob-havo haqida': translated_description,
                'Havo harorati (°C)': temp,
                'Shamol tezligi (m/s)': wind,
                'Quyosh chiqish vaqti': sunrise_utc,
                'Quyosh botish vaqti': sunset_utc,
                'Shahardagi hozirgi vaqt': city_time_str
            }

            with open(f'{name}.json', mode='w', encoding='utf-8') as json_file:
                json.dump(output_data, json_file, indent=4, ensure_ascii=False)

            pprint(output_data)

        else:
            print("❌ Shahar topilmadi yoki boshqa xatolik yuz berdi.")

    except Exception as e:
        print(f"🚫 Xatolik yuz berdi: {e}")
