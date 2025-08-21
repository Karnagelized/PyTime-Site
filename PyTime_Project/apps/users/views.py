
from django.contrib.auth import login, logout
from django.http import HttpRequest, HttpResponseNotAllowed
from django.shortcuts import render, HttpResponse, redirect
from apps.users.forms import (
    UserLoginForm, UserRegistrationForm, ProfileForm, AvatarProfileForm, UserVerifyEmail,
)
from apps.users.models import ProfileAvatarModel, EmailVerification, CustomUser
from apps.users.backends import EmailAuthBackend
from django.views import View
from random import choice
from mixins.authenticated import LoginRequiredMixin
from apps.mail.models import VerifyEmail



class UploadUserAvatar(View):
    """
        Представление для загрузки пользовательского аватара в профиль Пользователя
    """

    def post(self, request:HttpRequest) -> HttpResponse:
        user = request.user
        form = AvatarProfileForm(request.POST, request.FILES)

        if not form.is_valid():
            return redirect('profilePage')

        form = form.save()
        userAvatar = ProfileAvatarModel.objects.get(avatar=form.avatar)
        user.avatar = userAvatar
        user.save(update_fields=['avatar'])

        return redirect('profilePage')


    def get(self, request:HttpRequest) -> HttpResponse:
        return HttpResponseNotAllowed(['GET'])



class GenerateUserAvatar(View):
    """
        Представление для установки существующего аватара Пользователя
    """

    def post(self, request:HttpRequest) -> HttpResponse:
        user = request.user
        avatars = ProfileAvatarModel.objects.filter(isDefault=True).all()

        if avatars.count() < 2:
            return redirect('profilePage')

        if user.avatar and avatars.count() > 1:
            avatars = ProfileAvatarModel.objects.filter(isDefault=True).exclude(id=user.avatar.id).all()

        user.avatar = choice(avatars)
        user.save(update_fields=['avatar'])

        return redirect('profilePage')


    def get(self, request:HttpRequest) -> HttpResponse:
        return HttpResponseNotAllowed(['GET'])



