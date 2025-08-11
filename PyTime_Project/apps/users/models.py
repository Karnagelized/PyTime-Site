
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_bleach.models import BleachField

# Модель профиля Пользователя
class CustomUser(AbstractUser):
    aboutMe = models.CharField(null=True, max_length=255, blank=True, verbose_name='Обо мне')
    gitLink = models.URLField(null=True, blank=True, verbose_name='Ссылка на GitHub')
    # TODO Дописать поля у модели юзера для Профиля
    # aboutMe = BleachField(
    #     null=True,
    #     max_length=255,
    #     blank=True,
    #     verbose_name='Обо мне'
    # )
    # gitLink = BleachField(
    #     null=True,
    #     blank=True,
    #     verbose_name='Ссылка на GitHub'
    # )


    class Meta:
        db_table = 'custom_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    def __str__(self):
        return f'{self.username}'
