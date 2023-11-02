import requests

from src.abstract_class import Job
from src.implemented.implemented import api_key, convert_valutes_super, top_salary_super, save_data_to_json, get_json_data
from src.vacancie.vacancie import Vacancie

class VacanciesSuperJob(Job):
    def __init__(self, platform, search_request, amount):
        self.platform = platform
        self.search_request = search_request
        self.amount = amount
        self.headers = {
            'X-Api-App-Id': api_key
        }
        self.params = {
            'keywords': self.search_request,
        }
        self.save = self.get_vacancies_and_save()

    def get_vacancies_and_save(self):

        vacancies = requests.get(
            'https://api.superjob.ru/2.0/vacancies/',
            headers=self.headers,
            params=self.params
        ).json()['objects']
        save_data_to_json(vacancies, 'superjob')
        return vacancies

    def get_vacancies(self):
        data = get_json_data('superjob')
        return data

    def initialization_vacancie_class(self):
        items = []
        for item in self.get_vacancies():
            if item.get('payment_to') is not None and item.get('payment_to') != 0:

                vacancie = Vacancie(
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

                vacancie = Vacancie(
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

                vacancie = Vacancie(
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

    def salary_to_rubles(self):
        data = self.get_vacancies()

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

    def top_vacancies(self):
        return top_salary_super(self.salary_to_rubles(), self.amount)