import csv
import re
from prettytable import PrettyTable

name_file = input()
number = input()
name_headlines = input()


dic = ['№', 'Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия', 'Компания',
            'Оклад', 'Название региона', 'Дата публикации вакансии']

dic2 = {'FALSE': 'Нет', 'False': 'Нет', 'TRUE': 'Да', 'True': 'Да',
       'noExperience': 'Нет опыта', 'between1And3': 'От 1 года до 3 лет',
       'between3And6': 'От 3 до 6 лет', 'moreThan6': 'Более 6 лет',
        'AZN': 'Манаты', 'BYR': 'Белорусские рубли', 'EUR': 'Евро',
        'GEL': 'Грузинский лари', 'KGS': 'Киргизский сом',
        'KZT': 'Тенге', 'RUR': 'Рубли', 'UAH': 'Гривны', 'USD': 'Доллары',
        '"UZS': 'Узбекский сум'}


def csv_reader(file_name):
    reader = []
    with open(file_name, encoding="utf-8-sig") as file:
        read_file = csv.reader(file)
        for i in read_file:
            reader.append(i)
        if len(reader) == 0:
            return [{}], [{}]
        list_naming = reader.pop(0)
    return list_naming, reader


list_name, list_mean = csv_reader(name_file)


def csv_filter(reader, dic_bool):
    for lists in reader:
        for index, item in enumerate(lists):
            if dic_bool.get(item):
                lists[index] = dic_bool.get(item)
    return reader


list_reader = csv_filter(list_mean, dic2)


def print_vacancies(list_naming, reader):
    if len(list_naming) <= 1 or len(reader) <= 1:
        if len(list_naming) == 0 or len(reader) == 0:
            print('Нет данных')
            return
        if len(list_naming[0]) == 0 or len(reader[0]) == 0:
            print('Пустой файл')
            return
    up_border = 0
    low_border = 0
    result_dict_vacancies = {}
    nalog = ''
    name = ''
    description = ''
    skill = ''
    time_work = ''
    premiym = ''
    compamy = ''
    oklad = ''
    region = ''
    data = ''
    num = 0
    mytable = PrettyTable(border=True, header=True, hrules=1, align="l", field_names=dic)
    mytable._max_width = {val: 20 for val in dic}
    for i in reader:
        if len(list_naming) == len(i) and all(i):
            dict_vacancies = zip(list_naming, i)
            for header, body in dict_vacancies:
                a = re.sub(r'<[^<>]+>', '', body)
                a = re.sub(r'\n', ', ', a)
                a = str.strip(re.sub(r'\s+', ' ', a))
                result_dict_vacancies[header] = a
                if header == 'name':
                    name = a
                if header == 'description':
                    if len(a) > 100:
                        description = f'{a[:100]}...'
                if header == 'key_skills':
                    z = a.replace('\\n', '\n').replace(', ', '\n')
                    if len(z) > 100:
                        skill = f'{z[:100]}...'
                    else: skill = z
                if header == 'experience_id':
                    time_work = a
                if header == 'premium':
                    premiym = a
                if header == 'employer_name':
                    compamy = a
                if header == 'salary_gross':
                    if a == 'Нет':
                        nalog = 'С вычетом налогов'
                    else:
                        nalog = 'Без вычета налогов'
                if header == 'salary_from':
                    low_border = '{0:,}'.format(round(float(a))).replace(',', ' ')
                if header == 'salary_to':
                    up_border = '{0:,}'.format(round(float(a))).replace(',', ' ')
                if header == 'salary_currency':
                    value_valuta = a
                    value = f'{low_border} - {up_border} ({value_valuta}) ({nalog})'
                    oklad = value
                if header == 'area_name':
                    region = a
                if header == 'published_at':
                    str1 = a
                    str2 = str1[:10]
                    day = str2[8:10]
                    month = str2[5:7]
                    year = str2[:4]
                    value_data = f'{day}.{month}.{year}'
                    a = value_data
                    data = a
            num += 1
            list_for_table = [str(num), name, description, skill, time_work, premiym, compamy, oklad, region, data]
            mytable.add_row(list_for_table)
    if not name_headlines:
        list_name_headlines = dic
    else:
        list_name_headlines = name_headlines.split(', ')
        list_name_headlines.insert(0, '№')
    if not number:
        num1 = 0
        num2 = num
    else:
        number_list = number.split(' ')
        if len(number_list) == 1:
            num1 = int(number_list[0]) - 1
            num2 = num
        else:
            num1 = int(number_list[0]) - 1
            num2 = int(number_list[1]) - 1
    table = mytable.get_string(fields=list_name_headlines, start=num1, end=num2)
    print(table)


print_vacancies(list_name, list_reader)