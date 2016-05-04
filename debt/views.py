from django.shortcuts import render, redirect
from debt.models import Debt
from django.db.models import Sum, Count


def mydebt(request, year=None):
    
    if year:
        debt = Debt.objects.filter(user_id=request.user.id, year=year)\
            .select_related('type')
        args = {
            'filter': True,
            'debt_type': {item.type.name for item in debt},
            'years': sorted({(item.month, item.year) for item in debt}),
            'debt_sum': sum([item.amount for item in debt]),
            'all': {((item.month, item.year), item.type.name): item.amount for
                      item in debt}
        }
    else:
        debt = Debt.objects.filter(user_id=request.user.id)\
            .select_related('type').values('year', 'type__slug','type__name')\
            .annotate(sum_year=Sum('amount'))
        args = {
            'years': sorted({item['year'] for item in debt}),
            'debt_type': {item['type__name'] for item in debt},
            'debt_sum': sum([item['sum_year'] for item in debt]),
            'all': {(item['year'], item['type__name']):item['sum_year'] for item in debt},
        }
        if len(args['years']) == 1:
            return_url = redirect('mydebt').url + str(args['years'][0])
            return redirect(return_url)

    return render(request, 'jinja2_view_debt.jinja', args)
