
import factory.django
from apps.users.models import CustomUser


# Фабрика для генерации моделей Пользователей
class UserCustomFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj}_email@mail.ru")
    password = factory.LazyAttribute(lambda obj: f"password_{obj.username}")


    class Meta:
        model = CustomUser
