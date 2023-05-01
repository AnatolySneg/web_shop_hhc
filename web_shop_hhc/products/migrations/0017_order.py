# Generated by Django 3.2 on 2023-04-28 13:07

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_alter_userbucketproducts_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('NEW', 'New order'), ('CONFIRM', 'Confirmed order'), ('EXECUTION', 'Executing order'), ('COMPLETE', 'Completed order'), ('REJECT', 'Rejected order')], default='NEW', max_length=50)),
                ('created_date', models.DateTimeField()),
                ('is_customer', models.BooleanField(default=False)),
                ('username', models.CharField(blank=True, max_length=150, null=True)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='UA')),
                ('delivery_option', models.CharField(choices=[('PICKUP', 'Pickup'), ('STORE_COURIER', 'Store courier'), ('DELIVERY_SERVICE_1', 'Delivery service 1'), ('DELIVERY_SERVICE_2', 'Delivery service 2'), ('DELIVERY_SERVICE_3', 'Delivery service 3')], default='PICKUP', max_length=50)),
                ('payment_option', models.CharField(choices=[('ONLINE_PAYMENT', 'Online payment'), ('PAYMENT_BY_CARD', 'Payment by card upon receipt'), ('PAYMENT_IN_CASH', 'Cash payment'), ('CASH_ON_DELIVERY', 'Cash on delivery')], default='PAYMENT_BY_CARD', max_length=50)),
                ('destination_region', models.CharField(blank=True, max_length=100, null=True)),
                ('destination_country', models.CharField(blank=True, max_length=50, null=True)),
                ('destination_delivery_service', models.CharField(blank=True, max_length=100, null=True)),
                ('destination_street', models.CharField(blank=True, max_length=100, null=True)),
                ('destination_house', models.CharField(blank=True, max_length=20, null=True)),
                ('destination_apartment', models.CharField(blank=True, max_length=20, null=True)),
                ('order_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]