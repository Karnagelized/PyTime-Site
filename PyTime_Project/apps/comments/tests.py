
from django.test import TestCase
from apps.comments.factories import CommentFactory
from apps.comments.models import Comment
from apps.articles.factories import ArticleFactory
from apps.projects.factories import ProjectFactory
from django.db.models.query import QuerySet
from apps.users.factories import UserCustomFactory
from django.urls import reverse



class CommentsModelTestCase(TestCase):
    """
        Тестирование модели Comment
    """

    def test_str_dunder(self):
        """
            Тестируем правильный вывод str метода
        """

        comment = CommentFactory(
            contentType=Comment.ARTICLE[0],
        )

        self.assertEquals(
            comment.__str__(),
            f'Комментарий "{comment.author}" в "{comment.contentType}/{comment.contentSlug}"'
        )


    def test_get_comments_with_invalid_type(self):
        """
            Тестируем что метод getAllByTypeAndSlug(slug:str, postType:str) -> QuerySet
            при неверном типе поста выдаст ошибку ValueError
        """

        article = ArticleFactory(slug='SlugTest')

        data = {
            'slug': article.slug,
            'postType': 'invalid',
        }

        errorMessage = (
            f'Тип комментария указан неверно. Получено {data["postType"]}, ' +
            f'ожидалось {", ".join([contentType[0] for contentType in Comment.COMMENT_TYPE])}'
        )

        self.assertRaises(ValueError, Comment.getAllByTypeAndSlug, **data)
        self.assertRaisesMessage(ValueError, errorMessage, Comment.getAllByTypeAndSlug, **data)


    def test_get_comments_returns_0(self):
        """
            Тестируем что метод getAllByTypeAndSlug(slug:str, postType:str) -> QuerySet
            при верных данных выдаст для пустого поста 0
        """

        article = ArticleFactory(slug='SlugTest')

        data = {
            'slug': article.slug,
            'postType': Comment.ARTICLE[0],
        }

        self.assertEqual(Comment.getAllByTypeAndSlug(**data).count(), 0)


    def test_get_comments_returns_10(self):
        """
            Тестируем что метод getAllByTypeAndSlug(slug:str, postType:str) -> QuerySet
            при верных данных выдаст для поста с 10 комментариями вернёт 10
        """

        article = ArticleFactory(slug='SlugTest')

        for _ in range(10):
            articleComment = CommentFactory(
                contentSlug=article.slug,
                contentType=Comment.ARTICLE[0],
            )

        data = {
            'slug': article.slug,
            'postType': Comment.ARTICLE[0],
        }

        self.assertEqual(Comment.getAllByTypeAndSlug(**data).count(), 10)



class ReplyCommentViewTestCase(TestCase):
    """
        Тестирование представления для ответа на комментарий
    """

    def setUp(self):
        self.user = UserCustomFactory()
        self.client.force_login(
            self.user
        )


    def test_comment_form_is_valid_for_article(self):
        """
            Тестируем, когда форма комментария валидна
            происходит редирект на страницу статьи с кодом 302
        """

        article = ArticleFactory(
            slug='articleSlug'
        )

        comment = CommentFactory(
            contentSlug=article.slug,
            contentType=Comment.ARTICLE[0],
            author=self.user,
        )

        replyText = 'ReplyText'
        response = self.client.post(
            reverse('replyComment'),
            data={
                'commentSlug': article.slug,
                'commentType': Comment.ARTICLE[0],
                'commentID': comment.id,
                'content': replyText,
            }
        )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('articlePage', kwargs={'articleSlug': article.slug}))

        newComment = Comment.objects.filter(text=replyText).first()

        self.assertIsNotNone(newComment)
        self.assertEqual(newComment.contentSlug, article.slug)
        self.assertEqual(newComment.contentType, Comment.ARTICLE[0])
        self.assertEqual(newComment.author, self.user)
        self.assertEqual(newComment.text, replyText)
        self.assertEqual(newComment.isReply, True)


    def test_comment_form_is_valid_for_project(self):
        """
            Тестируем, когда форма комментария валидна
            происходит редирект на страницу проекта с кодом 302
        """

        project = ProjectFactory(
            slug='articleSlug'
        )

        comment = CommentFactory(
            contentSlug=project.slug,
            contentType=Comment.PROJECT[0],
            author=self.user,
        )

        replyText = 'ReplyText'
        response = self.client.post(
            reverse('replyComment'),
            data={
                'commentSlug': project.slug,
                'commentType': Comment.PROJECT[0],
                'commentID': comment.id,
                'content': replyText,
            }
        )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('projectPage', kwargs={'projectSlug': project.slug}))

        newComment = Comment.objects.filter(text=replyText).first()

        self.assertIsNotNone(newComment)
        self.assertEqual(newComment.contentSlug, project.slug)
        self.assertEqual(newComment.contentType, Comment.PROJECT[0])
        self.assertEqual(newComment.author, self.user)
        self.assertEqual(newComment.text, replyText)
        self.assertEqual(newComment.isReply, True)
