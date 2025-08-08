
from apps.users.factories import UserCustomFactory
from django.test import TestCase
from django.urls import reverse
from apps.users.forms import UserRegistrationForm, UserLoginForm
from apps.users.models import CustomUser


# Тестирование представления страницы с профилем Пользователя
class UserProfileViewTestCase(TestCase):
    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        postResponse = self.client.post(
            reverse('profilePage'),
        )

        self.assertEquals(postResponse.status_code, 405)


    def test_anonymous_user_redirected_without_params(self):
        """
            Тестируем, что Анонимный Пользователь не имеет доступа к профилю.
            Параметры для GET запроса не передаются
        """

        getResponse = self.client.get(
            reverse('profilePage'),
            context={}
        )

        # Перенаправление Пользователя
        self.assertEquals(getResponse.status_code, 302)
        self.assertRedirects(getResponse, '/')


    def test_anonymous_user_redirected_with_invalid_params(self):
        """
            Тестируем, что Анонимный Пользователь не имеет доступа к профилю.
            Параметры для GET запроса передаются некорректные
        """

        getResponse = self.client.get(
            reverse('profilePage'),
            context={
                'navigationSelected': 'None',
                'Param': 'Invalid',
            }
        )

        # Перенаправление Пользователя
        self.assertEquals(getResponse.status_code, 302)
        self.assertRedirects(getResponse, '/')


    def test_anonymous_user_redirected_with_valid_params(self):
        """
            Тестируем, что Анонимный Пользователь не имеет доступа к профилю.
            Параметры для GET запроса передаются корректные
        """

        getResponse = self.client.get(
            reverse('profilePage'),
            context={
                'navigationSelected': 'Profile',
            }
        )

        # Перенаправление Пользователя
        self.assertEquals(getResponse.status_code, 302)
        self.assertRedirects(getResponse, '/')


    def test_auth_user_redirected_without_params(self):
        """
            Тестируем, что авторизованный Пользователь имеет доступ к профилю.
            Параметры GET запроса не передаются.
        """

        # Авторизуем Пользователя
        self.client.force_login(
            UserCustomFactory()
        )

        getResponse = self.client.get(
            reverse('profilePage'),
            context={}
        )

        # Перенаправление Пользователя
        self.assertEquals(getResponse.status_code, 200)


    def test_auth_user_redirected_with_invalid_params(self):
        """
            Тестируем, что авторизованный Пользователь имеет доступ к профилю.
            Параметры GET запроса передаются некорректные.
        """

        # Авторизуем Пользователя
        self.client.force_login(
            UserCustomFactory()
        )

        getResponse = self.client.get(
            reverse('profilePage'),
            context={
                'navigationSelected': 'None',
                'Param': 'Invalid',
            }
        )

        # Перенаправление Пользователя
        self.assertEquals(getResponse.status_code, 200)


    def test_auth_user_redirected_with_valid_params(self):
        """
            Тестируем, что авторизованный Пользователь имеет доступ к профилю.
            Параметры GET запроса передаются корректные.
        """

        # Авторизуем Пользователя
        self.client.force_login(
            UserCustomFactory()
        )

        getResponse = self.client.get(
            reverse('profilePage'),
            context={
                'navigationSelected': 'Profile',
            }
        )

        # Перенаправление Пользователя
        self.assertEquals(getResponse.status_code, 200)


