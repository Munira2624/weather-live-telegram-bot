from datetime import datetime, timezone, timedelta
from translate import Translator
import requests

async def get_weather(city_name, lang="uz"):
    API_KEY = '###########################'

    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_name.lower()}&appid={API_KEY}&units=metric&lang={lang}"
        )

        if response.status_code == 200:
            data = response.json()
            temp = int(data['main']['temp'])
            wind = data['wind']['speed']
            timezone_offset = data['timezone']
            description = data['weather'][0]['description']
            name = data['name']
            sunrise = datetime.fromtimestamp(data['sys']['sunrise'] + timezone_offset, tz=timezone.utc).strftime('%H:%M:%S')
            sunset = datetime.fromtimestamp(data['sys']['sunset'] + timezone_offset, tz=timezone.utc).strftime('%H:%M:%S')
            local_time = datetime.utcnow() + timedelta(seconds=timezone_offset)
            time_str = local_time.strftime('%H:%M:%S')

            translator = Translator(to_lang=lang)
            translated_description = translator.translate(description)

            if lang == "uz":
                return (f"📍 Shahar: <b>{name}</b>\n🌡 Harorat: {temp}°C\n🕒 Shahardagi hozirgi vaqt: {time_str}\n"
                        f"🌤 Ob-havo: \"{translated_description}\"\n🌅 Quyosh chiqishi: {sunrise}\n🌇 Quyosh botishi: {sunset}\n💨 Shamol: {wind} m/s")
            elif lang == "ru":
                return (f"📍 Город: <b>{name}</b>\n🌡 Температура: {temp}°C\n🕒 Текущее время в городе: {time_str}\n"
                        f"🌤 Погода: \"{translated_description}\"\n🌅 Восход: {sunrise}\n🌇 Закат: {sunset}\n💨 Ветер: {wind} м/c")
            else:
                return (f"📍 City: <b>{name}</b>\n🌡 Temperature: {temp}°C\n🕒 Current local time in the city: {time_str}\n"
                        f"🌤 Weather: \"{translated_description}\"\n🌅 Sunrise: {sunrise}\n🌇 Sunset: {sunset}\n💨 Wind: {wind} m/s")

        else:
            return {
                "uz": "❌ Bunday shahar topilmadi.",
                "ru": "❌ Город не найден.",
                "en": "❌ City not found."
            }[lang]

    except Exception as e:
        return {
            "uz": "⚠️ Xatolik yuz berdi.",
            "ru": "⚠️ Произошла ошибка.",
            "en": "⚠️ An error occurred."
        }[lang]
