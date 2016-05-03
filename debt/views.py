from django.shortcuts import render, redirect
from debt.models import Debt
from django.db.models import Sum, Count


def row_sum(sum, size):
    row = []
    for index in range(size):
        if index == 0:
            row.append('Sum')
        elif index == (size - 1):
            row.append('<font color="red" >' + str(sum) + '</font>')
        else:
            row.append('')
    return row


def my_all(debt, debt_type, years, sum):
    all_row = []
    url = redirect('mydebt')

    row = ['']
    for year in years:
        url_year = r'<a href="'+ url.url + str(year) + r'">' +  str(year) + r'</a>'
        row.append(url_year)
    all_row.append(row)

    for d_type in debt_type:
        row = []
        row.append(d_type)
        for year in years:
            not_found = True
            for item in debt:
                if item['year'] == year and item['type__name'] == d_type:
                    url_sum_year = r'<a href="' + url.url + str(year) + r'">' \
                                   + str(item['sum_year']) + r'</a>'
                    row.append(url_sum_year)
                    not_found = False
            if not_found:
                row.append('')
        all_row.append(row)

    all_row.append(row_sum(sum, len(all_row[0])))

    return all_row


def my_all_filter(debt, debt_type, sum):
    all_row = []

    row = []
    for item in debt:
        year, month = item.year, item.month
        row.append((month, year))
    row = sorted(set(row))
    row.insert(0, '')
    all_row.append(row)

    for d_type in debt_type:
        row = []
        row.append(d_type)

        for year_month in all_row[0]:
            not_found = True
            if not year_month:
                continue
            for item in debt:
                if item.year == year_month[1]\
                        and item.month == year_month[0]\
                        and item.type.name == d_type:
                    row.append(item.amount)
                    not_found = False
            if not_found:
                row.append('')
        all_row.append(row)

    all_row.append(row_sum(sum, len(all_row[0])))

    return all_row


def mydebt(request, year=None):
    args = {}

    if year:
        args['debt'] = Debt.objects.filter(user_id=request.user.id, year=year)\
            .select_related('type')
        args['debt_type'] = {item.type.name for item in args['debt']}
        args['sum'] = sum([item.amount for item in args['debt']])
        args['years'] = sorted({item.year for item in args['debt']})
        args['all'] = my_all_filter(args['debt'], args['debt_type'], args['sum'])
    else:
        args['debt'] = Debt.objects.filter(user_id=request.user.id)\
            .select_related('type').values('year', 'type__name')\
            .annotate(sum_year=Sum('amount'))
        args['years'] = sorted({item['year'] for item in args['debt']})
        args['debt_type'] = {item['type__name'] for item in args['debt']}
        args['sum'] = sum([item['sum_year'] for item in args['debt']])
        args['all'] = my_all(args['debt'], args['debt_type'], args['years'], args['sum'])
        if len(args['years']) == 1:
            return_url = redirect('mydebt').url + str(args['years'][0])
            return redirect(return_url)


    return render(request, 'debt_view.html', args)

