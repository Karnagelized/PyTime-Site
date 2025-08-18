
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.users.factories import UserCustomFactory, AvatarProfileFactory
from django.test import TestCase, RequestFactory
from django.urls import reverse
from apps.users.forms import UserRegistrationForm, UserLoginForm
from apps.users.models import CustomUser


# Тестирование модели Пользователя
class CustomUserModelTestCase(TestCase):
    def test_str_dunder(self):
        """
            Тестируем правильный вывод str метода
        """

        user = UserCustomFactory(
            username='usernameTest',
        )

        self.assertEquals(user.__str__(), 'usernameTest')


# Тестирование представления страницы с профилем Пользователя
class UserProfileViewTestCase(TestCase):
    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 302
        """

        response = self.client.post(
            reverse('profilePage'),
        )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')


    def test_anonymous_user_redirected_without_params(self):
        """
            Тестируем, что Анонимный Пользователь не имеет доступа к профилю.
            Параметры для GET запроса не передаются
        """

        response = self.client.get(
            reverse('profilePage'),
            context={}
        )

        # Перенаправление Пользователя
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')


    def test_anonymous_user_redirected_with_invalid_params(self):
        """
            Тестируем, что Анонимный Пользователь не имеет доступа к профилю.
            Параметры для GET запроса передаются некорректные
        """

        response = self.client.get(
            reverse('profilePage'),
            context={
                'navigationSelected': 'None',
                'Param': 'Invalid',
            }
        )

        # Перенаправление Пользователя
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')


    def test_anonymous_user_redirected_with_valid_params(self):
        """
            Тестируем, что Анонимный Пользователь не имеет доступа к профилю.
            Параметры для GET запроса передаются корректные
        """

        response = self.client.get(
            reverse('profilePage'),
            context={
                'navigationSelected': 'Profile',
            }
        )

        # Перенаправление Пользователя
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')


    def test_auth_user_redirected_without_params(self):
        """
            Тестируем, что авторизованный Пользователь имеет доступ к профилю.
            Параметры GET запроса не передаются.
        """

        # Авторизуем Пользователя
        self.client.force_login(
            UserCustomFactory()
        )

        response = self.client.get(
            reverse('profilePage'),
            context={}
        )

        # Перенаправление Пользователя
        self.assertEquals(response.status_code, 200)


    def test_auth_user_redirected_with_invalid_params(self):
        """
            Тестируем, что авторизованный Пользователь имеет доступ к профилю.
            Параметры GET запроса передаются некорректные.
        """

        # Авторизуем Пользователя
        self.client.force_login(
            UserCustomFactory()
        )

        response = self.client.get(
            reverse('profilePage'),
            context={
                'navigationSelected': 'None',
                'Param': 'Invalid',
            }
        )

        # Перенаправление Пользователя
        self.assertEquals(response.status_code, 200)


    def test_auth_user_redirected_with_valid_params(self):
        """
            Тестируем, что авторизованный Пользователь имеет доступ к профилю.
            Параметры GET запроса передаются корректные.
        """

        # Авторизуем Пользователя
        self.client.force_login(
            UserCustomFactory()
        )

        response = self.client.get(
            reverse('profilePage'),
            context={
                'navigationSelected': 'Profile',
            }
        )

        # Перенаправление Пользователя
        self.assertEquals(response.status_code, 200)


    def test_anonymous_edit_profile(self):
        """
            Тестируем, что Анонимный Пользователь не может изменить профиль
        """

        self.client.logout()

        response = self.client.post(
            reverse('saveEditProfile'),
        )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')


    def test_edit_profile(self):
        """
            Тестируем, изменение профиля пользователя
        """

        user = UserCustomFactory(
            username='usernameTest',
        )

        self.client.force_login(
            user
        )

        response = self.client.post(
            reverse('saveEditProfile'),
            data={
                'first_name': 'firstNameTest',
                'last_name': 'lastNameTest',
                'aboutMe': 'aboutMeTest',
            }
        )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('profilePage'))

        self.assertEquals(response.wsgi_request.user.first_name, 'firstNameTest')
        self.assertEquals(response.wsgi_request.user.last_name, 'lastNameTest')
        self.assertEquals(response.wsgi_request.user.aboutMe, 'aboutMeTest')


# Тестирование представления с Регистрацией Пользователя
class RegistrationUserViewTestCase(TestCase):
    def clientLogout(self) -> None:
        self.client.logout()


    def test_invalid_username_in_form_after_submit(self):
        """
            Тестируем, что при регистрации нельзя указать уже существующий
            никнейм
        """

        # Явно указываем Анонимного Пользователя
        self.clientLogout()

        formData = {
            'username': 'Username',
            'email': 'Username@mail.ru',
            'password': 'Password',
        }

        # Создаем Пользователя с данными формы
        user = UserCustomFactory(**formData)

        response = self.client.post(
            reverse('registrationUser'),
            follow=True,
            data=formData,
        )

        self.assertEquals(response.status_code, 200)

        # Проверяем валидность
        self.assertIn(
            'registrationForm',
            response.context,
        )
        self.assertFalse(response.context['registrationForm'].is_valid())
        self.assertFormError(
            response.context['registrationForm'],
            'username',
            'Такое Имя уже существует!',
        )


    def test_invalid_email_in_form_after_submit(self):
        """
            Тестируем, что при регистрации нельзя указать уже существующий
            email
        """

        # Явно указываем Анонимного Пользователя
        self.clientLogout()

        formData = {
            'username': 'Username',
            'email': 'Username@mail.ru',
            'password': 'Password',
        }

        # Создаем Пользователя с данными формы
        user = UserCustomFactory(**formData)

        response = self.client.post(
            reverse('registrationUser'),
            follow=True,
            data=formData,
        )

        self.assertEquals(response.status_code, 200)

        # Проверяем валидность
        self.assertIn(
            'registrationForm',
            response.context,
        )
        self.assertFalse(response.context['registrationForm'].is_valid())
        self.assertFormError(
            response.context['registrationForm'],
            'email',
            'Такой E-mail уже существует!',
        )


    def test_invalid_email_in_form_after_submit(self):
        """
            Тестируем, что при корректной регистрации создаётся Пользователь
            и перенаправляется на страницу Авторизации
        """

        # Явно указываем Анонимного Пользователя
        self.clientLogout()

        formData = {
            'username': 'Username',
            'email': 'Username@mail.ru',
            'password': 'Password',
        }

        response = self.client.post(
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
            response,
            reverse('loginUser'),
        )


    def test_auth_user_redirect_main_page(self):
        # Авторизуем Пользователя
        self.client.force_login(
            UserCustomFactory()
        )

        response = self.client.get(
            reverse('registrationUser'),
        )

        self.assertEquals(response.status_code, 302)


    def test_anonymous_user_get_register_page_without_context(self):
        # Явно указываем Анонимного Пользователя
        self.clientLogout()

        response = self.client.get(
            reverse('registrationUser'),
            context={},
        )

        self.assertEquals(response.status_code, 200)


    def test_anonymous_user_get_register_page_with_incorrect_context(self):
        # Явно указываем Анонимного Пользователя
        self.clientLogout()

        response = self.client.get(
            reverse('registrationUser'),
            context={
                'registrationForm': 'Invalid',
                'Param': 'Invalid',
            },
        )

        self.assertEquals(response.status_code, 200)


    def test_anonymous_user_get_register_page_with_correct_context(self):
        # Явно указываем Анонимного Пользователя
        self.clientLogout()

        response = self.client.get(
            reverse('registrationUser'),
            context={
                'registrationForm': UserRegistrationForm(),
            },
        )

        self.assertEquals(response.status_code, 200)


# Тестирование представления страницы Авторизации Пользователя
class LoginUserViewTestCase(TestCase):
    def clientLogout(self) -> None:
        self.client.logout()


    def test_auth_user_redirect_main_page(self):
        """
            Тестируем, что Авторизованный Пользователь будет
            перенаправлен на главную страницу
        """

        # Авторизуем Пользователя
        self.client.force_login(
            UserCustomFactory(),
        )

        response = self.client.get(
            reverse('loginUser'),
        )

        self.assertRedirects(
            response,
            reverse('mainPage'),
        )


    def test_anonymous_user_get_login_page_without_context(self):
        """
            Тестируем, что Авторизованный Пользователь будет
            перенаправлен на главную страницу
        """

        # Явно указываем Анонимного Пользователя
        self.clientLogout()

        response = self.client.get(
            reverse('loginUser'),
            context={},
        )

        self.assertEquals(response.status_code, 200)


    def test_anonymous_user_get_login_page_with_invalid_context(self):
        """
            Тестируем, что Авторизованный Пользователь будет
            перенаправлен на главную страницу. Параметры для GET
            запроса указаны некорректно
        """

        # Явно указываем Анонимного Пользователя
        self.clientLogout()

        response = self.client.get(
            reverse('loginUser'),
            context={
                'navigationSelected': 'Invalid',
                'loginForm': 'Invalid',
                'Param': 'Invalid',
            },
        )

        self.assertEquals(response.status_code, 200)


    def test_anonymous_user_get_login_page_with_valid_context(self):
        """
            Тестируем, что Авторизованный Пользователь будет
            перенаправлен на главную страницу. Параметры для GET
            запроса указаны корректно
        """

        # Явно указываем Анонимного Пользователя
        self.clientLogout()

        response = self.client.get(
            reverse('loginUser'),
            context={
                'navigationSelected': 'Authorization',
                'loginForm': UserLoginForm(),
            },
        )

        self.assertEquals(response.status_code, 200)


    def test_send_invalid_email_into_form(self):
        """
            Тестируем, что Пользователь может ввести несуществующий email
        """

        formData = {
            'email': 'invalid@mail.ru',
            'password': 'Password',
        }

        response = self.client.post(
            reverse('loginUser'),
            follow=True,
            data=formData,
        )

        self.assertEquals(response.status_code, 200)

        self.assertIn(
            'loginForm',
            response.context,
        )
        self.assertFalse(response.context['loginForm'].is_valid())
        self.assertIn(
            'Неверный пароль или email!',
            response.context['loginForm'].non_field_errors(),
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

        response = self.client.post(
            reverse('loginUser'),
            follow=True,
            data=formData,
        )

        self.assertEquals(response.status_code, 200)

        self.assertIn(
            'loginForm',
            response.context,
        )
        self.assertFalse(response.context['loginForm'].is_valid())
        self.assertIn(
            'Неверный пароль или email!',
            response.context['loginForm'].non_field_errors(),
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

        response = self.client.post(
            reverse('loginUser'),
            follow=True,
            data=formData,
        )

        self.assertEquals(response.status_code, 200)

        # Находим профиль Пользователя
        user = CustomUser.objects.filter(email=formData['email']).first()

        # Пользователь успешно вошёл в систему
        self.assertIsInstance(user, CustomUser)


    def test_send_valid_form_but_auth_not_success(self):
        """
            Тестируем, что Пользователь не проходит аутентификацию
        """

        formData = {
            'email': 'valid@mail.ru',
            'password': 'Password',
        }

        invalidFormData = {
            'email': 'invalid@mail.ru',
            'password': 'Password',
        }

        # Создаем Пользователя с данными
        user = UserCustomFactory(**formData)

        response = self.client.post(
            reverse('loginUser'),
            follow=True,
            data=invalidFormData,
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'authorization.html')


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

        response = self.client.post(
            reverse('loginUser'),
            data=formData,
        )

        self.assertEquals(response.status_code, 302)

        # Пользователь успешно вошёл в систему
        self.assertTrue(self.client.session['_auth_user_id'])

        # Перенаправление
        self.assertRedirects(
            response,
            reverse('mainPage'),
        )


# Тестирование представления страницы выхода из профиля Пользователя
class LogoutUserViewTestCase(TestCase):
    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        response = self.client.post(
            reverse('logoutUser'),
        )

        self.assertEquals(response.status_code, 405)


# Тестирование представления страницы Восстановления пароля - ввод почты
class PasswordResetEnterMailViewTestCase(TestCase):
    def test_view_in_development(self):
        response = self.client.get(
            reverse('passwordResetEnterMail')
        )

        self.assertEquals(response.status_code, 302)


    def test_redirect_when_anonymous_user_logout(self):
        """
            Тестируем, что Анонимный пользователь будет перенаправлен
            на страницу Авторизации при попытке выйти из профиля
        """

        # Явно указываем Анонимного Пользователя
        self.client.logout()

        response = self.client.get(
            reverse('logoutUser'),
        )

        self.assertEquals(response.status_code, 302)


    def test_redirect_when_auth_user_logout(self):
        """
            Тестируем, что Авторизованный пользователь будет разлогинен и
            перенаправлен на страницу Авторизации при попытке выйти из профиля
        """

        # Авторизуем Пользователя
        self.client.force_login(
            UserCustomFactory(),
        )

        response = self.client.get(
            reverse('logoutUser'),
        )

        self.assertEquals(response.status_code, 302)


# Тестирование представления страницы Восстановления пароля - ввод кода
class PasswordResetEnterCodeViewTestCase(TestCase):
    def test_view_in_development(self):
        response = self.client.get(
            reverse('passwordResetEnterCode')
        )

        self.assertEquals(response.status_code, 302)


# Тестирование представления страницы Восстановления пароля - ввод нового пароля
class PasswordResetEnterNewPasswordViewTestCase(TestCase):
    def test_view_in_development(self):
        response = self.client.get(
            reverse('passwordResetEnterNewPassword')
        )

        self.assertEquals(response.status_code, 302)


# Тестирование генерации существующего аватара
class GenerateAvatarTestCase(TestCase):
    def test_get_request_is_not_allowed(self):
        """
            Проверяем, что GET запрос не работает для данного представления
        """

        self.client.force_login(
            UserCustomFactory(),
        )

        response = self.client.get(
            reverse('generateAvatar'),
        )

        self.assertEquals(response.status_code, 405)


    def test_avatar_less_2(self):
        """
            Проверяем, что если загружено менее 2-х аватаров, будет редирект с кодом 302
        """

        self.client.force_login(
            UserCustomFactory(),
        )

        response = self.client.post(
            reverse('generateAvatar'),
        )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('profilePage'))


    def test_avatar_more_2(self):
        """
            Проверяем, что если загружено менее 2-х аватаров, будет редирект с кодом 302
        """

        self.client.force_login(
            UserCustomFactory(),
        )

        for _ in range(3):
            AvatarProfileFactory(
                isDefault=True,
            )

        response = self.client.post(
            reverse('generateAvatar'),
        )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('profilePage'))


# Тестирование загрузки аватара Пользователя
class UploadAvatarTestCase(TestCase):
    def setUp(self):
        self.client.force_login(
            UserCustomFactory(),
        )


    def test_get_request_is_not_allowed(self):
        """
            Проверяем, что GET запрос не работает для данного представления
        """

        response = self.client.get(
            reverse('uploadAvatar'),
        )

        self.assertEquals(response.status_code, 405)


    def test_form_is_invalid(self):
        """
            Тестируем, что при невалидной форме, происходит редирект на страницу профиля кодом 302
        """

        response = self.client.post(
            reverse('uploadAvatar'),
            data={
                'avatar': 'invalid.png',
            }
        )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('profilePage'))



    def test_form_is_valid(self):
        """
            Тестируем, что при валидной форме, происходит редирект на страницу профиля кодом 302
        """

        user = UserCustomFactory(avatar=None)
        self.assertEquals(user.avatar, None)

        avatarFile = SimpleUploadedFile(
            name='testAvatar.jpg',
            content=b'Image content',
            content_type='image/jpeg'
        )

        self.client.force_login(user)

        response = self.client.post(
            reverse('uploadAvatar'),
            data={
                'avatar': avatarFile,
            },
            format='multipart',
        )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('profilePage'))
        self.assertIsNotNone(response.wsgi_request.user.avatar)
