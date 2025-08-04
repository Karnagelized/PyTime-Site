from django.db import models


# Менеджер, который возвращает опубликованные объекты
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isPublished=True)
