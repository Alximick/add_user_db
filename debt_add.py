#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

import re
import xlrd
import django

CONFIG = {'ком.': 'community', 'охрана': 'guard',
          'э/энергия': 'power', 'снег': 'snow'}


def parser_debt_type(filename):
    from debt.models import DebtType, Debt
    from loginsys.admin import MyUser
    read_book = xlrd.open_workbook(filename, on_demand=True,
                                   encoding_override="utf-8")
    sheet = read_book.sheet_by_index(0)
    dct = {}
    first_row = sheet.row_values(0)

    # Create DebtType
    for index in range(len(first_row)):
        if first_row[index] in CONFIG:
            dct[index] = CONFIG[first_row[index]]
            obj, created = DebtType.objects.get_or_create(name=first_row[index],
                                                          slung=CONFIG[first_row[index]])
            print(obj, created)
    years = re.match(r'\d+', first_row[0])

    # Create Debt
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        for index in range(len(row)):
            if index in dct and row[index] and row[0] and type(row[index]) == float:
                username = None
                try:
                    if type(row[0]) == float:
                        username = MyUser.objects.get(username=int(row[0]))
                    elif type(row[0]) == str:
                        username = MyUser.objects.get(username=row[0])
                    else:
                        import ipdb; ipdb.set_trace()
                except:
                    pass
                obj, created = Debt.objects.get_or_create(
                    type=DebtType.objects.get(slung=CONFIG[first_row[index]]),
                    year=int(years.group()),
                    user=username,
                    month=None,
                    amount=row[index],
                )
                print(obj, created)
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


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: ./create_users.py file')
        sys.exit(1)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()
    debt_type = parser_debt_type(sys.argv[1])
