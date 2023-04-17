from abc import ABC

import requests


class Engine(ABC):
    def ge_request(self):
        pass


class HeadHunterAPI(Engine):
    def get_request(self, keyword, page):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Accept-Language": "ru,en-US;q=0.9,en;q=0.8"
        }

        params = {
            "text": keyword,  # Текст фильтра.
            "page": page,
            "per_page": 100
        }
        return requests.get('https://api.hh.ru/vacancies', headers=headers, params=params).json()['items']

    def get_vacancies(self, keyword, count=1000):
        pages = 1
        response = []
        for page in range(pages):
            print(f"Parsing page {page}", end=": ")
            values = self.get_request(keyword, page)
            print(f"Found {len(values)} vacancies")
            response.extend(values)
        return response


class SuperJobAPI(Engine):
    def get_request(self, keyword, page):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Accept-Language": "ru,en-US;q=0.9,en;q=0.8"
        }

        params = {
            "text": keyword,  # Текст фильтра.
            "page": page,
            "per_page": 100
        }
        return requests.get('https://www.superjob.ru/vakansii/', headers=headers, params=params).json()['items']

    def get_vacancies(self, keyword, count=1000):
        pages = 1
        response = []
        for page in range(pages):
            print(f"Parsing page {page}", end=": ")
            values = self.get_request(keyword, page)
            print(f"Found {len(values)} vacancies")
            response.extend(values)
        return response


a = SuperJobAPI()
#a.get_request('Python',)
