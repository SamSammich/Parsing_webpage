import json
import requests
import time
import os

input_text = input("Could you kindly specify the type of job you are interested in? \n -->")


def GetPage(page=0, input_text=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Accept-Language": "ru,en-US;q=0.9,en;q=0.8"
    }
    params = {
        'text': f'NAME:{input_text}',  # Текст фильтра. В имени должно быть слово "Аналитик"
        'area': 1,  # Поиск ощуществляется по вакансиям города Москва
        'page': page,  # Индекс страницы поиска на HH
        'per_page': 100  # Кол-во вакансий на 1 странице

    }

    req = requests.get('https://api.hh.ru/vacancies', headers=headers, params=params)  # Посылаем запрос к API
    data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    return data


for page in range(0, 2):
    json_file = json.loads(GetPage(page, input_text))
    with open('../vacancies.json', 'w', encoding='utf8') as vac_file:
        vac_file.write(json.dumps(json_file, ensure_ascii=False))
for el in json_file['items']:
    print(el['name'])
    print(el['salary'])
    if el["address"]!= None:
        print(el["address"]['city'])
    else:
        print("No city address")

    print(el['url'])

