from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Customer, Order


# TODO: ride https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#the-save-method for extending forms!!!!


class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', ]
        widgets = {'password1': forms.PasswordInput(),
                   'password2': forms.PasswordInput(),
                   }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        print("email", email)
        is_db_email = User.objects.filter(email=email).exists()
        print("is_db_email", is_db_email)
        if is_db_email:
            print("ValidationError")
            raise ValidationError("Email exist")


class CustomerSignupForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number', 'birth_date']


class OrderFirstCreationForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'phone_number', 'delivery_option',
                  'delivery_option']
