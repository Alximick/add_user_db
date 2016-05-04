#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xlrd
import django


def create_debt(user, debt_type, years, month, amount, filename, test=False):
    username = None
    from debt.models import DebtType, Debt
    from loginsys.admin import MyUser
    if type(user) == float:
        username = MyUser.objects.get(username=int(user))
    elif type(user) == str:
        username = MyUser.objects.get(username=user)
    else:
        import ipdb; ipdb.set_trace()
    obj, created = Debt.objects.update_or_create(
        type=DebtType.objects.get(slug=debt_type),
        year=years,
        user=username,
        month=month,
        amount=amount,
        imported_from=filename
    )
    # print(obj, created)


def parser_debt(lst_debt_type):
    read_book = xlrd.open_workbook(lst_debt_type[0], on_demand=True)
    print(lst_debt_type[0])
    sheet = read_book.sheet_by_index(0)
    for rownum in range(1, sheet.nrows):
        row = sheet.row_values(rownum)
        for index in range(1, len(row)):
            if row[index] and row[0] and type(row[index]) == float:
                for value in lst_debt_type[1:]:
                    if value[0] == index:
                        user = row[0]
                        debt_type, years, month = value[1:]
                        amount = row[index]
                        create_debt(user, debt_type, years, month, amount, lst_debt_type[0])


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
