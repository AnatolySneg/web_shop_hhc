from django import forms
from web_shop_hhc.products.models import Customer
from django.contrib.auth.forms import UserCreationForm


class SingUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, requiredUserCreationForm=False, label='Имя')
    second_name = forms.CharField(max_length=150, required=False, label='Фамилия')
    email = forms.EmailField(max_length=200, required=False)
