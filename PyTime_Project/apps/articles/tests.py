
from django.test import TestCase
from apps.users.factories import UserCustomFactory
from apps.articles.factories import ArticleFactory
from django.urls import reverse
from apps.comments.forms import WriteCommentForm


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
