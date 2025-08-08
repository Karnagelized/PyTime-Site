
from django.db import models
from django.shortcuts import reverse
from managers.content import PublishedManager
from apps.tags.models import Tag
from ckeditor_uploader.fields import RichTextUploadingField


# Модель для статей
class Article(models.Model):
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    description = models.CharField(max_length=500, blank=True, verbose_name='Описание')
    text = RichTextUploadingField(verbose_name='Текст')
    tags = models.ManyToManyField(Tag, blank=True, related_name='articleTags', verbose_name='Теги')
    image = models.ImageField(upload_to='uploads/articles/imageHead/%Y/%m/%d/', blank=True, verbose_name='Изображение')
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
        return f'{self.title}'

