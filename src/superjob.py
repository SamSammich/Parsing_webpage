import json

import requests

from src.absract_class import Engine


class SuperJobAPI(Engine):
    def get_request(self, keyword, page):
        """Getting request from the webpage """
        headers = {
            'X-Api-App-Id': 'v3.r.137495228.ce506973c321059e744631bcdcea3b45881b09a3.ee07852c02c10455e9604c357587a477334572ae',
            "Accept-Language": "ru,en-US;q=0.9,en;q=0.8"
        }

        params = {
            'keywords': keyword,  # Текст фильтра.
            'page': page,
            'count': 100,
            'more': True
        }
        return requests.get('https://api.superjob.ru/2.0/vacancies/?', headers=headers, params=params).json()['objects']

    def get_vacancies(self, keyword, pages):
        """Saving Information in response and returning it"""
        response = []
        for page in range(int(pages)):
            print(f"Parsing page {page}", end=": ")
            values = self.get_request(keyword, page)
            response.extend(values)
            print(f"Found {len(values)} vacancies")
        return response


class Vacancy:
    __slots__ = (
        'title', 'salary_min', 'salary_max', 'url', 'responsibility', 'currency', 'salary_sort_min',
        'salary_sort_max')

    def __init__(self, title, salary_min, salary_max, url, responsibility, currency):
        self.title = title

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
        salary_min = f"Salary: From -->:{self.salary_min}" if self.salary_min else 'Salary: From --> No information'
        salary_max = f" To {self.salary_max}" if self.salary_max else ' To --> No information'
        currency = f" Currency-> {self.currency}" if self.currency else 'No information'
        if self.salary_min is None and self.salary_max is None:
            salary_min = "No information about salary was provided"

        return f": {self.title}\n{salary_min}{salary_max} {currency}\nURL--> {self.url}\n{self.responsibility}"

    def __gt__(self, other):
        if not other.salary_sort_min:
            return True
        if not self.salary_sort_min:
            return False
        return self.salary_sort_min >= other.salary_sort_min


class JSONSaverSJ:
    def __init__(self, keyword_sj):
        self.__filename = f'{keyword_sj}.json'

    @property
    def filename(self):
        return self.__filename

    def add_vacancies(self, data):
        """Saving vacancies in JSON file """
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def select(self):
        """Extracting the relevant information from the JSON file."""
        with open(self.__filename, 'r', encoding='utf-8') as select_file:
            select_data = json.load(select_file)
        vacancies_sj = []
        for row_sj in select_data:
            salary_min, salary_max, currency = None, None, None
            vacancies_sj.append(
                Vacancy(row_sj['profession'], row_sj['payment_from'], row_sj['payment_to'], row_sj['link'],
                        row_sj['candidat'],

                        row_sj['currency'].title()))

        return vacancies_sj
