
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.users.factories import UserCustomFactory, AvatarProfileFactory, EmailVerificationFactory
from django.test import TestCase, RequestFactory
from django.urls import reverse
from apps.users.forms import UserRegistrationForm, UserLoginForm, ProfileForm, UserVerifyEmail
from apps.users.models import CustomUser, EmailVerification
from django_recaptcha.client import RecaptchaResponse
from unittest.mock import patch, MagicMock
from django.utils import timezone



class CustomUserModelTestCase(TestCase):
    """
        Тестирование модели Пользователя
    """

    def test_str_dunder(self):
        """
            Тестируем правильный вывод str метода
        """

        user = UserCustomFactory(
            username='usernameTest',
        )

        self.assertEquals(user.__str__(), 'usernameTest')



class EmailVerificationModelTestCase(TestCase):
    """
        Тестирование модели для содержание кода подтверждения почты Пользователя
    """

    def test_str_dunder(self):
        """
            Тестируем правильный вывод str метода
        """

        user = UserCustomFactory()
        verificationCode = EmailVerificationFactory(
            user=user,
            code='123456'
        )

        self.assertEquals(verificationCode.__str__(), f'{user.username} - {verificationCode.code}')


    def test_expired_time_code(self):
        """
            Тестируем истек ли срок службы кода подтверждения почты
        """

        verificationCode = EmailVerificationFactory()
        self.assertFalse(verificationCode.isExpired())

        verificationCode_2 = EmailVerificationFactory()
        verificationCode_2.timeCreate -= datetime.timedelta(minutes=20)

        self.assertTrue(verificationCode_2.isExpired())


    def test_create_new_code(self):
        """
            Тестируем создание нового кода для подтверждения почты Пользователем
        """

        user = UserCustomFactory()
        verificationCode = EmailVerificationFactory(
            user=user,
        )

        self.assertFalse(verificationCode.isExpired())

        newCode = EmailVerification.create(
            user=user,
        )

        self.assertFalse(newCode.isExpired())
        self.assertFalse(EmailVerification.objects.filter(code='123456').exists())


class UserVerifyEmailFormTestCase(TestCase):
    """
        Тестирование формы для подтверждения почты Пользователя
    """

    def test_clean_code_is_digit(self):
        """
            Тестируем, что код в форме должен быть числом
        """

        form = UserVerifyEmail(
            data={
                'code': '1#%$56'
            }
        )

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            'code',
            'Код должен содержать только цифры'
        )

        form = UserVerifyEmail(
            data={
                'code': 'afafd1'
            }
        )

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            'code',
            'Код должен содержать только цифры'
        )

        form = UserVerifyEmail(
            data={
                'code': ' 2 4 6'
            }
        )

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            'code',
            'Код должен содержать только цифры'
        )



    def test_clean_code_has_len_6(self):
        """
            Тестируем что код в форме должен иметь длину равную 6
        """

        form = UserVerifyEmail(
            data={
                'code': '123'
            }
        )

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            'code',
            'Убедитесь, что это значение содержит не менее 6 символов (сейчас 3).'
        )

        form = UserVerifyEmail(
            data={
                'code': '123456789'
            }
        )

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            'code',
            'Убедитесь, что это значение содержит не более 6 символов (сейчас 9).'
        )


    def test_clean_code_is_valid(self):
        """
            Тестируем что код успешно пройдёт валидацию
        """

        form = UserVerifyEmail(
            data={
                'code': '123456'
            }
        )

        self.assertTrue(form.is_valid())


class UserProfileViewTestCase(TestCase):
    """
        Тестирование представления страницы с профилем Пользователя
    """


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
        self.assertRedirects(response, '/login')


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
        self.assertRedirects(response, '/login')


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
        self.assertRedirects(response, '/login')


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
        self.assertRedirects(response, '/login')


    def test_edit_profile(self):
        """
            Тестируем, что Пользователь не может установить уже занятый username
        """

        user_1 = UserCustomFactory()

        user_2 = UserCustomFactory(
            username='usernameTest',
        )

        self.client.force_login(
            user_1
        )

        response = self.client.post(
            reverse('saveEditProfile'),
            data={
                'username': 'usernameTest',
                'first_name': 'firstNameTest',
                'last_name': 'lastNameTest',
                'aboutMe': 'aboutMeTest',
            }
        )

        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, reverse('profilePage'))

        form:ProfileForm = response.context['profileForm']

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            'username',
            'Такое Имя Пользователя уже занято!'
        )

        self.assertEquals(response.wsgi_request.user.first_name, user_1.username)
        self.assertEquals(response.wsgi_request.user.first_name, '')
        self.assertEquals(response.wsgi_request.user.last_name, '')
        self.assertEquals(response.wsgi_request.user.aboutMe, '')


    def test_edit_profile(self):
        """
            Тестируем, корректное изменение профиля пользователя
        """

        user = UserCustomFactory()
        self.client.force_login(user)

        response = self.client.post(
            reverse('saveEditProfile'),
            data={
                'first_name': 'firstNameTest',
                'last_name': 'lastNameTest',
                'aboutMe': 'aboutMeTest',
            }
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.wsgi_request.path, reverse('saveEditProfile'))

        self.assertEquals(response.wsgi_request.user.username, user.username)
        self.assertEquals(response.wsgi_request.user.first_name, 'firstNameTest')
        self.assertEquals(response.wsgi_request.user.last_name, 'lastNameTest')
        self.assertEquals(response.wsgi_request.user.aboutMe, 'aboutMeTest')