# Тестирование представления с Регистрацией Пользователя
class RegistrationUserViewTestCase(TestCase):
    def test_invalid_username_in_form_after_submit(self):
        """
            Тестируем, что при регистрации нельзя указать уже существующий
            никнейм
        """

        # Явно указываем Анонимного Пользователя
        self.client.logout()

        formData = {
            'username': 'Username',
            'email': 'Username@mail.ru',
            'password': 'Password',
        }

        # Создаем Пользователя с данными формы
        user = UserCustomFactory(**formData)

        postRequest = self.client.post(
            reverse('registrationUser'),
            follow=True,
            data=formData,
        )

        self.assertEquals(postRequest.status_code, 200)

        # Проверяем валидность
        self.assertIn(
            'registrationForm',
            postRequest.context,
        )
        self.assertFalse(postRequest.context['registrationForm'].is_valid())
        self.assertFormError(
            postRequest.context['registrationForm'],
            'username',
            'Такое Имя уже существует!',
        )


    def test_invalid_email_in_form_after_submit(self):
        """
            Тестируем, что при регистрации нельзя указать уже существующий
            email
        """

        # Явно указываем Анонимного Пользователя
        self.client.logout()

        formData = {
            'username': 'Username',
            'email': 'Username@mail.ru',
            'password': 'Password',
        }

        # Создаем Пользователя с данными формы
        user = UserCustomFactory(**formData)

        postRequest = self.client.post(
            reverse('registrationUser'),
            follow=True,
            data=formData,
        )

        self.assertEquals(postRequest.status_code, 200)

        # Проверяем валидность
        self.assertIn(
            'registrationForm',
            postRequest.context,
        )
        self.assertFalse(postRequest.context['registrationForm'].is_valid())
        self.assertFormError(
            postRequest.context['registrationForm'],
            'email',
            'Такой E-mail уже существует!',
        )


    def test_invalid_email_in_form_after_submit(self):
        """
            Тестируем, что при корректной регистрации создаётся Пользователь
            и перенаправляется на страницу Авторизации
        """

        # Явно указываем Анонимного Пользователя
        self.client.logout()

        formData = {
            'username': 'Username',
            'email': 'Username@mail.ru',
            'password': 'Password',
        }

        postRequest = self.client.post(
            reverse('registrationUser'),
            follow=True,
            data=formData,
        )

        # Получаем Пользователя
        user = CustomUser.objects.filter(email=formData['email']).first()

        # Проверяем, что Пользователь был создан
        self.assertIsInstance(user, CustomUser)

        # Проверяем, что Пользователя перенаправляет
        self.assertRedirects(
            postRequest,
            reverse('loginUser'),
        )


    def test_auth_user_redirect_main_page(self):
        # Авторизуем Пользователя
        self.client.force_login(
            UserCustomFactory()
        )

        getRequest = self.client.get(
            reverse('registrationUser'),
        )

        self.assertEquals(getRequest.status_code, 302)


    def test_anonymous_user_get_register_page_without_context(self):
        # Явно указываем Анонимного Пользователя
        self.client.logout()

        getRequest = self.client.get(
            reverse('registrationUser'),
            context={},
        )

        self.assertEquals(getRequest.status_code, 200)


    def test_anonymous_user_get_register_page_with_incorrect_context(self):
        # Явно указываем Анонимного Пользователя
        self.client.logout()

        getRequest = self.client.get(
            reverse('registrationUser'),
            context={
                'registrationForm': 'Invalid',
                'Param': 'Invalid',
            },
        )

        self.assertEquals(getRequest.status_code, 200)


    def test_anonymous_user_get_register_page_with_correct_context(self):
        # Явно указываем Анонимного Пользователя
        self.client.logout()

        getRequest = self.client.get(
            reverse('registrationUser'),
            context={
                'registrationForm': UserRegistrationForm(),
            },
        )

        self.assertEquals(getRequest.status_code, 200)


