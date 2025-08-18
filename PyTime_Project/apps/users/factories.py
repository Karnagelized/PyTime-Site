
import factory.django
from apps.users.models import CustomUser, ProfileAvatarModel


# Фабрика для Аватаров
class AvatarProfileFactory(factory.django.DjangoModelFactory):
    isDefault = factory.LazyAttribute(lambda obj: False)
    avatar = factory.django.ImageField()

    class Meta:
        model = ProfileAvatarModel


# Фабрика для генерации моделей Пользователей
class UserCustomFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj}_email@mail.ru")
    password = factory.LazyAttribute(lambda obj: f"password_{obj.username}")
    avatar = factory.SubFactory(AvatarProfileFactory)
    first_name = 'Anonymous'
    last_name = 'User'
    aboutMe = ''


    class Meta:
        model = CustomUser
