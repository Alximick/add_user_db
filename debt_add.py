#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
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
    # print(lst)

def parser_debt(filename, lst_debt_type):
    from debt.models import DebtType, Debt
    read_book = xlrd.open_workbook(filename, on_demand=True)
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
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()
    # debt_type = parser_debt_type(sys.argv[1])
    files = os.listdir(os.getcwd())
    my_xlsx = filter(lambda x: x.endswith('.xlsx'), files)
    with open('data.json', mode='w',  encoding='utf-8') as data_file:
        for file in my_xlsx:
            lst = parser_debt_type(file)
            js = json.dumps(lst, ensure_ascii=False, indent=4)
            data_file.write(js)
    #         print(json.loads(js))
        # parser_debt(file, lst)

    #
    # data = []
    # with codecs.open('data.json', encoding='utf-8') as f:
    #     for line in f:
    #         # print(line)
    #         data.append(json.loads(line, 'utf-8'))
    # print(data)


    with open('data.json', 'r', encoding='utf-8') as data_file:
        lst = json.load(data_file)
        print(lst)
        # lst = []
        # for line in data_file:
        #     lst.append(json.loads(line))
        # print(lst)
        # pass
        # print(data_file)
        # result = data_file.read()
        # data = json.loads(data_file)
        # print(data)
        # for file in my_xlsx:
            # parser_debt(file, data)
