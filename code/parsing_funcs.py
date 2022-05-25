from funcs import *
from models import fn, CadastralOkrug, CadastralRayon, CadastralKvartal


@background
def parsing_okrugs(index):
    '''
        Функция скачивания данных по округам РФ. Выкачивается в кеш и сразу в БД.
    '''
    if check_cache_isset('okrugs', index, index):
        df = get_from_cache('okrugs', index, index)
    else:
        url = 'https://pkk.rosreestr.ru/api/features/4/'+str(index)+'?date_format=%c&_=' + get_time()
        res = whiler_requester(url)
        df = res.json()
    
    # Выгружаем Json данные как файл
    save_cache('okrugs', index, index, df)

    elem = df['feature']
    
    center_x = None
    center_y = None
    if 'center' in elem and elem['center'] is not None:
        center_x = elem['center']['x']
        center_y = elem['center']['y']

    extent_ymin = None
    extent_ymax = None
    extent_xmin = None
    extent_xmax = None
    if 'extent' in elem and elem['extent'] is not None:
        extent_ymin = elem['extent']['ymin']
        extent_ymax = elem['extent']['ymax']
        extent_xmin = elem['extent']['xmin']
        extent_xmax = elem['extent']['xmax']

    stat_rayon_total = elem['stat']['rayon']['total']
    stat_rayon_geo = elem['stat']['rayon']['geo']

    stat_kvartal_total = elem['stat']['kvartal']['total']
    stat_kvartal_geo = elem['stat']['kvartal']['geo']

    stat_parcel_total = elem['stat']['parcel']['total']
    stat_parcel_geo = elem['stat']['parcel']['geo']

    stat_oks_total = elem['stat']['oks']['total']
    stat_oks_geo = elem['stat']['oks']['geo']

    item, is_created = CadastralOkrug.get_or_create(
        attrs_cn=elem['attrs']['cn'],
        attrs_id=elem['attrs']['id'],
        defaults={
            'sort': elem['sort'],
            'id_type': elem['type'],

            'center_x': center_x,
            'center_y': center_y,

            'extent_ymin': extent_ymin,
            'extent_ymax': extent_ymax,
            'extent_xmin': extent_xmin,
            'extent_xmax': extent_xmax,

            'stat_rayon_total':stat_rayon_total,
            'stat_rayon_geo':stat_rayon_geo,

            'stat_kvartal_total':stat_kvartal_total,
            'stat_kvartal_geo':stat_kvartal_geo,

            'stat_parcel_total':stat_parcel_total,
            'stat_parcel_geo':stat_parcel_geo,

            'stat_oks_total':stat_oks_total,
            'stat_oks_geo':stat_oks_geo,
        }
    )
    print('ok parsing_okrugs', item)


def check_amount_okgurs()->int:
    '''
        Возвращает количество округов в БД
    '''
    return CadastralOkrug.select(fn.Count(CadastralOkrug.id)).scalar()


def parsing_one_rayon_data(index, name_rayon):
    '''
        Получение информации о конкретном районе
    '''
    if check_cache_isset('rayons', index, name_rayon):
        df = get_from_cache('rayons', index, name_rayon)
    else:
        url = 'https://pkk.rosreestr.ru/api/features/3/' + name_rayon + '?date_format=%c&_=' + get_time()
        res = whiler_requester(url)
        df = res.json()
    return df

@background
def parsing_rayons(index, skip):
    '''
        Парсинг районов
    '''
    print(index)
    name_file = str(index)+'_'+str(skip)
    
    is_need_download = True
    
    if check_cache_isset('rayons', index, name_file):
        df = get_from_cache('rayons', index, name_file)
        is_need_download = False
        if len(df['features']) == 0:
            is_need_download = True
    
    if is_need_download:
        url = 'https://pkk.rosreestr.ru/api/features/3?_=' + get_time() + '&text='+str(index)+':*&limit=40&skip='+str(skip)
        res = whiler_requester(url)
        df = res.json()

    # Выгружаем Json данные как файл
    save_cache('rayons', index, name_file, df)
    
    if len(df['features']) == 0:
        return
    
    
    for elem in df['features']:

        center_x = None
        center_y = None
        if 'center' in elem and elem['center'] is not None:
            center_x = elem['center']['x']
            center_y = elem['center']['y']

        extent_ymin = None
        extent_ymax = None
        extent_xmin = None
        extent_xmax = None
        if 'extent' in elem and elem['extent'] is not None:
            extent_ymin = elem['extent']['ymin']
            extent_ymax = elem['extent']['ymax']
            extent_xmin = elem['extent']['xmin']
            extent_xmax = elem['extent']['xmax']

        # Дополнительная информация о районе
        info = parsing_one_rayon_data(index, elem['attrs']['id'])['feature']
        
        if not info:
            print('Произошла какая-то ошибка со parsing_rayons. <if not info> == ', index, url)

        stat_kvartal_total = info['stat']['kvartal']['total']
        stat_kvartal_geo = info['stat']['kvartal']['geo']

        stat_parcel_total = info['stat']['parcel']['total']
        stat_parcel_geo = info['stat']['parcel']['geo']

        stat_oks_total = info['stat']['oks']['total']
        stat_oks_geo = info['stat']['oks']['geo']

        item, is_created = CadastralRayon.get_or_create(
            attrs_cn = elem['attrs']['cn'],
            attrs_id = elem['attrs']['id'],
            defaults={
                'attrs_name': elem['attrs']['name'],
                'sort':elem['sort'],
                'id_type':elem['type'],

                'center_x': center_x,
                'center_y': center_y,

                'extent_ymin': extent_ymin,
                'extent_ymax': extent_ymax,
                'extent_xmin': extent_xmin,
                'extent_xmax': extent_xmax,

                'stat_kvartal_total':stat_kvartal_total,
                'stat_kvartal_geo':stat_kvartal_geo,

                'stat_parcel_total':stat_parcel_total,
                'stat_parcel_geo':stat_parcel_geo,

                'stat_oks_total':stat_oks_total,
                'stat_oks_geo':stat_oks_geo,
            }
        )
    print('ok parsing_rayons', index)


