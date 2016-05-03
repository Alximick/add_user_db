from django.shortcuts import render, render_to_response
from debt.models import Debt
from django.contrib import auth
from django.db.models import Sum, Count


def mydebt(request, year=None):
    args = {}
    if year:
        debt = Debt.objects.filter(user_id=request.user.id, year=year).select_related('type')
        args['filter'] = True
    else:
        debt = Debt.objects.filter(user_id=request.user.id).select_related('type')
        args['filter'] = False
    args['debt'] = debt
    args['debt_type'] = {item.type for item in debt}

    args['sum'] = debt.aggregate(Sum('amount'))
    args['years'] = {item.year for item in debt}
    args['test'] = debt.values('year', 'type__name').annotate(Sum('amount'))
    return render(request, 'jinja2/jinja2_view_debt.html', args)

