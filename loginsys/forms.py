from django import forms
from django.contrib.auth import password_validation

from loginsys.admin import UserCreationForm
from loginsys.models import MyUser
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'phone_number', 'password1', 'password2')

