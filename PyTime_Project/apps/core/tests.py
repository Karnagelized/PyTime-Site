
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import AnonymousUser
from apps.users.factories import UserCustomFactory
from apps.skills.factories import HardSkillsCategoryFactory
from django.test import TestCase
from django.urls import reverse
from apps.core.forms import ContactFeedbackForm



class MainViewTestCase(TestCase):
    """
        Тестирование представления Главной страницы
    """

    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        response = self.client.post(
            reverse('mainPage'),
        )

        self.assertEquals(response.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что страница вернет статус 200 без переданных параметров
        """

        response = self.client.get(
            reverse('mainPage'),
            context={},
        )

        # Проверяем код статуса
        self.assertEquals(response.status_code, 200)


    def test_get_request_with_invalid_params(self):
        """
            Тестируем, что страница вернет статус 200 с неверными параметрами
        """

        response = self.client.get(
            reverse('mainPage'),
            context={
                'user': 'Invalid',
                'skillsCategoryData': 'Invalid',
                'Param': 'Invalid',
            },
        )

        # Проверяем код статуса
        self.assertEquals(response.status_code, 200)


    def test_get_request_with_valid_params(self):
        """
            Тестируем, что страница вернет статус 200 с верными параметрами
        """

        skillsCategoryData = [
            HardSkillsCategoryFactory.create_batch(10),
            HardSkillsCategoryFactory.create_batch(5),
            HardSkillsCategoryFactory.create_batch(3),
            HardSkillsCategoryFactory.create_batch(1),
            HardSkillsCategoryFactory.create_batch(0),
        ]

        for skillCategory in skillsCategoryData[::-1]:
            response = self.client.get(
                reverse('mainPage'),
                context={
                    'user': UserCustomFactory(),
                    'skillsCategoryData': skillCategory,
                },
            )

            # Проверяем код статуса
            self.assertEquals(response.status_code, 200)



class ResumeViewTestCase(TestCase):
    """
        Тестирование представления страницы с Резюме
    """

    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        response = self.client.post(
            reverse('resumePage'),
        )

        self.assertEquals(response.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что страница вернет статус 200 без переданных параметров
        """

        response = self.client.get(
            reverse('resumePage'),
            context={},
        )

        # Проверяем код статуса
        self.assertEquals(response.status_code, 200)


    def test_get_request_with_invalid_params(self):
        """
            Тестируем, что страница вернет статус 200 с неверными параметрами
        """

        response = self.client.get(
            reverse('resumePage'),
            context={
                'navigationSelected': 'Invalid',
                'skillsCategoryData': 'Invalid',
                'Param': 'Invalid',
            },
        )

        # Проверяем код статуса
        self.assertEquals(response.status_code, 200)


    def test_get_request_with_valid_params(self):
        """
            Тестируем, что страница вернет статус 200 с верными параметрами
        """

        skillsCategoryData = [
            HardSkillsCategoryFactory.create_batch(10),
            HardSkillsCategoryFactory.create_batch(5),
            HardSkillsCategoryFactory.create_batch(3),
            HardSkillsCategoryFactory.create_batch(1),
            HardSkillsCategoryFactory.create_batch(0),
        ]

        for skillCategory in skillsCategoryData:
            response = self.client.get(
                reverse('resumePage'),
                context={
                    'navigationSelected': 'Resume',
                    'skillsCategoryData': skillCategory,
                },
            )

            # Проверяем код статуса
            self.assertEquals(response.status_code, 200)



class ContactViewTestCase(TestCase):
    """
        Тестирование представления контактов
    """

    def setUp(self):
        self.client.logout()


    def test_view_with_invalid_context(self):
        """
            Тестируем страницу контактов с правильно переданными данными
        """

        pageData = {
            'feedbackMessageForm': 'Test',
        }

        response = self.client.get(
            reverse('contactPage'),
            context=pageData,
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.wsgi_request.path, reverse('contactPage'))


    def test_view_with_valid_context(self):
        """
            Тестируем страницу контактов с неправильно переданными данными
        """

        form = ContactFeedbackForm(
            user=UserCustomFactory(),
        )

        pageData = {
            'feedbackMessageForm': form,
        }

        response = self.client.get(
            reverse('contactPage'),
            context=pageData,
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.wsgi_request.path, reverse('contactPage'))


    @patch('apps.core.views.SendFeedback.send')
    def test_not_success_send_email(self, mock_send:MagicMock):
        """
            Тестируем, что появится ошибка, если будет введена почта которой не существует в системе почты
        """

        user = UserCustomFactory(
            email='test@mail.ru',
        )

        mock_send.return_value = False

        pageData = {
            'email': user.email,
            'name': 'TestName',
            'message': 'Hello world!',
        }

        response = self.client.post(
            reverse('contactPage'),
            data=pageData,
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.wsgi_request.path, reverse('contactPage'))

        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            'email',
            'Почта не существует или введена неправильно.',
        )

        # Проверяем что отправка была вызвана
        mock_send.assert_called_once_with(
            email=user.email,
            username=pageData['name'],
            text=pageData['message'],
        )

        self.assertFalse(response.context['isSuccessSend'])



    @patch('apps.core.views.SendFeedback.send')
    def test_success_send_email(self, mock_send:MagicMock):
        """
            Тестируем, что при валидной форме обратной связи, и при успешной отправке письма на почту
            Пользователя перенаправит на страницу контактов и в данных страницы появится флаг isSuccessSend
        """

        user = UserCustomFactory(
            email='anyEmail@mail.ru',
        )

        mock_send.return_value = True

        pageData = {
            'email': user.email,
            'name': 'TestName',
            'message': 'Hello world!',
        }

        response = self.client.post(
            reverse('contactPage'),
            data=pageData,
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.wsgi_request.path, reverse('contactPage'))
        self.assertTrue(response.context['isSuccessSend'])

        form = response.context['form']
        self.assertTrue(form.is_valid())

        # Проверяем что отправка была вызвана
        mock_send.assert_called_once_with(
            email=user.email,
            username=pageData['name'],
            text=pageData['message'],
        )

        self.assertTrue(response.context['isSuccessSend'])



