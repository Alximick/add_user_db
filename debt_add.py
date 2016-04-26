#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import re
import xlrd
import django


DEBT_TYPE_DCT = {'ком.': 'community', 'охрана': 'guard',
          'э/энергия': 'power1', 'снег': 'snow',
          'Эл/Эн': 'power', 'Штраф': 'fine',
          'None': 'None'}


DEBT_TYPE = ('Эл/Эн', 'Штраф', 'ком.', 'охрана', 'э/энергия', 'снег')


MONTH_ALL = ('Янв', 'Фев', 'Мар', 'Апр', 'Ма', 'Июн',
         'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек')


DCT_MONTH = {'Янв': 1, 'Фев': 2, 'Мар': 3, 'Апр': 4, 'Ма': 5,
             'Июн': 6, 'Июл': 7, 'Авг': 8, 'Сен': 9, 'Окт': 10,
             'Ноя': 11, 'Дек': 12, 'None': None}


def parser_debt_type(filename):

    read_book = xlrd.open_workbook(filename, on_demand=True)
    sheet = read_book.sheet_by_index(0)
    first_row = sheet.row_values(0)

    print(filename)
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
                    # print(CONFIG[debt_t], year, DCT_MONTH[m])
                    index, type_debt, year, month = index, DEBT_TYPE_DCT[debt_t], year, DCT_MONTH[month_column]
                    lst.append((index, type_debt, year, month))
                    break
        elif type(first_row[index]) == float and first_row[index] > 2:
            year, month, *tail = xlrd.xldate_as_tuple(first_row[index], 0)
            # print('ком.', year, month)
            index, type_debt, year, month = index, DEBT_TYPE_DCT['ком.'], year, month
            lst.append((index, type_debt, year, month))

    print(lst)

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()
    # debt_type = parser_debt_type(sys.argv[1])
    files = os.listdir(os.getcwd())
    my_xlsx = filter(lambda x: x.endswith('.xlsx'), files)
    for file in my_xlsx:
        parser_debt_type(file)
