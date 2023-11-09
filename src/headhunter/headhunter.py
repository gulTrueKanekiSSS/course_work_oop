from typing import List, Dict

import requests
from src.implemented.implemented import save_data_to_json, convert_valutes_hh, top_salary_hh, get_json_data, sort_areas_hh
from src.vacancie.vacancie import Vacancie
from src.abstract_class import Job


class VacanciesHeadHunterApi(Job):

    def __init__(self, platform: str, search_request: str, amount: int, area=None):
        self.__platform: str = platform
        self.__search_request: str = search_request
        self.area = area
        self.amount: int = amount
        self.params = {
            'text': self.search_request,
            'only_with_salary': 'true'
        }
        self.save = self.get_data_and_save()

    @property
    def search_request(self) -> str:
        return self.__search_request

    @property
    def platform(self) -> str:
        return self.__platform

    def get_data_and_save(self) -> Dict:
        data: Dict = requests.get("https://api.hh.ru/vacancies", params=self.params).json()
        save_data_to_json(data, 'hh')
        return data

    def return_data(self) -> Dict:
        data: Dict = get_json_data('hh')
        return data

    def return_data_items(self) -> Dict:
        if self.area is not None:
            data = sort_areas_hh(self.return_data()['items'], self.area)['items']
        else:
            data = self.return_data()['items']
        return data

    def salary_to_rubles(self) -> Dict:
        data: Dict = self.return_data_items()
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

    def return_top_vacancies(self) -> Dict:
        return top_salary_hh(self.salary_to_rubles(), self.amount)


class DataVacancies(VacanciesHeadHunterApi):

    def objects(self) -> List[object]:
        items = []
        for item in self.return_data_items():
            vacancie: object = Vacancie(self.platform, self.search_request, self.amount,
                                        name=item.get('name'),
                                        salary=item.get('salary').get('from'),
                                        url=item.get('url'),
                                        requirement=item.get('snippet').get('requirement'))
            items.append(vacancie)
        return items
