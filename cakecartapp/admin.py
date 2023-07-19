from django.contrib import admin
from .models import Form, Topping, Levels, Berries, Decoration, Cake, Client, Order
# Register your models here.


admin.site.register(Form)
admin.site.register(Topping)
admin.site.register(Levels)
admin.site.register(Berries)
admin.site.register(Decoration)
admin.site.register(Cake)
admin.site.register(Client)
admin.site.register(Order)
