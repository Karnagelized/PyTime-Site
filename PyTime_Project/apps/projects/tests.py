
from apps.users.factories import UserCustomFactory
from apps.projects.factories import ProjectFactory
from django.test import TestCase
from django.urls import reverse
from apps.comments.forms import WriteCommentForm
from apps.skills.factories import HardSkillsFactory
from apps.projects.admin import ProjectAdmin
from apps.projects.models import Project
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory


# Тестирование модели проектов
class ProjectModelTestCase(TestCase):
    def test_str_dunder(self):
        """
            Тестируем правильный вывод str метода
        """

        project = ProjectFactory(
            slug='SlugProject',
            title='TitleProject',
        )

        self.assertEquals(project.__str__(), 'SlugProject - TitleProject')


# Тестирование Админки для модели Проектов
class AdminProjectTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = ProjectAdmin(Project, self.site)
        self.request = RequestFactory().get('/admin/')


    # TODO Дописать тест для проверки Админки
    # def test_tags_display(self):
    #     """
    #         Тестируем вывод тегов в Админке
    #     """
    #
    #     project = ProjectFactory(tags=[])
    #     self.assertEquals(self.admin.tagsDisplay(project), '')
    #
    #     project = ProjectFactory(tags=[HardSkillsFactory(name='Skill_1')])
    #     self.assertEquals(self.admin.tagsDisplay(project), 'Skill_1')
    #
    #     project = ProjectFactory(tags=[
    #         HardSkillsFactory(name='Skill_1'),
    #         HardSkillsFactory(name='Skill_2')
    #     ])
    #     self.assertEquals(self.admin.tagsDisplay(project), 'Skill_1, Skill_2')


    def test_view_on_site(self):
        """
            Тестируем что ссылка в Админке создаётся правильно
        """

        project = ProjectFactory()
        self.assertEquals(self.admin.view_on_site(project), project.get_absolute_url())


# Тестирование представления страницы с информацией о Проектах
class ProjectAboutViewTestCase(TestCase):
    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        response = self.client.post(
            reverse('projectsPage'),
        )

        self.assertEquals(response.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что страница вернет статус 200 без переданных параметров
        """

        response = self.client.get(
            reverse('projectsPage'),
            context={},
        )

        self.assertEquals(response.status_code, 200)


    def test_get_request_with_invalid_params(self):
        """
            Тестируем, что страница вернет статус 200 с неверными параметрами
        """

        response = self.client.get(
            reverse('projectsPage'),
            context={
                'navigationSelected': 'Invalid',
                'lastProjects': 'Invalid',
                'lastProject': 'Invalid',
                'Param': 'Invalid',
            },
        )

        self.assertEquals(response.status_code, 200)


    def test_get_request_with_valid_params(self):
        """
            Тестируем, что страница вернет статус 200 с верными параметрами
        """

        response = self.client.get(
            reverse('projectsPage'),
            context={
                'navigationSelected': 'Projects',
                'lastProjects': ProjectFactory.create_batch(4),
                'lastProject': ProjectFactory(),
            },
        )

        self.assertEquals(response.status_code, 200)


# Тестирование представления страницы с карточками всех Проектов
class ProjectListViewTestCase(TestCase):
    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        response = self.client.post(
            reverse('allProjectsPage'),
        )

        self.assertEquals(response.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что страница вернет статус 200 без переданных параметров
        """

        response = self.client.get(
            reverse('allProjectsPage'),
            context={},
        )

        self.assertEquals(response.status_code, 200)


    def test_get_request_with_invalid_params(self):
        """
            Тестируем, что страница вернет статус 200 с неверными параметрами
        """

        response = self.client.get(
            reverse('allProjectsPage'),
            context={
                'allProjects': 'Invalid',
                'Param': 'Invalid',
            },
        )

        self.assertEquals(response.status_code, 200)


    def test_get_request_with_valid_params(self):
        """
            Тестируем, что страница вернет статус 200 с верными параметрами
        """

        response = self.client.get(
            reverse('allProjectsPage'),
            context={
                'allProjects': ProjectFactory.create_batch(20),
            },
        )

        self.assertEquals(response.status_code, 200)


# Тестирование представления страницы Проекта
class ProjectPageViewTestCase(TestCase):
    def test_not_exist_page_returns_404(self):
        """
            Тестируем, что при попытке перехода на несуществующий проект
            страница вернет статус 404. Параметры GET запроса не передаются
        """

        # Авторизуем Пользователя
        self.client.force_login(
            UserCustomFactory()
        )

        response = self.client.get(
            reverse('projectPage', kwargs={'projectSlug': 'invalid-slug'}),
        )

        self.assertEquals(response.status_code, 404)


    def test_exist_page_returns_200(self):
        """
            Тестируем, что при попытке перехода на существующий проект
            страница вернет статус 200. Параметры GET запроса не передаются
        """

        project = ProjectFactory()

        response = self.client.get(
            reverse('projectPage', kwargs={'projectSlug': project.slug}),
        )

        self.assertEquals(response.status_code, 200)


    def test_page_with_invalid_params(self):
        """
            Тестируем, что страница вернет статус 200 с неверными параметрами
        """

        project = ProjectFactory()

        response = self.client.get(
            reverse('projectPage', kwargs={'projectSlug': project.slug}),
            context={
                'projectData': 'Invalid',
                'writeCommentForm': 'Invalid',
                'comments': 'Invalid',
                'Param': 'Invalid',
            },
        )

        self.assertEquals(response.status_code, 200)


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

        response = self.client.post(
            reverse('projectPage', kwargs={'projectSlug': project.slug}),
            data=formData,
        )

        # Проверяем, что страница возвращает код 200
        self.assertEquals(response.status_code, 200)

        # Проверяем форму
        self.assertIn('writeCommentForm', response.context)


    def test_auth_user_send_valid_form(self):
        """
            Тестируем, что Авторизованный Пользователь может отправить форму
        """

        # Авторизуем Пользователя
        self.client.force_login(
            UserCustomFactory()
        )

        project = ProjectFactory()
        # Значения не имеет, написал ли Пользователь что-то в форму или нет
        formData = {
            'content': 'Test',
        }

        response = self.client.post(
            reverse('projectPage', kwargs={'projectSlug': project.slug}),
            follow=True,
            data=formData,
        )

        # Проверяем, что страница возвращает код 302.
        # Произошло обновление страницы
        self.assertEquals(response.status_code, 200)

        # Проверяем форму
        self.assertIn('comments', response.context)
        self.assertContains(
            response,
            'Test'
        )

    # TODO Дописать тест, когда появится валидация комментария
    def test__invalid_form(self):
        """
            Тестируем, что при не прошедшей форме валидацию, Пользователь будет перенаправлен на главную страницу
        """
        pass
