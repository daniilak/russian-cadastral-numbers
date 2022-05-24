
from config import FILES_FOLDER, PKK_HEADER, LIST_PROXY
import asyncio
import requests
import json
import time
from secrets import choice
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_diretories():
    if not os.path.exists(FILES_FOLDER + 'search'):
        os.makedirs(FILES_FOLDER + + 'search')
    if not os.path.exists(FILES_FOLDER + 'search/0'):
        os.makedirs(FILES_FOLDER + + 'search/0')
    for item in ['okrugs', 'rayons', 'kvartals']:
        if not os.path.exists(FILES_FOLDER + item):
            os.makedirs(FILES_FOLDER + item)
        for index in range(1, 92):
            if not os.path.exists(FILES_FOLDER + item +'/'+str(index)):
                os.makedirs(FILES_FOLDER + item +'/'+str(index))
    

def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    return wrapped


def getRandomProxy() -> dict:
    '''
        Возврат словаря со случайным прокси
    '''
    return {"https": "https://" + choice(LIST_PROXY)}


def check_cache_isset(type_folder: str, index: int, name: str) -> bool:
    '''
        Проверка, создан ли такой файл.
        Создан - True. Не создан - False
    '''
    try:
        filename = FILES_FOLDER + str(type_folder)+'/'+str(index) + '/'+str(name)+'.json'
        f = open(filename, 'r', encoding='utf-8')
        f.close()
    except FileNotFoundError:
        return False
    return True


def save_cache(type_folder: str, index: int, name: str, data) -> bool:
    '''
        Сохранение json-данных как json-файла, который используется как кэш для дальнейшего скраппинга.
    '''
    filename = FILES_FOLDER + str(type_folder)+'/'+str(index) + '/'+str(name)+'.json'
    with open(filename, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(data))
    return True


def get_from_cache(type_folder: str, index: int, name: str):
    '''
        Чтение json-данных из имеющегося json-файла, который используется как кэш для дальнейшего скраппинга.
    '''
    filename = FILES_FOLDER + str(type_folder)+'/'+str(index) + '/'+str(name)+'.json'
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    return data


def whiler_requester(url: str):
    '''
        Выполнение запроса
    '''
    is_ok = True
    while is_ok:
        try:
            res = requests.get(url, headers=PKK_HEADER,
                               verify=False, proxies=getRandomProxy(), timeout=10)
            is_ok = False
        except Exception as e:
            print('Err', url, str(e))
            is_ok = True
    return res


def get_time() -> str:
    '''
        Возвращает количество микросекунд, необходимое для запроса на сайт
    '''
    return str(int(time.time()*1000))

def parse_kvartals_search_files(filename:str):
    '''
        Парсинг файла
    '''
    kvartals = []
    with open(FILES_FOLDER + 'search/0/'+filename, 'r') as f:
        data = f.read()

    df = json.loads(data)

    if len(df['results']) == 0:
        return []

    for el in df['results']:
        kvartals.append(el['title'])

    return kvartals

def start_parse_kvartals_search_files():
    '''
        Проходим по всем скачанным файлам при помощи функции search_kvartals и вытаскиваем весь список кварталов в файл
    '''
    kvartals_search_files = [f for f in os.listdir(FILES_FOLDER + 'search/0/') if os.path.isfile(os.path.join(FILES_FOLDER + 'search/0/', f))]

    full_list_kvartals = []
    for filename in kvartals_search_files:
        full_list_kvartals =  full_list_kvartals + parse_kvartals_search_files(filename)
    
    full_list_kvartals = list(set(full_list_kvartals))

    with open(FILES_FOLDER + 'full_list_kvartals.json','w+') as f:
        f.write(json.dumps(full_list_kvartals))


def get_list_with_kvartals()->list:
    '''
        Считать файл full_list_kvartals.json
    '''
    
    with open(FILES_FOLDER + 'full_list_kvartals.json','r') as f:
        full_list_kvartals = json.loads(f.read())
    return full_list_kvartals