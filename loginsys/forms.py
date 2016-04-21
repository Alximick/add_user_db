from django import forms
from loginsys.admin import UserCreationForm
from loginsys.models import MyUser

class RegistrationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'house_number','password1', 'password2')

