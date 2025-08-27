
import factory.django
from apps.users.models import CustomUser, ProfileAvatarModel, EmailVerification
from django.utils import timezone, crypto



class AvatarProfileFactory(factory.django.DjangoModelFactory):
    """
        Фабрика для Аватаров
    """

    isDefault = False
    avatar = factory.django.ImageField()


    class Meta:
        model = ProfileAvatarModel



class UserCustomFactory(factory.django.DjangoModelFactory):
    """
        Фабрика для генерации моделей Пользователей
    """

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.Sequence(lambda n: f"{n}_email@mail.ru")
    password = factory.LazyAttribute(lambda obj: f"password_{obj.username}")
    avatar = factory.SubFactory(AvatarProfileFactory)
    first_name = 'Anonymous'
    last_name = 'User'
    aboutMe = ''
    is_active = True


    class Meta:
        model = CustomUser



class EmailVerificationFactory(factory.django.DjangoModelFactory):
    """
        Фабрика для генерации Кодов подтверждения почты Пользователя
    """

    user = factory.SubFactory(UserCustomFactory)
    code = crypto.get_random_string(6, '0123456789')
    timeCreate = timezone.now()


    class Meta:
        model = EmailVerification
