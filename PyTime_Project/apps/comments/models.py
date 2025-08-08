
from django.db.models import QuerySet
from django.db import models
from apps.users.models import CustomUser


# Модель для комментариев
class Comment(models.Model):
    ARTICLE = ('ARTICLE', 'article')
    PROJECT = ('PROJECT', 'project')

    COMMENT_TYPE = [
        ARTICLE,
        PROJECT,
    ]

    contentSlug = models.SlugField(verbose_name='Slug контента')
    contentType = models.CharField(max_length=7, choices=COMMENT_TYPE, verbose_name='Тип контента')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст')
    isVisible = models.BooleanField(default=True, verbose_name='Видимость')
    dateCreate = models.DateTimeField(blank=False, auto_now_add=True, verbose_name='Дата создания')


    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


    # Получить комментарии по типу и слагу поста(Проект или Статья)
    @staticmethod
    def getAllByTypeAndSlug(*, slug:str, postType:str) -> QuerySet:
        # Проверка правильного указания типа поста
        if postType not in [contentType[0] for contentType in Comment.COMMENT_TYPE]:
            raise ValueError(
                f'Тип комментария указан неверно. Получено {postType}, ' +
                f'ожидалось {", ".join([contentType[0] for contentType in Comment.COMMENT_TYPE])}'
            )

        return Comment.objects.all().filter(
            contentSlug=slug, contentType=postType,
            isVisible=True,
        ).order_by('-dateCreate').all()


    def __str__(self):
        return (
            f'Comment by \"{self.author}\". Href - \"{self.contentType}/{self.contentSlug}\"'
        )
