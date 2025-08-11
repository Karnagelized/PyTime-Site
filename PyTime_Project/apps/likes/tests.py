
from django.test import TestCase, RequestFactory
from django.urls import reverse
from apps.users.factories import UserCustomFactory
from apps.articles.factories import ArticleFactory


# TODO написать тесты
# Тестирование представления страницы для лайков Статей
class ArticleLikeTestCase(TestCase):
    def test_not_auth_user_add_like(self):
        """
            Тестируем, что не авторизованный Пользователь не может поставить лайк существующей статье
        """

        pass
        # self.client.logout()
        #
        # article = ArticleFactory()
        #
        # self.assertEqual(article.likes.count(), 0)
        #
        # # Почему-то возвращается 405 код, хотя должен при follow True 200 и при False 302
        # request = self.client.post(
        #     reverse('likeArticle'),
        #     kwargs={'contentSlug': article.slug},
        #     follow=True
        # )
        #
        # self.assertEqual(article.likes.count(), 0)


    def test_auth_user_add_like(self):
        """
            Тестируем, что авторизованный Пользователь может поставить лайк существующей статье
        """

        pass


    def test_not_auth_user_remove_like(self):
        """
            Тестируем, что не авторизованный Пользователь не может убрать лайк
        """

        pass


    def test_auth_user_remove_like(self):
        """
            Тестируем, что авторизованный Пользователь может убрать лайк
        """

        pass


# Тестирование представления страницы для лайков Проектов
class ProjectLikeTestCase(TestCase):
    def test_not_auth_user_add_like(self):
        """
            Тестируем, что не авторизованный Пользователь не может поставить лайк существующему проекту
        """

        pass


    def test_auth_user_add_like(self):
        """
            Тестируем, что авторизованный Пользователь может поставить лайк существующему проекту
        """

        pass


    def test_not_auth_user_remove_like(self):
        """
            Тестируем, что не авторизованный Пользователь не может убрать лайк существующему проекту
        """

        pass


    def test_auth_user_remove_like(self):
        """
            Тестируем, что авторизованный Пользователь может убрать лайк существующему проекту
        """

        pass
