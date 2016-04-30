from django.shortcuts import render, render_to_response
from debt.models import Debt
from django.contrib import auth



def add_my_set(lst):
    st = set()
    for l in lst:
        s = l.type.name
        st.add(s)
        # import ipdb;
        # ipdb.set_trace()
    return st

def sum_debt(lst):
    sum = 0
    for l in lst:
        sum += l.amount
    return sum

# Create your views here.
def mydebt(request):
    args = {
        'debt' : Debt.objects.filter(
            user=auth.get_user(request)
        ).select_related('type'),
    }
    args['debt_type'] = add_my_set(args['debt'])
    args['sum'] = sum_debt(args['debt'])

    return render(request, 'jinja2/jinja2_view_debt.html', args)

