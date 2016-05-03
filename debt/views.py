from django.shortcuts import render
from debt.models import Debt
from django.db.models import Sum, Count


def my_all(debt, debt_type, years, sum):
    all_row = []

    row = ['']
    for year in years:
        # Если убрать коментарии в шаблоне нужно тогда row.append(year)
        row.append(r'<a href="/my/debt/' + str(year) + r'">' +  str(year) + r'</a>')
    all_row.append(row)

    for d_type in debt_type:
        row = []
        row.append(d_type.name)
        not_found = True
        for year in years:
            for item in debt:
                if item['year'] == year and item['type__name'] == d_type.name:
                    row.append(item['sum_year'])
                    not_found = False
            if not_found:
                row.append('')
        all_row.append(row)

    row = []
    for index in range(len(years) + 1):
        if index == 0:
            row.append('Sum')
        elif index == len(years):
            row.append('<font color="red" >' + str(sum) + '</font>')
        else:
            row.append('')
    all_row.append(row)

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
        args['all'] = my_all(args['debt'], args['debt_type'], args['years'], args['sum'])
    if args['filter']:
        pass


    return render(request, 'jinja2/jinja2_view_debt.html', args)

