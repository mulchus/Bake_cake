from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Form, Topping, Levels, Berries, Decoration, Cake, Client, Order


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
