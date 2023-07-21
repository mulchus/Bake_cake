# Generated by Django 4.2.3 on 2023-07-21 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cakecartapp', '0004_alter_levels_quantity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='berries',
            options={'verbose_name': 'Ягода', 'verbose_name_plural': 'Ягоды'},
        ),
        migrations.AlterModelOptions(
            name='cake',
            options={'verbose_name': 'Торт', 'verbose_name_plural': 'Торты'},
        ),
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Клиент', 'verbose_name_plural': 'Клиенты'},
        ),
        migrations.AlterModelOptions(
            name='decoration',
            options={'verbose_name': 'Декор', 'verbose_name_plural': 'Декоры'},
        ),
        migrations.AlterModelOptions(
            name='form',
            options={'verbose_name': 'Форма', 'verbose_name_plural': 'Формы'},
        ),
        migrations.AlterModelOptions(
            name='levels',
            options={'verbose_name': 'Уровней', 'verbose_name_plural': 'Уровни'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='topping',
            options={'verbose_name': 'Топпинг', 'verbose_name_plural': 'Топпинги'},
        ),
    ]
