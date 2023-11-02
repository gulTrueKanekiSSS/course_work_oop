import requests
from src.implemented.implemented import save_data_to_json, convert_valutes_hh, top_salary_hh, get_json_data
from src.vacancie.vacancie import Vacancie

class VacanciesHeadHunterApi:

    def __init__(self, platform: str, search_request: str, amount: int):
        self.__platform = platform
        self.__search_request = search_request
        self.amount = amount
        self.params = {
            'text': self.search_request,
            'only_with_salary': 'true'
        }
        self.save = self.get_data_hh_ru_and_save()

    @property
    def search_request(self):
        return self.__search_request

    @property
    def platform(self):
        return self.__platform

    def get_data_hh_ru_and_save(self):
        data = requests.get("https://api.hh.ru/vacancies", params=self.params).json()
        save_data_to_json(data, 'hh')
        return data

    def return_data_hh_ru(self):
        data = get_json_data('hh')
        return data

    def return_data_hh_ru_items(self):
        return self.return_data_hh_ru()['items']


    def rubles_salary(self):
        data = self.return_data_hh_ru_items()
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
            vacancie = Vacancie(self.platform, self.search_request, self.amount,
                                name=item.get('name'),
                                salary=item.get('salary').get('from'),
                                url=item.get('url'),
                                requirement=item.get('snippet').get('requirement'))
            items.append(vacancie)
        return items