class UserProfileView(LoginRequiredMixin, View):
    """
        Представление страницы профиля Пользователя на сайте
    """

    def post(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        form = ProfileForm(user=request.user, data=request.POST, *args, **kwargs)

        # Валидация формы
        if not form.is_valid():
            return render(request, 'profile.html', context={'profileForm': form})

        form.save()

        return redirect('profilePage')


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        # Форма редактируемая Пользователем
        avatarForm = AvatarProfileForm()
        profileForm = ProfileForm(user=request.user)
        generateAvatars = ProfileAvatarModel.objects.filter(isDefault=True).all()

        # Выбор раздела навигации
        pageData = {
            'title': f'Профиль {request.user.username} | PyTime',
            'og_description': f'Профиль {request.user.username}.',
            'navigationSelected': 'Profile',
            'avatarForm': avatarForm,
            'profileForm': profileForm,
            'reloadAvatarIsPossible': True if generateAvatars.count() > 1 else False,
        }

        return render(request, 'profile.html', context=pageData)



class RegistrationUserView(View):
    """
        Представление регистрации Пользователя на сайте
    """

    def post(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        registrationForm = UserRegistrationForm(request.POST)

        pageData = {
            'title': f'Регистрация | PyTime',
            'og_description': f'Создание нового аккаунта с подтверждением почты.',
            'registrationForm': registrationForm,
        }

        # Проверяем валидность формы
        if not registrationForm.is_valid():
            return render(request, 'registration.html', context=pageData)

        # Создаём объект Пользователя без сохранения в БД
        newUser = registrationForm.save(commit=False)
        newUser.is_active = False
        newUser.set_password(registrationForm.cleaned_data['password'])
        newUser.save()

        # Отправляем на почту код подтверждения
        successSendEmail = VerifyEmail.send(
            user=newUser,
        )

        if not successSendEmail:
            newUser.delete()

            registrationForm.add_error(
                'email',
                'Почта не существует или введена неправильно.'
            )

            return render(request, 'registration.html', context=pageData)

        # Сохраняем в сессии Email
        self.request.session['userEmail'] = newUser.email
        self.request.session['needEmailVerification'] = True

        return redirect('needVerifyEmail')


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('mainPage')

        pageData = {
            'title': f'Регистрация | PyTime',
            'og_description': f'Создание нового аккаунта с подтверждением почты.',
            'registrationForm': UserRegistrationForm(),
        }

        return render(request, 'registration.html', context=pageData)



class NeedVerifyEmailView(View):
    """
        Класс для представления о необходимости подтвердить почту
    """

    def post(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        """
            Обработка подтверждения почты Пользователя на странице подтверждения почты
        """

        # Обработка нажатия кнопки с заменой кода
        if 'resendCode' in request.POST:
            return self.__sendCodeAgain(request, *args, **kwargs)

        userEmail = self.request.session['userEmail']
        user = CustomUser.objects.filter(email=userEmail).first()
        verificationCode = EmailVerification.objects.filter(user=user).first()
        form = UserVerifyEmail(request.POST)

        pageData = {
            'title': f'Подтверждение почты | PyTime',
            'og_description': f'Подтверждение почты для авторизации в аккаунт.',
            'verifyForm': form,
        }

        if not form.is_valid():
            return render(request, 'verify_email.html', context=pageData)

        # Код действителен не более чем 15 минут
        if verificationCode.isExpired():
            form.add_error(
                'code',
                'Код больше не действителен.',
            )

            return render(request, 'verify_email.html', context=pageData)

        if int(verificationCode.code) != int(form.cleaned_data['code']):
            form.add_error(
                'code',
                'Код не совпадает.',
            )

            return render(request, 'verify_email.html', context=pageData)

        verificationCode.delete()
        user.is_active = True
        user.save(update_fields=['is_active'])

        userAuthenticate = EmailAuthBackend().authenticate(request, email=userEmail, password=user.password)

        # Аутентификация не прошла
        if not user or not user.is_authenticated:
            form = UserLoginForm()

            form.add_error(
                'email',
                'Ошибка авторизации.'
            )

            pageData = {
                'title': f'Авторизация | PyTime',
                'og_description': f'Вход в личный кабинет с помощью email и пароля.',
                'navigationSelected': 'Authorization',
                'loginForm': form,
            }

            return render(request, 'authorization.html', context=pageData)

        # Авторизуем Пользователя
        login(request, user=user)

        # Удаляем из сессии userEmail и needEmailVerification Пользователя
        self.request.session.delete('userEmail')
        self.request.session.delete('needEmailVerification')

        return redirect('mainPage')


    def __sendCodeAgain(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        """
            Отправка кода повторно на почту Пользователя
        """

        userEmail = self.request.session['userEmail']
        user = CustomUser.objects.filter(email=userEmail).first()
        form = UserVerifyEmail()

        pageData = {
            'title': f'Подтверждение почты | PyTime',
            'og_description': f'Подтверждение почты для авторизации в аккаунт.',
            'verifyForm': form,
        }

        # Отправляем на почту код подтверждения
        successSendEmail = VerifyEmail.send(
            user=user,
        )

        return self.get(request, *args, **kwargs)


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        """
            Обработка страницы подтверждения почты
        """

        if request.user.is_authenticated:
            return redirect('mainPage')

        # Если Анонимный Пользователь зашёл на страницу подтверждения почты
        if not self.request.session.get('needEmailVerification', False):
            return redirect('mainPage')

        pageData = {
            'title': f'Подтверждение почты | PyTime',
            'og_description': f'Подтверждение почты для авторизации в аккаунт.',
            'verifyForm': UserVerifyEmail(),
        }

        return render(request, 'verify_email.html', context=pageData)



class LoginUserView(View):
    """
        Представление для авторизации Пользователя на сайте
    """

    def post(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        pageData = {
            'title': f'Авторизация | PyTime',
            'og_description': f'Вход в личный кабинет с помощью email и пароля.',
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

        # Требуется подтверждение почты
        if user and not user.is_active:
            return redirect('needVerifyEmail')

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
            'title': f'Авторизация | PyTime',
            'og_description': f'Вход в личный кабинет с помощью email и пароля.',
            'navigationSelected': 'Authorization',
            'loginForm': UserLoginForm(),
        }

        return render(request, 'authorization.html', context=pageData)



class LogoutUserView(View):
    """
        Представление для выхода из профиля Пользователем на сайте
    """

    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            logout(request)

        return redirect('loginUser')



def passwordResetEnterMail(request: HttpRequest) -> HttpResponse:
    """
        Представление для восстановления пароля Пользователем
        Этап - ввод почты
    """

    # Заглушка - В реализации
    return redirect('mainPage')

    pageData = {
        'title': f'Восстановление доступа | PyTime',
        'og_description': f'Запрос кода для сброса пароля на Email.',
    }

    return render(request, 'recovery_password/enter_mail.html')



def passwordResetEnterCode(request: HttpRequest) -> HttpResponse:
    """
        Представление для восстановления пароля Пользователем
        Этап - ввод кода
    """

    # Заглушка - В реализации
    return redirect('mainPage')

    pageData = {
        'title': f'Восстановление доступа | PyTime',
        'og_description': f'Подтверждение личности через код из письма.',
    }

    return render(request, 'recovery_password/confirm_mail_by_code.html')



def passwordResetEnterNewPassword(request: HttpRequest) -> HttpResponse:
    """
        Представление для восстановления пароля Пользователем
        Этап - ввод нового пароля
    """

    # Заглушка - В реализации
    return redirect('mainPage')

    pageData = {
        'title': f'Восстановление доступа | PyTime',
        'og_description': f'Установка нового пароля для аккаунта.',
    }

    return render(request, 'recovery_password/enter_new_password.html')
