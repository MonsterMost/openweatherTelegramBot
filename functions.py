# файл для своих функций

import requests
from bs4 import BeautifulSoup
from pprint import pprint


def get_weather_by_city_name(city_name):
    parameters = {
        'appid': '137d62f3c460fac41edca5930e84af7c',
        'units': 'metric',
        'lang': 'ru',
        'q': city_name
    }  # это параметры для openweather API
    responce = requests.get('http://api.openweathermap.org/data/2.5/weather', parameters)
    # api.openweathermap.org/data/2.5/weather взяли с сайта https://openweathermap.org/current

    data = responce.json()  # превращаем в json
    # pprint(data) Красиво распечатает все данные

    # Если нет такого городадолжны обработать ошибку. Try except писать позже, посде первого запуска
    try:  # Добавим оформления <b></b> - жирный <i></i> - курсив
        message = f'''В городе <b>{data['name']}</b>  
<i>{data['weather'][0]['description'].capitalize()}</i>,
температура воздуха: {data['main']['temp']} градусов по Цельсию,
Скорость ветра {data['wind']['speed']} м/с
'''
    except KeyError:  # обработка если ошибка о не существующем городе
        message = 'Такого города не существует'
    return message


#функция парсинга и получения описания слова
def word_quiry(word):
    print(word)
    try:
        url = f'https://www.merriam-webster.com/dictionary/{word}'
        request = requests.get(url).text
        soup = BeautifulSoup(request, 'html.parser')
        definition = soup.find('span', class_='dtText').text.strip(": ").capitalize()
        pprint(definition)
        message = f'Слово: <b>{word.upper()}<b>.\nОписание: {definition}'
    except Exception:
        message = "Тут ошибка, не могу найти"
    return message
