
from django.test import TestCase, RequestFactory
from django.urls import reverse
from apps.users.factories import UserCustomFactory
from apps.articles.factories import ArticleFactory
from apps.projects.factories import ProjectFactory
from apps.comments.models import Comment
from apps.comments.factories import CommentFactory


class ArticleLikeTestCase(TestCase):
    """
        Тестирование представления страницы для лайков Статей
    """

    def test_not_auth_user_add_like(self):
        """
            Тестируем, что не авторизованный Пользователь не может поставить лайк существующей статье
        """

        self.client.logout()

        article = ArticleFactory(slug='articleSlugTest')
        self.assertEqual(article.likes.count(), 0)

        self.request = RequestFactory().get(
            'articlePage', kwargs={'articleSlug': article.slug}
        )

        response = self.client.post(
            reverse('likeArticle'),
            data={
                'contentSlug': article.slug,
                'parentURL': self.request.build_absolute_uri(),
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.client.session['skipViewIncrement'], True)
        self.assertEqual(self.request.build_absolute_uri(), response.url)
        self.assertEqual(article.likes.count(), 0)


    def test_auth_user_add_like(self):
        """
            Тестируем, что авторизованный Пользователь может поставить лайк существующей статье
        """

        self.client.force_login(
            UserCustomFactory()
        )

        article = ArticleFactory(slug='articleSlugTest')
        self.assertEqual(article.likes.count(), 0)

        self.request = RequestFactory().get(
            'articlePage', kwargs={'articleSlug': article.slug}
        )

        response = self.client.post(
            reverse('likeArticle'),
            data={
                'contentSlug': article.slug,
                'parentURL': self.request.build_absolute_uri(),
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.client.session['skipViewIncrement'], True)
        self.assertEqual(self.request.build_absolute_uri(), response.url)
        self.assertEqual(article.likes.count(), 1)

        response = self.client.post(
            reverse('likeArticle'),
            data={
                'contentSlug': article.slug,
                'parentURL': self.request.build_absolute_uri(),
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.client.session['skipViewIncrement'], True)
        self.assertEqual(self.request.build_absolute_uri(), response.url)
        self.assertEqual(article.likes.count(), 0)

        self.client.logout()

        for _ in range(10):
            self.client.force_login(
                UserCustomFactory()
            )

            response = self.client.post(
                reverse('likeArticle'),
                data={
                    'contentSlug': article.slug,
                    'parentURL': self.request.build_absolute_uri(),
                },
            )

        self.assertEqual(article.likes.count(), 10)


    def test_not_auth_user_remove_like(self):
        """
            Тестируем, что не авторизованный Пользователь не может убрать лайк существующей статье
        """

        self.client.force_login(
            UserCustomFactory()
        )

        article = ArticleFactory(slug='articleSlugTest')
        self.assertEqual(article.likes.count(), 0)

        self.request = RequestFactory().get(
            'articlePage', kwargs={'articleSlug': article.slug}
        )

        response = self.client.post(
            reverse('likeArticle'),
            data={
                'contentSlug': article.slug,
                'parentURL': self.request.build_absolute_uri(),
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.client.session['skipViewIncrement'], True)
        self.assertEqual(self.request.build_absolute_uri(), response.url)
        self.assertEqual(article.likes.count(), 1)

        self.client.logout()

        response = self.client.post(
            reverse('likeArticle'),
            data={
                'contentSlug': article.slug,
                'parentURL': self.request.build_absolute_uri(),
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.client.session['skipViewIncrement'], True)
        self.assertEqual(self.request.build_absolute_uri(), response.url)
        self.assertEqual(article.likes.count(), 1)


    def test_auth_user_remove_like(self):
        """
            Тестируем, что авторизованный Пользователь может убрать лайк существующей статье
        """

        self.client.force_login(
            UserCustomFactory()
        )

        article = ArticleFactory(slug='articleSlugTest')
        self.assertEqual(article.likes.count(), 0)

        self.request = RequestFactory().get(
            'articlePage', kwargs={'articleSlug': article.slug}
        )

        response = self.client.post(
            reverse('likeArticle'),
            data={
                'contentSlug': article.slug,
                'parentURL': self.request.build_absolute_uri(),
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.client.session['skipViewIncrement'], True)
        self.assertEqual(self.request.build_absolute_uri(), response.url)
        self.assertEqual(article.likes.count(), 1)

        response = self.client.post(
            reverse('likeArticle'),
            data={
                'contentSlug': article.slug,
                'parentURL': self.request.build_absolute_uri(),
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.client.session['skipViewIncrement'], True)
        self.assertEqual(self.request.build_absolute_uri(), response.url)
        self.assertEqual(article.likes.count(), 0)



class ProjectLikeTestCase(TestCase):
    """
        Тестирование представления страницы для лайков Проектов
    """

    def test_not_auth_user_add_like(self):
        """
            Тестируем, что не авторизованный Пользователь не может поставить лайк существующему проекту
        """

        self.client.logout()

        project = ProjectFactory(slug='projectSlugTest')
        self.assertEqual(project.likes.count(), 0)

        self.request = RequestFactory().get(
            'projectPage', kwargs={'projectSlug': project.slug}
        )

        response = self.client.post(
            reverse('likeProject'),
            data={
                'contentSlug': project.slug,
                'parentURL': self.request.build_absolute_uri(),
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.client.session['skipViewIncrement'], True)
        self.assertEqual(self.request.build_absolute_uri(), response.url)
        self.assertEqual(project.likes.count(), 0)


    def test_auth_user_add_like(self):
        """
            Тестируем, что авторизованный Пользователь может поставить лайк существующему проекту
        """

        self.client.force_login(
            UserCustomFactory()
        )

        project = ProjectFactory(slug='projectSlugTest')
        self.assertEqual(project.likes.count(), 0)

        self.request = RequestFactory().get(
            'projectPage', kwargs={'projectSlug': project.slug}
        )

        response = self.client.post(
            reverse('likeProject'),
            data={
                'contentSlug': project.slug,
                'parentURL': self.request.build_absolute_uri(),
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.client.session['skipViewIncrement'], True)
        self.assertEqual(self.request.build_absolute_uri(), response.url)
        self.assertEqual(project.likes.count(), 1)

        response = self.client.post(
            reverse('likeProject'),
            data={
                'contentSlug': project.slug,
                'parentURL': self.request.build_absolute_uri(),
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.client.session['skipViewIncrement'], True)
        self.assertEqual(self.request.build_absolute_uri(), response.url)
        self.assertEqual(project.likes.count(), 0)

        self.client.logout()

        for _ in range(10):
            self.client.force_login(
                UserCustomFactory()
            )

            response = self.client.post(
                reverse('likeProject'),
                data={
                    'contentSlug': project.slug,
                    'parentURL': self.request.build_absolute_uri(),
                },
            )

        self.assertEqual(project.likes.count(), 10)


    def test_not_auth_user_remove_like(self):
        """
            Тестируем, что не авторизованный Пользователь не может убрать лайк существующему проекту
        """

        self.client.force_login(
            UserCustomFactory()
        )

        project = ProjectFactory(slug='projectSlugTest')
        self.assertEqual(project.likes.count(), 0)

        self.request = RequestFactory().get(
            'projectPage', kwargs={'projectSlug': project.slug}
        )

        response = self.client.post(
            reverse('likeProject'),
            data={
                'contentSlug': project.slug,
                'parentURL': self.request.build_absolute_uri(),
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.client.session['skipViewIncrement'], True)
        self.assertEqual(self.request.build_absolute_uri(), response.url)
        self.assertEqual(project.likes.count(), 1)

        self.client.logout()

        response = self.client.post(
            reverse('likeProject'),
            data={
                'contentSlug': project.slug,
                'parentURL': self.request.build_absolute_uri(),
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.client.session['skipViewIncrement'], True)
        self.assertEqual(self.request.build_absolute_uri(), response.url)
        self.assertEqual(project.likes.count(), 1)


    def test_auth_user_remove_like(self):
        """
            Тестируем, что авторизованный Пользователь может убрать лайк существующему проекту
        """

        self.client.force_login(
            UserCustomFactory()
        )

        project = ProjectFactory(slug='projectSlugTest')
        self.assertEqual(project.likes.count(), 0)

        self.request = RequestFactory().get(
            'projectPage', kwargs={'projectSlug': project.slug}
        )

        response = self.client.post(
            reverse('likeProject'),
            data={
                'contentSlug': project.slug,
                'parentURL': self.request.build_absolute_uri(),
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.client.session['skipViewIncrement'], True)
        self.assertEqual(self.request.build_absolute_uri(), response.url)
        self.assertEqual(project.likes.count(), 1)

        response = self.client.post(
            reverse('likeProject'),
            data={
                'contentSlug': project.slug,
                'parentURL': self.request.build_absolute_uri(),
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.client.session['skipViewIncrement'], True)
        self.assertEqual(self.request.build_absolute_uri(), response.url)
        self.assertEqual(project.likes.count(), 0)



class CommentLikeViewTestCase(TestCase):
    """
        Тестирование представления страницы для лайков Комментария
    """

    def test_add_like_in_article(self):
        """
            Тестируем, что Пользователь может поставить лайк существующему комментарию у статьи
        """

        user = UserCustomFactory(
            username='CustomUser',
        )
        self.client.force_login(user)

        article = ArticleFactory(slug='articleSlugTest')
        comment = CommentFactory(
            contentSlug=article.slug,
            contentType=Comment.ARTICLE[0],
            author=user,
            toWhomReply=None,
            isReply=False,
            text='Обычный комментарий',
        )

        self.assertEqual(comment.likes.count(), 0)
        self.assertEqual(comment.dislikes.count(), 0)

        response = self.client.post(
            reverse('likeComment'),
            data={
                'commentSlug': article.slug,
                'commentType': Comment.ARTICLE[0],
                'commentID': comment.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('articlePage', kwargs={'articleSlug': article.slug}))
        self.assertEqual(comment.likes.count(), 1)
        self.assertEqual(comment.dislikes.count(), 0)

        response = self.client.post(
            reverse('likeComment'),
            data={
                'commentSlug': article.slug,
                'commentType': Comment.ARTICLE[0],
                'commentID': comment.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('articlePage', kwargs={'articleSlug': article.slug}))
        self.assertEqual(comment.likes.count(), 0)
        self.assertEqual(comment.dislikes.count(), 0)


    def test_add_like_with_dislike_in_article(self):
        """
            Тестируем, что Пользователь может поставить лайк существующему комментарию у статьи,
            где уже поставил дизлайк. В таком случае дизлайк уберётся, а лайк останется
        """

        user = UserCustomFactory(
            username='CustomUser',
        )
        self.client.force_login(user)

        article = ArticleFactory(slug='articleSlugTest')
        comment = CommentFactory(
            contentSlug=article.slug,
            contentType=Comment.ARTICLE[0],
            author=user,
            toWhomReply=None,
            isReply=False,
            text='Обычный комментарий',
        )

        self.assertEqual(comment.likes.count(), 0)
        self.assertEqual(comment.dislikes.count(), 0)

        response = self.client.post(
            reverse('dislikeComment'),
            data={
                'commentSlug': article.slug,
                'commentType': Comment.ARTICLE[0],
                'commentID': comment.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('articlePage', kwargs={'articleSlug': article.slug}))
        self.assertEqual(comment.likes.count(), 0)
        self.assertEqual(comment.dislikes.count(), 1)

        response = self.client.post(
            reverse('likeComment'),
            data={
                'commentSlug': article.slug,
                'commentType': Comment.ARTICLE[0],
                'commentID': comment.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('articlePage', kwargs={'articleSlug': article.slug}))
        self.assertEqual(comment.likes.count(), 1)
        self.assertEqual(comment.dislikes.count(), 0)


    def test_add_like_in_project(self):
        """
            Тестируем, что Пользователь может поставить лайк существующему комментарию у проекта
        """

        user = UserCustomFactory(
            username='CustomUser',
        )
        self.client.force_login(user)

        project = ProjectFactory(slug='projectSlugTest')
        comment = CommentFactory(
            contentSlug=project.slug,
            contentType=Comment.PROJECT[0],
            author=user,
            toWhomReply=None,
            isReply=False,
            text='Обычный комментарий',
        )

        self.assertEqual(comment.likes.count(), 0)
        self.assertEqual(comment.dislikes.count(), 0)

        response = self.client.post(
            reverse('likeComment'),
            data={
                'commentSlug': project.slug,
                'commentType': Comment.PROJECT[0],
                'commentID': comment.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('projectPage', kwargs={'projectSlug': project.slug}))
        self.assertEqual(comment.likes.count(), 1)
        self.assertEqual(comment.dislikes.count(), 0)

        response = self.client.post(
            reverse('likeComment'),
            data={
                'commentSlug': project.slug,
                'commentType': Comment.PROJECT[0],
                'commentID': comment.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('projectPage', kwargs={'projectSlug': project.slug}))
        self.assertEqual(comment.likes.count(), 0)
        self.assertEqual(comment.dislikes.count(), 0)


    def test_add_like_with_dislike_in_project(self):
        """
            Тестируем, что Пользователь может поставить лайк существующему комментарию у проекта,
            где уже поставил дизлайк. В таком случае дизлайк уберётся, а лайк останется
        """

        user = UserCustomFactory(
            username='CustomUser',
        )
        self.client.force_login(user)

        project = ProjectFactory(slug='projectSlugTest')
        comment = CommentFactory(
            contentSlug=project.slug,
            contentType=Comment.PROJECT[0],
            author=user,
            toWhomReply=None,
            isReply=False,
            text='Обычный комментарий',
        )

        self.assertEqual(comment.likes.count(), 0)
        self.assertEqual(comment.dislikes.count(), 0)

        response = self.client.post(
            reverse('dislikeComment'),
            data={
                'commentSlug': project.slug,
                'commentType': Comment.PROJECT[0],
                'commentID': comment.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('projectPage', kwargs={'projectSlug': project.slug}))
        self.assertEqual(comment.likes.count(), 0)
        self.assertEqual(comment.dislikes.count(), 1)

        response = self.client.post(
            reverse('likeComment'),
            data={
                'commentSlug': project.slug,
                'commentType': Comment.PROJECT[0],
                'commentID': comment.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('projectPage', kwargs={'projectSlug': project.slug}))
        self.assertEqual(comment.likes.count(), 1)
        self.assertEqual(comment.dislikes.count(), 0)



class CommentDislikeViewTestCase(TestCase):
    """
        Тестирование представления страницы для дизлайков Комментария
    """

    def test_add_dislike_in_article(self):
        """
            Тестируем, что Пользователь может поставить дизлайк существующему комментарию у статьи
        """

        user = UserCustomFactory(
            username='CustomUser',
        )
        self.client.force_login(user)

        article = ArticleFactory(slug='articleSlugTest')
        comment = CommentFactory(
            contentSlug=article.slug,
            contentType=Comment.ARTICLE[0],
            author=user,
            toWhomReply=None,
            isReply=False,
            text='Обычный комментарий',
        )

        self.assertEqual(comment.likes.count(), 0)
        self.assertEqual(comment.dislikes.count(), 0)

        response = self.client.post(
            reverse('dislikeComment'),
            data={
                'commentSlug': article.slug,
                'commentType': Comment.ARTICLE[0],
                'commentID': comment.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('articlePage', kwargs={'articleSlug': article.slug}))
        self.assertEqual(comment.likes.count(), 0)
        self.assertEqual(comment.dislikes.count(), 1)

        response = self.client.post(
            reverse('dislikeComment'),
            data={
                'commentSlug': article.slug,
                'commentType': Comment.ARTICLE[0],
                'commentID': comment.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('articlePage', kwargs={'articleSlug': article.slug}))
        self.assertEqual(comment.likes.count(), 0)
        self.assertEqual(comment.dislikes.count(), 0)


    def test_add_like_with_like_in_article(self):
        """
            Тестируем, что Пользователь может поставить дизлайк существующему комментарию у статьи,
            где уже поставил лайк. В таком случае лайк уберётся, а дизлайк останется
        """

        user = UserCustomFactory(
            username='CustomUser',
        )
        self.client.force_login(user)

        article = ArticleFactory(slug='articleSlugTest')
        comment = CommentFactory(
            contentSlug=article.slug,
            contentType=Comment.ARTICLE[0],
            author=user,
            toWhomReply=None,
            isReply=False,
            text='Обычный комментарий',
        )

        self.assertEqual(comment.likes.count(), 0)
        self.assertEqual(comment.dislikes.count(), 0)

        response = self.client.post(
            reverse('likeComment'),
            data={
                'commentSlug': article.slug,
                'commentType': Comment.ARTICLE[0],
                'commentID': comment.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('articlePage', kwargs={'articleSlug': article.slug}))
        self.assertEqual(comment.likes.count(), 1)
        self.assertEqual(comment.dislikes.count(), 0)

        response = self.client.post(
            reverse('dislikeComment'),
            data={
                'commentSlug': article.slug,
                'commentType': Comment.ARTICLE[0],
                'commentID': comment.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('articlePage', kwargs={'articleSlug': article.slug}))
        self.assertEqual(comment.likes.count(), 0)
        self.assertEqual(comment.dislikes.count(), 1)


    def test_add_like_in_project(self):
        """
            Тестируем, что Пользователь может поставить дизлайк существующему комментарию у проекта
        """

        user = UserCustomFactory(
            username='CustomUser',
        )
        self.client.force_login(user)

        project = ProjectFactory(slug='projectSlugTest')
        comment = CommentFactory(
            contentSlug=project.slug,
            contentType=Comment.PROJECT[0],
            author=user,
            toWhomReply=None,
            isReply=False,
            text='Обычный комментарий',
        )

        self.assertEqual(comment.likes.count(), 0)
        self.assertEqual(comment.dislikes.count(), 0)

        response = self.client.post(
            reverse('dislikeComment'),
            data={
                'commentSlug': project.slug,
                'commentType': Comment.PROJECT[0],
                'commentID': comment.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('projectPage', kwargs={'projectSlug': project.slug}))
        self.assertEqual(comment.likes.count(), 0)
        self.assertEqual(comment.dislikes.count(), 1)

        response = self.client.post(
            reverse('dislikeComment'),
            data={
                'commentSlug': project.slug,
                'commentType': Comment.PROJECT[0],
                'commentID': comment.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('projectPage', kwargs={'projectSlug': project.slug}))
        self.assertEqual(comment.likes.count(), 0)
        self.assertEqual(comment.dislikes.count(), 0)


    def test_add_like_with_dislike_in_project(self):
        """
            Тестируем, что Пользователь может поставить дизлайк существующему комментарию у проекта,
            где уже поставил лайк. В таком случае лайк уберётся, а дизлайк останется
        """

        user = UserCustomFactory(
            username='CustomUser',
        )
        self.client.force_login(user)

        project = ProjectFactory(slug='projectSlugTest')
        comment = CommentFactory(
            contentSlug=project.slug,
            contentType=Comment.PROJECT[0],
            author=user,
            toWhomReply=None,
            isReply=False,
            text='Обычный комментарий',
        )

        self.assertEqual(comment.likes.count(), 0)
        self.assertEqual(comment.dislikes.count(), 0)

        response = self.client.post(
            reverse('likeComment'),
            data={
                'commentSlug': project.slug,
                'commentType': Comment.PROJECT[0],
                'commentID': comment.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('projectPage', kwargs={'projectSlug': project.slug}))
        self.assertEqual(comment.likes.count(), 1)
        self.assertEqual(comment.dislikes.count(), 0)

        response = self.client.post(
            reverse('dislikeComment'),
            data={
                'commentSlug': project.slug,
                'commentType': Comment.PROJECT[0],
                'commentID': comment.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('projectPage', kwargs={'projectSlug': project.slug}))
        self.assertEqual(comment.likes.count(), 0)
        self.assertEqual(comment.dislikes.count(), 1)
