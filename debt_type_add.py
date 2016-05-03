#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import xlrd
import django


DEBT_TYPE_DCT = {'ком.': 'community', 'охрана': 'guard',
                 'снег': 'snow', 'Эл/Эн': 'power', 'Штраф': 'fine',
                 'None': 'None', 'Штраф эл/эн': 'fine_power'}


DEBT_TYPE = ('Штраф', 'Штраф эл/эн','Эл/Эн', 'ком.',
             'охрана', 'э/энергия', 'снег')


MONTH_ALL = ('Янв', 'Фев', 'Мар', 'Апр', 'Ма', 'Июн',
             'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек')


DCT_MONTH = {'Янв': 1, 'Фев': 2, 'Мар': 3, 'Апр': 4, 'Ма': 5,
             'Июн': 6, 'Июл': 7, 'Авг': 8, 'Сен': 9, 'Окт': 10,
             'Ноя': 11, 'Дек': 12, 'None': None}


def create_debt_type(name_type, slug_type):
    from debt.models import DebtType
    obj, created = DebtType.objects.get_or_create(name=name_type, slug=slug_type)
    # print(obj, created)


def parser_debt_type(filename):

    read_book = xlrd.open_workbook(filename, on_demand=True)
    sheet = read_book.sheet_by_index(0)
    first_row = sheet.row_values(0)
    create_debt_type('Заезды', 'races')
    year = re.search(r'\d+', filename.lower()).group()
    lst = [filename,]

    for index in range(len(first_row)):
        if type(first_row[index]) == str:
            month_column = 'None'
            for month in MONTH_ALL:
                if re.search(month.lower(), first_row[index].lower()):
                    month_column = month
            for debt_t in DEBT_TYPE:
                if re.search(debt_t.lower(), first_row[index].lower()):
                    if 'э/энергия' == debt_t:
                        debt_t = 'Эл/Эн'
                    index, type_debt = index, DEBT_TYPE_DCT[debt_t]
                    year, month = int(year), DCT_MONTH[month_column]
                    create_debt_type(debt_t, type_debt)
                    lst.append((index, type_debt, year, month))
                    break
        elif type(first_row[index]) == float and first_row[index] > 2:
            year, month, *tail = xlrd.xldate_as_tuple(first_row[index], 0)
            index, type_debt, year, month = index, DEBT_TYPE_DCT['ком.'], year, month
            create_debt_type('ком.', type_debt)
            lst.append((index, type_debt, year, month))

    return lst


if __name__ == '__main__':
    import json
    import io

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()
    files = os.listdir(os.getcwd())
    my_xlsx = filter(lambda x: x.endswith('.xlsx'), files)

    for file in my_xlsx:
        lst = parser_debt_type(file)
        with io.open(file[:-5] +'.json', 'w', encoding='utf-8') as file_json:
            json.dump(lst, file_json, ensure_ascii=False)
