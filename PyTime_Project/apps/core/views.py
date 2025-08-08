
from django.http import HttpRequest, HttpResponseNotAllowed, Http404
from django.shortcuts import render, HttpResponse
from apps.skills.models import HardSkillsCategory
from django.views import View


# Представление Главной страницы
class MainView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        """Заглушка. POST запроса нет на Главную страницу"""
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        pageData = {
            'title': 'Начало Backend разработчика на Python | PyTime',
            'og_description': 'PyTime – это виртуальная визитная карточка, отражающая страсть к разработке и ' +
                              'стремление к постоянному профессиональному росту.',
            'skillsCategoryData': HardSkillsCategory.visibleCategory.all(),
        }

        return render(request, 'index.html', context=pageData)


# Представление страницы с Резюме
class ResumeView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        pageData = {
            'title': 'Резюме Разработчика | PyTime',
            'og_description': 'Персональная страница Разработчика с профессиональными навыками, ' +
                              'опытом работы и образованием.',
            'navigationSelected': 'Resume',
            'skillsCategoryData': HardSkillsCategory.visibleCategory.all(),
        }

        return render(request, 'resume.html', context=pageData)


# Представление страницы Контактов
class ContactView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        raise Http404


# Представление страницы Пользовательского соглашения
class UserAgreementView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        pageData = {
            'title': 'Пользовательское соглашение | PyTime',
            'og_description': 'Условия использования сайта и ответственность сторон.',
        }

        return render(request, 'agreements/user_agreement.html', context=pageData)


# Представление страницы Политики конфиденциальности
class PrivacyView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        pageData = {
            'title': 'Политика конфиденциальности | PyTime',
            'og_description': 'Правила обработки и защиты персональных данных пользователей.',
        }

        return render(request, 'agreements/privacy.html', context=pageData)


# Представление страницы 400 ошибки - Bad request
class BadRequestView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'errors/400.html', status=400)


# Представление страницы 403 ошибки - Forbidden
class ForbiddenView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'errors/403.html', status=403)


# Представление страницы 404 ошибки - Page not found
class PageNotFoundView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'errors/404.html', status=404)


# Представление страницы 500 ошибки - Internal server error
class InternalServerErrorView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'errors/500.html', status=500)


# Представление страницы 503 ошибки - Service is unavailable
class ServiceUnavailableView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'errors/503.html', status=503)
