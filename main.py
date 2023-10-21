from src.HeadHunter.headhunter import VacanciesHeadHunterApi, DataVacancies

if __name__ == '__main__':
    platform = input('Выберите платформу(superjob or hh.ru) введите ее название:')
    search_request = input('Введите интересующий вас поисковой запрос')
    amount = int(input("Введите сколько вакансий должен включать топ по зарплате"))
    obj = VacanciesHeadHunterApi(platform, search_request, amount)
    for i in obj.return_top_vacancies():
        print(i['salary'])

