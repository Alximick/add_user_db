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
        row.append(d_type.name)
        not_found = True
        for year in years:
            for item in debt:
                if item['year'] == year and item['type__name'] == d_type.name:
                    url_sum_year = r'<a href="' + url.url + str(year) + r'">' +  \
                                   str(item['sum_year']) + r'</a>'
                    row.append(url_sum_year)
                    not_found = False
            if not_found:
                row.append('')
        all_row.append(row)

    all_row.append(row_sum(sum, len(all_row[0])))

    return all_row


def my_all_filter(debt, debt_type, sum):
    all_row = []
    row = ['']
    for item in debt:
        year, month = item.year, item.month
        row.append((year, month))
    all_row.append(set(row))

    for d_type in debt_type:
        row = []
        print(d_type)
        row.append(d_type)
        not_found = True
        for year_month in all_row[0]:
            if not year_month:
                continue
            for item in debt:
                if item.year == year_month[0] and item.month == year_month[1]\
                        and item.type.name == d_type.name:
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
        debt = Debt.objects.filter(user_id=request.user.id, year=year).select_related('type')
        args['filter'] = True
        args['debt'] = debt
    else:
        debt = Debt.objects.filter(user_id=request.user.id).select_related('type')
        args['filter'] = False
        args['debt'] = debt.values('year', 'type__name').annotate(sum_year=Sum('amount'))

    debt_type = {item.type for item in debt}
    args['debt_type'] = debt_type
    args['sum'] = sum([item.amount for item in debt])
    args['years'] = sorted({item.year for item in debt})


    if not args['filter']:

        if len(args['years']) == 1:
            return_url = redirect('mydebt').url + str(args['years'][0])
            # print(return_url)
            return redirect(return_url)

        args['all'] = my_all(args['debt'], args['debt_type'], args['years'], args['sum'])

    if args['filter']:
        args['all'] = my_all_filter(args['debt'], args['debt_type'], args['sum'])


    return render(request, 'jinja2/jinja2_view_debt.html', args)

