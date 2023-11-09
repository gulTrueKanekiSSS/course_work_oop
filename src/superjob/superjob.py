from typing import Dict, List

import requests

from src.abstract_class import Job
from src.implemented.implemented import api_key, convert_valutes_super, top_salary_super, save_data_to_json, \
    get_json_data, sort_areas_super
from src.vacancie.vacancie import Vacancie


class VacanciesSuperJob(Job):
    def __init__(self, platform: str, search_request: str, amount: int, area=None):
        self.platform: str = platform
        self.search_request: str = search_request
        self.amount: int = amount
        self.area: str = area
        self.headers: Dict = {
            'X-Api-App-Id': api_key
        }
        self.params: Dict = {
            'keywords': self.search_request,
        }
        self.save: Dict = self.get_data_and_save()

    def get_data_and_save(self) -> Dict:

        vacancies: Dict = requests.get(
            'https://api.superjob.ru/2.0/vacancies/',
            headers=self.headers,
            params=self.params
        ).json()['objects']
        save_data_to_json(vacancies, 'superjob')
        return vacancies

    def return_data(self) -> Dict:
        if self.area is None:
            data: Dict = get_json_data('superjob')
            return data
        else:
            data: Dict = get_json_data('superjob')
            return sort_areas_super(data, self.area)

    def initialization_vacancie_class(self) -> List[object]:
        items = []
        for item in self.return_data():
            if item.get('payment_to') is not None and item.get('payment_to') != 0:

                vacancie: object = Vacancie(
                    self.search_request,
                    self.platform,
                    self.amount,
                    name=item.get('profession'),
                    salary=item.get('payment_to'),
                    url=item.get('link'),
                    requirement=item.get('candidat')
                )

                items.append(vacancie)

            elif item.get('payment_from') is not None and item.get('payment_from') != 0:

                vacancie: object = Vacancie(
                    self.search_request,
                    self.platform,
                    self.amount,
                    name=item.get('profession'),
                    salary=item.get('payment_from'),
                    url=item.get('link'),
                    requirement=item.get('candidat')
                )

                items.append(vacancie)

            else:

                vacancie: object = Vacancie(
                    self.search_request,
                    self.platform,
                    self.amount,
                    name=item.get('profession'),
                    salary='Не указано',
                    url=item.get('link'),
                    requirement=item.get('candidat')
                )

                items.append(vacancie)
        return items

    def salary_to_rubles(self) -> Dict:
        data: Dict = self.return_data()

        for item in data:
            if item.get('payment_to') is not None and item.get('payment_to') != 0:
                item['payment_to'] = convert_valutes_super(item.get('currency'), item.get('payment_to'))
                item['currency'] = 'rub'


            elif item.get('payment_from') is not None and item.get('payment_from') != 0:
                item['payment_from'] = convert_valutes_super(item.get('currency'), item.get('payment_from'))
                item['currency'] = 'rub'

            else:
                item['payment_from'] = 0
                item['payment_to'] = 0
                item['currency'] = 'rub'
        return data

    def return_top_vacancies(self) -> Dict:
        return top_salary_super(self.salary_to_rubles(), self.amount)
