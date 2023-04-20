from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Customer


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

    # def clean(self):
    #     cleaned_data = super().clean()
    #     phone_number = cleaned_data.get("phone_number")
    #     print("phone_number", phone_number)
    #     db_phone_numbers = Customer.objects.filter(phone_number=phone_number)
    #     print("db_phone_numbers", db_phone_numbers)
    #     if db_phone_numbers:
    #         print("ValidationError")
    #         raise ValidationError("Customer with this %(value)s already exist",
    #                               code="invalid",
    #                               params={'value': 'phone number'}
    #                               )
