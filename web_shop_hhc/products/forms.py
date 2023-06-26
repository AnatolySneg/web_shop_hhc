from django.forms import PasswordInput, ModelForm, CharField, EmailField, RadioSelect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Customer, Order


# TODO: ride https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#the-save-method for extending forms!!!!


class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', ]
        widgets = {'password1': PasswordInput(),
                   'password2': PasswordInput(),
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


class CustomerSignupForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number']


class OrderFirstCreationForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'phone_number', 'delivery_option']


ONLINE_PAYMENT = 'ONLINE_PAYMENT'
PAYMENT_BY_CARD_ON_RECEIPT = 'PAYMENT_BY_CARD'
PAYMENT_IN_CASH_ON_RECEIPT = 'PAYMENT_IN_CASH'

PAYMENT_OPTIONS = [
    (ONLINE_PAYMENT, 'Online payment'),
    (PAYMENT_BY_CARD_ON_RECEIPT, 'Payment by card upon receipt'),
    (PAYMENT_IN_CASH_ON_RECEIPT, 'Cash payment'),
]


class OrderSecondPickupCreationForm(ModelForm):
    payment_option = CharField(widget=RadioSelect(choices=PAYMENT_OPTIONS), max_length=50)

    class Meta:
        model = Order
        fields = ['payment_option']


class OrderSecondCourierCreationForm(ModelForm):
    payment_option = CharField(widget=RadioSelect(choices=PAYMENT_OPTIONS), max_length=50)
    destination_region = CharField(max_length=100, required=False)
    destination_country = CharField(max_length=50)
    destination_street = CharField(max_length=100)
    destination_house = CharField(max_length=20)
    destination_apartment = CharField(max_length=20, required=False)

    class Meta:
        model = Order
        fields = ['payment_option', 'destination_region', 'destination_country',
                  'destination_street', 'destination_house', 'destination_apartment']


class OrderSecondDeliveryCreationForm(ModelForm):
    ONLINE_PAYMENT = 'ONLINE_PAYMENT'
    PAYMENT_BY_CARD_ON_RECEIPT = 'PAYMENT_BY_CARD'
    PAYMENT_IN_CASH_ON_RECEIPT = 'PAYMENT_IN_CASH'
    CASH_ON_DELIVERY = 'CASH_ON_DELIVERY'

    PAYMENT_OPTIONS = [
        (ONLINE_PAYMENT, 'Online payment'),
        (CASH_ON_DELIVERY, 'Cash on delivery'),
    ]

    payment_option = CharField(widget=RadioSelect(choices=PAYMENT_OPTIONS), max_length=50)
    destination_region = CharField(max_length=100, required=False)
    destination_country = CharField(max_length=50)
    destination_delivery_service = CharField(max_length=100)

    class Meta:
        model = Order
        fields = ['payment_option', 'destination_region', 'destination_country', 'destination_delivery_service']
