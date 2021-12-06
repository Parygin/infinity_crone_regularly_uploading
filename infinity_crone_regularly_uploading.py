import logging
import os
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv

load_dotenv()
# Параметры подключения к Infinity:
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
PROVIDER = os.getenv('PROVIDER')
TABLE = os.getenv('TABLE')
DATA_URL = 'http://{host}:{port}/data/{data_method}/'
STAT_URL = 'http://{host}:{port}/stat/{stat_method}/'

# Параметры скачивания и сохранения.
# today — сегодняшние записи,
# yesterday — записи вчерашнего дня.
DAY = 'yesterday'
PERIOD_START = datetime.strptime('2021-11-24', '%Y-%m-%d').date()
PERIOD_END = datetime.strptime('2021-12-05', '%Y-%m-%d').date()

logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s'
)


def main():
    logging.debug('Приложение запущенно')
    try:
        correct_days = []
        if PERIOD_START and PERIOD_END:
            logging.debug('Инициализация работы с периодом')
            one_day = PERIOD_START
            while one_day <= PERIOD_END:
                correct_days.append(one_day)
                one_day += timedelta(days=1)
        else:
            correct_days.append(get_dates())
        for correct_day in correct_days:
            os.mkdir(str(correct_day))
            data_db = getting_all_data_of_db_table()
            data_day = choosing_one_day(data_db, correct_day)
            for line in data_day:
                seance, phone = line.replace('\n', '').split(', ')
                connection = get_connection_by_seance(seance)
                # todo
                # описать, зачем берём connection[1]
                if len(connection) == 2:
                    title = f'{correct_day}/{phone}.wav'
                    get_recorded_file_by_connection(connection[1], title)
    except Exception as e:
        message = f'Неразрешимая ошибка: {e}'
        logging.error(message)


def get_dates():
    logging.debug('Формирование словаря дат')
    date_format = '%Y-%m-%d'
    today = datetime.now()
    yesterday = today + timedelta(days=-1)
    dates_list = {'today': today.strftime(date_format),
                  'yesterday': yesterday.strftime(date_format)}
    return dates_list[DAY]


def getting_all_data_of_db_table():
    """
    Получение информации из БД Infinity.
    Проверяем определённую таблицу, заданную в параметрах.
    """
    logging.debug('Попытка получить список звонков за день')
    try:
        params = {
            'ProviderName': PROVIDER
        }
        data_db = requests.get(
            DATA_URL.format(host=HOST,
                            port=PORT,
                            data_method='getdata'),
            params=params
        )
        logging.debug('Данные таблицы БД получены')
        return data_db.json()['result']['Data']
    except ConnectionError as e:
        message = f'Не удалось получить данные из БД. {e}'
        logging.error(message)


def choosing_one_day(data_db, correct_day):
    try:
        data_day = []
        logging.debug(f'{correct_day} \n ---------')
        for i in data_db:
            date_control = datetime.strptime(i['ts'],
                                             '%d.%m.%Y %H:%M:%S').date()
            if str(date_control) == str(correct_day) and i['seans'] != 'null':
                element = f"{i['seans']}, {i['respondent']}_{i['ID']}"
                data_day.append(element)
        return data_day
    except KeyError as e:
        message = f'Не удалось сделать выборку данных за день. {e}'
        logging.error(message)


def get_connection_by_seance(seance):
    """
    Получение connection по известному seance.
    На выходе — (int) connection id.
    """
    logging.debug(f'Попытка получить connection для {seance}')
    try:
        params = {
            'IDSeance': seance,
            'Recorded': 1
        }
        connection = requests.get(
            STAT_URL.format(host=HOST,
                            port=PORT,
                            stat_method='connectionsbyseance'),
            params=params
        )
        logging.debug(f'Connection для {seance} получен')
        return connection.json()['result']['Connections']
    except ConnectionError as e:
        message = f'Не удалось получить connection для seance={seance}. {e}'
        logging.error(message)


def get_recorded_file_by_connection(connection, title):
    """
    Скачивание файла, переименовывание его.
    Формат нового имени: phoneNumber_code.
    Code — случайная комбинация букв и цифр,
    нужен для корректной обработки дублирующихся телефонов.
    """
    logging.debug(f'Попытка скачать файл {connection}')
    try:
        params = {
            'IDConnection': connection
        }
        sound = requests.post(
            STAT_URL.format(host=HOST,
                            port=PORT,
                            stat_method='getrecordedfile'),
            params=params,
            stream=True
        )
        with open(title, 'wb') as audio_file:
            for chunk in sound.iter_content(chunk_size=128):
                audio_file.write(chunk)
        logging.debug(f'{title} успешно сохранён')
    except ConnectionError as e:
        message = f'Не удалось скачать {connection}. {e}'
        logging.error(message)


if __name__ == '__main__':
    main()
