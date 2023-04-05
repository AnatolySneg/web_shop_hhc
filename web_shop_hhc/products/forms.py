from django import forms
from .models import Customer


class SignupForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'password', 'email', 'phone_number', 'birth_date']
        widgets = {'password': forms.PasswordInput()}
