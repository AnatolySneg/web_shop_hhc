from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Customer


class UserSignupForm(UserCreationForm):
    # email = forms.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']
        widgets = {'password1': forms.PasswordInput(),
                   'password2': forms.PasswordInput(),
                   }


class CustomerSignupForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number', 'birth_date']

