# Generated by Django 3.2 on 2023-04-05 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_customers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customers',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='customers',
            name='lust_name',
        ),
    ]