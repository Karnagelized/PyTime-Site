
from django.urls import reverse
from django.db import models


# Класс, описывающий "Теги"
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    datetimeCreate = models.DateTimeField(auto_now_add=True)
    datetimeUpdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Менеджер, который возвращает опубликованные объекты
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isPublished=True)


# Класс описывающий "Статью"
class Article(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    shortTitle = models.CharField(max_length=50)
    description = models.CharField(max_length=300, blank=True)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, related_name='articleTags')
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True)
    datetimeCreate = models.DateTimeField(auto_now_add=True)
    datetimeUpdate = models.DateTimeField(auto_now=True)
    isPublished = models.BooleanField(default=True)

    # Базовый менеджер
    objects = models.Manager()
    # Менеджер, возвращающий все опубликованные статьи
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('articlePage', kwargs={'articleSlug': self.slug})

    def __str__(self):
        return f'{self.slug} - {self.title}'


# Класс, описывающий "Проект"
class Project(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    shortTitle = models.CharField(max_length=50)
    description = models.CharField(max_length=300, blank=True)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, related_name='projectTags')
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True)
    datetimeCreate = models.DateTimeField(auto_now_add=True)
    datetimeUpdate = models.DateTimeField(auto_now=True)
    isPublished = models.BooleanField(default=True)

    # Базовый менеджер
    objects = models.Manager()
    # Менеджер, возвращающий все опубликованные проекты
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('projectPage', kwargs={'projectSlug': self.slug})

    def __str__(self):
        return f'{self.slug} - {self.title}'
