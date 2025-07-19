
from core.factories import (
    UserCustomFactory, ArticleFactory, ProjectFactory, HardSkillsCategoryFactory,
    CommentFactory
)
from django.test import TestCase
from django.urls import reverse
from core.forms import WriteCommentForm, UserRegistrationForm, UserLoginForm
from core.models import CustomUser


# Тестирование представления Главной страницы
class MainViewTestCase(TestCase):
    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        postResponse = self.client.post(
            reverse('mainPage'),
        )

        self.assertEquals(postResponse.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что страница вернет статус 200 без переданных параметров
        """

        getResponse = self.client.get(
            reverse('mainPage'),
            context={},
        )

        # Проверяем код статуса
        self.assertEquals(getResponse.status_code, 200)


    def test_get_request_with_invalid_params(self):
        """
            Тестируем, что страница вернет статус 200 с неверными параметрами
        """

        getResponse = self.client.get(
            reverse('mainPage'),
            context={
                'user': 'Invalid',
                'skillsCategoryData': 'Invalid',
                'Param': 'Invalid',
            },
        )

        # Проверяем код статуса
        self.assertEquals(getResponse.status_code, 200)


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
            getResponse = self.client.get(
                reverse('mainPage'),
                context={
                    'user': UserCustomFactory(),
                    'skillsCategoryData': skillCategory,
                },
            )

            # Проверяем код статуса
            self.assertEquals(getResponse.status_code, 200)


# Тестирование представления страницы с Резюме
class ResumeViewTestCase(TestCase):
    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        postResponse = self.client.post(
            reverse('resumePage'),
        )

        self.assertEquals(postResponse.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что страница вернет статус 200 без переданных параметров
        """

        getResponse = self.client.get(
            reverse('resumePage'),
            context={},
        )

        # Проверяем код статуса
        self.assertEquals(getResponse.status_code, 200)


    def test_get_request_with_invalid_params(self):
        """
            Тестируем, что страница вернет статус 200 с неверными параметрами
        """

        getResponse = self.client.get(
            reverse('resumePage'),
            context={
                'navigationSelected': 'Invalid',
                'skillsCategoryData': 'Invalid',
                'Param': 'Invalid',
            },
        )

        # Проверяем код статуса
        self.assertEquals(getResponse.status_code, 200)


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
            getResponse = self.client.get(
                reverse('resumePage'),
                context={
                    'navigationSelected': 'Resume',
                    'skillsCategoryData': skillCategory,
                },
            )

            # Проверяем код статуса
            self.assertEquals(getResponse.status_code, 200)


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


# Тестирование представления страницы с информацией о Статьях
class ArticleAboutViewTestCase(TestCase):
    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        postResponse = self.client.post(
            reverse('articlesPage'),
        )

        self.assertEquals(postResponse.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что страница вернет статус 200 без переданных параметров
        """

        postResponse = self.client.get(
            reverse('articlesPage'),
            context={},
        )

        self.assertEquals(postResponse.status_code, 200)


    def test_get_request_with_invalid_params(self):
        """
            Тестируем, что страница вернет статус 200 с неверными параметрами
        """

        postResponse = self.client.get(
            reverse('articlesPage'),
            context={
                'navigationSelected': 'Invalid',
                'lastArticles': 'Invalid',
                'lastArticle': 'Invalid',
                'Param': 'Invalid',
            },
        )

        self.assertEquals(postResponse.status_code, 200)


    def test_get_request_with_valid_params(self):
        """
            Тестируем, что страница вернет статус 200 с верными параметрами
        """

        postResponse = self.client.get(
            reverse('articlesPage'),
            context={
                'navigationSelected': 'Articles',
                'lastArticles': ArticleFactory.create_batch(4),
                'lastArticle': ArticleFactory(),
            },
        )

        self.assertEquals(postResponse.status_code, 200)


# Тестирование представления страницы с карточками всех Статей
class ArticleListViewTestCase(TestCase):
    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        postResponse = self.client.post(
            reverse('allArticlesPage'),
        )

        self.assertEquals(postResponse.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что страница вернет статус 200 без переданных параметров
        """

        postResponse = self.client.get(
            reverse('allArticlesPage'),
            context={},
        )

        self.assertEquals(postResponse.status_code, 200)


    def test_get_request_with_invalid_params(self):
        """
            Тестируем, что страница вернет статус 200 с неверными параметрами
        """

        postResponse = self.client.get(
            reverse('allArticlesPage'),
            context={
                'allArticles': 'Invalid',
                'Param': 'Invalid',
            },
        )

        self.assertEquals(postResponse.status_code, 200)


    def test_get_request_with_valid_params(self):
        """
            Тестируем, что страница вернет статус 200 с верными параметрами
        """

        postResponse = self.client.get(
            reverse('allArticlesPage'),
            context={
                'allArticles': ArticleFactory.create_batch(20),
            },
        )

        self.assertEquals(postResponse.status_code, 200)


# Тестирование представления страницы Стати
class ArticlePageViewTestCase(TestCase):
    def test_not_exist_page_returns_404(self):
        """
            Тестируем, что при попытке перехода на несуществующую статью
            страница вернет статус 404. Параметры GET запроса не передаются
        """

        # Авторизуем Пользователя, иначе происходит redirect с кодом 302
        self.client.force_login(
            UserCustomFactory()
        )

        getResponse = self.client.get(
            reverse('articlePage', kwargs={'articleSlug': 'invalid-slug'}),
        )

        self.assertEquals(getResponse.status_code, 404)


    def test_exist_page_returns_200(self):
        """
            Тестируем, что при попытке перехода на существующую статью
            страница вернет статус 200. Параметры GET запроса не передаются
        """

        article = ArticleFactory()

        getResponse = self.client.get(
            reverse('articlePage', kwargs={'articleSlug': article.slug}),
        )

        self.assertEquals(getResponse.status_code, 200)


    def test_page_with_invalid_params(self):
        """
            Тестируем, что страница вернет статус 200 с неверными параметрами
        """

        article = ArticleFactory()

        postResponse = self.client.get(
            reverse('articlePage', kwargs={'articleSlug': article.slug}),
            context={
                'articleData': 'Invalid',
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

        article = ArticleFactory()
        # Значения не имеет, написал ли Пользователь что-то в форму или нет
        formData = {
            'content': 'Test',
        }

        postResponse = self.client.post(
            reverse('articlePage', kwargs={'articleSlug': article.slug}),
            data=formData,
        )

        # Проверяем, что страница возвращает код 200
        self.assertEquals(postResponse.status_code, 200)

        # Проверяем форму
        self.assertIn('writeCommentForm', postResponse.context)

        self.assertIn(
            'Пользователь не авторизован!',
            postResponse.context['writeCommentForm'].non_field_errors(),
        )


    def test_auth_user_send_valid_form(self):
        """
            Тестируем, что Авторизованный Пользователь может отправить форму
        """

        # Явное указание анонимности Пользователя
        self.client.force_login(
            UserCustomFactory()
        )

        article = ArticleFactory()
        # Значения не имеет, написал ли Пользователь что-то в форму или нет
        formData = {
            'content': 'Test',
        }

        postResponse = self.client.post(
            reverse('articlePage', kwargs={'articleSlug': article.slug}),
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

        self.assertIn(
            'Пользователь не авторизован!',
            postResponse.context['writeCommentForm'].non_field_errors(),
        )


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


# Тестирование представления Пользовательского соглашения
class UserAgreementsViewTestCase(TestCase):
    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        postResponse = self.client.post(
            reverse('userAgreement'),
        )

        self.assertEquals(postResponse.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что при GET запросе страница возвращает статус 200
        """

        postResponse = self.client.get(
            reverse('userAgreement'),
        )

        self.assertEquals(postResponse.status_code, 200)


# Тестирование представления Политики конфиденциальности
class PrivacyViewTestCase(TestCase):
    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        postResponse = self.client.post(
            reverse('privacy'),
        )

        self.assertEquals(postResponse.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что при GET запросе страница возвращает статус 200
        """

        postResponse = self.client.get(
            reverse('privacy'),
        )

        self.assertEquals(postResponse.status_code, 200)


# Тестирование представления страницы 400 ошибки - Bad request
class BadRequestViewTestCase(TestCase):
    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        postResponse = self.client.post(
            reverse('badRequest'),
        )

        self.assertEquals(postResponse.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что при GET запросе страница возвращает статус 400
        """

        postResponse = self.client.get(
            reverse('badRequest'),
        )

        self.assertEquals(postResponse.status_code, 400)


# Тестирование представления страницы 403 ошибки - Forbidden
class ForbiddenViewTestCase(TestCase):
    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        postResponse = self.client.post(
            reverse('forbidden'),
        )

        self.assertEquals(postResponse.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что при GET запросе страница возвращает статус 403
        """

        postResponse = self.client.get(
            reverse('forbidden'),
        )

        self.assertEquals(postResponse.status_code, 403)


# Тестирование представления страницы 404 ошибки - Page not found
class PageNotFoundViewTestCase(TestCase):
    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        postResponse = self.client.post(
            reverse('pageNotFound'),
        )

        self.assertEquals(postResponse.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что при GET запросе страница возвращает статус 404
        """

        postResponse = self.client.get(
            reverse('pageNotFound'),
        )

        self.assertEquals(postResponse.status_code, 404)


# Тестирование представления страницы 500 ошибки - Internal server error
class InternalServerErrorViewTestCase(TestCase):
    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        postResponse = self.client.post(
            reverse('internalServerError'),
        )

        self.assertEquals(postResponse.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что при GET запросе страница возвращает статус 500
        """

        postResponse = self.client.get(
            reverse('internalServerError'),
        )

        self.assertEquals(postResponse.status_code, 500)


# Тестирование представления страницы 503 ошибки - Service is unavailable
class ServiceIsUnavailableViewTestCase(TestCase):
    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        postResponse = self.client.post(
            reverse('serviceUnavailable'),
        )

        self.assertEquals(postResponse.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что при GET запросе страница возвращает статус 503
        """

        postResponse = self.client.get(
            reverse('serviceUnavailable'),
        )

        self.assertEquals(postResponse.status_code, 503)

