
from django.http import HttpRequest
from django.shortcuts import render, HttpResponse


# Главная страница сайта
def mainPage(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')
