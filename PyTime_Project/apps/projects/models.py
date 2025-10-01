
from django.db import models
from django.shortcuts import reverse
from managers.content import PublishedManager
from apps.tags.models import Tag
from ckeditor_uploader.fields import RichTextUploadingField
from apps.comments.models import Comment



class Project(models.Model):
    """
        Модель Проектов
    """

    slug = models.SlugField(unique=True, verbose_name='Слаг')
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Описание')
    text = RichTextUploadingField(verbose_name='Текст')
    tags = models.ManyToManyField(Tag, blank=True, related_name='projectTags', verbose_name='Теги')
    image = models.ImageField(upload_to='uploads/projects/imageHead/%Y/%m/%d/', blank=True, verbose_name='Изображение')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    likes = models.ManyToManyField("users.CustomUser", blank=True, related_name='projectsLikes')
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


    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])


    def get_value_likes(self):
        return len(self.likes.all())


    def get_value_comments(self):
        return Comment.objects.filter(contentSlug=self.slug, contentType='PROJECT').count()


    def get_absolute_url(self):
        return reverse('projectPage', kwargs={'projectSlug': self.slug})


    def __str__(self):
        return f'{self.slug} - {self.title}'
