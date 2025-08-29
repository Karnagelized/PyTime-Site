
from django.http import HttpRequest, HttpResponseNotAllowed, Http404
from django.shortcuts import render, HttpResponse
from apps.skills.models import HardSkillsCategory
from django.views import View
from apps.core.forms import ContactFeedbackForm
from apps.mail.models import SendFeedback



class MainView(View):
    """
        Представление Главной страницы
    """

    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        pageData = {
            'title': 'Начало Backend Python разработчика | PyTime',
            'og_description': 'PyTime – это виртуальная визитная карточка, отражающая страсть к разработке и ' +
                              'стремление к постоянному профессиональному росту.',
            'skillsCategoryData': HardSkillsCategory.visibleCategory.all(),
        }

        return render(request, 'index.html', context=pageData)



class ResumeView(View):
    """
        Представление страницы Резюме
    """

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



class ContactView(View):
    """
        Представление страницы Контактов
    """

    def post(self, request:HttpRequest, *args, **kwargs) -> HttpResponseNotAllowed:
        form = ContactFeedbackForm(user=request.user, data=request.POST, *args, **kwargs)
        form.is_valid()

        pageData = {
            'title': 'Контакты | PyTime',
            'og_description': 'Публичные контакты о Разработчике сайта.',
            'navigationSelected': 'Contact',
            'feedbackMessageForm': form,
            'isSuccessSend': False,
        }


        isSuccessSend = SendFeedback.send(
            email=form.cleaned_data['email'],
            username=form.cleaned_data['name'],
            text=form.cleaned_data['message'],
        )

        if not isSuccessSend:
            form.add_error(
                'email',
                'Почта не существует или введена неправильно.'
            )

            return render(request, 'contact.html', context=pageData)

        pageData['isSuccessSend'] = True
        return render(request, 'contact.html', context=pageData)


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        form = ContactFeedbackForm(user=request.user)
        form.is_valid()

        pageData = {
            'title': 'Контакты | PyTime',
            'og_description': 'Публичные контакты о Разработчике сайта.',
            'navigationSelected': 'Contact',
            'feedbackMessageForm': form,
        }

        return render(request, 'contact.html', context=pageData)



class UserAgreementView(View):
    """
        Представление страницы Пользовательского соглашения
    """

    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        pageData = {
            'title': 'Пользовательское соглашение | PyTime',
            'og_description': 'Условия использования сайта и ответственность сторон.',
        }

        return render(request, 'agreements/user_agreement.html', context=pageData)



class PrivacyView(View):
    """
        Представление страницы Политики конфиденциальности
    """

    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        pageData = {
            'title': 'Политика конфиденциальности | PyTime',
            'og_description': 'Правила обработки и защиты персональных данных пользователей.',
        }

        return render(request, 'agreements/privacy.html', context=pageData)



class BadRequestView(View):
    """
        Представление страницы ошибки 400 - Bad Request
    """

    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'errors/400.html', status=400)



class ForbiddenView(View):
    """
        Представление страницы ошибки 403 - Forbidden
    """

    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'errors/403.html', status=403)



class PageNotFoundView(View):
    """
        Представление страницы ошибки 404 - Page Not Found
    """

    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'errors/404.html', status=404)



class InternalServerErrorView(View):
    """
        Представление страницы ошибки 500 - Internal Server Error
    """

    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'errors/500.html', status=500)



class ServiceUnavailableView(View):
    """
        Представление страницы ошибки 503 - Service Unavailable
    """

    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'errors/503.html', status=503)
