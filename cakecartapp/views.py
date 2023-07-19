from django.shortcuts import render
from django.http import HttpResponse
from .forms import TableForm


def html_button(request):
    if request.method == "POST":
        form = TableForm(request.POST)
        if form.is_valid():
            num = form.cleaned_data['num']
            return render(request, 'home.html', {'Number': num, 'range': range(1,11)})
    else:
        form = TableForm()
    return render(request, 'home.html', {'form': form})


# Create your views here.
def index(request):
    if request.method == "POST":
        print(request.POST.getlist)
        form_id = request.POST.get('form')
        print(form_id)
    else:
        form_id = ''
    return render(request, "index.html", {'Cost': form_id})


def postorder(request):
    # получаем из строки запроса имя пользователя
    # print(request.POST.getlist)
    lvls = request.POST.get("lvls")
    form = request.POST.get("form")
    topping = request.POST.get("topping")
    berries = request.POST.get("berries")
    decor = request.POST.get("decor")
    words = request.POST.get("words")
    comment = request.POST.get("comment")

    return HttpResponse(f"""
                <div>Количество уровней: {lvls}</div>  
                <div>Форма: {form}<div>
                <div>Топпинг: {topping}</div>
                <div>Ягоды: {berries}</div>
                <div>Декор: {decor}</div>
                <div>Надпись: {words}</div>
                <div>Комментарий к заказу: {comment}</div>                
            """)
