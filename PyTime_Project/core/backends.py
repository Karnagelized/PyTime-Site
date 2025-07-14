
from typing import Union
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser


class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs) -> Union[AbstractBaseUser, None]:
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(email=email)

            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None