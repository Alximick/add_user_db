from django.shortcuts import render, render_to_response
from debt.models import Debt
from django.contrib import auth


# Create your views here.
def mydebt(request):
    args = {
        'debt' : Debt.objects.filter(
            user=auth.get_user(request)
        ).select_related('type'),
    }
    return render(request, 'jinja2/jinja2_view_debt.html', args)

