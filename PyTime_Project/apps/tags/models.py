
from django.db import models


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
