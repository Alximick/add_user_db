from django.contrib import auth
from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from loginsys.forms import RegistrationForm

# Create your views here.

@csrf_exempt
def login(request):
    args = {}
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "Не найдена комбинация логин/пароль"
            return render_to_response('login.html', args)

    else:
        return render_to_response('login.html', args)



def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    pass