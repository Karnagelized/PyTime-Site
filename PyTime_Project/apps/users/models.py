
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_bleach.models import BleachField


# Модель, для выбора аватаров Пользователя
class ProfileAvatarModel(models.Model):
    isDefault = models.BooleanField(default=False)

    avatar = models.FileField(
        upload_to='avatars/users/',
        default='avatars/generate/default.svg',
        verbose_name='Аватар',
    )


    class Meta:
        verbose_name = 'Аватар'
        verbose_name_plural = 'Аватары'


    def __str__(self):
        return f'{self.avatar.name}'


# Модель профиля Пользователя
class CustomUser(AbstractUser):
    first_name = BleachField(
        default='Anonymous',
        blank=True,
        max_length=100,
        verbose_name='Имя'
    )

    last_name = BleachField(
        default='User',
        blank=True,
        max_length=100,
        verbose_name='Фамилия'
    )

    aboutMe = BleachField(
        null=True,
        default='',
        max_length=255,
        blank=True,
        verbose_name='Обо мне'
    )

    avatar = models.ForeignKey(
        ProfileAvatarModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Аватар Пользователя',
    )


    class Meta:
        db_table = 'custom_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    def __str__(self):
        return f'{self.username}'
