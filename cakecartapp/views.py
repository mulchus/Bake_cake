from django.shortcuts import render
from django.http import HttpResponse
from .models import Levels, Form, Topping, Berries, Decoration, Order, Cake, Client
from datetime import datetime


CAKE = {}


# Create your views here.
def index(request):
    cake_elements = {
        'levels': Levels.objects.all(),
        'forms': Form.objects.all(),
        'toppings': Topping.objects.all(),
        'berries': Berries.objects.all(),
        'decors': Decoration.objects.all(),
    }
    print(cake_elements)
    return render(request, "index.html", context=cake_elements)


def making_order(request):      # Сохраняем торт и заказ {CAKE}
    global CAKE

    try:
        new_cake = Cake.objects.create(
            levels=Levels.objects.get(pk=CAKE['levels_pk']),
            form=Form.objects.get(pk=CAKE['form_pk']),
            topping=Topping.objects.get(pk=CAKE['topping_pk']),
            berries=Berries.objects.get(pk=CAKE['berries_pk']) if CAKE['berries_pk'] else None,
            decoration=Decoration.objects.get(pk=CAKE['decor_pk']) if CAKE['decor_pk'] else None,
            inscription=CAKE['words'],
            price=CAKE['cost'],
        )
    except ValueError as error:
        return HttpResponse(f"Ошибка сохранения торта, {error}", content_type="text/plain")  # , charset="utf-8")

    delivery_date_time = datetime.strptime(f"{CAKE['date']} {CAKE['time']}", "%Y-%m-%d %H:%M").isoformat()

    try:
        client, created = Client.objects.get_or_create(
            phone_number=CAKE['phone'],
            defaults={'email': CAKE['email'], 'name': CAKE['email']},
        )
    except ValueError as error:
        return HttpResponse(f"Ошибка сохранения клиента {error}", content_type="text/plain")  # , charset="utf-8")

    try:
        new_order = Order.objects.create(
            client=client,
            comment=CAKE['comment'],
            address=CAKE['address'],
            delivery_date_time=delivery_date_time,
            status='TBA',
            courier_comment=CAKE['courier_comment'],
            cost=CAKE['cost'],
        )
        new_order.cake.add(new_cake)
    except ValueError as error:
        return HttpResponse(f"Ошибка сохранения заказа {error}", content_type="text/plain")  # , charset="utf-8")

    CAKE.clear()
    return render(request, "making_order.html")


def pay(request):   # отображаем заказ на странице ввода данных клиента и оплаты
    global CAKE
    CAKE.update(
        {'name': request.POST.get('name_format'),
         'phone': request.POST.get('phone_format'),
         'email': request.POST.get('email_format'),
         'address': request.POST.get('address'),
         'date': request.POST.get('date'),
         'time': request.POST.get('time'),
         'courier_comment': request.POST.get('deliv-comment'),
        }
    )
    return render(request, "pay.html", context=CAKE)


def order(request):     # отображаем заказ на странице ввода данных клиента
    global CAKE
    berries_id = request.POST.get("berries")
    decor_id = request.POST.get("decor")
    words = request.POST.get("words")
    comment = request.POST.get("comment")

    berries_name = None
    decor_name = None
    cost = 0

    levels = Levels.objects.get(pk=int(request.POST.get("lvls")))
    form = Form.objects.get(pk=int(request.POST.get("form")))
    topping = Topping.objects.get(pk=int(request.POST.get("topping")))

    cost += (levels.price + form.price + topping.price)

    if berries_id:
        berries = Berries.objects.get(pk=int(berries_id))
        berries_name = berries.name
        cost += berries.price

    if decor_id:
        decor = Decoration.objects.get(pk=int(decor_id))
        decor_name = decor.name
        cost += decor.price

    CAKE = {
        'levels': levels.quantity,
        'levels_pk': levels.pk,
        'form': form.name,
        'form_pk': form.pk,
        'topping': topping.name,
        'topping_pk': topping.pk,
        'berries': berries_name,
        'berries_pk': berries_id,
        'decor': decor_name,
        'decor_pk': decor_id,
        'words': words,
        'comment': comment,
        'cost': cost,
    }
    return render(request, "order.html", context=CAKE)
