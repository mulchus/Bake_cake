from django.contrib import admin
# Register your models here.
from .models import Form, Topping, Levels, Berries, Decoration, Cake, Client, Order
from django.utils.html import format_html


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


admin.site.register(Form)
admin.site.register(Topping)
admin.site.register(Levels)
admin.site.register(Berries)
admin.site.register(Decoration)
admin.site.register(Cake, CakeAdmin)
admin.site.register(Client)
admin.site.register(Order)
