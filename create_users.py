#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django
import xlrd
import sys
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()


def parser_lot(filename):
    lots = []
    read_book = xlrd.open_workbook(filename, on_demand=True,
                                   encoding_override="utf-8")
    sheet = read_book.sheet_by_index(0)

    i = 1
    for rownum in range(sheet.nrows):
        try:
            lot = sheet.cell_value(i, 0)
            i += 1
            if type(lot) == float:
                lots.append(int(lot))
            elif type(lot) == str:
                lots.append(str(lot))
        except:
            pass
    return lots


def add_user_db(filename):
    from loginsys.admin import UserCreationForm
    users = parser_lot(filename)
    error = 0

    for user in users:
        if not user:
            continue
        username = user
        phone_number = '700000'
        password = 'qwerty123'
        try:
            form = UserCreationForm({
                'username': username,
                'phone_number': phone_number,
                'password1': password,
                'password2': password,
            })
            form.is_valid()
            comment = form.save()
            print('add user', comment.username)
        except Exception as E:
            error += 1
            # print(user)
            # print(E)
    print('Error:', error)


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('usage: ./create_users.py file')
        sys.exit(1)
    django.setup()
    add_user_db(sys.argv[1])
