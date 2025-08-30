
from django.test import TestCase
from apps.users.factories import UserCustomFactory
from apps.articles.factories import ArticleFactory
from django.urls import reverse
from apps.comments.forms import WriteCommentForm
from apps.articles.models import Article
from django.test import RequestFactory
from apps.skills.factories import HardSkillsFactory
from apps.articles.admin import ArticleAdmin
from django.contrib.admin import AdminSite



class ArticleModelTestCase(TestCase):
    """
        Тестирование модели Статей
    """

    def test_str_dunder(self):
        """
            Тестируем правильный вывод str метода
        """

        article = ArticleFactory(
            title='TitleArticle',
        )

        self.assertEquals(article.__str__(), 'TitleArticle')



class AdminArticleTestCase(TestCase):
    """
        Тестирование Админки для модели Статей
    """

    def setUp(self):
        self.site = AdminSite()
        self.admin = ArticleAdmin(Article, self.site)
        self.request = RequestFactory().get('/admin/')


    def test_view_on_site(self):
        """
            Тестируем что ссылка в Админке создаётся правильно
        """

        article = ArticleFactory()
        self.assertEquals(self.admin.view_on_site(article), article.get_absolute_url())



class ArticleAboutViewTestCase(TestCase):
    """
        Тестирование представления страницы с информацией о Статьях
    """

    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        response = self.client.post(
            reverse('articlesPage'),
        )

        self.assertEquals(response.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что страница вернет статус 200 без переданных параметров
        """

        response = self.client.get(
            reverse('articlesPage'),
            context={},
        )

        self.assertEquals(response.status_code, 200)


    def test_get_request_with_invalid_params(self):
        """
            Тестируем, что страница вернет статус 200 с неверными параметрами
        """

        response = self.client.get(
            reverse('articlesPage'),
            context={
                'navigationSelected': 'Invalid',
                'lastArticles': 'Invalid',
                'lastArticle': 'Invalid',
                'Param': 'Invalid',
            },
        )

        self.assertEquals(response.status_code, 200)


    def test_get_request_with_valid_params(self):
        """
            Тестируем, что страница вернет статус 200 с верными параметрами
        """

        response = self.client.get(
            reverse('articlesPage'),
            context={
                'navigationSelected': 'Articles',
                'lastArticles': ArticleFactory.create_batch(4),
                'lastArticle': ArticleFactory(),
            },
        )

        self.assertEquals(response.status_code, 200)


    def test_clear_image(self):
        """
            Тестируем, что если изображение посла будет отсутствовать в папке, изображение будет очищено
        """

        # Создаем 3 поста
        for _ in range(3):
            ArticleFactory()

        # Последний 4-й пост
        ArticleFactory(
            image=''
        )

        response = self.client.get(reverse('articlesPage'))

        self.assertContains(
            response,
            '<img src="/static/errors/imageNotFound.png" class="article_card_img">',
            html=True
        )



class ArticleListViewTestCase(TestCase):
    """
        Тестирование представления страницы с карточками всех Статей
    """

    def test_post_request_not_allowed(self):
        """
            Тестируем, что при POST запросе страница возвращает статус 405
        """

        response = self.client.post(
            reverse('allArticlesPage'),
        )

        self.assertEquals(response.status_code, 405)


    def test_get_request_with_empty_params(self):
        """
            Тестируем, что страница вернет статус 200 без переданных параметров
        """

        response = self.client.get(
            reverse('allArticlesPage'),
            context={},
        )

        self.assertEquals(response.status_code, 200)


    def test_get_request_with_invalid_params(self):
        """
            Тестируем, что страница вернет статус 200 с неверными параметрами
        """

        response = self.client.get(
            reverse('allArticlesPage'),
            context={
                'allArticles': 'Invalid',
                'Param': 'Invalid',
            },
        )

        self.assertEquals(response.status_code, 200)


    def test_get_request_with_valid_params(self):
        """
            Тестируем, что страница вернет статус 200 с верными параметрами
        """

        response = self.client.get(
            reverse('allArticlesPage'),
            context={
                'allArticles': ArticleFactory.create_batch(20),
            },
        )

        self.assertEquals(response.status_code, 200)



class ArticlePageViewTestCase(TestCase):
    """
        Тестирование представления страницы Статьи
    """

    def test_not_exist_page_returns_404(self):
        """
            Тестируем, что при попытке перехода на несуществующую статью
            страница вернет статус 404. Параметры GET запроса не передаются
        """

        # Авторизуем Пользователя, иначе происходит redirect с кодом 302
        self.client.force_login(
            UserCustomFactory()
        )

        response = self.client.get(
            reverse('articlePage', kwargs={'articleSlug': 'invalid-slug'}),
        )

        self.assertEquals(response.status_code, 404)


    def test_exist_page_returns_200(self):
        """
            Тестируем, что при попытке перехода на существующую статью
            страница вернет статус 200. Параметры GET запроса не передаются
        """

        article = ArticleFactory()

        response = self.client.get(
            reverse('articlePage', kwargs={'articleSlug': article.slug}),
        )

        self.assertEquals(response.status_code, 200)


    def test_page_with_invalid_params(self):
        """
            Тестируем, что страница вернет статус 200 с неверными параметрами
        """

        article = ArticleFactory()

        response = self.client.get(
            reverse('articlePage', kwargs={'articleSlug': article.slug}),
            context={
                'articleData': 'Invalid',
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

        article = ArticleFactory()
        # Значения не имеет, написал ли Пользователь что-то в форму или нет
        formData = {
            'content': 'Test',
        }

        response = self.client.post(
            reverse('articlePage', kwargs={'articleSlug': article.slug}),
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

        # Явное указание анонимности Пользователя
        self.client.force_login(
            UserCustomFactory()
        )

        article = ArticleFactory()
        # Значения не имеет, написал ли Пользователь что-то в форму или нет
        formData = {
            'content': 'Test',
        }

        response = self.client.post(
            reverse('articlePage', kwargs={'articleSlug': article.slug}),
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
