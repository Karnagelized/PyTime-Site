
from django.db.models import QuerySet, Count
from django.db import models
from apps.users.models import CustomUser



class Comment(models.Model):
    """
        Модель для Комментариев
    """

    ARTICLE = ('ARTICLE', 'article')
    PROJECT = ('PROJECT', 'project')

    COMMENT_TYPE = [
        ARTICLE,
        PROJECT,
    ]

    contentSlug = models.SlugField(verbose_name='Slug контента')
    contentType = models.CharField(max_length=7, choices=COMMENT_TYPE, verbose_name='Тип контента')
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name='Автор', related_name='authorComments'
    )
    text = models.TextField(verbose_name='Текст')
    likes = models.ManyToManyField(
        CustomUser, blank=True, related_name='likesComment', verbose_name='Лайки',
    )
    dislikes = models.ManyToManyField(
        CustomUser, blank=True, related_name='dislikesComment', verbose_name='Дизлайки',
    )
    parentComment = models.ForeignKey(
        'self', blank=True, null=True, default=None, on_delete=models.SET_DEFAULT,
        verbose_name='Комментарий родитель', related_name='parent'
    )
    toWhomReply = models.ForeignKey(
        CustomUser, blank=True, null=True, default=None, on_delete=models.SET_DEFAULT,
        verbose_name='Кому ответ', related_name='toWhomReply'
    )
    isReply = models.BooleanField(default=False, verbose_name='Является ответом')
    isVisible = models.BooleanField(default=True, verbose_name='Видимость')
    dateCreate = models.DateTimeField(blank=False, auto_now_add=True, verbose_name='Дата создания')


    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


    # Количество лайков
    def getCountLikes(self) -> int:
        return self.likes.count()


    # Количество дизлайков
    def getCountDislikes(self) -> int:
        return self.dislikes.count()


    # Получить все ответы на комментарий
    def getAllReplies(self) -> QuerySet:
        replies = Comment.objects.filter(
            parentComment=self,
            contentType=self.contentType,
            contentSlug=self.contentSlug,
            isReply=True,
            isVisible=True,
        ).order_by(
            'dateCreate'
        ).all()

        return replies


    # Получить все комментарии по типу и слагу поста (Проект или Статья),
    # который не является ответом на комментарии
    @staticmethod
    def getAllByTypeAndSlug(*, slug:str, postType:str) -> QuerySet:
        # Проверка правильного указания типа поста
        if postType not in [contentType[0] for contentType in Comment.COMMENT_TYPE]:
            raise ValueError(
                f'Тип комментария указан неверно. Получено {postType}, ' +
                f'ожидалось {", ".join([contentType[0] for contentType in Comment.COMMENT_TYPE])}'
            )

        comments = Comment.objects.all().filter(
            contentSlug=slug,
            contentType=postType,
            isVisible=True,
            isReply=False,
        ).annotate(
            countLikes=Count('likes'),
        ).order_by(
            '-countLikes', '-dateCreate'
        ).all()

        return comments


    def __str__(self):
        return (
            f'Комментарий \"{self.author}\" в \"{self.contentType}/{self.contentSlug}\"'
        )
