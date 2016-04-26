#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import sys
import os
import re
import xlrd
import django


DEBT_TYPE_DCT = {'ком.': 'community', 'охрана': 'guard',
                 'снег': 'snow', 'Эл/Эн': 'power', 'Штраф': 'fine',
                 'None': 'None', 'Штраф эл/эн': 'fine_power'}


DEBT_TYPE = ('Штраф', 'Штраф эл/эн','Эл/Эн', 'ком.', 'охрана', 'э/энергия', 'снег')


MONTH_ALL = ('Янв', 'Фев', 'Мар', 'Апр', 'Ма', 'Июн',
             'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек')


DCT_MONTH = {'Янв': 1, 'Фев': 2, 'Мар': 3, 'Апр': 4, 'Ма': 5,
             'Июн': 6, 'Июл': 7, 'Авг': 8, 'Сен': 9, 'Окт': 10,
             'Ноя': 11, 'Дек': 12, 'None': None}

def create_debt_type(name_type, slug_type):

    from debt.models import DebtType, Debt
    from loginsys.admin import MyUser
    # print(name_type, slug_type)
    obj, created = DebtType.objects.get_or_create(name=name_type, slug=slug_type)
    # print(obj, created)


def create_debt(user, debt_type, years, month, amount, test=False):
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
    # if test:print(obj.amount)
    if created == False:
        return obj.amount
    else:
        return 0

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
                    if 'э/энергия' == debt_t:
                        debt_t = 'Эл/Эн'
                    index, type_debt, year, month = index, DEBT_TYPE_DCT[debt_t], year, DCT_MONTH[month_column]
                    lst.append((index, type_debt, year, month))
                    create_debt_type(debt_t, type_debt)
                    break
        elif type(first_row[index]) == float and first_row[index] > 2:
            year, month, *tail = xlrd.xldate_as_tuple(first_row[index], 0)
            # print('ком.', year, month)
            index, type_debt, year, month = index, DEBT_TYPE_DCT['ком.'], year, month
            create_debt_type('ком.', type_debt)
            lst.append((index, type_debt, year, month))

    return lst

def parser_debt(lst_debt_type):
    from debt.models import DebtType, Debt
    read_book = xlrd.open_workbook(lst_debt_type[0], on_demand=True)
    sheet = read_book.sheet_by_index(0)
    sum = 0
    sum_lot = 0
    for rownum in range(sheet.nrows):
        if rownum == 0:
            continue
        row = sheet.row_values(rownum)
        for index in range(1, len(row)):
            if row[index] and row[0]:
                for value in lst_debt_type[1:]:
                    if value[0] == index:

                        user = row[0]
                        debt_type, years, month = value[1:]
                        amount = row[index]

                        create_debt(user, debt_type, years, month, amount)
                        # print(user, debt_type, years, month, amount, end='')
                        test = random.randint(1,len(range(sheet.nrows)))
                        if rownum == (test):
                            #random selection of cells:
                            #  выбирает случайную ячейку и смотрит была ли занесена в базу
                            #  тест выполняется случайное кол-во раз
                            #  под конец выводит результат сумм
                            # print(test)
                            sum += amount
                            sum_lot += create_debt(user, debt_type, years, month, amount, test=True)
        # print()
        # print(row)
    # print('Sum second_row', sum)
    # print('Sum in db', sum_lot)



if __name__ == '__main__':
    import json
    import io


    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()
    files = os.listdir(os.getcwd())
    my_xlsx = filter(lambda x: x.endswith('.xlsx'), files)

    for file in my_xlsx:
        lst = parser_debt_type(file)
        with io.open(file +'.json', 'w', encoding='utf-8') as file_json:
            json.dump(lst, file_json, ensure_ascii=False)

    my_json = filter(lambda x: x.endswith('.json'), files)
    for file in my_json:
        with open(file, 'r') as file_json:
            lst = json.load(file_json)
            parser_debt(lst)
