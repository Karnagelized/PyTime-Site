
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_bleach.models import BleachField
from apps.users.utils import UserModelUtils
from django.utils.crypto import get_random_string
from django.utils import timezone



class ProfileAvatarModel(models.Model):
    """
        Модель, для выбора Аватара Пользователя
    """

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



class CustomUser(AbstractUser):
    """
        Модель Профиля Пользователя
    """

    username = models.CharField(
        unique=True,
        max_length=50,
        default=UserModelUtils.get,
        verbose_name='Никнейм'
    )

    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )

    first_name = BleachField(
        default='',
        blank=True,
        max_length=80,
        verbose_name='Имя'
    )

    last_name = BleachField(
        default='',
        blank=True,
        max_length=80,
        verbose_name='Фамилия'
    )

    aboutMe = BleachField(
        default='',
        blank=True,
        max_length=255,
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



class EmailVerification(models.Model):
    """
        Модель, для хранения кодов подтверждения почты
    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    code = models.CharField(
        max_length=6,
        verbose_name='Код подтверждения',
    )

    timeCreate = models.DateTimeField(
        auto_now_add=True,
    )


    def isExpired(self, expirationMinutes:int=15) -> bool:
        """
            Проверяет, истек ли срок действия кода.
            Если истек, возвращается True, иначе False
        """

        return (timezone.now() - self.timeCreate).total_seconds() > 60 * expirationMinutes


    @classmethod
    def create(cls, user:'CustomUser') -> 'EmailVerification':
        """
            Создает новый код для пользователя, удаляя старые
        """

        # Удаляем старые коды пользователя
        cls.objects.filter(user=user).delete()

        # Создаем новый код
        code = get_random_string(6, '0123456789')
        return cls.objects.create(user=user, code=code)


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-timeCreate']


    def __str__(self):
        return f'{self.user.username} - {self.code}'