# Тестирование представления страницы Авторизации Пользователя
class LoginUserViewTestCase(TestCase):
    def test_auth_user_redirect_main_page(self):
        """
            Тестируем, что Авторизованный Пользователь будет
            перенаправлен на главную страницу
        """

        # Авторизуем Пользователя
        self.client.force_login(
            UserCustomFactory(),
        )

        getRequest = self.client.get(
            reverse('loginUser'),
        )

        self.assertRedirects(
            getRequest,
            reverse('mainPage'),
        )


    def test_anonymous_user_get_login_page_without_context(self):
        """
            Тестируем, что Авторизованный Пользователь будет
            перенаправлен на главную страницу
        """

        # Явно указываем Анонимного Пользователя
        self.client.logout()

        getRequest = self.client.get(
            reverse('loginUser'),
            context={},
        )

        self.assertEquals(getRequest.status_code, 200)


    def test_anonymous_user_get_login_page_with_invalid_context(self):
        """
            Тестируем, что Авторизованный Пользователь будет
            перенаправлен на главную страницу. Параметры для GET
            запроса указаны некорректно
        """

        # Явно указываем Анонимного Пользователя
        self.client.logout()

        getRequest = self.client.get(
            reverse('loginUser'),
            context={
                'navigationSelected': 'Invalid',
                'loginForm': 'Invalid',
                'Param': 'Invalid',
            },
        )

        self.assertEquals(getRequest.status_code, 200)


    def test_anonymous_user_get_login_page_with_valid_context(self):
        """
            Тестируем, что Авторизованный Пользователь будет
            перенаправлен на главную страницу. Параметры для GET
            запроса указаны корректно
        """

        # Явно указываем Анонимного Пользователя
        self.client.logout()

        getRequest = self.client.get(
            reverse('loginUser'),
            context={
                'navigationSelected': 'Authorization',
                'loginForm': UserLoginForm(),
            },
        )

        self.assertEquals(getRequest.status_code, 200)


    def test_send_invalid_email_into_form(self):
        """
            Тестируем, что Пользователь может ввести несуществующий email
        """

        formData = {
            'email': 'invalid@mail.ru',
            'password': 'Password',
        }

        postRequest = self.client.post(
            reverse('loginUser'),
            follow=True,
            data=formData,
        )

        self.assertEquals(postRequest.status_code, 200)

        self.assertIn(
            'loginForm',
            postRequest.context,
        )
        self.assertFalse(postRequest.context['loginForm'].is_valid())
        self.assertIn(
            'Неверный пароль или email!',
            postRequest.context['loginForm'].non_field_errors(),
        )


    def test_send_invalid_password_into_form(self):
        """
            Тестируем, что Пользователь может ввести неверный пароль
        """

        formData = {
            'email': 'valid@mail.ru',
            'password': 'Password',
        }

        # Создаем Пользователя с данными
        user = UserCustomFactory(**formData)

        # Меняем пароль
        formData['password'] = 'any_password'

        postRequest = self.client.post(
            reverse('loginUser'),
            follow=True,
            data=formData,
        )

        self.assertEquals(postRequest.status_code, 200)

        self.assertIn(
            'loginForm',
            postRequest.context,
        )
        self.assertFalse(postRequest.context['loginForm'].is_valid())
        self.assertIn(
            'Неверный пароль или email!',
            postRequest.context['loginForm'].non_field_errors(),
        )


    def test_send_valid_form(self):
        """
            Тестируем, что Пользователь успешно проходит аутентификацию
        """

        formData = {
            'email': 'valid@mail.ru',
            'password': 'Password',
        }

        # Создаем Пользователя с данными
        user = UserCustomFactory(**formData)

        postRequest = self.client.post(
            reverse('loginUser'),
            follow=True,
            data=formData,
        )

        self.assertEquals(postRequest.status_code, 200)

        # Находим профиль Пользователя
        user = CustomUser.objects.filter(email=formData['email']).first()

        # Пользователь успешно вошёл в систему
        self.assertIsInstance(user, CustomUser)


    def test_user_redirect_when_login(self):
        """
            Тестируем, что Пользователя после успешной аутентификации
            перенаправляет на главную страницу
        """

        formData = {
            'email': 'valid@mail.ru',
            'password': 'Password',
        }

        # Создаем Пользователя с данными
        user = UserCustomFactory(
            email=formData['email'],
        )
        user.set_password(formData['password'])
        user.save()

        postRequest = self.client.post(
            reverse('loginUser'),
            data=formData,
        )

        self.assertEquals(postRequest.status_code, 302)

        # Пользователь успешно вошёл в систему
        self.assertTrue(self.client.session['_auth_user_id'])

        # Перенаправление
        self.assertRedirects(
            postRequest,
            reverse('mainPage'),
        )


# Тестирование представления страницы выхода из профиля Пользователя
class LogoutUserViewTestCase(TestCase):
    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        postResponse = self.client.post(
            reverse('logoutUser'),
        )

        self.assertEquals(postResponse.status_code, 405)


# Тестирование представления страницы Восстановления пароля - ввод почты
class PasswordResetEnterMailViewTestCase(TestCase):
    def test_view_in_development(self):
        getResponse = self.client.get(
            reverse('passwordResetEnterMail')
        )

        self.assertEquals(getResponse.status_code, 302)


    def test_redirect_when_anonymous_user_logout(self):
        """
            Тестируем, что Анонимный пользователь будет перенаправлен
            на страницу Авторизации при попытке выйти из профиля
        """

        # Явно указываем Анонимного Пользователя
        self.client.logout()

        getResponse = self.client.get(
            reverse('logoutUser'),
        )

        self.assertEquals(getResponse.status_code, 302)


    def test_redirect_when_auth_user_logout(self):
        """
            Тестируем, что Авторизованный пользователь будет разлогинен и
            перенаправлен на страницу Авторизации при попытке выйти из профиля
        """

        # Авторизуем Пользователя
        self.client.force_login(
            UserCustomFactory(),
        )

        getResponse = self.client.get(
            reverse('logoutUser'),
        )

        self.assertEquals(getResponse.status_code, 302)


# Тестирование представления страницы Восстановления пароля - ввод кода
class PasswordResetEnterCodeViewTestCase(TestCase):
    def test_view_in_development(self):
        getResponse = self.client.get(
            reverse('passwordResetEnterCode')
        )

        self.assertEquals(getResponse.status_code, 302)


# Тестирование представления страницы Восстановления пароля - ввод нового пароля
class PasswordResetEnterNewPasswordViewTestCase(TestCase):
    def test_view_in_development(self):
        getResponse = self.client.get(
            reverse('passwordResetEnterNewPassword')
        )

        self.assertEquals(getResponse.status_code, 302)
