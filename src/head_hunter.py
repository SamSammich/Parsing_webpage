import json
from abc import ABC, abstractmethod

import requests
from pprint import pprint


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


class Vacancy:
    __slots__ = (
        'title', 'salary_min', 'salary_max', 'url', 'responsibility', 'employer', 'currency', 'salary_sort_min',
        'salary_sort_max')

    def __init__(self, title, salary_min, salary_max, url, responsibility, employer, currency):
        self.title = title
        self.employer = employer
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.url = url
        self.responsibility = responsibility
        self.currency = currency

        self.salary_sort_min = salary_min
        self.salary_sort_max = salary_max
        if currency and currency == 'USD':
            self.salary_sort_min = self.salary_sort_min * 83.5 if self.salary_sort_min else None
            self.salary_sort_max = self.salary_sort_max * 83.5 if self.salary_sort_max else None

    def __str__(self):
        salary_min = f"From -->:{self.salary_min}" if self.salary_min else ''
        salary_max = f" To {self.salary_max}" if self.salary_max else ''
        currency = self.currency if self.currency else ''
        if self.salary_min is None and self.salary_max is None:
            salary_min = "No information about salary was provided"

        return f"{self.employer}: {self.title}\n{salary_min}{salary_max} {currency}\nURL--> {self.url}\n{self.responsibility}"

    def __gt__(self, other):
        if not other.salary_sort_min:
            return True
        if not self.salary_sort_min:
            return False
        return self.salary_sort_min >= other.salary_sort_min


class JSONSaver:
    def __init__(self, keyword):
        self.__filename = f'{keyword}.json'

    @property
    def filename(self):
        return self.__filename

    def add_vacancies(self, data):
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def select(self):
        with open(self.__filename, 'r', encoding='utf-8') as select_file:
            select_data = json.load(select_file)

        vacancies = []

        for row in select_data:
            salary_min, salary_max, currency = None, None, None
            if row['salary']:
                salary_min, salary_max, currency = row['salary']['from'], row['salary']['to'], row['salary']['currency']
            vacancies.append(
                Vacancy(row['name'], salary_min, salary_max, row['alternate_url'],
                        row['snippet']['responsibility'], row['employer']['name'], currency))
        return vacancies
