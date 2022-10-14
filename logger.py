from datetime import datetime as dt
import logging
from time import time

def num_create_file(Phone_Book):

    time = dt.now().strftime('%d-%b-%y %H:%M:%S')
    with open('logger.txt', 'a', encoding='utf-8') as file:
        file.write(time + '\n')
        file.write('\n' + f'{Phone_Book} = добавили контакт' + '\n')

def data_create_file(Phone_Book):

    time = dt.now().strftime('%d-%b-%y %H:%M:%S')
    with open('logger.txt', 'a', encoding='utf-8') as file:
        file.write(time + '\n')
        file.write('\n' + f'{Phone_Book} = добавили контакт' + '\n')
        
def data_del_contact(search_contact_list):

    time = dt.now().strftime('%d-%b-%y %H:%M:%S')
    with open('logger.txt', 'a', encoding='utf-8') as file:
        file.write(time + '\n')
        file.write('\n' + f'{search_contact_list} = контакт удалён' + '\n')

def data_search_contact_name(search_contact_list):

    time = dt.now().strftime('%d-%b-%y %H:%M:%S')
    with open('logger.txt', 'a', encoding='utf-8') as file:
        file.write(time + '\n')
        file.write('\n' + f'{search_contact_list} = найден контакт' + '\n')

def data_clear_oll():

    time = dt.now().strftime('%d-%b-%y %H:%M:%S')
    with open('logger.txt', 'a', encoding='utf-8') as file:
        file.write(time + ' список контактов очищен' + '\n')

def data_num(text):

    time = dt.now().strftime('%d-%b-%y %H:%M:%S')
    with open('logger.txt', 'a', encoding='utf-8') as file:
        file.write(time + text + '\n')       

def data_name(text):
    time = dt.now().strftime('%d-%b-%y %H:%M:%S')
    with open('logger.txt', 'a', encoding='utf-8') as file:
        file.write(time + text + '\n')

def data_exit():
    time = dt.now().strftime('%d-%b-%y %H:%M:%S')
    with open('logger.txt', 'a', encoding='utf-8') as file:
        file.write(time + " ->Работа окончена" + '\n')

def data_export():
    time = dt.now().strftime('%d-%b-%y %H:%M:%S')
    with open('logger.txt', 'a', encoding='utf-8') as file:
        file.write(time + " ->Экспорт в csv завершен успешно" + '\n')

def data_import():
    time = dt.now().strftime('%d-%b-%y %H:%M:%S')
    with open('logger.txt', 'a', encoding='utf-8') as file:
        file.write(time + " ->Импорт данных из csv завершен успешно" + '\n')        
