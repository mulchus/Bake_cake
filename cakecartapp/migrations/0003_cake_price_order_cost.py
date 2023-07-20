# Generated by Django 4.2.3 on 2023-07-20 10:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakecartapp', '0002_alter_client_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='cake',
            name='price',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000000)], verbose_name='Цена'),
        ),
        migrations.AddField(
            model_name='order',
            name='cost',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000000)], verbose_name='Стоимость'),
        ),
    ]