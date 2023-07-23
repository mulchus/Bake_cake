import requests
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django_object_actions import DjangoObjectActions, action
from django.conf import settings as conf_settings

from .models import Form, Topping, Levels, Berries, Decoration, Cake, Client, Order, Links


def is_bitlink(token, bitlink):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    bitlink_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    response = requests.get(bitlink_url, headers=headers)
    return response.ok


def shorten_link(token, url):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    payload = {"long_url": url}
    shorten_url = 'https://api-ssl.bitly.com/v4/shorten'
    response = requests.post(shorten_url,
                             headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['id']


def count_clicks(token, bitlink):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    clicks_url = f'https://api-ssl.bitly.com/v4/bitlinks/' \
                 f'{bitlink}/clicks/summary'
    response = requests.get(clicks_url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


class CakeAdmin(admin.ModelAdmin):
    def admin_image(self, obj):
        if obj.image:
            return format_html(
                f'''<a href="{obj.image.url}" target="_blank">
                  <img src="{obj.image.url}" alt="{obj.image}" 
                    width="50" height="50" style="object-fit: cover;"/></a>
                ''')

    admin_image.allow_tags = True

    list_display = ('name', 'category', 'price', 'admin_image')


class ClientInline(admin.StackedInline):
    model = Client
    can_delete = False
    verbose_name_plural = 'Клиенты'


class UserAdmin(BaseUserAdmin):
    inlines = (ClientInline,)


@admin.register(Links)
class LinksAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ('name', 'long_link', 'short_link', 'views_number', )

    @action(label='Обновить ссылки', description='Обновить информацию по всем ссылкам в базе '
                                                 'и создать из длинных короткие ссылки')
    def update_links(self, request, obj):
        bitly_token = conf_settings.BITLY_TOKEN
        all_links = Links.objects.all()
        for link in all_links:
            if not link.short_link:
                try:
                    bitlink = shorten_link(bitly_token, link.long_link)
                except requests.exceptions.HTTPError:
                    print('Ошибка в ссылке')
                else:
                    print('Битлинк: ', bitlink)
                    link.short_link = bitlink
                    link.save()
            else:
                if is_bitlink(bitly_token, link.short_link):
                    try:
                        clicks_count = count_clicks(bitly_token, link.short_link)
                    except requests.exceptions.HTTPError:
                        print('Ошибка при попытке получить количество кликов на ссылке')
                    else:
                        print(f'По ссылке {link.short_link} перешли {clicks_count} раз(а)')
                        link.views_number = clicks_count
                        link.save()
                else:
                    try:
                        bitlink = shorten_link(bitly_token, link.long_link)
                    except requests.exceptions.HTTPError:
                        print('Ошибка в ссылке')
                    else:
                        print('Битлинк: ', bitlink)
                        link.short_link = bitlink
                        link.save()

    changelist_actions = ('update_links', )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Form)
admin.site.register(Topping)
admin.site.register(Levels)
admin.site.register(Berries)
admin.site.register(Decoration)
admin.site.register(Cake, CakeAdmin)
admin.site.register(Client)
admin.site.register(Order)