def identify_not_match_rayons_and_okrugs():
    '''
        Выводит список недостающего количества кадастровых районов, которых не хватает в таблице БД
    '''
    for okrug in CadastralOkrug.select(CadastralOkrug.attrs_cn, CadastralOkrug.stat_rayon_total).order_by(CadastralOkrug.id):
        okrug.attrs_cn
        okrug.stat_rayon_total
        amount = CadastralRayon.select(fn.Count(CadastralRayon.id)).where(CadastralRayon.attrs_cn.contains(okrug.attrs_cn + ':')).scalar()
        if int(amount) != int(okrug.stat_rayon_total):
            print('attrs_cn =', okrug.attrs_cn, 'total =', okrug.stat_rayon_total, 'amount in db =', amount)

def check_amount_raoyns():
    '''
        Сравнивает количество районов, указанных в таблице Округов, с количеством районов, которые находятся в таблице CadastralRayon.
    '''
    sum_rayons = CadastralOkrug.select(fn.Sum(CadastralOkrug.stat_rayon_total)).scalar()
    amount_rayons = CadastralRayon.select(fn.Count(CadastralRayon.id)).scalar()
    if sum_rayons != amount_rayons:
        print('Должно быть количество', sum_rayons, 'Однако, в таблице находится', amount_rayons)
        identify_not_match_rayons_and_okrugs()
    else:
        print('количество районов, указанных в таблице Округов, совпадает с количеством районов')





def request_download_get_count(name:str)->int:
    if check_cache_isset('search', 0, name.replace(':', '_')):
        df = get_from_cache('search', 0, name.replace(':', '_'))
    else:
        url = 'https://pkk.rosreestr.ru/api/typeahead/2?text=' + name.replace(':', '%3A') + '&_='+ get_time()
        res = whiler_requester(url)
        df = res.json()
    save_cache('search', 0, name.replace(':', '_'), df)
    
    if len(df['results']) == 0:
        return 0

    return len(df['results'])
                
@background
def search_kvartals(index:str):
    '''
        Поиск кварталов при помощи перебора. 
        Суть заключается в том, что у Публичной кадастровой карты при вводе номера не до конца, выходят подсказки. 
        Вот на этой логике основано это всё.
    '''
    for el in CadastralKvartal.select().where(CadastralKvartal.attrs_cn.contains(str(index)+':')).order_by(CadastralKvartal.id):
        attrs_cn = el.attrs_cn.split(':')

        search_field_main = attrs_cn[0] + ':' + attrs_cn[1]

        # Превращать это в цикл было бы неудобно, ибо внутрь каждого подцикла
        # нужно иногда добавлять условия
        for k0 in range(1,10):
            count_0 = request_download_get_count(search_field_main+':'+str(k0))
            if count_0 == 0 or count_0 < 20:
                continue
            for k1 in range(0,10):
                if k1 == 0 and k0 == 0:
                    continue
                print(search_field_main+':'+str(k0)+str(k1))
                count_1 = request_download_get_count(search_field_main+':'+str(k0)+str(k1))
                if count_1 == 0 or count_1 < 20:
                    continue
                for k2 in range(0,10):
                    if k1 == 0 and k0 == 0 and k2 == 0:
                        continue
                    count_2 = request_download_get_count(search_field_main+':'+str(k0)+str(k1)+str(k2))
                    if count_2 == 0 or count_2 < 20:
                        continue
                    for k3 in range(0,10):
                        if k1 == 0 and k0 == 0 and k2 == 0 and k3 == 0:
                            continue
                        count_3 = request_download_get_count(search_field_main+':'+str(k0)+str(k1)+str(k2)+str(k3))
                        if count_3 == 0 or count_3 < 20:
                            continue
                        for k4 in range(0,10):
                            if k1 == 0 and k0 == 0 and k2 == 0 and k3 == 0 and k4 == 0:
                                continue
                            count_4 = request_download_get_count(search_field_main+':'+str(k0)+str(k1)+str(k2)+str(k3)+str(k4))
                            if count_4 == 0 or count_4 < 20:
                                continue
                            for k5 in range(0,10):
                                count_5 = request_download_get_count(search_field_main+':'+str(k0)+str(k1)+str(k2)+str(k3)+str(k4)+str(k5))
                                if count_5 == 0:
                                    continue