class ProfileFormTestCase(TestCase):
    """
        Тестирование формы профиля Пользователя
    """

    def setUp(self):
        self.user_1 = UserCustomFactory(
            username='usernameTest_1',
        )

        self.user_2 = UserCustomFactory(
            username='usernameTest_2',
        )

        self.client.force_login(self.user_1)


    def test_clean_username_is_exist(self):
        """
            Тестируем, что Пользователь не может установить уже существующий ник
        """

        form = ProfileForm(
            user=self.user_1,
            data={
                'username': 'usernameTest_2',
                'email': self.user_1.email,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            'username',
            'Такое Имя Пользователя уже занято!'
        )


    def test_clean_username_is_valid(self):
        """
            Тестируем, что Пользователь может установить не занятый ник
        """

        form = ProfileForm(
            user=self.user_1,
            data={
                'username': 'anyUsername',
                'email': self.user_1.email,
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data['username'], 'anyUsername')


    def test_save_with_not_edit_username(self):
        """
            Тестируем, что Пользователю вернется тот же ник, если он его не изменил
        """

        form = ProfileForm(
            user=self.user_1,
            data={
                'username': 'usernameTest_1',
                'email': self.user_1.email,
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data['username'], 'usernameTest_1')


class RegistrationUserViewTestCase(TestCase):
    """
        Тестирование представления с Регистрацией Пользователя
    """

    def clientLogout(self) -> None:
        self.client.logout()


    def test_invalid_email_in_form(self):
        """
            Тестируем, что при регистрации нельзя указать уже существующий
            email
        """

        # Явно указываем Анонимного Пользователя
        self.clientLogout()

        formData = {
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

        form: UserRegistrationForm = response.context['registrationForm']
        self.assertFalse(form.is_valid())

        self.assertFormError(
            response.context['registrationForm'],
            'email',
            'Такой E-mail уже существует!',
        )


    def test_not_confirm_captcha_in_form(self):
        """
            Тестируем, ошибку о том что поле с капчей обязательное
        """

        # Явно указываем Анонимного Пользователя
        self.clientLogout()

        formData = {
            'email': 'Username@mail.ru',
            'password': 'Password',
        }

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

        form: UserRegistrationForm = response.context['registrationForm']
        self.assertFalse(form.is_valid())

        self.assertFormError(
            form,
            'captcha',
            'Обязательное поле.',
        )


    @patch('django_recaptcha.fields.client.submit')
    def test_create_new_inactive_user(self, mocked_captcha:MagicMock):
        """
            Тестируем, что при регистрации создается неподтвержденный Пользователь
        """

        # Явно указываем Анонимного Пользователя
        self.clientLogout()

        formData = {
            'email': 'username@mail.ru',
            'password': 'Password',
            'captcha': 'TestToken',
        }

        mocked_captcha.return_value = RecaptchaResponse(is_valid=True)

        response = self.client.post(
            reverse('registrationUser'),
            data=formData,
        )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('needVerifyEmail'))

        user = CustomUser.objects.filter(email=formData['email']).first()
        self.assertIsNotNone(user)
        self.assertEquals(user.is_active, False)


    @patch('apps.users.views.VerifyEmail.send')
    @patch('django_recaptcha.fields.client.submit')
    def test_invalid_send_code_in_mail(self, mocked_captcha:MagicMock, mocked_mail:MagicMock):
        """
            Тестируем, что может возникнуть ошибка отправки письма на почту
            из-за невалидной почты
        """

        mocked_captcha.return_value = RecaptchaResponse(is_valid=True)
        mocked_mail.return_value = 0

        # Явно указываем Анонимного Пользователя
        self.clientLogout()

        formData = {
            'email': 'username@mail.ru',
            'password': 'Password',
            'captcha': 'TestToken',
        }

        response = self.client.post(
            reverse('registrationUser'),
            data=formData,
        )

        self.assertEquals(response.status_code, 200)

        form: UserRegistrationForm = response.context['registrationForm']
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            'email',
            'Почта не существует или введена неправильно.',
        )

        user = CustomUser.objects.filter(email=formData['email']).first()
        self.assertIsNone(user)

        mocked_mail.assert_called_once()
        self.assertEquals(mocked_mail.call_args[1]['user'].email, formData['email'])
        self.assertEquals(response.wsgi_request.path, reverse('registrationUser'))


    @patch('apps.users.views.VerifyEmail.send')
    @patch('django_recaptcha.fields.client.submit')
    def test_valid_send_code_in_mail(self, mocked_captcha:MagicMock, mocked_mail:MagicMock):
        """
            Тестируем, успешную отправки письма на почту и редирект на страницу подтверждения
        """

        mocked_captcha.return_value = RecaptchaResponse(is_valid=True)
        mocked_mail.return_value = 1

        # Явно указываем Анонимного Пользователя
        self.clientLogout()

        formData = {
            'email': 'test@mail.ru',
            'password': 'Password',
            'captcha': 'TestToken',
        }

        response = self.client.post(
            reverse('registrationUser'),
            follow=True,
            data=formData,
        )

        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, reverse('needVerifyEmail'))

        user = CustomUser.objects.filter(email=formData['email']).first()
        self.assertIsNotNone(user)
        self.assertEquals(user.is_active, False)

        self.assertIn('userEmail', self.client.session)
        self.assertEqual(self.client.session['userEmail'], 'test@mail.ru')

        mocked_mail.assert_called_once()
        self.assertEquals(mocked_mail.call_args[1]['user'].email, formData['email'])


    def test_auth_user_redirect_main_page(self):
        """
            Тестируем, что авторизованный Пользователь переходя на странице регистрации
            будет перенаправлен на главную страницу
        """

        # Авторизуем Пользователя
        self.client.force_login(
            UserCustomFactory()
        )

        response = self.client.get(
            reverse('registrationUser'),
        )

        self.assertEquals(response.status_code, 302)


    def test_anonymous_user_get_register_page_without_context(self):
        """
            Тестируем, что неавторизованный Пользователь сможет перейти на страницу регистрации
            без переданных данных
        """

        # Явно указываем Анонимного Пользователя
        self.clientLogout()

        response = self.client.get(
            reverse('registrationUser'),
            context={},
        )

        self.assertEquals(response.status_code, 200)


    def test_anonymous_user_get_register_page_with_incorrect_context(self):
        """
            Тестируем, что анонимный Пользователь сможет войти на страницу регистрации
            передавая неправильные данные
        """

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
        """
            Тестируем, что анонимный Пользователь сможет войти на страницу регистрации
            передавая правильные данные
        """

        # Явно указываем Анонимного Пользователя
        self.clientLogout()

        response = self.client.get(
            reverse('registrationUser'),
            context={
                'registrationForm': UserRegistrationForm(),
            },
        )

        self.assertEquals(response.status_code, 200)



class NeedVerifyEmailViewTestCase(TestCase):
    """
        Тестирование представления подтверждения пароля через код
    """

    def test_auth_user_redirect_main_page(self):
        """
            Тестируем, что авторизованный Пользователь не может войти на страницу подтверждения почты
            и будет перенаправлен на главную страницу сайта
        """

        self.client.force_login(
            UserCustomFactory()
        )

        response = self.client.get(
            reverse('needVerifyEmail'),
        )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('mainPage'))
        self.assertNotIn('userEmail', response.wsgi_request.session)


    def test_not_auth_user_get_verify_email_page(self):
        """
            Тестируем, что неавторизованный Пользователь, не может войти вручную на страницу подтверждения почты
        """

        response = self.client.get(
            reverse('needVerifyEmail'),
        )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('mainPage'))
        self.assertIsNone(response.wsgi_request.session['userEmail'])


    def test_not_auth_user_get_verify_email_page(self):
        """
            Тестируем, что неавторизованный Пользователь, может войти на страницу подтверждения почты,
            если будет указан параметр в сессии "userEmail".

            Параметр записывается во время попытки авторизации, на неподтвержденный аккаунт Пользователя
        """

        self.client.logout()

        user = UserCustomFactory(
            email='test@mail.ru',
            is_active=False,
        )

        session = self.client.session
        session['userEmail'] = user.email
        session.save()

        self.assertIn('userEmail', self.client.session)

        response = self.client.get(
            reverse('needVerifyEmail'),
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.wsgi_request.path, reverse('needVerifyEmail'))
        self.assertEquals(response.wsgi_request.session['userEmail'], user.email)



    @patch('apps.users.views.VerifyEmail.send')
    def test_resend_code(self, mocked_email:MagicMock):
        """
            Тестируем обработку события повторной отправки кода на почту
        """

        user = UserCustomFactory(
            email='test@mail.ru',
            is_active=False,
        )

        session = self.client.session
        session['userEmail'] = user.email
        session.save()

        self.assertIn('userEmail', self.client.session)

        mocked_email.return_value = 1

        response = self.client.post(
            reverse('needVerifyEmail'),
            follow=True,
            data={
                'resendCode': True,
            }
        )

        mocked_email.assert_called_once()
        self.assertEquals(mocked_email.call_args[1]['user'].email, user.email)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.wsgi_request.path, reverse('needVerifyEmail'))
        self.assertEquals(response.wsgi_request.session['userEmail'], user.email)



    def test_invalid_form(self):
        """
            Тестируем, что при невалидной форме Пользователь получит ошибку
        """

        user = UserCustomFactory(
            email='test@mail.ru',
            is_active=False,
        )

        session = self.client.session
        session['userEmail'] = user.email
        session.save()

        self.assertIn('userEmail', self.client.session)

        response = self.client.post(
            reverse('needVerifyEmail'),
            follow=True,
            data={
                'code': '12a456',
            }
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.wsgi_request.path, reverse('needVerifyEmail'))
        self.assertEquals(response.wsgi_request.session['userEmail'], user.email)

        form:UserVerifyEmail = response.context['verifyForm']
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            'code',
            'Код должен содержать только цифры'
        )


    @patch('apps.users.models.EmailVerification.isExpired')
    def test_expired_code(self, mocked_isExpired:MagicMock):
        """
            Тестируем случай, что код может быть уже просрочен и требуется повторная его отправка
        """

        user = UserCustomFactory(
            email='test@mail.ru',
            is_active=False,
        )

        session = self.client.session
        session['userEmail'] = user.email
        session.save()

        self.assertIn('userEmail', self.client.session)

        verification_code = EmailVerificationFactory(
            user=user,
            code='123456'
        )

        mocked_isExpired.return_value = True

        response = self.client.post(
            reverse('needVerifyEmail'),
            follow=True,
            data={
                'code': '123456',
            }
        )

        mocked_isExpired.assert_called_once()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.wsgi_request.path, reverse('needVerifyEmail'))
        self.assertEquals(response.wsgi_request.session['userEmail'], user.email)

        form:UserVerifyEmail = response.context['verifyForm']
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            'code',
            'Код больше не действителен.'
        )


    @patch('apps.users.views.EmailVerification.objects.filter')
    def test_code_not_match(self, mocked_EmailVerificationFirst:MagicMock):
        """
            Тестируем случай, когда Пользователь ввел не тот код
        """

        user = UserCustomFactory(
            email='test@mail.ru',
            is_active=False,
        )

        session = self.client.session
        session['userEmail'] = user.email
        session.save()

        self.assertIn('userEmail', self.client.session)

        verification_code = EmailVerificationFactory(
            user=user,
            code='111111',
        )

        mocked_EmailVerificationFirst.return_value.first.return_value = verification_code

        response = self.client.post(
            reverse('needVerifyEmail'),
            follow=True,
            data={
                'code': '222222',
            }
        )

        mocked_EmailVerificationFirst.assert_called_once_with(user=user)
        mocked_EmailVerificationFirst.return_value.first.assert_called_once()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.wsgi_request.path, reverse('needVerifyEmail'))
        self.assertEquals(response.wsgi_request.session['userEmail'], user.email)

        form:UserVerifyEmail = response.context['verifyForm']
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            'code',
            'Код не совпадает.'
        )


    @patch('apps.users.views.EmailAuthBackend.authenticate')
    @patch('apps.users.views.EmailVerification.objects.filter')
    def test_user_not_success_login(self, mocked_EmailVerificationFirst:MagicMock, mocked_EmailAuthBackend:MagicMock):
        """
            Тестируем случай, когда Пользователь успешно ввел пароль, но при аутентификации произошла ошибка
        """

        user = UserCustomFactory(
            email='test@mail.ru',
            is_active=False,
        )

        session = self.client.session
        session['userEmail'] = user.email
        session.save()

        self.assertIn('userEmail', self.client.session)

        verification_code = EmailVerificationFactory(
            user=user,
            code='111111',
        )

        mocked_EmailVerificationFirst.return_value.first.return_value = verification_code
        mocked_EmailAuthBackend.return_value = None

        response = self.client.post(
            reverse('needVerifyEmail'),
            follow=True,
            data={
                'code': '111111',
            }
        )

        mocked_EmailVerificationFirst.assert_called_once_with(user=user)
        mocked_EmailVerificationFirst.return_value.first.assert_called_once()

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'authorization.html')
        self.assertEquals(response.wsgi_request.session['userEmail'], user.email)

        form: UserLoginForm = response.context['loginForm']
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            'email',
            'Ошибка авторизации.'
        )


    @patch('apps.users.views.EmailAuthBackend.authenticate')
    @patch('apps.users.views.EmailVerification.objects.filter')
    def test_user_success_login(self, mocked_EmailVerificationFirst:MagicMock, mocked_authenticate:MagicMock):
        """
            Тестируем успешное подтверждения почты профиля и вход в аккаунт на сайте
        """

        user = UserCustomFactory(
            email='test@mail.ru',
            is_active=False,
        )

        session = self.client.session
        session['userEmail'] = user.email
        session.save()

        self.assertIn('userEmail', self.client.session)

        verification_code = EmailVerificationFactory(
            user=user,
            code='111111',
        )

        mocked_EmailVerificationFirst.return_value.first.return_value = verification_code
        mocked_authenticate.return_value = user

        response = self.client.post(
            reverse('needVerifyEmail'),
            follow=True,
            data={
                'code': '111111',
            }
        )

        mocked_EmailVerificationFirst.assert_called_once_with(user=user)
        mocked_EmailVerificationFirst.return_value.first.assert_called_once()

        mocked_authenticate.assert_called_once()

        verifyUser = CustomUser.objects.get(email=user.email)
        self.assertEquals(EmailVerification.objects.all().count(), 0)
        self.assertTrue(verifyUser.is_active)

        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.wsgi_request.path, reverse('mainPage'))



