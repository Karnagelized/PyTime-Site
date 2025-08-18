
from apps.users.factories import UserCustomFactory
from apps.skills.factories import HardSkillsCategoryFactory
from django.test import TestCase
from django.urls import reverse


# Тестирование представления Главной страницы
class MainViewTestCase(TestCase):
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


# Тестирование представления страницы с Резюме
class ResumeViewTestCase(TestCase):
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


# Тестирование представления Пользовательского соглашения
class UserAgreementsViewTestCase(TestCase):
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


# Тестирование представления Политики конфиденциальности
class PrivacyViewTestCase(TestCase):
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


# Тестирование представления страницы контактов
class ContactViewTestCase(TestCase):
    def setUp(self):
        self.client.logout()


    def test_post_request_not_allowed(self):
        """
            Тестируем, что POST запрос отключен и возвращает статус 405
        """

        response = self.client.post(
            reverse('contactPage'),
        )

        self.assertEquals(response.status_code, 405)


    def test_get_request_not_allowed(self):
        """
            Тестируем, что страницы не существует и страница возвращает статус 404
        """

        response = self.client.get(
            reverse('contactPage'),
        )

        self.assertEquals(response.status_code, 404)


# Тестирование представления страницы 400 ошибки - Bad request
class BadRequestViewTestCase(TestCase):
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


# Тестирование представления страницы 403 ошибки - Forbidden
class ForbiddenViewTestCase(TestCase):
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


# Тестирование представления страницы 404 ошибки - Page not found
class PageNotFoundViewTestCase(TestCase):
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


# Тестирование представления страницы 500 ошибки - Internal server error
class InternalServerErrorViewTestCase(TestCase):
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


# Тестирование представления страницы 503 ошибки - Service is unavailable
class ServiceIsUnavailableViewTestCase(TestCase):
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

