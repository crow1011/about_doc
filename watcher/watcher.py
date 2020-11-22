# -*- coding: utf-8 -*-
import os
import time
import yaml
import logging
import requests
import pandas as pd
from datetime import datetime


# забирает и парсит конфиг
def get_conf(conf_path='conf/conf.yaml'):
    with open(conf_path) as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    return conf


# возвращает уже настроенный логер
def get_logger(logger_conf):
    log_file = logger_conf['log_dir'] + logger_conf['log_file']
    logger = logging.getLogger(__name__)
    if not os.path.exists(logger_conf['log_dir']):
        os.makedirs(logger_conf['log_dir'])
    fh = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    log_level = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR
    }
    logger.setLevel(log_level[logger_conf['log_level']])
    return logger


# обращается за данными по юрлам из конфига
def get_data(users_url, todos_url):
    users_data = requests.get(users_url).json()
    todos_data = requests.get(todos_url).json()
    return users_data, todos_data


# обрезает строки больше указанного в конфиге размера
def cut_50(title, title_max_len):
    if len(title) > title_max_len:
        title = title[:title_max_len] + '...'
    return title


def create_df(users_data, todos_data, title_max_len):
    df_users = pd.DataFrame(users_data)
    df_todos = pd.DataFrame(todos_data)
    # удаляет полностью пустые эелементы
    # если all сменить на any будет удалять строки с одним и больше пустым элементом
    # в subset перечислены все столбцы кроме id, так как не бывает пустым и не дает использовать метод all
    df_users = df_users.dropna(how='all', subset=['name',
                                                  'username',
                                                  'email',
                                                  'address',
                                                  'phone',
                                                  'website',
                                                  'company'])
    # заменяет оставшиеся пустые значения(пуст один элемент или больше, но не все) на 0
    df_users = df_users.fillna(0)

    # удаляет полностью пустые элементы
    df_todos = df_todos.dropna(how='all', subset=['userId', 'title', 'completed'])
    # заменяет оставшиеся пустые значения на 0
    df_todos = df_todos.fillna(0)
    # обрезает длину значения title до указанного в параметре title_max_len
    df_todos['title'] = df_todos['title'].apply(cut_50, args=(title_max_len,))
    # возвращает два очищенных датафрейма
    # df_users хранит информацию о юзерах
    # df_todos хранит информацию о всех тасках
    return df_users, df_todos


def gen_report(user, df_todos):
    # запрашивает все таски конкретного пользователя из общего сприска тасков
    user_todo = df_todos[df_todos['userId'] == user['id']]
    # из списка тасков конкретного юзера составляет тектовые списки с завершенными и незавершенными
    # здесь логичее было использовать метод .to_list(), но у него баг с justify, невозможно сменить на left
    todo_completed = user_todo[user_todo['completed'] == True]['title'].to_list()
    todo_completed = '\n'.join(todo_completed)
    todo_uncompleted = user_todo[user_todo['completed'] == False]['title'].to_list()
    todo_uncompleted = '\n'.join(todo_uncompleted)
    # формирует дату у время, которые будут установлены рядом с email
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    # собирает по строкам репорт
    report = ''
    report += user['name'] + ' <' + user['email'] + '> ' + now + '\n'
    report += user['company']['name'] + '\n\n'
    report += 'Завершённые задачи:' + '\n'
    report += todo_completed
    report += '\n\n'
    report += 'Оставшиеся задачи:' + '\n'
    report += todo_uncompleted
    return report


def save_report(user, report, file_dir):
    # проверка на случай отсутвия директории для репортов
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    # формирует список существующих файлов
    exist_reports = os.listdir(file_dir)
    filename = f"{user['username']}.txt"
    # переименовывает существующий файл
    if filename in exist_reports:
        file_created_dt = time.ctime(os.path.getctime(file_dir + filename), )
        file_created_dt = datetime.strptime(file_created_dt, "%a %b %d %H:%M:%S %Y")
        file_created_dt = file_created_dt.strftime("%d-%m-%YT%H:%M")
        updated_file = file_dir + user['username'] + '_' + file_created_dt + '.txt'
        os.rename(file_dir + filename, updated_file)
    # сохраняет репорт
    with open(file_dir + filename, 'w') as f:
        f.write(report)
    # result создается для последующей записи в лог в main
    result = file_dir + filename
    return result


def main(conf):
    logger.debug('Configuration: ')
    logger.debug(conf)
    logger.debug('Get users and todos data')
    users_data, todos_data = get_data(conf['users_url'], conf['todos_url'])
    logger.debug(users_data)
    logger.debug(todos_data)
    logger.debug('Create users and todos DataFrames')
    df_users, df_todos = create_df(users_data, todos_data, conf['title_max_len'])
    logger.debug(f'Users shape: {df_users.shape}')
    logger.debug(f'Users columns: {df_users.columns}')
    logger.debug(f'Todos shape: {df_todos.shape}')
    logger.debug(f'Todos columns: {df_todos.columns}')
    results = []
    for row_id, user in df_users.iterrows():
        # при проблемном юзере ошибка по нему будет запсиана в лог и скрипт пойдет по остальным
        try:
            report = gen_report(user, df_todos)
            result = save_report(user, report, conf['file_dir'])
            results.append(result)
        except:
            logger.exception('Exception: ')

    logger.info('Created: ' + ', '.join(results))


if __name__ == '__main__':
    conf = get_conf()
    logger = get_logger(conf['logger'])
    logger.debug('DEBUG MODE')
    while True:
        # общая проверка, в случае непредвиденной ошибки она будет записана в лог
        try:
            main(conf)
        except:
            logger.exception('Exception: ')
        time.sleep(conf['query_interval'])