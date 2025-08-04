
from django.contrib.auth import login, logout
from django.http import HttpRequest, HttpResponseNotAllowed
from django.shortcuts import render, HttpResponse, redirect
from users.forms import UserLoginForm, UserRegistrationForm
from users.backends import EmailAuthBackend
from django.views import View


# Представление страницы Профиля Пользователя
class UserProfileView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_anonymous:
            return redirect('mainPage')

        # Выбор раздела навигации
        pageData = {
            'navigationSelected': 'Profile',
        }

        return render(request, 'profile.html', context=pageData)


# Представление регистрации Пользователя
class RegistrationUserView(View):
    def post(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        registrationForm = UserRegistrationForm(request.POST)

        pageData = {
            'registrationForm': registrationForm,
        }

        # Проверяем валидность формы
        if not registrationForm.is_valid():
            return render(request, 'registration.html', context=pageData)

        # Создаём объект Пользователя без сохранения в БД
        newUser = registrationForm.save(commit=False)
        newUser.set_password(registrationForm.cleaned_data['password'])
        newUser.save()

        return redirect('loginUser')


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('mainPage')

        return render(
            request,
            'registration.html',
            context={
                'registrationForm': UserRegistrationForm()
            }
        )


# Представление авторизации Пользователя
class LoginUserView(View):
    def post(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        pageData = {
            'navigationSelected': 'Authorization',
        }

        loginForm = UserLoginForm(request.POST)

        # Проверяем валидность формы
        if not loginForm.is_valid():
            pageData['loginForm'] = loginForm

            return render(request, 'authorization.html', context=pageData)

        # Получаем данные
        email = loginForm.cleaned_data['email']
        password = loginForm.cleaned_data['password']

        user = EmailAuthBackend().authenticate(request, email=email, password=password)

        # Аутентификация не прошла
        if not user or not user.is_authenticated:
            pageData['loginForm'] = loginForm

            return render(request, 'authorization.html', context=pageData)

        # Авторизуем Пользователя
        login(request, user=user)

        return redirect('mainPage')


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('mainPage')

        pageData = {
            'navigationSelected': 'Authorization',
            'loginForm': UserLoginForm(),
        }

        return render(request, 'authorization.html', context=pageData)


# Представление страницы выхода из профиля Пользователя
class LogoutUserView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            logout(request)

        return redirect('loginUser')


# Страница для восстановления пароля Пользователя - Ввод почты
def passwordResetEnterMail(request: HttpRequest) -> HttpResponse:
    # Заглушка - В реализации
    return redirect('mainPage')

    return render(request, 'recovery_password/enter_mail.html')


# Страница для восстановления пароля Пользователя - Ввод кода
def passwordResetEnterCode(request: HttpRequest) -> HttpResponse:
    # Заглушка - В реализации
    return redirect('mainPage')

    return render(request, 'recovery_password/confirm_mail_by_code.html')


# Страница для восстановления пароля Пользователя - Ввод нового пароля
def passwordResetEnterNewPassword(request: HttpRequest) -> HttpResponse:
    # Заглушка - В реализации
    return redirect('mainPage')

    return render(request, 'recovery_password/enter_new_password.html')