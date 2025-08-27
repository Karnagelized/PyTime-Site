
from typing import Union
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from apps.users.models import CustomUser


class EmailAuthBackend(ModelBackend):
    """
        Кастомная система аутентификации Пользователя через почту
    """

    def authenticate(self, request, email=None, password=None, **kwargs) -> Union[CustomUser, None]:
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(email=email)

            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None