class LoginUserViewTestCase(TestCase):
    """
        Тестирование представления страницы Авторизации Пользователя
    """

    def clientLogout(self) -> None:
        self.client.logout()


    def test_auth_user_redirect_main_page(self):
        """
            Тестируем, что Авторизованный Пользователь будет
            перенаправлен на главную страницу
        """

        # Авторизуем Пользователя
        self.client.force_login(
            UserCustomFactory()
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

        form:UserLoginForm = response.context['loginForm']

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            'email',
            'Такого Email не существует.'
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

        form:UserLoginForm = response.context['loginForm']

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            'password',
            'Неверный пароль.'
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


    def test_user_profile_need_verification(self):
        """
            Тестируем, что Пользователю нужно подтвердить почту
        """

        formData = {
            'email': 'valid@mail.ru',
            'password': 'Password',
        }

        # Создаем Пользователя с данными
        user = UserCustomFactory(
            email=formData['email'],
            is_active=False,
        )
        user.set_password(formData['password'])
        user.save()

        response = self.client.post(
            reverse('loginUser'),
            data=formData,
        )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('needVerifyEmail'))


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



class LogoutUserViewTestCase(TestCase):
    """
        Тестирование представления страницы выхода из профиля Пользователя
    """

    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        response = self.client.post(
            reverse('logoutUser'),
        )

        self.assertEquals(response.status_code, 405)



class PasswordResetEnterMailViewTestCase(TestCase):
    """
        Тестирование представления страницы Восстановления пароля - ввод почты
    """

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



class PasswordResetEnterCodeViewTestCase(TestCase):
    """
        Тестирование представления страницы Восстановления пароля - ввод кода
    """

    def test_view_in_development(self):
        response = self.client.get(
            reverse('passwordResetEnterCode')
        )

        self.assertEquals(response.status_code, 302)



class PasswordResetEnterNewPasswordViewTestCase(TestCase):
    """
        Тестирование представления страницы Восстановления пароля - ввод нового пароля
    """

    def test_view_in_development(self):
        response = self.client.get(
            reverse('passwordResetEnterNewPassword')
        )

        self.assertEquals(response.status_code, 302)



class GenerateAvatarViewTestCase(TestCase):
    """
        Тестирование генерации существующего аватара
    """

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
            UserCustomFactory()
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
            UserCustomFactory()
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



class UploadAvatarViewTestCase(TestCase):
    """
        Тестирование загрузки аватара Пользователя
    """

    def setUp(self):
        self.client.force_login(
            UserCustomFactory()
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

        user = UserCustomFactory(
            avatar=None,
        )
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
