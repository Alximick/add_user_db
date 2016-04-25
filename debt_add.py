#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

import re
import xlrd
import django


CONFIG = {'ком.': 'community', 'охрана': 'guard',
          'э/энергия': 'power1', 'снег': 'snow',
          'Эл/Эн': 'power', 'Штраф': 'fine',
          'None': 'None'
          }

DEBT_TYPE = ('Эл/Эн', 'Штраф', 'ком.', 'охрана', 'э/энергия', 'снег')


MOUNTHS = ('Янв', 'Фев', 'Мар', 'Апр', 'Ма', 'Июн',
           'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек')


DCT_MOUNTHS = {'Янв': 1, 'Фев': 2, 'Мар': 3, 'Апр': 4, 'Ма': 5, 'Июн': 6,
               'Июл': 7, 'Авг': 8, 'Сен': 9, 'Окт': 10, 'Ноя': 11, 'Дек': 12}


def create_debt_type(name_type, slug_type):

    from debt.models import DebtType, Debt
    from loginsys.admin import MyUser
    # print(name_type, slug_type)
    obj, created = DebtType.objects.get_or_create(name=name_type, slug=slug_type)
    # print(obj, created)


def create_debt(user, debt_type, years, month, amount):
    username = None
    from debt.models import DebtType, Debt
    from loginsys.admin import MyUser
    if type(user) == float:
        username = MyUser.objects.get(username=int(user))
    elif type(user) == str:
        username = MyUser.objects.get(username=user)
    else:
        import ipdb; ipdb.set_trace()
    obj, created = Debt.objects.get_or_create(
        type=DebtType.objects.get(slug=debt_type),
        year=years,
        user=username,
        month=month,
        amount=amount,
    )
    # print(obj, created)

def parser_debt_type(filename):
    read_book = xlrd.open_workbook(filename, on_demand=True,
                                   encoding_override="utf-8")
    sheet = read_book.sheet_by_index(0)
    dct = {}
    YEAR = None
    first_row = sheet.row_values(0)
    if not first_row[0]:
        print('Введите год в первую ячейку')
        print('На пример 2014')
        exit(1)
    try:
        YEAR = int(first_row[0])
    except:
        print('некорректно введен год')
        print('Введите год в первую ячейку')
        print('На пример 2014')
        exit(1)

    print(YEAR)
    for rownum in range(sheet.nrows):
        if rownum == 0:
            continue
        row = sheet.row_values(rownum)
        for index in range(len(first_row)):
            if type(first_row[index]) == str and len(first_row[index]) > 0 and row[0] and row[index]:
                for mounth in MOUNTHS:
                    if re.search(mounth.lower(), first_row[index].lower()):
                        for debt_t in DEBT_TYPE:
                            if re.search(debt_t.lower(), first_row[index].lower()):
                                dct[index] = debt_t
                                create_debt_type(debt_t, CONFIG[debt_t])
                                create_debt(row[0], CONFIG[debt_t], YEAR, DCT_MOUNTHS[mounth],
                                            row[index])
                                # print(row[0], debt_t, 'Год', DCT_MOUNTHS[mounth], row[index])
                if row[0] and row[index]:
                    for debt_t in DEBT_TYPE:
                        if re.search(debt_t.lower(), first_row[index].lower()):
                            # print(row[0], debt_t, 'Год', 'месяц', row[index])
                            dct[index] = debt_t
                            create_debt_type(debt_t, CONFIG[debt_t])
                            create_debt(row[0], CONFIG[debt_t], YEAR, None, row[index])
            elif type(first_row[index]) == float and index > 0  and row[0] and row[index]:
                year, month, *tail = xlrd.xldate_as_tuple(first_row[index], 0)
                dct[index] = 'None'
                # print(row[0], 'None', year, month, row[index])
                create_debt_type('None', 'None')
                create_debt(row[0], 'None', year, month, row[index])
    print(len(first_row))
    if first_row[-1] == 'Итого':
        print(first_row)
    print(dct)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: ./create_users.py file')
        sys.exit(1)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()
    debt_type = parser_debt_type(sys.argv[1])


# def test():
#     print(int(first_row[0]))
#     years = re.match(r'\d+', first_row[0])
#
#     for i in first_row[1:]:
#         if i == 'Итого' or i == '':
#             continue
#         if type(i) == str:
#             print(i)
#         if type(i) == float:
#             year, month, *tail = xlrd.xldate_as_tuple(i, 0)
#             print('None', year, month)
#
#     # Create DebtType
#     for index in range(len(first_row)):
#         if first_row[index] in CONFIG:
#             dct[index] = CONFIG[first_row[index]]
#     obj, created = DebtType.objects.get_or_create(name=first_row[index],
#                                                   slug=CONFIG[first_row[index]])
#
#     print(obj, created)
#
#
#     # Create Debt
#     for rownum in range(sheet.nrows):
#         row = sheet.row_values(rownum)
#         for index in range(len(row)):
#             if index in dct and row[index] and row[0] and type(row[index]) == float:
#                 # username = None
#                 if type(row[0]) == float:
#                     username = MyUser.objects.get(username=int(row[0]))
#                 elif type(row[0]) == str:
#                     username = MyUser.objects.get(username=row[0])
#                 else:
#                     import ipdb; ipdb.set_trace()
#                 obj, created = Debt.objects.get_or_create(
#                     type=DebtType.objects.get(slug=CONFIG[first_row[index]]),
#                     year=int(years.group()),
#                     user=username,
#                     month=None,
#                     amount=row[index],
#                 )
#                 print(obj, created)
#
#     for rownum in range(sheet.nrows):
#         row = sheet.row_values(rownum)
#         for index in range(len(row)):
#             if row[index]:
#                 print(row[index], end='')
#         print()
