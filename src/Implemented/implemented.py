import json


def save_data_to_json(data, filename='jobs.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f'Данные сохранены в файл {filename}')
    except Exception as e:
        print(f'Произошла ошибка при сохранении данных: {str(e)}')


def convert_valutes(currency, to):
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


def top_salary(data, amount: int):

    sorted_data = sorted(data, key=lambda item: item.get('salary').get('to') if item.get('salary').get('to') is not None else item.get('salary').get('from'))

    return sorted_data[:amount]
