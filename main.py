from src.headhunter.headhunter import VacanciesHeadHunterApi
from src.superjob.superjob import VacanciesSuperJob


def user_interface(platform, search_request, amount):

    if platform == 'hh.ru':
        obj = VacanciesHeadHunterApi(platform, search_request, amount)
        data = obj.return_top_vacancies()
        return data

    elif platform == 'superjob':
        obj = VacanciesSuperJob(platform, search_request, amount)
        return obj.top_vacancies()

    else:
        raise ValueError("Неверное название платформы")


if __name__ == '__main__':
    platform = input('Выберите платформу(superjob or hh.ru) введите ее название:')
    search_request = input('Введите интересующий вас поисковой запрос')
    amount = int(input("Введите сколько вакансий должен включать топ по зарплате"))

    print(user_interface(platform, search_request, amount))

