from datetime import datetime as dt
from time import time

def start():

    time = dt.now().strftime('%d-%b-%y %H:%M:%S')
    with open('logger.txt', 'a', encoding='utf-8') as file:
        file.write(time + ' импортировали справочник' + '\n')
        