@background
def parsing_kvartal_full(name):
    '''
        Парсинг кварталов
    '''
    url = 'https://pkk.rosreestr.ru/api/features/2/'+str(name)+'?date_format=%c&_=' + get_time()
    res = whiler_requester(url)
    
    df = res.json()

    if df['feature'] is None:
        return
    
    if len(df['feature']) == 0:
        return
    
    elem = df['feature']
    print(elem)
    
    center_x = None
    center_y = None
    if 'center' in elem:
        if elem['center'] is not None:
            center_x = elem['center']['x']
            center_y = elem['center']['y']
    
    extent_ymin = None
    extent_ymax = None
    extent_xmin = None
    extent_xmax = None
    
    if 'extent' in elem:
        if elem['extent'] is not None:
            extent_ymin = elem['extent']['ymin']
            extent_ymax = elem['extent']['ymax']
            extent_xmin = elem['extent']['xmin']
            extent_xmax = elem['extent']['xmax']
    
    attrs = elem['attrs']

    attrs_cn = attrs['cn'].replace('\n', ' ') if 'cn' in attrs else None
    attrs_id = attrs['id'].replace('\n', ' ') if 'id' in attrs else None
    
    field_sort = elem['sort'] if 'sort' in elem else None

    item, is_created = CadastralKvartal.get_or_create(
        attrs_cn = attrs_cn,
        attrs_id = attrs_id,
        defaults={
            'sort':field_sort,
            'id_type':elem['type'],

            'center_x': center_x,
            'center_y': center_y,

            'extent_ymin': extent_ymin,
            'extent_ymax': extent_ymax,
            'extent_xmin': extent_xmin,
            'extent_xmax': extent_xmax,

            'attrs_customer_phone': attrs['customer_phone'].replace('\n', ' ') if 'customer_phone' in attrs else None,
            'attrs_cad_eng_doc_date': attrs['cad_eng_doc_date'].replace('\n', ' ') if 'cad_eng_doc_date' in attrs else None,
            'attrs_customer_email': attrs['customer_email'].replace('\n', ' ') if 'customer_email' in attrs else None,
            'attrs_address': attrs['address'].replace('\n', ' ') if 'address' in attrs else None,
            'attrs_status_id': attrs['status_id'].replace('\n', ' ') if 'status_id' in attrs else None,
            'attrs_customer_address': attrs['customer_address'].replace('\n', ' ') if 'customer_address' in attrs else None,
            'attrs_status': attrs['status'].replace('\n', ' ') if 'status' in attrs else None,
            'attrs_date_begin': attrs['date_begin'].replace('\n', ' ') if 'date_begin' in attrs else None,
            'attrs_rayon_cn': attrs['rayon_cn'].replace('\n', ' ') if 'rayon_cn' in attrs else None,
            'attrs_contract_num': attrs['contract_num'].replace('\n', ' ') if 'contract_num' in attrs else None,
            'attrs_contract_date': attrs['contract_date'].replace('\n', ' ') if 'contract_date' in attrs else None,
            'attrs_date_end': attrs['date_end'].replace('\n', ' ') if 'date_end' in attrs else None,
            'attrs_cad_eng_email': attrs['cad_eng_email'].replace('\n', ' ') if 'cad_eng_email' in attrs else None,
            'attrs_info': attrs['info'].replace('\n', ' ') if 'info' in attrs else None,
            'attrs_cad_eng_phone': attrs['cad_eng_phone'].replace('\n', ' ') if 'cad_eng_phone' in attrs else None,
            'attrs_customer_name': attrs['customer_name'].replace('\n', ' ') if 'customer_name' in attrs else None,
            'attrs_contractor': attrs['contractor'].replace('\n', ' ') if 'contractor' in attrs else None,
            'attrs_kkr': attrs['kkr'].replace('\n', ' ') if 'kkr' in attrs else None,
            'attrs_cad_eng_doc_num ': attrs['cad_eng_doc_num'].replace('\n', ' ') if 'cad_eng_doc_num' in attrs else None,
            'attrs_cad_eng_organ': attrs['cad_eng_organ'].replace('\n', ' ') if 'cad_eng_organ' in attrs else None,
            'attrs_cad_eng_name': attrs['cad_eng_name'].replace('\n', ' ') if 'cad_eng_name' in attrs else None,
            'attrs_rayon': attrs['rayon'].replace('\n', ' ') if 'rayon' in attrs else None,
            'attrs_cad_eng_address': attrs['cad_eng_address'].replace('\n', ' ') if 'cad_eng_address' in attrs else None
        }
    )


# with open('/home/daniilak/pkk_files/full_list_kvartals.json','r') as f:
#     full_list_kvartals = json.loads(f.read())
# for el in full_list_kvartals:
#     parsing_kvartals(el)