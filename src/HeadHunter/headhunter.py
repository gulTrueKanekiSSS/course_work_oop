import requests
from src.Implemented.implemented import save_data_to_json, convert_valutes_hh, top_salary_hh
from src.Vacancie.vacancie import Vacancie

class VacanciesHeadHunterApi:

    def __init__(self, platform: str, search_request: str, amount: int):
        self._platform = platform
        self._search_request = search_request
        self.amount = amount

    @property
    def search_request(self):
        return self._search_request

    @property
    def platform(self):
        return self._platform

    def return_data_hh_ru(self):
        params = {
            'text': self.search_request
        }
        data = requests.get("https://api.hh.ru/vacancies", params=params).json()
        return data

    def return_data_hh_ru_items(self):
        return self.return_data_hh_ru()['items']

    def filtered_salary_data(self):
        filtered_data = []
        for item in self.return_data_hh_ru_items():
            if item.get("salary") is None:
                continue
            else:
                filtered_data.append(item)
        return filtered_data

    def rubles_salary(self):
        data = self.filtered_salary_data()
        for item in data:
            if item['salary']['from'] is None and item['salary']['to'] is not None:
                item['salary']['to'] = convert_valutes_hh(item['salary']['currency'], item['salary']['to'])
                item['salary']['currency'] = 'RUR'
            elif item['salary']['from'] is not None and item['salary']['to'] is None:
                item['salary']['from'] = convert_valutes_hh(item['salary']['currency'], item['salary']['from'])
                item['salary']['currency'] = 'RUR'
            else:
                continue
        return data

    def return_top_vacancies(self):
        return top_salary_hh(self.rubles_salary(), self.amount)


class DataVacancies(VacanciesHeadHunterApi):

    def objects(self) -> list:
        items = []
        for item in self.return_data_hh_ru()["items"]:
            vacancie = Vacancie(self._platform, self._search_request, self.amount,
                                name=item.get('name'),
                                salary=item.get('salary').get('from'),
                                url=item.get('url'),
                                requirement=item.get('snippet').get('requirement'))
            items.append(vacancie)
        return items


class SaveVacancies(VacanciesHeadHunterApi):

    def save_to_json(self):
        save_data_to_json(self.return_top_vacancies())