class ContactFeedbackFormTestCase(TestCase):
    """
        Тестирование формы обратной связи
    """

    def test_init_email_filed_by_auth_user(self):
        """
            Тестируем, что при авторизованном Пользователе поле email будет предварительно заполнено
        """

        user = UserCustomFactory()

        pageData = {
            'email': user.email,
            'name': 'TestName',
            'message': 'Hello world!',
        }

        form = ContactFeedbackForm(
            user=user,
            data=pageData,
        )

        self.assertTrue(form.is_valid())
        self.assertEquals(form.fields['email'].initial, user.email)
        self.assertEquals(form.cleaned_data['name'], pageData['name'])
        self.assertEquals(form.cleaned_data['message'], pageData['message'])


    def test_not_init_email_filed_by_not_auth_user(self):
        """
            Тестируем, что при неавторизованном Пользователе поле email будет не заполнено
        """

        user = AnonymousUser()

        pageData = {
            'name': 'TestName',
            'message': 'Hello world!',
        }

        form = ContactFeedbackForm(
            user=user,
            data=pageData,
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(form.fields['email'].initial, None)
        self.assertEquals(form.cleaned_data['name'], pageData['name'])
        self.assertEquals(form.cleaned_data['message'], pageData['message'])


class UserAgreementsViewTestCase(TestCase):
    """
        Тестирование представления Пользовательского соглашения
    """

    def setUp(self):
        self.client.logout()


    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        response = self.client.post(
            reverse('userAgreement'),
        )

        self.assertEquals(response.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что при GET запросе страница возвращает статус 200
        """

        response = self.client.get(
            reverse('userAgreement'),
        )

        self.assertEquals(response.status_code, 200)



class PrivacyViewTestCase(TestCase):
    """
        Тестирование представления Политики конфиденциальности
    """

    def setUp(self):
        self.client.logout()


    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        response = self.client.post(
            reverse('privacy'),
        )

        self.assertEquals(response.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что при GET запросе страница возвращает статус 200
        """

        response = self.client.get(
            reverse('privacy'),
        )

        self.assertEquals(response.status_code, 200)



class BadRequestViewTestCase(TestCase):
    """
        Тестирование представления страницы 400 ошибки - Bad request
    """

    def setUp(self):
        self.client.logout()


    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        response = self.client.post(
            reverse('badRequest'),
        )

        self.assertEquals(response.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что при GET запросе страница возвращает статус 400
        """

        response = self.client.get(
            reverse('badRequest'),
        )

        self.assertEquals(response.status_code, 400)



class ForbiddenViewTestCase(TestCase):
    """
        Тестирование представления страницы 403 ошибки - Forbidden
    """

    def setUp(self):
        self.client.logout()


    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        response = self.client.post(
            reverse('forbidden'),
        )

        self.assertEquals(response.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что при GET запросе страница возвращает статус 403
        """

        response = self.client.get(
            reverse('forbidden'),
        )

        self.assertEquals(response.status_code, 403)



class PageNotFoundViewTestCase(TestCase):
    """
        Тестирование представления страницы 404 ошибки - Page not found
    """

    def setUp(self):
        self.client.logout()


    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        response = self.client.post(
            reverse('pageNotFound'),
        )

        self.assertEquals(response.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что при GET запросе страница возвращает статус 404
        """

        response = self.client.get(
            reverse('pageNotFound'),
        )

        self.assertEquals(response.status_code, 404)



class InternalServerErrorViewTestCase(TestCase):
    """
        Тестирование представления страницы 500 ошибки - Internal server error
    """

    def setUp(self):
        self.client.logout()


    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        response = self.client.post(
            reverse('internalServerError'),
        )

        self.assertEquals(response.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что при GET запросе страница возвращает статус 500
        """

        response = self.client.get(
            reverse('internalServerError'),
        )

        self.assertEquals(response.status_code, 500)



class ServiceIsUnavailableViewTestCase(TestCase):
    """
        Тестирование представления страницы 503 ошибки - Service is unavailable
    """

    def setUp(self):
        self.client.logout()


    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        response = self.client.post(
            reverse('serviceUnavailable'),
        )

        self.assertEquals(response.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что при GET запросе страница возвращает статус 503
        """

        response = self.client.get(
            reverse('serviceUnavailable'),
        )

        self.assertEquals(response.status_code, 503)
