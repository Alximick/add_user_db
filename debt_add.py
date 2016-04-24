#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from itertools import count

import re
import xlrd
import django

def parser_debt_type(filename):
    lots = {}
    read_book = xlrd.open_workbook(filename, on_demand=True,
                                   encoding_override="utf-8")
    sheet = read_book.sheet_by_index(0)
    mounths = ('Янв', 'Фев', 'Мар', 'Апр', 'Ма', 'Июн','Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек' , '15')
    debt_type = ('Эл/Эн', 'Штраф', '15')
    for row in sheet.row_values(0):
        if type(row) == str and len(row) > 0:
            for mounth in mounths:
                if re.search(mounth.lower(), row.lower()):
                    for debt_t in debt_type:
                        if re.search(debt_t.lower(), row.lower()):
                            print('mounth', mounth, 'за что ', debt_t, ' = ', row)
        # if type(row) == float:
        #     print('float', row)

    return  lots

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
