# Generated by Django 3.2 on 2023-04-21 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_userbucketproducts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userbucketproducts',
            old_name='customer',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='userbucketproducts',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
