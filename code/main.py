
from parsing_funcs import *

create_diretories()

type_parsing = int(input(
    "Выберите тип парсинга pkk.rosreestr.ru\n 1 - Проверить количество\n 2 - Округа\n 3 - Районы \n 4 - Кварталы \n Введите цифру: "))

try:
    type_parsing = int(type_parsing)
except ValueError:
    print("Введите цифру от 1 до 4")
    exit()
############################################################################
# Проверка количества
if type_parsing == 1:
    type_check = int(input(
        "Выберите, количество чего проверить\n 1 - Проверить количество округов\n 2 - Проверить количество районов\n 3 - Проверить количество кварталов\n Введите цифру: "))
    if type_check == 1:
        print(check_amount_okgurs(), ' округов в БД')
    if type_check == 2:
        check_amount_raoyns()
    if type_check == 3:
        print("Это еще не сделано")

############################################################################
# Парсер округов
if type_parsing == 2:
    for index in range(1, 92):
        parsing_okrugs(index)

############################################################################
# Парсер районов
if type_parsing == 3:

    for index in range(1, 92):
        parsing_rayons(index, 0)
        # Если > 40, то нужно еще выгрузить следующую страницу.
        # По идее, можно и так оставить
        parsing_rayons(index, 40)


############################################################################
# Парсер кварталов: тут сложнее ситуация
# Можно парсить через запрос, например, https://pkk.rosreestr.ru/api/features/2?_=1653414272971&text=21:01:*&limit=40&skip=40
# А можно перебором, что гораздо лучше, ибо в предыдущем запросе максимум skip == 210. Дальше сервер просто оборвет соединение
if type_parsing == 4:
    type_parse_kvartals = int(input(
        "Что будем делать с кварталами?\n 1 - Выкачать перебором json-файлы \n 2 - Объединить из json-файла в 1 список и пройтись по списку и выгрузить в БД\n Введите цифру: "))
    if type_parse_kvartals == 1:
        search_kvartals()
    if type_parse_kvartals == 2:
        start_parse_kvartals_search_files()
        list_kvartals = get_list_with_kvartals()
        for elem in parsing_kvartal_full:
            parsing_kvartal_full(elem)
