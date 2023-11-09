import json
import os
from typing import NoReturn, Dict

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')


def save_data_to_json(data: Dict, type: str, filename='jobs.json') -> NoReturn:
    try:
        with open(f'{type}_{filename}', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f'Данные сохранены в файл {type}_{filename}')
    except Exception as e:
        print(f'Произошла ошибка при сохранении данных: {str(e)}')


def get_json_data(type: str, file='jobs.json') -> Dict:
    file_name: str = f'{type}_{file}'
    with open(file_name, 'r') as file:
        data: Dict = json.load(file)
    return data


def sort_areas_hh(data: Dict, area: str) -> Dict:
    sorted_data = {
        'items': []
    }
    for item in data:
        if item['area']['name'] == area:
            sorted_data['items'].append(item)
    return sorted_data

def sort_areas_super(data: Dict, area: str):
    sorted_data = []
    for item in data:
        if item['town']['title'] == area:
            sorted_data.append(item)
    return sorted_data

def convert_valutes_hh(currency: str, to: int) -> int:
    currrency_to_rubles: Dict[str, int] = {
        'EUR': 100,
        'USD': 100,
        'AZN': 56,
        'BYR': 29,
        'GEL': 35,
        'KGS': 1,
        'KZT': 0.20,
        'RUR': 1,
        'UAH': 2.62,
        'UZS': 0.0078
    }

    return to * currrency_to_rubles.get(currency)


def convert_valutes_super(currency: str, to: int) -> int:
    currrency_to_rubles: Dict[str, int] = {
        'rub': 1,
        'uah': 2.62,
        'uzs': 0.0078
    }

    return to * currrency_to_rubles.get(currency)


def top_salary_hh(data: Dict, amount: int) -> Dict:
    sorted_data: object = sorted(data, key=lambda item: item.get('salary').get('to') if item.get('salary').get(
        'to') is not None else item.get('salary').get('from'), reverse=True)

    return sorted_data[:amount]


def top_salary_super(data: Dict, amount: int) -> Dict:
    sorted_data: object = sorted(data, key=lambda item: item.get('payment_to') if item.get(
        'payment_to') is not None else item.get('payment_from'), reverse=True)

    return sorted_data[:amount]

def beauty_console_log_super(data):
    answer = ''

    counter = 1
    for item in data:
        answer += f'\n\nВакансия {counter}, подробнее на {item["link"]}\n'
        answer += f'Наименование вакансии - {item["profession"]}\n'
        if item['payment_to'] is not None:
            answer += f'Зарплата может достигнуть - {item["payment_to"]}\n\n'
        elif item['payment_to'] is None and item['payment_from'] is not None:
            answer += f'Зарплата начинается с {item["payment_from"]}\n\n'
        answer += f'{item["candidat"]}\n'
        counter += 1
    return answer

def beauty_console_log_hh(data):
    answer = ''

    counter = 1
    for item in data:
        answer += f'\n\nВакансия {counter}, подробнее о вакансии на {item["url"]}\n'
        answer += f'Наименование вакансии - {item["name"]}\n'
        if item['salary']['to'] is not None:
            answer += f'Зарплата может достигнуть - {item["salary"]["to"]}\n\n'
        elif item['salary']['to'] is None and item['salary']['from'] is not None:
            answer += f'Зарплата начинается с {item["salary"]["from"]}\n\n'
        if item['snippet']['requirement']:
            answer += f'Требования - {item["snippet"]["requirement"]}\n'
        if item['snippet']['responsibility']:
            answer += f'Обяанности - {item["snippet"]["responsibility"]}\n'
        counter += 1
    return answer
