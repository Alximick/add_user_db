from django.shortcuts import render, render_to_response
from debt.models import Debt
from django.contrib import auth
from django.db.models import Sum


def add_my_set(lst):
    st = set()
    for l in lst:
        s = l.type
        st.add(s)
        # import ipdb;
        # ipdb.set_trace()
    return st


def mydebt(request):
    args = {}
    debt = Debt.objects.filter(user=auth.get_user(request)).select_related('type')
    args['debt'] = debt
    args['debt_type'] = add_my_set(debt)
    # import ipdb;
    # ipdb.set_trace()
    args['sum'] = debt.aggregate(Sum('amount'))
    return render(request, 'jinja2/jinja2_view_debt.html', args)

