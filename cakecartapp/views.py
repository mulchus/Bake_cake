import hashlib
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from datetime import datetime
from decimal import Decimal
from phonenumber_field.phonenumber import PhoneNumber


from .forms import CreationForm
from .models import Levels, Form, Topping, Berries, Decoration, Order, Cake, Client


CAKE = {}
PASSWORD = 'MzMJb6YTy03wLySB36bW'


def lk(request):
    client = Client.objects.get(user=request.user)

    orders = client.orders.all()
    context = {
        'name': client.name,
        'phone_number': client.phone_number,
        'email': client.email,
        'orders': orders,
    }
    return render(request, 'lk.html', context=context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index_view')
        else:
            messages.success(request, ('Возникла ошибка. Попробуйте ещё раз.'))
            return redirect('login')
    else:
        return render(request, 'registration/login.html')


def signup(request):
    form = CreationForm(request.POST)
    if form.is_valid():
        new_user = form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        Client.objects.create(
            user=new_user,
            name=form.cleaned_data['client_name'],
            email=form.cleaned_data['email'],
            phone_number=form.cleaned_data['phone_number'],)
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, 'Вы успешно зарегистрировались!')
        return redirect('index_view')
    else:
            # messages.success(request, 'Данный логин уже занят')
        form = CreationForm()

    context = {'form': form}
    return render(request, 'signup.html', context)


def logout_user(request):
    logout(request)
    return redirect('index_view')


def catalog_pay(request):  # Сохраняем торты и заказ {CAKE}
    global CAKE
    cakes = CAKE['selected_cakes']

    serialized_phone = PhoneNumber.from_string(request.POST.get('phone_format'), region='RU').as_e164

    try:
        client, created = Client.objects.get_or_create(
            phone_number=serialized_phone,
            defaults={'email': request.POST.get('email_format'), 'name': request.POST.get('name_format')},
        )
    except ValueError as error:
        return HttpResponse(f"Ошибка сохранения клиента {error}", content_type="text/plain")

    delivery_date_time = datetime.strptime(f"{request.POST.get('date')} {request.POST.get('time')}", "%Y-%m-%d %H:%M")

    try:
        new_order = Order.objects.create(
            client=client,
            address=request.POST.get('address'),
            delivery_date_time=delivery_date_time.isoformat(),
            status='TBA',
            comment=request.POST.get('comment'),
            courier_comment=request.POST.get('deliv-comment'),
            cost=CAKE['cost'],
        )
        new_order.cake.add(*(list(cakes)))
    except ValueError as error:
        return HttpResponse(f"Ошибка сохранения заказа {error}", content_type="text/plain")

    CAKE.clear()
    return render(request, "catalog_pay.html")


def catalog_order(request):
    global CAKE
    selected_cakes = Cake.objects.filter(pk__in=request.POST.getlist('selected_cakes'))

    cost = sum([cake.price for cake in selected_cakes])

    context = {
        'selected_cakes': selected_cakes,
        'cost': cost,
    }
    CAKE = context
    return render(request, "catalog_order.html", context=context)


def catalog(request):
    category = request.GET.get('category', '')
    if category:
        context = {
            'catalog_of_cakes': Cake.objects.filter(category__exact=category),
            'category': (dict(Cake.Categories.choices))[category]
        }
    else:
        context = {
            'catalog_of_cakes': Cake.objects.exclude(category__exact='CUSTOM'),
            'category': 'Все категории',
        }

    return render(request, "catalog.html", context=context)


def index(request):
    cake_elements = {
        'levels': Levels.objects.all(),
        'forms': Form.objects.all(),
        'toppings': Topping.objects.all(),
        'berries': Berries.objects.all(),
        'decors': Decoration.objects.all(),
    }
    return render(request, "index.html", context=cake_elements)


def pay(request):  # Сохраняем торт и заказ {CAKE}
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
        return HttpResponse(f"Ошибка сохранения торта, {error}", content_type="text/plain")
    print(request.POST.get('phone_format'))
    serialized_phone = PhoneNumber.from_string(request.POST.get('phone_format'), region='RU').as_e164

    try:
        client, created = Client.objects.get_or_create(
            phone_number=serialized_phone,
            defaults={'email': request.POST.get('email_format'), 'name': request.POST.get('name_format')},
        )
    except ValueError as error:
        return HttpResponse(f"Ошибка сохранения клиента {error}", content_type="text/plain")

    try:
        new_order = Order.objects.create(
            client=client,
            comment=CAKE['comment'],
            address=CAKE['address'],
            delivery_date_time=CAKE['delivery_date_time'].isoformat(),
            status='TBA',
            courier_comment=CAKE['courier_comment'],
            cost=CAKE['cost'],
        )
        new_order.cake.add(new_cake)
    except ValueError as error:
        return HttpResponse(f"Ошибка сохранения заказа {error}", content_type="text/plain")
    cost = new_order.cost
    print(cost)
    crc = f'tortiru:{cost}::{PASSWORD}'
    print(crc)
    signature = hashlib.md5(crc.encode())
    print(signature)
    context = {
        'address': CAKE['address'],
        'delivery_date_time': CAKE['delivery_date_time'],
        'phone': client.phone_number,
        'email': client.email,
        'cost': cost,
        'signature': signature,
    }
    # CAKE.clear()
    return render(request, "pay.html", context=context)


def order(request):  # отображаем заказ на странице ввода данных клиента
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

    delivery_date_time = datetime.strptime(f"{request.POST.get('date')} {request.POST.get('time')}", "%Y-%m-%d %H:%M")
    difference = (delivery_date_time - datetime.now()).seconds / 3600
    print(difference, cost)
    if difference < 24:
        cost *= 1.2
        print(cost)
    print(cost)
    # dec_cost = Decimal(cost)
    # crc = f'tortiru:{cost}::{PASSWORD}'
    # signature = hashlib.md5(crc.encode())

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
        'address': request.POST.get('address'),
        'delivery_date_time': delivery_date_time,
        'courier_comment': request.POST.get('deliv-comment'),
        'cost': cost,
        # 'signature': signature,
    }
    return render(request, "order.html", context=CAKE)
