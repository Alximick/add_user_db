#!/usr/bin/env python
# -*- coding: utf-8 -*-



if __name__ == '__main__':
    import os
    import django

    sum_files = {
        '2014_15.марта.2016.xlsx': '295906.00',
        '2015_15.марта.2016.xlsx': '544209.40',
        '2016_15.марта.2016.xlsx': '410943.00',
        'Roads_15.марта.2016.xlsx': '21500.00'
    }

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()

    files = os.listdir(os.getcwd())
    my_json = filter(lambda x: x.endswith('.xlsx'), files)
    from debt.models import Debt
    for file in my_json:
        print(file)
        sum_db = sum([item.amount for item in Debt.objects.filter(imported_from=file)])
        if str(sum_db) == sum_files[file]:
            print('Good')
        else:
            print(sum_db, ' != ', sum_files[file])
