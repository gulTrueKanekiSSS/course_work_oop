from pprint import pprint

from src.headhunter.headhunter import VacanciesHeadHunterApi
from src.superjob.superjob import VacanciesSuperJob
from src.implemented.implemented import beauty_console_log_super, beauty_console_log_hh


def user_interface(platform: str, search_request: str, amount: int, area=None):
    if platform == 'hh.ru':
        if area is None:
            obj = VacanciesHeadHunterApi(platform, search_request, amount)
            data = obj.return_top_vacancies()
            if data == []:
                return 'Вакансий не найдено'
            else:
                return beauty_console_log_hh(data)
        else:
            obj = VacanciesHeadHunterApi(platform, search_request, amount, area)
            data = obj.return_top_vacancies()
            if data == []:
                return 'Вакансий не найдено'
            else:
                return beauty_console_log_hh(data)

    elif platform == 'superjob':
        if area is None:
            obj = VacanciesSuperJob(platform, search_request, amount)
            pprint(obj.return_top_vacancies())
        else:
            obj = VacanciesSuperJob(platform, search_request, amount, area)
            data = obj.return_top_vacancies()
            if data == []:
                return 'Вакансий не найдено'
            else:
                return beauty_console_log_super(data)

    else:
        raise ValueError("Неверное название платформы")


if __name__ == '__main__':
    platform = input('Выберите платформу(superjob or hh.ru) введите ее название:')
    search_request = input('Введите интересующий вас поисковой запрос')
    area = input('Вы хотите видеть вакансии только из вашего города? Если да то введите его название с большой буквы, если нет, то просто напишите нет')
    amount = int(input("Введите сколько вакансий должен включать топ по зарплате"))

    if area == 'нет':
        print(user_interface(platform, search_request, amount))
    else:
        if area[0].isupper() and area[0].isalpha():
            print(user_interface(platform, search_request, amount, area))
