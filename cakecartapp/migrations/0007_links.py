# Generated by Django 4.2.3 on 2023-07-23 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakecartapp', '0006_client_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название рекламы')),
                ('long_link', models.URLField(verbose_name='Длинная ссылка')),
                ('short_link', models.URLField(blank=True, max_length=30, null=True, verbose_name='Короткая ссылка')),
                ('views_number', models.IntegerField(default=0, verbose_name='Количество просмотров')),
            ],
            options={
                'verbose_name': 'Ссылка',
                'verbose_name_plural': 'Ссылки',
            },
        ),
    ]