#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xlrd
import django


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


def sum_list(lst):
    sum_lst = 0
    for element in lst:
        if element:
            sum_lst += element
    return sum_lst


def parser_debt(lst_debt_type):
    read_book = xlrd.open_workbook(lst_debt_type[0], on_demand=True)
    print(lst_debt_type[0])
    sheet = read_book.sheet_by_index(0)
    sum_all, sum_lot = 0, 0
    for rownum in range(1, sheet.nrows):
        row = sheet.row_values(rownum)
        if row[0] and type(row[0]) == float:
            # print(row[0], row[1: len(lst_debt_type)])
            sum_all += sum_list(row[1: len(lst_debt_type)])
        for index in range(1, len(row)):
            if row[index] and row[0] and type(row[index]) == float:
                for value in lst_debt_type[1:]:
                    if value[0] == index:
                        user = row[0]
                        debt_type, years, month = value[1:]
                        amount = row[index]
                        # print(user, debt_type, years, month, amount)
                        create_debt(user, debt_type, years, month, amount)
                        sum_lot += amount
    print('Sum exel file', sum_all)
    print('Sum in db', sum_lot)


if __name__ == '__main__':
    import json

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()

    files = os.listdir(os.getcwd())
    my_json = filter(lambda x: x.endswith('.json'), files)

    for file in my_json:
        with open(file, 'r') as file_json:
            lst = json.load(file_json)
            parser_debt(lst)