
from apps.users.factories import UserCustomFactory
from apps.projects.factories import ProjectFactory
from django.test import TestCase
from django.urls import reverse
from apps.comments.forms import WriteCommentForm


# Тестирование представления страницы с информацией о Проектах
class ProjectAboutViewTestCase(TestCase):
    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        postResponse = self.client.post(
            reverse('projectsPage'),
        )

        self.assertEquals(postResponse.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что страница вернет статус 200 без переданных параметров
        """

        postResponse = self.client.get(
            reverse('projectsPage'),
            context={},
        )

        self.assertEquals(postResponse.status_code, 200)


    def test_get_request_with_invalid_params(self):
        """
            Тестируем, что страница вернет статус 200 с неверными параметрами
        """

        postResponse = self.client.get(
            reverse('projectsPage'),
            context={
                'navigationSelected': 'Invalid',
                'lastProjects': 'Invalid',
                'lastProject': 'Invalid',
                'Param': 'Invalid',
            },
        )

        self.assertEquals(postResponse.status_code, 200)


    def test_get_request_with_valid_params(self):
        """
            Тестируем, что страница вернет статус 200 с верными параметрами
        """

        postResponse = self.client.get(
            reverse('projectsPage'),
            context={
                'navigationSelected': 'Projects',
                'lastProjects': ProjectFactory.create_batch(4),
                'lastProject': ProjectFactory(),
            },
        )

        self.assertEquals(postResponse.status_code, 200)


# Тестирование представления страницы с карточками всех Проектов
class ProjectListViewTestCase(TestCase):
    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        postResponse = self.client.post(
            reverse('allProjectsPage'),
        )

        self.assertEquals(postResponse.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что страница вернет статус 200 без переданных параметров
        """

        postResponse = self.client.get(
            reverse('allProjectsPage'),
            context={},
        )

        self.assertEquals(postResponse.status_code, 200)


    def test_get_request_with_invalid_params(self):
        """
            Тестируем, что страница вернет статус 200 с неверными параметрами
        """

        postResponse = self.client.get(
            reverse('allProjectsPage'),
            context={
                'allProjects': 'Invalid',
                'Param': 'Invalid',
            },
        )

        self.assertEquals(postResponse.status_code, 200)


    def test_get_request_with_valid_params(self):
        """
            Тестируем, что страница вернет статус 200 с верными параметрами
        """

        postResponse = self.client.get(
            reverse('allProjectsPage'),
            context={
                'allProjects': ProjectFactory.create_batch(20),
            },
        )

        self.assertEquals(postResponse.status_code, 200)


# Тестирование представления страницы Проекта
class ProjectPageViewTestCase(TestCase):
    def test_not_exist_page_returns_404(self):
        """
            Тестируем, что при попытке перехода на несуществующий проект
            страница вернет статус 404. Параметры GET запроса не передаются
        """

        # Авторизуем Пользователя, иначе происходит redirect с кодом 302
        self.client.force_login(
            UserCustomFactory()
        )

        getResponse = self.client.get(
            reverse('projectPage', kwargs={'projectSlug': 'invalid-slug'}),
        )

        self.assertEquals(getResponse.status_code, 404)


    def test_exist_page_returns_200(self):
        """
            Тестируем, что при попытке перехода на существующий проект
            страница вернет статус 200. Параметры GET запроса не передаются
        """

        project = ProjectFactory()

        getResponse = self.client.get(
            reverse('projectPage', kwargs={'projectSlug': project.slug}),
        )

        self.assertEquals(getResponse.status_code, 200)


    def test_page_with_invalid_params(self):
        """
            Тестируем, что страница вернет статус 200 с неверными параметрами
        """

        project = ProjectFactory()

        postResponse = self.client.get(
            reverse('projectPage', kwargs={'projectSlug': project.slug}),
            context={
                'projectData': 'Invalid',
                'writeCommentForm': 'Invalid',
                'comments': 'Invalid',
                'Param': 'Invalid',
            },
        )

        self.assertEquals(postResponse.status_code, 200)


    def test_anonymous_prohibited_sending_form(self):
        """
            Тестируем, что Анонимный Пользователь не может отправить форму
        """

        # Явное указание анонимности Пользователя
        self.client.logout()

        project = ProjectFactory()
        # Значения не имеет, написал ли Пользователь что-то в форму или нет
        formData = {
            'content': 'Test',
        }

        postResponse = self.client.post(
            reverse('projectPage', kwargs={'projectSlug': project.slug}),
            data=formData,
        )

        # Проверяем, что страница возвращает код 200
        self.assertEquals(postResponse.status_code, 200)

        # Проверяем форму
        self.assertIn('writeCommentForm', postResponse.context)


    def test_auth_user_send_valid_form(self):
        """
            Тестируем, что Авторизованный Пользователь может отправить форму
        """

        # Явное указание анонимности Пользователя
        self.client.force_login(
            UserCustomFactory()
        )

        project = ProjectFactory()
        # Значения не имеет, написал ли Пользователь что-то в форму или нет
        formData = {
            'content': 'Test',
        }

        postResponse = self.client.post(
            reverse('projectPage', kwargs={'projectSlug': project.slug}),
            follow=True,
            data=formData,
        )

        # Проверяем, что страница возвращает код 302.
        # Произошло обновление страницы
        self.assertEquals(postResponse.status_code, 200)

        # Проверяем форму
        self.assertIn('comments', postResponse.context)
        self.assertContains(
            postResponse,
            'Test'
        )