from django.db.models import QuerySet
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser


# Модель профиля Пользователя
class CustomUser(AbstractUser):

    class Meta:
        db_table = 'custom_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    def __str__(self):
        return f'{self.username}'


# Модель для тегов
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    datetimeCreate = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    datetimeUpdate = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')


    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


    def __str__(self):
        return self.name


# Менеджер, который возвращает опубликованные объекты
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isPublished=True)


# Модель для статей
class Article(models.Model):
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    shortTitle = models.CharField(max_length=50, verbose_name='Краткий заголовок')
    description = models.CharField(max_length=300, blank=True, verbose_name='Описание')
    text = models.TextField(verbose_name='Текст')
    tags = models.ManyToManyField(Tag, blank=True, related_name='articleTags', verbose_name='Теги')
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, verbose_name='Изображение')
    datetimeCreate = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    datetimeUpdate = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    isPublished = models.BooleanField(default=True, verbose_name='Видимость')

    # Базовый менеджер
    objects = models.Manager()
    # Менеджер, возвращающий все опубликованные статьи
    published = PublishedManager()


    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


    def get_absolute_url(self):
        return reverse('articlePage', kwargs={'articleSlug': self.slug})


    def __str__(self):
        return f'{self.slug} - {self.title}'


# Модель для проектов
class Project(models.Model):
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    shortTitle = models.CharField(max_length=50, verbose_name='Краткий заголовок')
    description = models.CharField(max_length=300, blank=True, verbose_name='Описание')
    text = models.TextField(verbose_name='Текст')
    tags = models.ManyToManyField(Tag, blank=True, related_name='projectTags', verbose_name='Теги')
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, verbose_name='Изображение')
    datetimeCreate = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    datetimeUpdate = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    isPublished = models.BooleanField(default=True, verbose_name='Видимость')

    # Базовый менеджер
    objects = models.Manager()
    # Менеджер, возвращающий все опубликованные проекты
    published = PublishedManager()

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


    def get_absolute_url(self):
        return reverse('projectPage', kwargs={'projectSlug': self.slug})


    def __str__(self):
        return f'{self.slug} - {self.title}'


# Модель для Hard скиллов
class HardSkills(models.Model):
    name = models.CharField(unique=True, blank=False, max_length=50, verbose_name='Название')
    isVisible = models.BooleanField(default=True, verbose_name='Видимость')
    dateCreate = models.DateTimeField(blank=False, auto_now_add=True, verbose_name='Дата создания')


    class Meta:
        verbose_name = 'Скилл'
        verbose_name_plural = 'Скиллы'


    def __str__(self):
        return (
            f'{self.name}'
        )


# Менеджер для Hard скиллов, который возвращает опубликованные категории
class VisibleHardSkillsCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isVisible=True).order_by('position')


# Модель для категорий Hard скиллов
class HardSkillsCategory(models.Model):
    name = models.CharField(unique=True, blank=False, max_length=50, verbose_name='Название')
    position = models.PositiveSmallIntegerField(blank=False, default=0, verbose_name='Позиция')
    skills = models.ManyToManyField(HardSkills, blank=True)
    isVisible = models.BooleanField(default=True, verbose_name='Видимость')
    dateCreate = models.DateTimeField(blank=False, auto_now_add=True, verbose_name='Дата создания')

    # Стандартный менеджер представления
    objects = models.Manager()
    # Менеджер отображающий только "включенные" категории
    visibleCategory = VisibleHardSkillsCategoryManager()


    class Meta:
        verbose_name = 'Категория скилла'
        verbose_name_plural = 'Категории скиллов'


    # Метод для получения всех скиллов данной категории
    def getSkills(self):
        return ', '.join([skill.name for skill in self.skills.all() if skill.isVisible])


    def __str__(self):
        return f'{self.name}'


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



