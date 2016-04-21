# -*- coding: utf-8 -*-
import xlrd
import sys
from loginsys.admin import UserCreationForm


def parser_lot(filename):
    lots = []
    read_book = xlrd.open_workbook(filename, on_demand=True, encoding_override="utf-8")
    sheet = read_book.sheet_by_index(0)

    i = 1
    for rownum in range(sheet.nrows):
        try:
            lot = sheet.cell_value(i, 0)
            i += 1
            if int(lot):
                lots.append(int(lot))
        except:
            pass
    return lots


def add_user_db(filename):
    users = parser_lot(filename)
    error = 0

    for user in users:
        username = str(user)
        house_number = user
        password = 'qwerty' + str(user)
        try:
            form = UserCreationForm({
                'username': username,
                'house_number': house_number,
                'password1': password,
                'password2': password,
            })
            form.is_valid()
            comment = form.save()
            print('add user', comment.username)
        except Exception as E:
            error += 1
            print(E)
    return error


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print ('usage: ./create_users.py file')
        print(''' or 

./manager.py shell
»> from create_users import add_user_db
»> filename = '1.xlsx'
»> test = add_user_db(filename)

            ''')
        sys.exit(1)

    print(parser_lot(sys.argv[1]))
