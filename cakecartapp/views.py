from django.shortcuts import render
from django.http import HttpResponse
from .forms import TableForm
from .models import Levels, Form, Topping, Berries, Decoration


# Create your views here.
def index(request):
    return render(request, "index.html")


def order(request):
    berries_id = request.POST.get("berries")
    decor_id = request.POST.get("decor")
    words = request.POST.get("words")
    comment = request.POST.get("comment")

    berries_name = ''
    decor_name = ''
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

    cake = {
        'levels': levels.quantity,
        'form': form.name,
        'topping': topping.name,
        'berries': berries_name,
        'decor': decor_name,
        'words': words,
        'comment': comment,
        'cost': cost,
    }
    return render(request, "order.html", context=cake)
