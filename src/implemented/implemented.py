import json
import os

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')



def save_data_to_json(data, type: str, filename='jobs.json') -> None:
    try:
        with open(f'{type}_{filename}', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f'Данные сохранены в файл {type}_{filename}')
    except Exception as e:
        print(f'Произошла ошибка при сохранении данных: {str(e)}')

def get_json_data(type, file='jobs.json'):
    file_name = f'{type}_{file}'
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data

def convert_valutes_hh(currency, to) -> int:
    currrency_to_rubles = {
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

def convert_valutes_super(currency, to):
    currrency_to_rubles = {
        'rub': 1,
        'uah': 2.62,
        'uzs': 0.0078
    }

    return to * currrency_to_rubles.get(currency)


def top_salary_hh(data, amount: int):

    sorted_data = sorted(data, key=lambda item: item.get('salary').get('to') if item.get('salary').get('to') is not None else item.get('salary').get('from'), reverse=True)

    return sorted_data[:amount]

def top_salary_super(data, amount: int):

    sorted_data = sorted(data, key=lambda item: item.get('payment_to') if item.get('payment_to') is not None else item.get('payment_from'), reverse=True)

    return sorted_data[:amount]