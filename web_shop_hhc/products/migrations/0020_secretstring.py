# Generated by Django 3.2 on 2023-07-10 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_remove_customer_birth_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecretString',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secret_string', models.CharField(max_length=50)),
                ('creation_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
