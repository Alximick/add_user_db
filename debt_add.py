#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from itertools import count

import re
import xlrd, xlwt
import django

CONFIG = {'ком.': 'community', 'охрана': 'guard',
          'э/энергия': 'power', 'снег': 'snow',}


def parser_debt_type(filename):
    # lots = parser_lot(filename)
    read_book = xlrd.open_workbook(filename, on_demand=True,
                                   encoding_override="utf-8")
    sheet = read_book.sheet_by_index(0)
    dct = {}
    first_row = sheet.row_values(0)
    for index in range(len(first_row)):
        if first_row[index] in CONFIG:
            dct[index] = CONFIG[first_row[index]]
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        for index in range(len(row)):
            if index in dct and row[index] and row[0] \
                    and type(row[index]) == float:
                print(int(row[0]), first_row[index],
                      '(',dct[index], ') = ',row[index])

    # mounths = ('Янв', 'Фев', 'Мар', 'Апр', 'Ма', 'Июн','Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек' , '15')
    # debt_type = ('Эл/Эн', 'Штраф', '15')
    # for row in sheet.row_values(0):
    #     if type(row) == str and len(row) > 0:
    #         for mounth in mounths:
    #             if re.search(mounth.lower(), row.lower()):
    #                 for debt_t in debt_type:
    #                     if re.search(debt_t.lower(), row.lower()):
    #                         print('mounth', mounth, 'за что ', debt_t, ' = ', row)
    #     # if type(row) == float:
    #     #     print('float', row)

    # return  lots

def add_debt_type(debt_type):
    '''Заготовок'''
    for type in debt_type:
        # user = MyUser.objects.create_user(
        #     username = lot,
        #     phone_number = '700000',
        #     password = 'qwerty123',
        # )
        print(type)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: ./create_users.py file')
        sys.exit(1)
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    # django.setup()
    debt_type = parser_debt_type(sys.argv[1])
    # add_user_db(sys.argv[1])
