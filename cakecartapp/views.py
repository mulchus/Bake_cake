from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, "index.html")


def postuser(request):
    # получаем из строки запроса имя пользователя
    name = request.POST.get("name", "Undefined")
    age = request.POST.get("age", 1)
    langs = request.POST.getlist("languages", ["python"])

    return HttpResponse(f"""
                <div>Name: {name}  Age: {age}<div>
                <div>Languages: {langs}</div>
            """)
