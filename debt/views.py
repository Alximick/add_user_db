from django.shortcuts import render
from debt.models import Debt
from django.db.models import Sum, Count


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

    args['debt_type'] = {item.type for item in debt}
    args['sum'] = sum([item.amount for item in debt])#debt.aggregate(Sum('amount'))
    args['years'] = {item.year for item in debt}
    
    return render(request, 'jinja2/jinja2_view_debt.html', args)

